"""Registre des anomalies : une ligne JSON par constat, reproductible et prouvee."""
import json
from datetime import datetime
from pathlib import Path

REGISTRE = Path(__file__).resolve().parent.parent / "rapport" / "registre-anomalies.jsonl"
GRAVITES = ("bloquante", "majeure", "mineure", "cosmetique")


def consigner(module, titre, gravite, scenario, attendu, obtenu, preuves=(), probabilite="moyenne"):
    if gravite not in GRAVITES:
        raise ValueError(f"gravite inconnue : {gravite}")
    REGISTRE.parent.mkdir(parents=True, exist_ok=True)
    n = sum(1 for _ in REGISTRE.open(encoding="utf-8")) + 1 if REGISTRE.exists() else 1
    ligne = {
        "id": f"ANO-{module:02d}-{n:03d}", "module": module, "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "titre": titre, "gravite": gravite, "probabilite": probabilite, "scenario": scenario,
        "attendu": attendu, "obtenu": obtenu, "preuves": list(preuves), "statut": "ouverte",
    }
    with REGISTRE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return ligne["id"]
