"""Concordance entre les chiffres cites dans les rapports redigés et les fichiers generes."""
from pathlib import Path
import subprocess
import sys

RACINE = Path(__file__).resolve().parents[1]
NBSP = " "


def _lire(rel):
    return (RACINE / rel).read_text(encoding="utf-8").replace(NBSP, " ")


def setup_module(_):
    subprocess.run([sys.executable, str(RACINE / "run_all.py")], check=True, capture_output=True)


def test_chiffres_lot4_concordent():
    g = _lire("04_marche/gisement.md")
    for fragment in ("| 74 % | 27 % |", "| 20 % | 7 % |", "312 ; 331 ; 370", "6,8 fois", "**5,3** | **11,4** | **21,4**", "| 77,8 |"):
        assert fragment in g, fragment


def test_chiffres_lot2_concordent():
    c = _lire("02_reglementaire/calendrier.md")
    assert "soit 6,0 à 25,0 mois" in c


def test_chiffres_lot0_concordent():
    m = _lire("00b_amorcage/matrice_amorcage.md")
    assert "2,40 M FCFA (cas bas) à 21,00 M FCFA" in m
    b = _lire("04b_validation_terrain/budget_protocoles.md")
    assert "8 869 600 FCFA" in b


def test_sources_citees_existent():
    sources = _lire("00_registres/sources.md")
    import re
    ids = set(re.findall(r"^\| (S-\d+) \|", sources, re.M))
    for md in RACINE.rglob("*.md"):
        for sid in re.findall(r"\[(S-\d+)\]", md.read_text(encoding="utf-8")):
            assert sid in ids, f"{md.name} cite {sid} absent du registre"


def test_hypotheses_citees_existent():
    import re
    sys.path.insert(0, str(RACINE))
    from commun.hypotheses import HYPOTHESES
    for md in RACINE.rglob("*.md"):
        if md.name == "hypotheses.md":
            continue
        for hid in re.findall(r"\bH-\d{2}\b", md.read_text(encoding="utf-8")):
            assert hid in HYPOTHESES, f"{md.name} cite {hid} absent du registre"


def test_chiffres_lot8_concordent():
    c = _lire("08_modele_entreprise/comparaison_modeles.md")
    for fragment in ("**4,14** | **2,54** | **1,50** | **3,79** | **4,35**", "| M1 | 5,14 | 7,8 |", "| M5 | 5,14 | 8,9 |",
                     "| 250 | -59,1 |", "| 400 | 241,4 |", "contribution 2,14 M FCFA, point mort 18,7", "point mort 21,5",
                     "| Capital année 0 (M FCFA) | 15,0 | 15,0 | 87,0 | 4,0 | 4,0 |"):
        assert fragment in c, fragment


def test_chiffres_lot4ter_concordent():
    e = _lire("04c_extensions/matrice_extensions.md")
    assert "10 238 t/an en cas central" in e and "51 % du seuil bas" in e


def test_chiffres_lot5_concordent():
    b = _lire("05_technique/bilan_procede.md")
    assert "| 96,3 % | 85,6 % | 65,1 % |" in b
    assert "| 0,000 | 0,000 | 0,000 |" in b
    m = _lire("05_technique/matrice_filieres.md")
    assert "| 4,30 |" in m and "| 3,55 |" in m


def test_chiffres_lot6_concordent():
    t = _lire("06_logistique/tournees.md")
    for fragment in ("| Sous-traitance à un collecteur agréé (H-48 par enlèvement) | 200 | 200 |", "coefficient de détour calé sur deux paires sourcées : 1,30".capitalize(),
                     "23 420 km", "40 FCFA/L pour 2 400 L"):
        assert fragment in t, fragment


def test_chiffres_lot7_concordent():
    r = _lire("07_hse_eies/matrice_risques_hse.md")
    assert "avant mesures : 11 sur 12 ; après mesures : 1 sur 12" in r
    e = _lire("07_hse_eies/emissions.md")
    assert "| 100 | 90,0 | 9,00 |" in e


def test_chiffres_lot9_concordent():
    f = _lire("09_finance/resultats_finance.md")
    for fragment in ("| VAN à 5 ans, sans valeur terminale | -190,3 | 9,0 | 321,8 |", "| 27,5 % |", "année 2 : -2,02 ; année 3 : 1,66",
                     "| 29,5 % |", "| 2,3 % |", "| 45,6 |", "8,5 M FCFA, en plus", "| VAN à 5 ans | 9,0 | -23,6 |",
                     "| VAN avec valeur terminale | 137,4 | 26,9 |", "| mois 20 |", "0,000000 FCFA"):
        assert fragment in f, fragment


def test_lot9_amorcage_coherent_avec_lot0():
    sys.path.insert(0, str(RACINE))
    from commun.hypotheses import HYPOTHESES
    import importlib.util
    spec = importlib.util.spec_from_file_location("mat", RACINE / "00b_amorcage" / "matrice_amorcage.py")
    mat = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mat)
    top3 = mat.evaluer()[:3]
    h = HYPOTHESES["H-161"]
    assert abs(sum(d["rev_central"] for d in top3) / 12 - h.central) < 1
    assert abs(sum(d["rev_bas"] for d in top3) / 12 - h.bas) < 1
    assert abs(sum(d["rev_haut"] for d in top3) / 12 - h.haut) < 1


def test_xlsx_formules_egales_python(tmp_path):
    import shutil
    from openpyxl import load_workbook
    if shutil.which("soffice") is None:
        import pytest
        pytest.skip("LibreOffice absent")
    src = RACINE / "09_finance" / "modele_financier.xlsx"
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx", "--outdir", str(tmp_path), str(src)],
                   check=True, capture_output=True, timeout=180)
    ws = load_workbook(tmp_path / "modele_financier.xlsx", data_only=True)["Mensuel"]
    for r in range(1, ws.max_row + 1):
        if str(ws.cell(r, 1).value).startswith("Contrôle"):
            ecarts = [abs(ws.cell(r, c).value or 0) for c in range(2, 62)]
            assert max(ecarts) < 1
            return
    raise AssertionError("ligne de controle absente")


def test_chiffres_lot10_concordent():
    m = _lire("10_organisation/masse_salariale.md")
    assert "| 1 109 000 | 600 000 (H-150) | -46 % |" in m and "13,7 %" in m


def test_chiffres_lot11_concordent():
    m = _lire("11_juridique/matrice_forme_sociale.md")
    assert "**2,60** | **4,05** | **4,10** | **3,40**" in m
    assert "SAS 4,10, SARL 4,05, SA 3,40, établissement individuel 2,60" in _lire("11_juridique/lot11_juridique.md")


def test_guides_entretien_10_a_15_questions():
    import re
    texte = _lire("12_parties_prenantes/guides_entretien.md")
    blocs = re.split(r"^## ", texte, flags=re.M)[1:]
    assert len(blocs) == 34
    for b in blocs:
        n = len(re.findall(r"^\d+\. ", b, flags=re.M))
        assert 10 <= n <= 15, b.splitlines()[0]


def test_chiffres_lot13_concordent():
    r = _lire("13_risques/registre_risques.md")
    assert "17 sur 20 avant mesures, 2 après mesures" in r and "P04, P11, P18" in r


def test_chiffres_lot14_concordent():
    b = _lire("14_plan_action/budget_preoperationnel.md")
    assert "**16,64** |" in b and "9,84 M FCFA" in b and "marge de seulement 0,16 M FCFA" in b
