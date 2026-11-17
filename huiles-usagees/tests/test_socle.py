from pathlib import Path
import sys

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))

from commun.hypotheses import HYPOTHESES  # noqa: E402
from commun.format import nombre, NBSP  # noqa: E402
from commun.controles import tirets_interdits  # noqa: E402
import importlib.util  # noqa: E402


def _charger(rel):
    spec = importlib.util.spec_from_file_location(rel.replace("/", "_"), RACINE / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_hypotheses_ordonnees():
    for h in HYPOTHESES.values():
        assert h.bas <= h.central <= h.haut, h.id
        assert h.statut in {"supposé", "probable", "vérifié"}


def test_format_francais():
    assert nombre(1234567.5, 1) == f"1{NBSP}234{NBSP}567,5"


def test_lot0_plafond_et_eliminations():
    m = _charger("00b_amorcage/matrice_amorcage.py")
    assert m.depenses_avant_encaissement("haut") <= m.PLAFOND_DEPENSES
    ids = {d["id"] for d in m.evaluer()}
    assert "A7" not in ids  # conflit d'interets avec HIKMA
    assert "A11" not in ids  # depasse le plafond
    assert len(m.evaluer()) >= 3


def test_budget_4bis_coherent():
    m = _charger("04b_validation_terrain/budget_protocoles.py")
    t = m.totaux()
    assert sum(t["bas"].values()) < sum(t["central"].values()) < sum(t["haut"].values())


def test_aucun_tiret_long():
    assert tirets_interdits(RACINE) == []
