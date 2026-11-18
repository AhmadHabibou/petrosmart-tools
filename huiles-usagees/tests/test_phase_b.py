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
