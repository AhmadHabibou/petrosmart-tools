"""Lot 9 : rapport chiffre du modele mensuel. Sortie : 09_finance/resultats_finance.md et modele_financier.xlsx."""
from pathlib import Path
import importlib.util
import sys

import numpy as np

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from commun.format import m_fcfa, nombre, pct  # noqa: E402
from commun.hypotheses import HYPOTHESES  # noqa: E402
import modele_mensuel as mm  # noqa: E402
import export_xlsx  # noqa: E402

N_TIRAGES = 10_000


def _tri(v):
    return "non défini" if v is None else pct(v, 1)


def _mois(v):
    return "non atteint" if v is None else f"mois {v}"


def rapport():
    out = ["# Résultats du modèle financier mensuel", "",
           "Fichier généré par `09_finance/rapport_finance.py`. Trajectoire retenue (D-09) : M5 jusqu'à la porte de l'étape 1, puis M1. "
           "Montants en M FCFA. Statut : supposé (hypothèses listées dans `modele_financier.xlsx`, feuille Hypotheses).", "",
           "## Scénarios", "",
           "| Indicateur | Pessimiste | Base | Optimiste |", "|---|---:|---:|---:|"]
    res = {sc: mm.simuler(mm.parametres(sc)) for sc in ("pessimiste", "base", "optimiste")}
    ind = {sc: r[1] for sc, r in res.items()}
    rows = [("VAN à 5 ans, sans valeur terminale", lambda i: m_fcfa(i["van"], 1)),
            ("VAN avec valeur terminale", lambda i: m_fcfa(i["van_vt"], 1)),
            ("TRI (flux disponibles)", lambda i: _tri(i["tri"])),
            ("Besoin de financement maximal (flux disponibles cumulés)", lambda i: m_fcfa(i["besoin_financement"], 1)),
            ("Trésorerie minimale après apport et emprunt", lambda i: m_fcfa(i["tresorerie_min"], 1)),
            ("Point mort (EBITDA positif durablement)", lambda i: _mois(i["point_mort_mois"])),
            ("Délai de récupération (cumul durablement positif)", lambda i: _mois(i["recuperation_mois"])),
            ("Mois de passage en M1", lambda i: _mois(i["mois_bascule"])),
            ("DSCR minimal annuel", lambda i: "sans dette" if i["dscr_min"] is None else nombre(i["dscr_min"], 2)),
            ("Chiffre d'affaires de l'année 5", lambda i: m_fcfa(i["ca_an5"], 1)),
            ("Résultat net de l'année 5", lambda i: m_fcfa(i["rn_an5"], 1))]
    for lib, f in rows:
        out.append(f"| {lib} | " + " | ".join(f(ind[sc]) for sc in ind) + " |")
    out += ["", "Les scénarios pessimiste et optimiste combinent toutes les bornes défavorables ou favorables : ce sont des enveloppes. La distribution réaliste est donnée par le Monte-Carlo.", ""]

    s = res["base"][0]
    out += ["## Compte de résultat et trésorerie annuels (scénario de base)", "",
            "| Poste | Année 1 | Année 2 | Année 3 | Année 4 | Année 5 |", "|---|---:|---:|---:|---:|---:|"]
    postes = [("Clients forestiers en fin d'année", "clients", "fin"), ("Chiffre d'affaires", "ca", "somme"),
              ("dont contrats de conformité", "ca_contrat", "somme"), ("dont purification du gasoil", "ca_gasoil", "somme"),
              ("dont commission urbaine", "ca_commission_urbaine", "somme"), ("dont activités d'amorçage", "ca_amorcage", "somme"),
              ("Charges d'exploitation", "charges", "somme"), ("EBITDA", "ebitda", "somme"), ("Amortissements", "amortissement", "somme"),
              ("Intérêts", "interets", "somme"), ("Impôt", "impot", "somme"), ("Résultat net", "resultat_net", "somme"),
              ("Investissements", "capex", "somme"), ("Flux de trésorerie disponible", "flux_disponible", "somme"),
              ("Trésorerie de fin d'année", "tresorerie", "fin"), ("Créances clients (BFR) en fin d'année", "creances", "fin"),
              ("Capital restant dû en fin d'année", "capital_restant", "fin")]
    for lib, k, mode in postes:
        vals = []
        for a in range(5):
            serie = s[k][12 * a: 12 * a + 12]
            v = serie[-1] if mode == "fin" else serie.sum()
            vals.append(nombre(v, 1) if k == "clients" else m_fcfa(v, 1))
        out.append(f"| {lib} | " + " | ".join(vals) + " |")
    dscr = ind["base"]["dscr"]
    out += ["", "DSCR par année (EBITDA moins impôt, divisé par le service de la dette) : "
            + " ; ".join(f"année {a} : {nombre(v, 2)}" for a, v in dscr.items()) + ".",
            f"Apport ou ligne de trésorerie supplémentaire nécessaire pour que la trésorerie reste positive en scénario de base : "
            f"{m_fcfa(max(0.0, -ind['base']['tresorerie_min']), 1)} M FCFA, en plus de l'apport de {m_fcfa(HYPOTHESES['H-157'].central, 1)} M FCFA (H-157) et de l'emprunt de {m_fcfa(HYPOTHESES['H-158'].central, 1)} M FCFA (H-158).",
            f"Écart maximal du bilan (actif moins passif) sur 60 mois : {nombre(float(np.abs(mm.bilan_equilibre(s)).max()), 6)} FCFA.", ""]

    base, tor = mm.tornado()
    out += ["## Analyse de sensibilité (tornado, VAN avec valeur terminale)", "",
            f"VAN de base : {m_fcfa(base, 1)} M FCFA. Chaque hypothèse est placée à sa borne basse puis haute, les autres restant centrales.", "",
            "| Hypothèse | Libellé | VAN à la borne basse | VAN à la borne haute | Amplitude |", "|---|---|---:|---:|---:|"]
    for k, lo, hi, amp in tor:
        out.append(f"| {k} | {HYPOTHESES[k].libelle} | {m_fcfa(lo, 1)} | {m_fcfa(hi, 1)} | {m_fcfa(amp, 1)} |")

    mc = mm.monte_carlo(N_TIRAGES)
    out += ["", f"## Simulation de Monte-Carlo ({nombre(N_TIRAGES)} tirages)", "",
            "Lois triangulaires (borne basse, valeur centrale, borne haute) sur " + ", ".join(mm.MC_CLES) + ". Graine fixe : résultats reproductibles.", "",
            "| Résultat | Valeur |", "|---|---:|",
            f"| Probabilité de VAN à 5 ans négative (sans valeur terminale) | {pct(mc['p_van5_negative'], 1)} |",
            f"| Probabilité de VAN avec valeur terminale négative | {pct(mc['p_van_negative'], 1)} |",
            f"| VAN avec valeur terminale, 10e centile | {m_fcfa(mc['van_p10'], 1)} |",
            f"| VAN avec valeur terminale, médiane | {m_fcfa(mc['van_p50'], 1)} |",
            f"| VAN avec valeur terminale, 90e centile | {m_fcfa(mc['van_p90'], 1)} |",
            f"| Besoin de financement maximal au 90e centile | {m_fcfa(mc['besoin_p90'], 1)} |", ""]

    pg = mm.parametres()
    pg["guerre_prix"] = True
    ig = mm.simuler(pg)[1]
    out += ["## Scénario de guerre des prix", "",
            f"À partir du mois 25, un concurrent ou le circuit informel offre l'enlèvement gratuit : le prix des contrats baisse de {pct(HYPOTHESES['H-162'].central)} (H-162) "
            "et la commission urbaine disparaît.", "",
            "| Indicateur | Base | Guerre des prix |", "|---|---:|---:|",
            f"| VAN à 5 ans | {m_fcfa(ind['base']['van'], 1)} | {m_fcfa(ig['van'], 1)} |",
            f"| VAN avec valeur terminale | {m_fcfa(ind['base']['van_vt'], 1)} | {m_fcfa(ig['van_vt'], 1)} |",
            f"| Besoin de financement maximal | {m_fcfa(ind['base']['besoin_financement'], 1)} | {m_fcfa(ig['besoin_financement'], 1)} |",
            f"| Résultat net de l'année 5 | {m_fcfa(ind['base']['rn_an5'], 1)} | {m_fcfa(ig['rn_an5'], 1)} |", ""]

    spec = importlib.util.spec_from_file_location("comparaison", RACINE / "08_modele_entreprise" / "comparaison.py")
    comp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(comp)
    out += ["## Comparaison avec les modèles du lot 8 (comparateur annuel, scénario de base)", "",
            "| Modèle | Besoin de financement | VAN avec valeur terminale |", "|---|---:|---:|"]
    for m in comp.MODELES:
        i = comp.indicateurs(m)
        out.append(f"| {m} (annuel) | {m_fcfa(i['besoin_financement'], 1)} | {m_fcfa(i['van_vt'], 1)} |")
    out.append(f"| Trajectoire M5 puis M1 (mensuel) | {m_fcfa(ind['base']['besoin_financement'], 1)} | {m_fcfa(ind['base']['van_vt'], 1)} |")
    out += ["", "Le modèle mensuel fait monter les charges de structure avec les embauches et ajoute la marge des activités d'amorçage : "
            "son besoin de financement est plus faible que celui des comparateurs annuels à charges fixes pleines.", ""]
    return "\n".join(out) + "\n", ind, mc


if __name__ == "__main__":
    texte, ind, mc = rapport()
    Path(__file__).with_name("resultats_finance.md").write_text(texte, encoding="utf-8")
    export_xlsx.construire()
    print("Lot 9 : VAN base", round(ind["base"]["van"] / 1e6, 1), "P(VAN5<0)", round(mc["p_van5_negative"], 3))
