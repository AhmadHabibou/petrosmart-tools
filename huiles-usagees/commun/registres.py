"""Genere 00_registres/hypotheses.md a partir de commun/hypotheses.py."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from commun.hypotheses import HYPOTHESES  # noqa: E402
from commun.format import nombre  # noqa: E402


def _v(x):
    return nombre(x, 2) if abs(x) < 10 and x != int(x) else nombre(x)


def generer():
    out = ["# Registre des hypothèses", "",
           "Fichier généré par `commun/registres.py` depuis `commun/hypotheses.py`. Toute modification se fait dans le module Python, puis `python run_all.py`.", "",
           "| ID | Lot | Libellé | Bas | Central | Haut | Unité | Justification | Impact | Vérification | Statut |",
           "|---|---|---|---:|---:|---:|---|---|---|---|---|"]
    for h in HYPOTHESES.values():
        out.append(f"| {h.id} | {h.lot} | {h.libelle} | {_v(h.bas)} | {_v(h.central)} | {_v(h.haut)} | {h.unite} | "
                   f"{h.justification} | {h.impact} | {h.verification} | {h.statut} |")
    racine = Path(__file__).resolve().parents[1]
    (racine / "00_registres" / "hypotheses.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    return len(HYPOTHESES)


if __name__ == "__main__":
    print("Hypotheses :", generer())
