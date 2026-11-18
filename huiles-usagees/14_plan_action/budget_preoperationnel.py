"""Lot 14 : budget pre-operationnel des 6 premiers mois, mois par mois (decaissements et encaissements prevus).

Regles : le materiel du pilote est le materiel loue du modele M5 (H-93 en depot au mois 3, H-94 en loyers a partir
du mois 4), pour ne pas compter deux fois l'unite de purification (H-47 du lot 4 bis n'est donc pas repris).
L'essai de combustion (4 bis n°3) est hors budget de base : il n'est utile qu'a l'etape 4 (D-06).
Sortie : 14_plan_action/budget_preoperationnel.md
"""
from pathlib import Path
import importlib.util
import sys

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from commun.hypotheses import val  # noqa: E402
from commun.format import m_fcfa, nombre  # noqa: E402

_spec = importlib.util.spec_from_file_location("bp", RACINE / "04b_validation_terrain" / "budget_protocoles.py")
bp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bp)

MOIS = 6


def postes():
    L = bp.lignes("central")
    p2 = {x[0]: x[2] for x in L["2. Échantillonnage et analyse"]}
    p1 = {x[0]: x[2] for x in L["1. Pilote commercial 3 mois"]}
    p4 = sum(x[2] for x in L["4. Relevé des sanctions"])
    d = {}

    def ajoute(nom, src, mois_val):
        d[nom] = (src, [mois_val.get(m, 0.0) for m in range(1, MOIS + 1)])

    ajoute("Création de la société", "H-30", {1: val("H-30")})
    ajoute("Supports commerciaux", "H-31", {1: val("H-31")})
    ajoute("Déplacements de prospection", "H-32", {m: val("H-32") / 3 for m in (1, 2, 3)})
    k_mat = next(k for k in p2 if k.startswith("Matériel"))
    k_kits = next(k for k in p2 if "Clor-D-Tect" in k)
    k_ana = next(k for k in p2 if "analyses" in k)
    k_env = next(k for k in p2 if "envois" in k)
    ajoute("Échantillonnage : matériel de prélèvement", "H-45", {1: p2[k_mat]})
    ajoute("Échantillonnage : kits de dépistage", "H-40 à H-42", {1: p2[k_kits]})
    ajoute("Échantillonnage : analyses de laboratoire", "H-43", {2: p2[k_ana] / 2, 3: p2[k_ana] / 2})
    ajoute("Échantillonnage : envois", "H-44", {2: p2[k_env] / 2, 3: p2[k_env] / 2})
    ajoute("Relevé des sanctions", "H-51", {1: p4 / 2, 2: p4 / 2})
    k_tour = next(k for k in p1 if k.startswith("Tournées"))
    k_miss = next(k for k in p1 if k.startswith("Frais de mission"))
    ajoute("Pilote : enlèvements sous-traités", "H-48, H-49", {m: p1[k_tour] / 3 for m in (4, 5, 6)})
    ajoute("Pilote : frais de mission", "H-50", {m: p1[k_miss] / 3 for m in (4, 5, 6)})
    ajoute("Dépôt de crédit-bail ou location (purificateur, véhicule)", "H-93", {3: val("H-93")})
    ajoute("Loyers de crédit-bail ou location", "H-94", {m: val("H-94") / 12 for m in (4, 5, 6)})
    ajoute("Technicien (coût chargé)", "H-151", {m: val("H-151") for m in (4, 5, 6)})
    ajoute("Frais généraux", "H-153", {m: val("H-153") for m in (4, 5, 6)})
    ajoute("Assurances", "H-154", {m: val("H-154") / 12 for m in (4, 5, 6)})
    return d


def encaissements():
    return {"Marge des activités d'amorçage (lot 0)": ("H-161", [val("H-161")] * MOIS),
            "Contrats pilotes (2 clients, prix annuel au prorata)": ("H-80", [0, 0, 0] + [2 * val("H-80") / 12] * 3)}


def rapport():
    d = postes()
    e = encaissements()
    tete = "| Poste | Hypothèses | " + " | ".join(f"Mois {m}" for m in range(1, MOIS + 1)) + " | Total |"
    sep = "|---|---|" + "---:|" * (MOIS + 1)
    out = ["# Budget pré-opérationnel des 6 premiers mois", "",
           "Fichier généré par `14_plan_action/budget_preoperationnel.py`. Montants en M FCFA, scénario central. Statut : supposé.", "",
           "## Décaissements", "", tete, sep]
    tot = [0.0] * MOIS
    for nom, (src, v) in d.items():
        tot = [a + b for a, b in zip(tot, v)]
        out.append(f"| {nom} | {src} | " + " | ".join(m_fcfa(x) for x in v) + f" | {m_fcfa(sum(v))} |")
    out.append("| **Total des décaissements** | | " + " | ".join(f"**{m_fcfa(x)}**" for x in tot) + f" | **{m_fcfa(sum(tot))}** |")
    out += ["", "## Encaissements prévus", "", tete, sep]
    enc = [0.0] * MOIS
    for nom, (src, v) in e.items():
        enc = [a + b for a, b in zip(enc, v)]
        out.append(f"| {nom} | {src} | " + " | ".join(m_fcfa(x) for x in v) + f" | {m_fcfa(sum(v))} |")
    out.append("| **Total des encaissements** | | " + " | ".join(f"**{m_fcfa(x)}**" for x in enc) + f" | **{m_fcfa(sum(enc))}** |")
    net = [a - b for a, b in zip(enc, tot)]
    cum, c = [], 0.0
    for x in net:
        c += x
        cum.append(c)
    out += ["", "## Solde", "", tete, sep,
            "| Solde du mois | | " + " | ".join(m_fcfa(x) for x in net) + f" | {m_fcfa(sum(net))} |",
            "| Solde cumulé | | " + " | ".join(m_fcfa(x) for x in cum) + " | |", "",
            f"Besoin de financement maximal sur les 6 premiers mois : {m_fcfa(max(0.0, -min(cum)))} M FCFA, "
            + (f"couvert par l'apport initial de {m_fcfa(val('H-157'))} M FCFA (H-157) avec une marge de seulement {m_fcfa(val('H-157') + min(cum))} M FCFA. "
               if val('H-157') + min(cum) >= 0 else f"non couvert par l'apport initial de {m_fcfa(val('H-157'))} M FCFA (H-157). ") +
            "Les encaissements des contrats pilotes sont comptés sans délai de paiement : avec un paiement à 60 jours (H-155), le besoin augmente d'environ deux mois de facturation pilote.", "",
            f"Hors budget de base : essai de combustion (protocole 4 bis n°3), {m_fcfa(sum(x[2] for x in bp.lignes('central')['3. Essai de combustion']))} M FCFA en cas central, à engager seulement à l'étape 4.", ""]
    return "\n".join(out) + "\n", tot, cum


if __name__ == "__main__":
    t, tot, cum = rapport()
    Path(__file__).with_name("budget_preoperationnel.md").write_text(t, encoding="utf-8")
    print("Lot 14 : decaissements 6 mois", round(sum(tot)), "besoin max", round(max(0, -min(cum))))
