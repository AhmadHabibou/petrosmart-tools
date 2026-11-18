"""Regles metier : realisation d'un enlevement, decision d'analyse, stocks, tableau de bord, rapport annuel."""
from . import db

SEUIL_CHLORE_PPM = 1000  # procedure d'acceptation des lots (lot 4 bis)


class ErreurMetier(ValueError):
    pass


def _numero(con, prefixe, table, colonne, annee):
    n = con.execute(f"SELECT COUNT(*) FROM {table} WHERE {colonne} LIKE ?", (f"{prefixe}-{annee}-%",)).fetchone()[0]
    return f"{prefixe}-{annee}-{n + 1:04d}"


def realiser_enlevement(con, enl_id, volume_l, depistage, fut_ids, date=None, transporteur=None):
    enl = con.execute("SELECT * FROM enlevements WHERE id = ?", (enl_id,)).fetchone()
    if enl is None:
        raise ErreurMetier("enlèvement inconnu")
    if enl["statut"] == "realise":
        return dict(enl)
    if depistage not in ("negatif", "positif"):
        raise ErreurMetier("dépistage obligatoire : negatif ou positif")
    if volume_l is None or float(volume_l) <= 0:
        raise ErreurMetier("volume strictement positif obligatoire")
    date = date or db.maintenant()[:10]
    annee = date[:4]
    bordereau = _numero(con, "BSD", "enlevements", "bordereau", annee)
    con.execute("UPDATE enlevements SET statut='realise', date_realisee=?, volume_l=?, depistage=?, bordereau=?, transporteur=COALESCE(?, transporteur) WHERE id=?",
                (date, float(volume_l), depistage, bordereau, transporteur, enl_id))
    for f in fut_ids or []:
        con.execute("INSERT OR IGNORE INTO enlevement_futs VALUES (?, ?)", (enl_id, f))
        con.execute("UPDATE futs SET statut='enleve' WHERE id = ?", (f,))
    statut_lot = "en_attente" if depistage == "positif" else "accepte_provisoire"
    lot_id = db.nouvel_id()
    numero = _numero(con, "LOT", "lots", "numero", annee)
    con.execute("INSERT INTO lots VALUES (?,?,?,?,?,?,?)", (lot_id, numero, enl_id, date, float(volume_l), statut_lot, db.maintenant()))
    con.execute("INSERT INTO mouvements VALUES (?,?,?,?,?,?,?)", (db.nouvel_id(), date, "entree", float(volume_l), lot_id, bordereau, db.maintenant()))
    con.commit()
    return dict(con.execute("SELECT * FROM enlevements WHERE id = ?", (enl_id,)).fetchone())


def enregistrer_analyse(con, lot_id, chlore_ppm, pcb_detecte, eau_pct=None, point_eclair_c=None, laboratoire=None, date=None, ana_id=None):
    if con.execute("SELECT 1 FROM lots WHERE id = ?", (lot_id,)).fetchone() is None:
        raise ErreurMetier("lot inconnu")
    pcb = bool(pcb_detecte)
    decision = "refuse" if (pcb or (chlore_ppm is not None and float(chlore_ppm) >= SEUIL_CHLORE_PPM)) else "accepte"
    ana_id = ana_id or db.nouvel_id()
    con.execute("INSERT OR IGNORE INTO analyses VALUES (?,?,?,?,?,?,?,?,?,?)",
                (ana_id, lot_id, date or db.maintenant()[:10], laboratoire, chlore_ppm, int(pcb), eau_pct, point_eclair_c, decision, db.maintenant()))
    con.execute("UPDATE lots SET statut = ? WHERE id = ?", (decision, lot_id))
    con.commit()
    return decision


def sortie_stock(con, lot_id, volume_l, reference, date=None):
    stock = stock_par_lot(con).get(lot_id, 0.0)
    if float(volume_l) > stock + 1e-6:
        raise ErreurMetier(f"stock insuffisant : {stock} L disponibles")
    con.execute("INSERT INTO mouvements VALUES (?,?,?,?,?,?,?)", (db.nouvel_id(), date or db.maintenant()[:10], "sortie", float(volume_l), lot_id, reference, db.maintenant()))
    con.commit()


def stock_par_lot(con):
    res = {}
    for r in con.execute("SELECT lot_id, SUM(CASE WHEN sens='entree' THEN volume_l ELSE -volume_l END) s FROM mouvements GROUP BY lot_id"):
        res[r["lot_id"]] = r["s"] or 0.0
    return res


def enregistrer_vente(con, vente):
    lot = con.execute("SELECT statut FROM lots WHERE id = ?", (vente.get("lot_id"),)).fetchone()
    if lot is None or lot["statut"] not in ("accepte", "traite"):
        raise ErreurMetier("seul un lot accepté ou traité peut être vendu")
    sortie_stock(con, vente["lot_id"], vente["volume_l"], f"vente {vente['acheteur']}", vente.get("date"))
    con.execute("INSERT INTO ventes VALUES (?,?,?,?,?,?,?)", (vente.get("id") or db.nouvel_id(), vente["date"], vente["acheteur"], vente["lot_id"],
                                                            float(vente["volume_l"]), float(vente["prix_l"]), db.maintenant()))
    con.commit()


def tableau_de_bord(con, annee=None):
    filtre, p = ("WHERE substr(date_realisee,1,4) = ?", (str(annee),)) if annee else ("", ())
    enl = con.execute(f"SELECT COUNT(*) n, COALESCE(SUM(volume_l),0) v FROM enlevements {filtre} {'AND' if filtre else 'WHERE'} statut='realise'", p).fetchone()
    lots = {r["statut"]: r["n"] for r in con.execute("SELECT statut, COUNT(*) n FROM lots GROUP BY statut")}
    ventes = con.execute("SELECT COALESCE(SUM(volume_l),0) v, COALESCE(SUM(volume_l*prix_l),0) ca FROM ventes").fetchone()
    controles = sum(lots.values())
    return dict(
        clients=con.execute("SELECT COUNT(*) FROM clients").fetchone()[0],
        sites=con.execute("SELECT COUNT(*) FROM sites").fetchone()[0],
        futs_chez_clients=con.execute("SELECT COUNT(*) FROM futs WHERE statut='chez_client'").fetchone()[0],
        enlevements_realises=enl["n"], volume_enleve_l=enl["v"],
        enlevements_planifies=con.execute("SELECT COUNT(*) FROM enlevements WHERE statut='planifie'").fetchone()[0],
        stock_total_l=round(sum(stock_par_lot(con).values()), 1),
        lots=lots, taux_lots_refuses=(lots.get("refuse", 0) / controles) if controles else None,
        volume_vendu_l=ventes["v"], chiffre_affaires_ventes=ventes["ca"])


def rapport_client(con, client_id, annee):
    client = con.execute("SELECT * FROM clients WHERE id = ?", (client_id,)).fetchone()
    if client is None:
        raise ErreurMetier("client inconnu")
    enl = db.lignes(con, """SELECT e.*, s.nom site FROM enlevements e JOIN sites s ON s.id = e.site_id
                           WHERE s.client_id = ? AND e.statut = 'realise' AND substr(e.date_realisee,1,4) = ?
                           ORDER BY e.date_realisee""", (client_id, str(annee)))
    return dict(client=dict(client), annee=annee, enlevements=enl, volume_total_l=sum(e["volume_l"] or 0 for e in enl),
                positifs=sum(1 for e in enl if e["depistage"] == "positif"))
