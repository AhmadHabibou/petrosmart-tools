"""Lot 8 : comparaison chiffree et matrice multicritere des modeles d'entreprise.

Sortie : 08_modele_entreprise/comparaison_modeles.md
"""
from pathlib import Path
import importlib.util
import sys

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from commun.modeles import MODELES, indicateurs, point_mort_clients, marge_par_client, flux, h  # noqa: E402
from commun.format import m_fcfa, nombre, pct  # noqa: E402

_spec = importlib.util.spec_from_file_location("calendrier", RACINE / "02_reglementaire" / "calendrier.py")
calendrier = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(calendrier)

MOIS = 30.4
_, FIN = calendrier.planifier("central")

# Delai avant le revenu propre au modele (mois). M1, M4, M5 : premier contrat signe apres
# prospection (2 mois) ou purification immediate avec unite louee (1 mois).
# M2 : fin du permis (etape C) ; M3 : fin du permis et de l'etablissement classe (etapes C et D).
DELAI = {"M1": 2, "M2": FIN["C"] / MOIS, "M3": max(FIN["C"], FIN["D"]) / MOIS, "M4": 2, "M5": 1}

# Jugements d'expert (1 = defavorable, 5 = favorable), justifies dans lot8_modele_entreprise.md
JUGEMENTS = {
    "risque_reglementaire": {"M1": 4, "M2": 2, "M3": 1, "M4": 4, "M5": 4},
    "dependance_hypotheses": {"M1": 3, "M2": 2, "M3": 1, "M4": 3, "M5": 3},
    "croissance_par_etapes": {"M1": 4, "M2": 3, "M3": 1, "M4": 3, "M5": 5},
    "adequation_profil": {"M1": 5, "M2": 4, "M3": 3, "M4": 3, "M5": 5},
}

POIDS = {"capital_initial": 0.20, "besoin_financement": 0.15, "delai": 0.10, "risque_reglementaire": 0.15,
         "dependance_hypotheses": 0.15, "marge": 0.10, "croissance_par_etapes": 0.10, "adequation_profil": 0.05}

LIBELLES = {"capital_initial": "Capital initial (année 0)", "besoin_financement": "Besoin de financement maximal",
            "delai": "Délai avant revenu propre", "risque_reglementaire": "Risque réglementaire",
            "dependance_hypotheses": "Dépendance aux hypothèses non vérifiées", "marge": "Marge (VAN avec valeur terminale)",
            "croissance_par_etapes": "Croissance par étapes", "adequation_profil": "Adéquation au profil du promoteur"}


def _echelle(valeurs, plus_bas_meilleur):
    lo, hi = min(valeurs.values()), max(valeurs.values())
    if hi == lo:
        return {k: 3.0 for k in valeurs}
    return {k: (1 + 4 * (hi - v) / (hi - lo)) if plus_bas_meilleur else (1 + 4 * (v - lo) / (hi - lo)) for k, v in valeurs.items()}


def notes():
    ind = {m: indicateurs(m) for m in MODELES}
    brut = {
        "capital_initial": {m: flux(m)[0]["capex"] for m in MODELES},
        "besoin_financement": {m: ind[m]["besoin_financement"] for m in MODELES},
        "delai": DELAI,
        "marge": {m: ind[m]["van_vt"] for m in MODELES},
    }
    n = {"capital_initial": _echelle(brut["capital_initial"], True),
         "besoin_financement": _echelle(brut["besoin_financement"], True),
         "delai": _echelle(brut["delai"], True),
         "marge": _echelle(brut["marge"], False)}
    n.update(JUGEMENTS)
    score = {m: sum(POIDS[c] * n[c][m] for c in POIDS) for m in MODELES}
    return brut, n, score


