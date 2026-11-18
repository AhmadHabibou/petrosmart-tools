"""Lot 2 : calendrier des autorisations (chemin critique), en trois cas.

Sortie : 02_reglementaire/calendrier.md
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from commun.hypotheses import val  # noqa: E402
from commun.format import nombre  # noqa: E402

# (code, libelle, hypothese de duree, predecesseurs)
ETAPES = [
    ("A", "Création de la société (CFCE)", "H-70", []),
    ("B", "Évaluation environnementale (NIE ou EIES) par un bureau agréé autre que HIKMA", "H-71", ["A"]),
    ("C", "Permis environnemental déchets dangereux (MINEPDED)", "H-72", ["B"]),
    ("D", "Autorisation ou déclaration d'établissement classé (MINMIDT)", "H-73", ["B"]),
    ("E", "Autorisation de transport de marchandises dangereuses (MINT), si flotte propre", "H-74", ["A"]),
]


def planifier(cas):
    fin = {}
    debut = {}
    for code, _, h, pred in ETAPES:
        debut[code] = max((fin[p] for p in pred), default=0)
        fin[code] = debut[code] + val(h, cas)
    return debut, fin


def rapport():
    out = ["# Calendrier des autorisations", "",
           "Fichier généré par `02_reglementaire/calendrier.py`. Durées en jours calendaires, à partir du jour 0. Statut : supposé (H-70 à H-74).", "",
           "| Étape | Libellé | Prédécesseurs | Début (central) | Fin bas | Fin central | Fin haut |",
           "|---|---|---|---:|---:|---:|---:|"]
    plans = {c: planifier(c) for c in ("bas", "central", "haut")}
    for code, lib, _, pred in ETAPES:
        out.append(f"| {code} | {lib} | {', '.join(pred) or 'aucun'} | {nombre(plans['central'][0][code])} | "
                   f"{nombre(plans['bas'][1][code])} | {nombre(plans['central'][1][code])} | {nombre(plans['haut'][1][code])} |")
    tot = {c: max(plans[c][1].values()) for c in plans}
    out += ["", f"Délai total avant exploitation d'une unité de traitement : {nombre(tot['bas'])} jours (bas), "
            f"{nombre(tot['central'])} jours (central), {nombre(tot['haut'])} jours (haut), soit "
            f"{nombre(tot['bas'] / 30.4, 1)} à {nombre(tot['haut'] / 30.4, 1)} mois.", ""]
    return "\n".join(out) + "\n", tot


if __name__ == "__main__":
    texte, tot = rapport()
    Path(__file__).with_name("calendrier.md").write_text(texte, encoding="utf-8")
    print("Lot 2 : delai total central (jours)", tot["central"])
