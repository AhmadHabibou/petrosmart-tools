"""Lot 5 : bilan matiere et energie du pretraitement (decantation, puis deshydratation sous vide),
pour trois qualites d'huile entrante, dimensionnement et matrice des filieres.

Sorties : 05_technique/bilan_procede.md, 05_technique/matrice_filieres.md
"""
from pathlib import Path
import sys

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from commun.hypotheses import val  # noqa: E402
from commun.format import nombre, pct  # noqa: E402

LATENT_EAU_70C = 2333.0  # kJ/kg, chaleur latente de vaporisation de l'eau vers 70 degC (tables de vapeur)
QUALITES = {"peu contaminée": "bas", "moyennement contaminée": "central", "très contaminée": "haut"}
TYA_DEBITS_L_MIN = [10, 20, 30, 50, 100, 150, 200, 250, 300]  # gamme annoncee [S-74]
HEURES_POSTE = 8


def bilan(qualite_cas, cas_proc="central", m=1000.0):
    """Bilan pour m kg d'huile entrante. qualite_cas fixe H-100 a H-102 ; cas_proc fixe les autres."""
    w, s, l = (val(h, qualite_cas) for h in ("H-100", "H-101", "H-102"))
    huile = m * (1 - w - s - l)
    # decantation et filtration
    eau_decant = m * w * val("H-103", cas_proc)
    sed_retire = m * s * val("H-104", cas_proc)
    huile_boues = sed_retire * val("H-111", cas_proc)
    m2 = m - eau_decant - sed_retire - huile_boues
    eau_2 = m * w - eau_decant
    # deshydratation sous vide
    legers = m * l
    base_produit = (huile - huile_boues) + (m * s - sed_retire)
    eau_res = val("H-105", cas_proc) * base_produit / (1 - val("H-105", cas_proc))
    eau_evap = max(eau_2 - eau_res, 0.0)
    produit = base_produit + min(eau_res, eau_2)
    # energie
    dT = val("H-106", cas_proc) - val("H-109", cas_proc)
    q_sensible = m2 * val("H-107", cas_proc) * dT
    q_eau = eau_evap * LATENT_EAU_70C
    q_legers = legers * val("H-112", cas_proc)
    q_total_kj = (q_sensible + q_eau + q_legers) / val("H-108", cas_proc)
    kwh = q_total_kj / 3600
    entrees = m
    sorties = produit + eau_decant + eau_evap + sed_retire + huile_boues + legers
    return dict(entree=m, eau_decant=eau_decant, boues=sed_retire + huile_boues, eau_evap=eau_evap, legers=legers,
                produit=produit, rendement=produit / m, kwh=kwh, cout_energie=kwh * val("H-113", cas_proc),
                ecart=entrees - sorties)


def debit_requis_l_h(volume_l_an, cas="central"):
    return volume_l_an / (val("H-110", cas) * HEURES_POSTE)


def modele_tya(debit_l_h):
    for q in TYA_DEBITS_L_MIN:
        if q * 60 >= debit_l_h:
            return q
    return None


FILIERES = {
    "F1 Décantation et filtration simples": dict(capital=5, energie=5, qualite=2, autorisation=2, volume=5, maturite=5, residus=3),
    "F2 Décantation puis déshydratation sous vide": dict(capital=4, energie=4, qualite=3, autorisation=2, volume=5, maturite=4, residus=3),
    "F3 Terre adsorbante activée (procédé publié au Cameroun)": dict(capital=3, energie=3, qualite=4, autorisation=2, volume=4, maturite=2, residus=1),
    "F4 Distillation sous vide": dict(capital=2, energie=2, qualite=4, autorisation=1, volume=3, maturite=3, residus=2),
    "F5 Re-raffinage en huile de base": dict(capital=1, energie=1, qualite=5, autorisation=1, volume=1, maturite=4, residus=2),
    "F6 Remise à un valorisateur existant, sans traitement propre": dict(capital=5, energie=5, qualite=3, autorisation=4, volume=5, maturite=3, residus=5),
}
POIDS = dict(capital=0.20, energie=0.10, qualite=0.10, autorisation=0.20, volume=0.15, maturite=0.15, residus=0.10)
LIB = dict(capital="Capital", energie="Énergie et consommables", qualite="Qualité du produit", autorisation="Autorisations",
           volume="Adéquation au volume", maturite="Maturité et risque technique", residus="Résidus")


