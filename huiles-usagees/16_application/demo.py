"""Cree une base de demonstration. TOUTES LES DONNEES SONT FICTIVES : les noms de clients sont
volontairement artificiels (prefixe « DEMO ») et ne designent aucune entreprise reelle.

Usage : python 16_application/demo.py [chemin_de_la_base]
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tracabilite import db, metier  # noqa: E402


def creer_demo(chemin):
    con = db.connecter(chemin)
    db.initialiser(con)
    m = db.maintenant()
    clients = [("c1", "DEMO Exploitant forestier A (fictif)", "forestier"), ("c2", "DEMO Scierie B (fictif)", "forestier"),
               ("c3", "DEMO Garage C (fictif)", "urbain")]
    for cid, nom, t in clients:
        con.execute("INSERT OR IGNORE INTO clients VALUES (?,?,?,?,?,?,?)", (cid, nom, t, "Contact fictif", "000 000 000", 1, m))
    sites = [("s1", "c1", "Chantier fictif 1", 4.5, 14.0, 50), ("s2", "c1", "Atelier fictif 2", 4.6, 14.1, 20),
             ("s3", "c2", "Scierie fictive", 4.4, 13.7, 5), ("s4", "c3", "Atelier fictif Douala", 4.05, 9.7, 0)]
    for sid, cid, nom, lat, lon, piste in sites:
        con.execute("INSERT OR IGNORE INTO sites VALUES (?,?,?,?,?,?,?,?)", (sid, cid, nom, "atelier", lat, lon, piste, m))
    for i in range(1, 13):
        site = ["s1", "s2", "s3", "s4"][i % 4]
        con.execute("INSERT OR IGNORE INTO futs VALUES (?,?,?,?,?,?)", (f"f{i}", f"DEMO-F-{i:04d}", site, "chez_client", "huiles usagees", m))
    enl = [("e1", "s1", "2026-03-10"), ("e2", "s3", "2026-03-12"), ("e3", "s1", "2026-06-15"), ("e4", "s2", "2026-12-05")]
    for eid, sid, d in enl:
        con.execute("INSERT OR IGNORE INTO enlevements (id, site_id, date_prevue, statut, transporteur, cree_le) VALUES (?,?,?,?,?,?)",
                    (eid, sid, d, "planifie", "Transporteur titulaire fictif", m))
    con.commit()
    if con.execute("SELECT statut FROM enlevements WHERE id='e1'").fetchone()["statut"] == "planifie":
        metier.realiser_enlevement(con, "e1", 2400, "negatif", ["f4", "f8"], "2026-03-10")
        metier.realiser_enlevement(con, "e2", 1800, "positif", ["f3"], "2026-03-12")
        metier.realiser_enlevement(con, "e3", 2600, "negatif", [], "2026-06-15")
        lots = {r["enlevement_id"]: r["id"] for r in con.execute("SELECT id, enlevement_id FROM lots")}
        metier.enregistrer_analyse(con, lots["e1"], 420, False, 3.5, None, "Laboratoire fictif", "2026-03-20")
        metier.enregistrer_analyse(con, lots["e2"], 2300, False, None, None, "Laboratoire fictif", "2026-03-25")
        metier.enregistrer_analyse(con, lots["e3"], 610, False, 6.0, None, "Laboratoire fictif", "2026-06-25")
        metier.sortie_stock(con, lots["e2"], 1800, "remise à un éliminateur titulaire fictif", "2026-04-02")
        metier.sortie_stock(con, lots["e1"], 2400, "remise à un valorisateur titulaire fictif", "2026-04-02")
    con.close()
    return chemin


if __name__ == "__main__":
    print("Base de démonstration créée :", creer_demo(sys.argv[1] if len(sys.argv) > 1 else "tracabilite.sqlite"))
