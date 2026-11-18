"""Lot 4 ter : matrice multicritere des extensions et tests d'exclusion chiffres.

Sortie : 04c_extensions/matrice_extensions.md
"""
from pathlib import Path
import importlib.util
import sys

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from commun.format import nombre, pct  # noqa: E402
from commun.hypotheses import val  # noqa: E402

_spec = importlib.util.spec_from_file_location("gisement", RACINE / "04_marche" / "gisement.py")
gisement = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gisement)

# Seuils de re-raffinage [S-67] et capital d'une unite de 50 000 t/an [S-67]
SEUIL_RERAFFINAGE_BAS_T = 20_000
SEUIL_RERAFFINAGE_HAUT_T = 60_000
CAPEX_50KT_USD = 40e6

CRITERES = ["marge", "investissement", "appareillage", "autorisation", "synergie"]
POIDS = {"marge": 0.25, "investissement": 0.20, "appareillage": 0.15, "autorisation": 0.20, "synergie": 0.20}

# Notes 1 (defavorable) a 5 (favorable), justifiees dans lot4ter_extensions.md
EXTENSIONS = {
    "E1 Collecte des autres déchets dangereux de chantier (filtres, chiffons, absorbants, batteries, terres)": dict(marge=3, investissement=4, appareillage=4, autorisation=2, synergie=5),
    "E2 Dossier de preuves pour les audits FSC et OLB": dict(marge=4, investissement=5, appareillage=5, autorisation=5, synergie=5),
    "E3 Contrôle qualité du gasoil à la livraison": dict(marge=3, investissement=4, appareillage=3, autorisation=5, synergie=4),
    "E4 Dépollution des sols par biotertre": dict(marge=3, investissement=3, appareillage=3, autorisation=2, synergie=3),
    "E5 Partenariat ou cofinancement avec les distributeurs de lubrifiants": dict(marge=3, investissement=5, appareillage=5, autorisation=4, synergie=4),
    "E6 Extension aux pays de la CEMAC des mêmes groupes forestiers": dict(marge=3, investissement=2, appareillage=4, autorisation=1, synergie=3),
    "E7 Certification ISO 14001 de la société en année 3": dict(marge=2, investissement=3, appareillage=5, autorisation=5, synergie=3),
    "E8 Incitations à l'investissement (loi n°2013/004 modifiée)": dict(marge=2, investissement=5, appareillage=5, autorisation=3, synergie=2),
}


def score(notes):
    return sum(POIDS[c] * notes[c] for c in CRITERES)


def rapport():
    g = gisement.resultats()
    dens = val("H-60")
    out = ["# Matrice des extensions de l'offre", "",
           "Fichier généré par `04c_extensions/extensions.py`. Méthode : matrice multicritère. Notes de 1 (défavorable) à 5 (favorable). Statut : supposé.", "",
           "| Extension | " + " | ".join(f"{c} ({pct(POIDS[c])})" for c in CRITERES) + " | Score |",
           "|---|" + "---:|" * (len(CRITERES) + 1)]
    for nom, nts in sorted(EXTENSIONS.items(), key=lambda kv: -score(kv[1])):
        out.append(f"| {nom} | " + " | ".join(str(nts[c]) for c in CRITERES) + f" | {nombre(score(nts), 2)} |")
    t_bas, t_c, t_haut = (g[c]["parc_total"] * dens / 1000 for c in ("bas", "central", "haut"))
    t_etude = gisement.GISEMENT_ETUDE_T
    out += ["", "## Exclusions chiffrées", "", "### Re-raffinage en huile de base", "",
            f"Gisement national estimé par le parc : {nombre(t_bas)} à {nombre(t_haut)} t/an, {nombre(t_c)} t/an en cas central (conversion par H-60). "
            f"Seuil de rentabilité d'une unité de re-raffinage : {nombre(SEUIL_RERAFFINAGE_BAS_T)} t/an selon un concepteur de procédé, {nombre(SEUIL_RERAFFINAGE_HAUT_T)} t/an selon l'OCDE (2005) [S-67].", "",
            f"- Même en captant tout le gisement central, la société n'atteint que {pct(t_c / SEUIL_RERAFFINAGE_BAS_T)} du seuil bas.",
            f"- Avec le chiffre de l'étude (70 000 t/an [S-01]), il faudrait capter {pct(SEUIL_RERAFFINAGE_BAS_T / t_etude)} à {pct(SEUIL_RERAFFINAGE_HAUT_T / t_etude)} du gisement national.",
            f"- Une unité de 50 000 t/an représente environ {nombre(CAPEX_50KT_USD / 1e6)} M USD d'investissement [S-67], sans rapport avec le capital du promoteur.",
            "- Conclusion : exclusion confirmée. Certitude : probable.", "",
            "### Crédits carbone", "",
            "- La seule méthode trouvée pour les huiles usagées est celle de l'American Carbon Registry sur le re-raffinage des huiles lubrifiantes, classée inactive [S-68].",
            "- Sa logique de réduction repose sur la combustion évitée des huiles usagées : un projet qui fabrique un combustible brûle ces huiles et ne peut pas revendiquer cette réduction.",
            "- Aucune méthode Verra ou Gold Standard propre aux huiles usagées n'a été trouvée.",
            "- Conclusion : exclusion confirmée. Certitude : probable.", ""]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    Path(__file__).with_name("matrice_extensions.md").write_text(rapport(), encoding="utf-8")
    print("Lot 4 ter : matrice generee")
