"""Lot 11 : matrice multicritere des formes sociales. Sortie : 11_juridique/matrice_forme_sociale.md"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from commun.format import nombre, pct  # noqa: E402

POIDS = {"Coût et délai de création": 0.20, "Responsabilité limitée aux apports": 0.25,
         "Entrée d'associés et d'investisseurs": 0.20, "Crédibilité auprès des banques et des grands comptes": 0.20,
         "Simplicité de fonctionnement": 0.15}
NOTES = {"Établissement individuel": [5, 1, 1, 2, 5], "SARL": [4, 5, 3, 4, 4], "SAS": [3, 5, 5, 4, 3], "SA": [1, 5, 4, 5, 1]}


def scores():
    return {f: sum(p * n for p, n in zip(POIDS.values(), v)) for f, v in NOTES.items()}


def rapport():
    sc = scores()
    out = ["# Matrice multicritère des formes sociales", "",
           "Fichier généré par `11_juridique/forme_sociale.py`. Notes de 1 (défavorable) à 5 (favorable), jugements d'expert.", "",
           "| Critère | Poids | " + " | ".join(NOTES) + " |", "|---|---:|" + "---:|" * len(NOTES)]
    for i, (c, p) in enumerate(POIDS.items()):
        out.append(f"| {c} | {pct(p)} | " + " | ".join(str(v[i]) for v in NOTES.values()) + " |")
    out.append("| **Score pondéré** | | " + " | ".join(f"**{nombre(sc[f], 2)}**" for f in NOTES) + " |")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    Path(__file__).with_name("matrice_forme_sociale.md").write_text(rapport(), encoding="utf-8")
    print("Lot 11 :", {k: round(v, 2) for k, v in scores().items()})
