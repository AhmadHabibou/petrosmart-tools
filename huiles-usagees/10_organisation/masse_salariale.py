"""Lot 10 : cout employeur des postes a partir des salaires de marche sources et des cotisations CNPS,
compare aux hypotheses de salaires du modele financier (lot 9).

Sortie : 10_organisation/masse_salariale.md
"""
from pathlib import Path
import sys

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from commun.hypotheses import val  # noqa: E402
from commun.format import nombre, pct  # noqa: E402

# Cotisations patronales CNPS [S-85]
PENSION_EMPLOYEUR = 0.042
PRESTATIONS_FAMILIALES = 0.07
ACCIDENTS_TRAVAIL = {"bas": 0.0175, "central": 0.025, "haut": 0.05}  # selon le risque de l'entreprise
PLAFOND_PENSION_PF = 750_000  # FCFA par mois [S-85]

# Salaires bruts mensuels de marche (FCFA)
MARCHE = {
    "Technicien de terrain (purification, prélèvements)": (102_544, 166_235, 229_926, "[S-86], fourchette « technicien » à 80 %, centre = milieu"),
    "Commercial à temps plein, Douala": (250_000, 325_000, 400_000, "[S-87], salaire moyen du secteur formel à Douala"),
    "Gérant ingénieur HSE (référence responsable HSE)": (700_000, 1_000_000, 1_300_000, "[S-86], responsable sécurité HSE"),
}
HYP_LOT9 = {"Technicien de terrain (purification, prélèvements)": ("H-151", 1.0),
            "Commercial à temps plein, Douala": ("H-152", 0.5),
            "Gérant ingénieur HSE (référence responsable HSE)": ("H-150", 1.0)}


def cout_employeur(brut, cas_at="central"):
    base = min(brut, PLAFOND_PENSION_PF)
    return brut + base * (PENSION_EMPLOYEUR + PRESTATIONS_FAMILIALES) + brut * ACCIDENTS_TRAVAIL[cas_at]


def rapport():
    taux = PENSION_EMPLOYEUR + PRESTATIONS_FAMILIALES + ACCIDENTS_TRAVAIL["central"]
    out = ["# Coût employeur des postes et comparaison avec le modèle financier", "",
           "Fichier généré par `10_organisation/masse_salariale.py`.", "",
           f"Cotisations patronales CNPS retenues [S-85] : pension {pct(PENSION_EMPLOYEUR, 1)}, prestations familiales {pct(PRESTATIONS_FAMILIALES, 0)} "
           f"(plafond de {nombre(PLAFOND_PENSION_PF)} FCFA par mois), accidents du travail {pct(ACCIDENTS_TRAVAIL['central'], 1)} en taux central "
           f"(1,75 % à 5 % selon le risque), soit {pct(taux, 1)} au total sous le plafond. Les autres prélèvements assis sur les salaires ne sont pas intégrés (Q-39).", "",
           "| Poste | Brut mensuel bas | central | haut | Coût employeur central | Hypothèse du lot 9 (coût chargé) | Écart du lot 9 sur le marché | Source |",
           "|---|---:|---:|---:|---:|---:|---:|---|"]
    for poste, (b, c, h, src) in MARCHE.items():
        hid, quotite = HYP_LOT9[poste]
        cout = cout_employeur(c) * quotite
        lot9 = val(hid)
        out.append(f"| {poste}{' (mi-temps dans le lot 9)' if quotite < 1 else ''} | {nombre(b)} | {nombre(c)} | {nombre(h)} | {nombre(cout)} | "
                   f"{nombre(lot9)} ({hid}) | {pct(lot9 / cout - 1)} | {src} |")
    out += ["", "Lecture : un écart positif signifie que le modèle financier est prudent (il compte plus que le marché) ; un écart négatif signifie qu'il sous-estime.", ""]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    Path(__file__).with_name("masse_salariale.md").write_text(rapport(), encoding="utf-8")
    print("Lot 10 : masse salariale generee")
