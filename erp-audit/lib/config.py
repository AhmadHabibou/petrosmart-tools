"""Chargement de la configuration avec garde-fous : pas de production, identifiants hors depot."""
import os
from pathlib import Path
import yaml

RACINE = Path(__file__).resolve().parent.parent


def charger():
    chemin = RACINE / "config.yaml"
    if not chemin.exists():
        raise SystemExit("config.yaml absent : copier config.example.yaml et renseigner l'adresse de recette.")
    cfg = yaml.safe_load(chemin.read_text(encoding="utf-8"))
    if cfg["erp"].get("production", True):
        raise SystemExit("Refus : l'instance declaree est une production. Audit sur recette uniquement.")
    return cfg


def identifiants(login=None):
    user = login or os.environ.get("ERP_USER")
    pwd = os.environ.get("ERP_PASSWORD")
    if not user or not pwd:
        raise SystemExit("ERP_USER et ERP_PASSWORD doivent etre definis dans l'environnement.")
    return user, pwd
