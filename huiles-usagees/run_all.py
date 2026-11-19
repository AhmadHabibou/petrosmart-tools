"""Regenere toutes les sorties chiffrees du depot, puis controle les regles de forme.

Usage : python run_all.py   (ou : make)
"""
from pathlib import Path
import os
import runpy
import sys

RACINE = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))

ETAPES = [
    "commun/registres.py",
    "00b_amorcage/matrice_amorcage.py",
    "04b_validation_terrain/budget_protocoles.py",
    "02_reglementaire/calendrier.py",
    "04_marche/gisement.py",
    "04c_extensions/extensions.py",
    "08_modele_entreprise/comparaison.py",
    "05_technique/procede.py",
    "06_logistique/tournees.py",
    "07_hse_eies/risques_hse.py",
    "10_organisation/masse_salariale.py",
    "11_juridique/forme_sociale.py",
    "12_parties_prenantes/parties_prenantes.py",
    "13_risques/registre_risques.py",
    "14_plan_action/budget_preoperationnel.py",
    "09_finance/rapport_finance.py",
    "15_kit_operationnel/construire_kit.py",
    "17_synthese/construire_synthese.py",
    "17_synthese/construire_business_plans.py",
]


def main() -> int:
    for e in ETAPES:
        print(f"> {e}")
        sys.argv = [e] + (["--sans-pdf"] if os.environ.get("HUILES_SANS_PDF") else [])
        runpy.run_path(str(RACINE / e), run_name="__main__")
    from commun.controles import tirets_interdits
    fautes = tirets_interdits(RACINE)
    if fautes:
        print("Tirets longs ou moyens trouves :")
        for f in fautes:
            print("  ", f)
        return 1
    print("Controle des tirets : aucun tiret long ni moyen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
