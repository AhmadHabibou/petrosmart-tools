"""Lot 4 bis : budget des quatre preuves de terrain, en trois cas (bas, central, haut).

Toutes les valeurs viennent de commun/hypotheses.py. Sortie : budget_protocoles.md
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from commun.hypotheses import val  # noqa: E402
from commun.format import fcfa, m_fcfa, pct  # noqa: E402

N_ECHANTILLONS_LABO = 12      # 10 a 15 demandes par le cahier des charges ; 12 retenus
N_KITS_DEXSIL = 20            # multiple de 20 impose au-dela de 10 kits [S-15]
N_ENVOIS = 2                  # deux envois groupes d'echantillons vers le laboratoire


def lignes(cas):
    usd = val("H-41", cas)
    fret = 1 + val("H-42", cas)
    p1 = [
        ("Unité de purification du gasoil, location ou mise à disposition 3 mois", "H-47", val("H-47", cas)),
        ("Tournées d'enlèvement sous-traitées à un collecteur agréé", "H-48 x H-49", val("H-48", cas) * val("H-49", cas)),
        ("Frais de mission promoteur et technicien", "H-50", val("H-50", cas)),
    ]
    p2 = [
        ("Matériel de prélèvement", "H-45", val("H-45", cas)),
        (f"{N_KITS_DEXSIL} kits Clor-D-Tect 1000, rendu Douala", "H-40, H-41, H-42", N_KITS_DEXSIL * val("H-40", cas) * usd * fret),
        (f"{N_ECHANTILLONS_LABO} analyses complètes en laboratoire", "H-43", N_ECHANTILLONS_LABO * val("H-43", cas)),
        (f"{N_ENVOIS} envois d'échantillons", "H-44", N_ENVOIS * val("H-44", cas)),
    ]
    p3 = [
        ("Fabrication d'un lot de 200 L par un partenaire autorisé", "H-52", val("H-52", cas)),
        ("Analyseur de gaz loué ou prestataire de mesure", "H-46", val("H-46", cas)),
        ("Analyse du lot avant essai (1 analyse complète)", "H-43", val("H-43", cas)),
    ]
    p4 = [("Déplacements et reproduction", "H-51", val("H-51", cas))]
    return {"1. Pilote commercial 3 mois": p1, "2. Échantillonnage et analyse": p2,
            "3. Essai de combustion": p3, "4. Relevé des sanctions": p4}


def totaux():
    return {cas: {k: sum(x[2] for x in v) for k, v in lignes(cas).items()} for cas in ("bas", "central", "haut")}


def rapport():
    t = totaux()
    out = ["# Budget des preuves de terrain (lot 4 bis)", "",
           "Fichier généré par `04b_validation_terrain/budget_protocoles.py`. Montants en M FCFA. Statut : supposé, à remplacer par les devis.", "",
           "| Protocole | Poste | Hypothèses | Bas | Central | Haut |", "|---|---|---|---:|---:|---:|"]
    lb, lc, lh = lignes("bas"), lignes("central"), lignes("haut")
    for k in lc:
        for (a, b, c) in zip(lb[k], lc[k], lh[k]):
            out.append(f"| {k} | {b[0]} | {b[1]} | {m_fcfa(a[2])} | {m_fcfa(b[2])} | {m_fcfa(c[2])} |")
        out.append(f"| **{k}** | **Sous-total** | | **{m_fcfa(t['bas'][k])}** | **{m_fcfa(t['central'][k])}** | **{m_fcfa(t['haut'][k])}** |")
    tot = {c: sum(t[c].values()) for c in t}
    out.append(f"| **Total** | | | **{m_fcfa(tot['bas'])}** | **{m_fcfa(tot['central'])}** | **{m_fcfa(tot['haut'])}** |")
    out += ["", f"Total central : {fcfa(tot['central'])}. Le pilote n°1 représente "
            f"{pct(t['central']['1. Pilote commercial 3 mois'] / tot['central'])} du total central.", ""]
    return "\n".join(out) + "\n", tot


if __name__ == "__main__":
    texte, tot = rapport()
    Path(__file__).with_name("budget_protocoles.md").write_text(texte, encoding="utf-8")
    print("Lot 4 bis : budget central", round(tot["central"]))