def rapport_bilan():
    out = ["# Bilan matière et énergie du prétraitement", "",
           "Fichier généré par `05_technique/procede.py`. Base : 1 000 kg d'huile usagée entrante. Filière simulée : décantation et filtration, puis déshydratation sous vide (F2). Statut : supposé (H-100 à H-113).", "",
           "| Grandeur (kg ou kWh) | " + " | ".join(QUALITES) + " |", "|---|" + "---:|" * len(QUALITES)]
    b = {q: bilan(c) for q, c in QUALITES.items()}
    lignes = [("Huile entrante", "entree"), ("Eau libre décantée", "eau_decant"), ("Boues (sédiments et huile entraînée)", "boues"),
              ("Eau évaporée sous vide", "eau_evap"), ("Fractions légères condensées", "legers"), ("Produit déshydraté", "produit")]
    for lib, k in lignes:
        out.append(f"| {lib} | " + " | ".join(nombre(b[q][k], 1) for q in QUALITES) + " |")
    out.append("| Rendement en produit | " + " | ".join(pct(b[q]["rendement"], 1) for q in QUALITES) + " |")
    out.append("| Énergie électrique (kWh/t) | " + " | ".join(nombre(b[q]["kwh"], 1) for q in QUALITES) + " |")
    out.append("| Coût de l'énergie (FCFA/t) | " + " | ".join(nombre(b[q]["cout_energie"]) for q in QUALITES) + " |")
    out.append("| Écart de bouclage (kg) | " + " | ".join(nombre(b[q]["ecart"], 3) for q in QUALITES) + " |")
    out += ["", f"Le premier business plan retenait un rendement de {pct(val('H-05'))} (H-05). "
            f"La simulation donne {pct(b['très contaminée']['rendement'], 1)} à {pct(b['peu contaminée']['rendement'], 1)} selon la qualité, avant toute perte de lot refusé (chlore, PCB).", "",
            "## Dimensionnement", "", "| Volume traité (L/an) | Débit requis (L/h, 1 poste) | Plus petit TYA suffisant (L/min) |", "|---:|---:|---:|"]
    for v in (320_000, val("H-96", "haut") + val("H-97", "haut") * val("H-01"), 1_200_000):
        d = debit_requis_l_h(v)
        out.append(f"| {nombre(v)} | {nombre(d)} | {modele_tya(d)} |")
    out += ["", "320 000 L/an : seuil de collecte de D-06 ; ligne 2 : collecte urbaine haute (H-96) et 25 clients forestiers (H-97 haut) ; 1 200 000 L/an : collecte urbaine du premier business plan (H-02). "
            "Le plus petit modèle de la gamme TYA (10 L/min, soit 600 L/h) [S-74] couvre tous les cas sur un poste : le débit n'est pas une contrainte, la matière première l'est.", ""]
    return "\n".join(out) + "\n", b


def rapport_matrice():
    score = {f: sum(POIDS[c] * n[c] for c in POIDS) for f, n in FILIERES.items()}
    out = ["# Matrice multicritère des filières de traitement", "",
           "Fichier généré par `05_technique/procede.py`. Notes de 1 (défavorable) à 5 (favorable), justifiées dans `lot5_technique.md`.", "",
           "| Filière | " + " | ".join(f"{LIB[c]} ({pct(POIDS[c])})" for c in POIDS) + " | Score |", "|---|" + "---:|" * (len(POIDS) + 1)]
    for f in sorted(FILIERES, key=lambda k: -score[k]):
        out.append(f"| {f} | " + " | ".join(str(FILIERES[f][c]) for c in POIDS) + f" | {nombre(score[f], 2)} |")
    return "\n".join(out) + "\n", score


if __name__ == "__main__":
    t, _ = rapport_bilan()
    Path(__file__).with_name("bilan_procede.md").write_text(t, encoding="utf-8")
    m, sc = rapport_matrice()
    Path(__file__).with_name("matrice_filieres.md").write_text(m, encoding="utf-8")
    print("Lot 5 : filiere en tete", max(sc, key=sc.get))
