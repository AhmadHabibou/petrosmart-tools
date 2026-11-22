"""Controles de coherence comptable. Les fonctions d'extraction seront branchees sur l'ERP au module 2."""
from decimal import Decimal


def piece_equilibree(lignes):
    return sum(Decimal(str(l["debit"])) for l in lignes) == sum(Decimal(str(l["credit"])) for l in lignes)


def numerotation_continue(numeros):
    """Renvoie (doublons, trous) sur une suite de numeros entiers."""
    vus, doublons = set(), set()
    for n in numeros:
        (doublons if n in vus else vus).add(n)
    trous = sorted(set(range(min(vus), max(vus) + 1)) - vus) if vus else []
    return sorted(doublons), trous


def test_piece_equilibree():
    assert piece_equilibree([{"debit": 119250, "credit": 0}, {"debit": 0, "credit": 100000}, {"debit": 0, "credit": 19250}])


def test_numerotation_detecte_doublon_et_trou():
    assert numerotation_continue([1, 2, 2, 4]) == ([2], [3])