def rapport():
    out = ["# Comparaison chiffrée des modèles d'entreprise", "",
           "Fichier généré par `08_modele_entreprise/comparaison.py`. Montants en M FCFA. Flux annuels non endettés, années 0 à 5. "
           "Statut : supposé (hypothèses H-80 à H-99 et premier business plan [S-29]).", "",
           "## Indicateurs par scénario", ""]
    for sc in ("pessimiste", "base", "optimiste"):
        out += [f"### Scénario {sc}", "",
                "| Modèle | Capital année 0 | Besoin de financement maximal | VAN 5 ans sans valeur terminale | VAN avec valeur terminale | CA année 5 | Résultat net année 5 |",
                "|---|---:|---:|---:|---:|---:|---:|"]
        for m in MODELES:
            i = indicateurs(m, sc)
            out.append(f"| {m} | {m_fcfa(flux(m, sc)[0]['capex'], 1)} | {m_fcfa(i['besoin_financement'], 1)} | {m_fcfa(i['van'], 1)} | "
                       f"{m_fcfa(i['van_vt'], 1)} | {m_fcfa(i['ca_an5'], 1)} | {m_fcfa(i['rn_an5'], 1)} |")
        out.append("")
    out += ["La valeur terminale est une rente perpétuelle sans croissance du flux d'exploitation de l'année 5, actualisée à "
            f"{pct(h('H-98', 'base'))}. Les scénarios combinent toutes les bornes défavorables (pessimiste) ou favorables (optimiste) : ce sont des enveloppes, pas des cas probables.", "",
            "## Point mort en nombre de clients forestiers (scénario de base)", "",
            "| Modèle | Contribution annuelle par client | Clients nécessaires pour couvrir les charges fixes de structure |", "|---|---:|---:|"]
    for m in ("M1", "M4", "M5"):
        out.append(f"| {m} | {m_fcfa(marge_par_client(m), 2)} | {nombre(point_mort_clients(m), 1)} |")
    from commun.hypotheses import HYPOTHESES as _H, Hypothese as _Hy
    o80 = _H["H-80"]
    _H["H-80"] = _Hy(o80.id, o80.libelle, 3e6, 3e6, 3e6, o80.unite, o80.justification, o80.impact, o80.verification)
    out += ["", "Test du contre-expert, contrat de conformité à 3 M FCFA par an : "
            + " ; ".join(f"{m} : contribution {m_fcfa(marge_par_client(m), 2)} M FCFA, point mort {nombre(point_mort_clients(m), 1)} clients" for m in ("M1", "M5")) + "."]
    _H["H-80"] = o80
    out += ["", "M2 et M3 ont la même contribution par client que M1, plus des charges fixes propres au traitement (H-90, H-91) que seuls les volumes d'huiles peuvent couvrir.", "",
            "## Sensibilité du modèle 3 au prix du combustible (scénario de base)", "",
            "| Prix du combustible (FCFA/L) | VAN avec valeur terminale |", "|---:|---:|"]
    import commun.modeles as mod
    from commun.hypotheses import HYPOTHESES, Hypothese
    origine = HYPOTHESES["H-04"]
    for prix in (250, 331, 400):
        HYPOTHESES["H-04"] = Hypothese(origine.id, origine.libelle, prix, prix, prix, origine.unite,
                                       origine.justification, origine.impact, origine.verification)
        out.append(f"| {nombre(prix)} | {m_fcfa(mod.indicateurs('M3')['van_vt'], 1)} |")
    HYPOTHESES["H-04"] = origine
    out += ["", "250 FCFA/L : seuil du premier business plan [S-29] ; 331 FCFA/L : prix moyen converti des carburants et lubrifiants importés en 2025 (`04_marche/gisement.md`) ; 400 FCFA/L : H-04.", ""]
    brut, n, score = notes()
    out += ["## Matrice multicritère", "",
            "Notes de 1 (défavorable) à 5 (favorable). Les quatre premiers critères chiffrés sont mis à l'échelle entre le meilleur et le moins bon modèle ; les autres sont des jugements d'expert justifiés dans `lot8_modele_entreprise.md`.", "",
            "| Critère | Poids | " + " | ".join(MODELES) + " |", "|---|---:|" + "---:|" * len(MODELES)]
    for c in POIDS:
        out.append(f"| {LIBELLES[c]} | {pct(POIDS[c])} | " + " | ".join(nombre(n[c][m], 1) for m in MODELES) + " |")
    out.append("| **Score pondéré** | | " + " | ".join(f"**{nombre(score[m], 2)}**" for m in MODELES) + " |")
    out += ["", "Valeurs brutes des critères chiffrés :", "",
            "| Critère | " + " | ".join(MODELES) + " |", "|---|" + "---:|" * len(MODELES)]
    out.append("| Capital année 0 (M FCFA) | " + " | ".join(m_fcfa(brut["capital_initial"][m], 1) for m in MODELES) + " |")
    out.append("| Besoin de financement (M FCFA) | " + " | ".join(m_fcfa(brut["besoin_financement"][m], 1) for m in MODELES) + " |")
    out.append("| Délai avant revenu propre (mois) | " + " | ".join(nombre(brut["delai"][m], 1) for m in MODELES) + " |")
    out.append("| VAN avec valeur terminale (M FCFA) | " + " | ".join(m_fcfa(brut["marge"][m], 1) for m in MODELES) + " |")
    classement = sorted(MODELES, key=lambda m: -score[m])
    out += ["", "Classement : " + ", ".join(f"{m} ({nombre(score[m], 2)})" for m in classement) + ".", ""]
    return "\n".join(out) + "\n", classement


if __name__ == "__main__":
    texte, cl = rapport()
    Path(__file__).with_name("comparaison_modeles.md").write_text(texte, encoding="utf-8")
    print("Lot 8 : classement", cl)
