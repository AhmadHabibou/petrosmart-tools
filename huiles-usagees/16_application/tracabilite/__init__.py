"""Application web de tracabilite des huiles usagees (Flask + SQLite).

API JSON sous /api, interface mobile hors ligne sous /. Authentification par jeton (en-tete X-Token),
defini par la variable d'environnement TRACABILITE_TOKEN.
"""
import json
import os
from pathlib import Path

from flask import Flask, Response, abort, g, jsonify, request, send_from_directory

from . import db, documents, metier

STATIC = Path(__file__).resolve().parent / "static"


def creer_app(config=None):
    app = Flask(__name__, static_folder=None)
    app.config.update(BASE=os.environ.get("TRACABILITE_BASE", str(Path.cwd() / "tracabilite.sqlite")),
                      TOKEN=os.environ.get("TRACABILITE_TOKEN", ""), SOCIETE=os.environ.get("TRACABILITE_SOCIETE", "[Dénomination de la société]"))
    if config:
        app.config.update(config)

    def con():
        if "con" not in g:
            g.con = db.connecter(app.config["BASE"])
            db.initialiser(g.con)
        return g.con

    @app.teardown_appcontext
    def fermer(_):
        c = g.pop("con", None)
        if c is not None:
            c.close()

    @app.before_request
    def authentifier():
        if request.path.startswith("/api/") and app.config["TOKEN"]:
            if request.headers.get("X-Token") != app.config["TOKEN"] and request.args.get("token") != app.config["TOKEN"]:
                abort(401)

    @app.errorhandler(metier.ErreurMetier)
    def erreur_metier(e):
        return jsonify(erreur=str(e)), 400

    # interface
    @app.get("/")
    def index():
        return send_from_directory(STATIC, "index.html")

    @app.get("/static/<path:nom>")
    def statique(nom):
        return send_from_directory(STATIC, nom)

    @app.get("/sw.js")
    def service_worker():
        r = send_from_directory(STATIC, "sw.js")
        r.headers["Service-Worker-Allowed"] = "/"
        return r

    # API generique
    def _creer(table, data):
        if table not in db.CHAMPS:
            abort(404)
        manquants = [c for c in db.OBLIGATOIRES[table] if data.get(c) in (None, "")]
        if manquants:
            raise metier.ErreurMetier("champs obligatoires manquants : " + ", ".join(manquants))
        if table == "ventes":
            metier.enregistrer_vente(con(), data)
            return data.get("id")
        champs = db.CHAMPS[table]
        rid = data.get("id") or db.nouvel_id()
        cols = ["id"] + champs + ["cree_le"]
        vals = [rid] + [data.get(c) for c in champs] + [db.maintenant()]
        if table == "futs" and not data.get("statut"):
            vals[cols.index("statut")] = "chez_client"
        if table == "futs" and not data.get("contenu"):
            vals[cols.index("contenu")] = "huiles usagees"
        if table == "enlevements" and not data.get("statut"):
            vals[cols.index("statut")] = "planifie"
        if table == "clients" and data.get("type") in (None, ""):
            vals[cols.index("type")] = "forestier"
        if table == "clients" and data.get("fictif") is None:
            vals[cols.index("fictif")] = 0
        con().execute(f"INSERT OR IGNORE INTO {table} ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})", vals)
        con().commit()
        return rid

    @app.get("/api/<table>")
    def lister(table):
        if table not in db.CHAMPS and table not in ("lots", "analyses", "mouvements"):
            abort(404)
        return jsonify(db.lignes(con(), f"SELECT * FROM {table} ORDER BY cree_le"))

    @app.post("/api/<table>")
    def creer(table):
        return jsonify(id=_creer(table, request.get_json(force=True))), 201

    @app.post("/api/enlevements/<eid>/realiser")
    def realiser(eid):
        d = request.get_json(force=True)
        return jsonify(metier.realiser_enlevement(con(), eid, d.get("volume_l"), d.get("depistage"), d.get("fut_ids"), d.get("date"), d.get("transporteur")))

    @app.post("/api/analyses")
    def analyser():
        d = request.get_json(force=True)
        return jsonify(decision=metier.enregistrer_analyse(con(), d.get("lot_id"), d.get("chlore_ppm"), d.get("pcb_detecte"), d.get("eau_pct"),
                                                           d.get("point_eclair_c"), d.get("laboratoire"), d.get("date"), d.get("id"))), 201

    @app.get("/api/stock")
    def stock():
        s = metier.stock_par_lot(con())
        lots = {l["id"]: l for l in db.lignes(con(), "SELECT * FROM lots")}
        return jsonify([dict(lot_id=k, numero=lots[k]["numero"], statut=lots[k]["statut"], stock_l=v) for k, v in s.items() if k in lots])

    @app.get("/api/tableau_de_bord")
    def tdb():
        return jsonify(metier.tableau_de_bord(con(), request.args.get("annee")))

    @app.get("/api/futs/<fid>/qr.svg")
    def qr(fid):
        f = con().execute("SELECT code FROM futs WHERE id = ?", (fid,)).fetchone()
        if f is None:
            abort(404)
        return Response(documents.qr_svg(f"FUT:{f['code']}"), mimetype="image/svg+xml")

    @app.get("/api/enlevements/<eid>/bordereau.pdf")
    def bordereau(eid):
        c = con()
        e = c.execute("SELECT * FROM enlevements WHERE id = ?", (eid,)).fetchone()
        if e is None or e["statut"] != "realise":
            abort(404)
        site = c.execute("SELECT * FROM sites WHERE id = ?", (e["site_id"],)).fetchone()
        client = c.execute("SELECT * FROM clients WHERE id = ?", (site["client_id"],)).fetchone()
        futs = db.lignes(c, "SELECT f.* FROM futs f JOIN enlevement_futs ef ON ef.fut_id = f.id WHERE ef.enlevement_id = ?", (eid,))
        return Response(documents.bordereau_pdf(dict(e), dict(site), dict(client), futs, app.config["SOCIETE"]), mimetype="application/pdf")

    @app.get("/api/clients/<cid>/rapport/<int:annee>.pdf")
    def rapport(cid, annee):
        return Response(documents.rapport_pdf(metier.rapport_client(con(), cid, annee), app.config["SOCIETE"]), mimetype="application/pdf")

    @app.post("/api/sync")
    def synchroniser():
        """Rejoue les operations saisies hors ligne. Idempotent : une operation deja recue n'est pas rejouee."""
        ops = request.get_json(force=True).get("operations", [])
        res = []
        for op in ops:
            oid = op.get("op_id")
            deja = con().execute("SELECT resultat FROM operations_sync WHERE op_id = ?", (oid,)).fetchone()
            if deja:
                res.append(dict(op_id=oid, statut="deja_recu", resultat=json.loads(deja["resultat"])))
                continue
            try:
                t, d = op.get("type"), op.get("data", {})
                if t == "creer":
                    r = dict(id=_creer(op["table"], d))
                elif t == "realiser":
                    r = metier.realiser_enlevement(con(), d["id"], d.get("volume_l"), d.get("depistage"), d.get("fut_ids"), d.get("date"), d.get("transporteur"))
                elif t == "analyse":
                    r = dict(decision=metier.enregistrer_analyse(con(), d.get("lot_id"), d.get("chlore_ppm"), d.get("pcb_detecte"), d.get("eau_pct"),
                                                                 d.get("point_eclair_c"), d.get("laboratoire"), d.get("date"), d.get("id")))
                else:
                    raise metier.ErreurMetier(f"type d'opération inconnu : {t}")
                statut = "ok"
            except metier.ErreurMetier as e:
                r, statut = dict(erreur=str(e)), "erreur"
            con().execute("INSERT INTO operations_sync VALUES (?,?,?)", (oid, db.maintenant(), json.dumps(r)))
            con().commit()
            res.append(dict(op_id=oid, statut=statut, resultat=r))
        return jsonify(resultats=res)

    return app
