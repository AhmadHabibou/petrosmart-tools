"""Base de simulation pour Aspen HYSYS et AutoCAD Plant 3D (pretraitement de l'etape 4).

Genere depuis le bilan simplifie du lot 5 (procede.py) et les hypotheses H-100 a H-113 :
- 05_technique/simulation/base_simulation_hysys.md : objet, partage du travail, donnees d'entree, schema, cas de calcul,
  resultats attendus, criteres d'acceptation, passage a Plant 3D ;
- 05_technique/simulation/cas_de_calcul.csv : les cas a simuler ;
- 05_technique/simulation/retour_simulation_modele.csv : le format des resultats a renvoyer.
Les resultats HYSYS deposes dans 05_technique/simulation/retour_simulation.csv sont compares au bilan simplifie par comparer().

Usage : python 05_technique/base_simulation.py
"""
from pathlib import Path
import csv
import sys

RACINE = Path(__file__).resolve().parents[1]
ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))
sys.path.insert(0, str(ICI))
from commun.format import nombre, pct  # noqa: E402
from commun.hypotheses import val  # noqa: E402
import procede  # noqa: E402

SIM = ICI / "simulation"
VOLUMES = (320_000, 1_050_000, 1_200_000)  # L/an : seuil de D-06, collecte haute, premier business plan (lot 5)
COURANTS = ("alimentation", "eau_decantee", "boues", "vapeur_condensee_eau", "vapeur_condensee_legers", "produit")
COLONNES = ["cas", "courant", "debit_kg_h", "temperature_c", "pression_mbar_abs", "fraction_eau", "fraction_legers", "fraction_huile",
            "fraction_solides", "puissance_kw"]


def cas_de_calcul():
    out = []
    for qualite, cq in procede.QUALITES.items():
        for v in VOLUMES:
            out.append(dict(cas=f"{cq}-{v // 1000}k", qualite=qualite, eau=val("H-100", cq), sediments=val("H-101", cq), legers=val("H-102", cq),
                            volume_l_an=v, debit_l_h=round(procede.debit_requis_l_h(v), 1), temperature_c=val("H-106")))
    return out


def comparer(chemin=SIM / "retour_simulation.csv"):
    """Compare le rendement en produit de chaque cas HYSYS au bilan simplifie. Renvoie [(cas, rendement HYSYS, rendement lot 5)]."""
    if not chemin.exists():
        return []
    lignes = list(csv.DictReader(chemin.open(encoding="utf-8")))
    ref = {c["cas"]: procede.bilan(c["cas"].split("-")[0])["rendement"] for c in cas_de_calcul()}
    out = []
    for cas in sorted({l["cas"] for l in lignes}):
        d = {l["courant"]: float(l["debit_kg_h"]) for l in lignes if l["cas"] == cas}
        if d.get("alimentation"):
            out.append((cas, d.get("produit", 0.0) / d["alimentation"], ref.get(cas)))
    return out


def document():
    cas = cas_de_calcul()
    b = {q: procede.bilan(c) for q, c in procede.QUALITES.items()}
    L = ["# Base de simulation du prétraitement : Aspen HYSYS et AutoCAD Plant 3D", "",
         "Fichier généré par `05_technique/base_simulation.py` à partir du bilan simplifié du lot 5 (`05_technique/bilan_procede.md`).", "",
         "## Objet", "",
         "Remplacer le bilan matière et énergie simplifié du lot 5 (hypothèses H-100 à H-113, statut supposé) par une simulation rigoureuse du prétraitement : "
         "décantation, chauffage, déshydratation sous vide, condensation, filtration. La simulation sert à trois choses : vérifier le rendement en produit et la consommation "
         "d'énergie, dimensionner les équipements de l'étape 4, et fournir les débits et compositions des rejets (eau huileuse, fractions légères, boues) à l'évaluation "
         "environnementale du centre de transit.", "",
         "Priorité : l'étape 4 reste soumise à la décision D-06. La simulation n'a de valeur qu'avec une huile caractérisée au laboratoire : elle se fait après l'échantillonnage "
         "du protocole de terrain (lot 4 bis).", "",
         "## Partage du travail", "",
         "| Tâche | Qui |", "|---|---|",
         "| caractérisation de l'huile au laboratoire (analyses ci-dessous) | laboratoire, sur les échantillons du lot 4 bis |",
         "| construction du cas HYSYS, choix des pseudo-composants, calcul des cas | promoteur (licence Aspen HYSYS sur son poste) |",
         "| préparation des cas, contrôle des résultats, mise à jour des hypothèses H-100 à H-113 et des documents | Claude, dans le dépôt |",
         "| liste des équipements et des lignes, schéma de procédé, implantation en AutoCAD Plant 3D | promoteur, à partir des résultats HYSYS |",
         "| intégration des dimensions et des rejets dans le dossier technique et l'évaluation environnementale | Claude, dans le dépôt |", "",
         "Échange : le promoteur exporte les tableaux de courants au format de `retour_simulation_modele.csv` et les dépose dans `05_technique/simulation/retour_simulation.csv`, "
         "par envoi du fichier ou par un dossier partagé de son poste. La fonction `comparer()` confronte alors chaque cas au bilan simplifié.", "",
         "## Données d'entrée à obtenir du laboratoire", "",
         "| Grandeur | Méthode | Usage dans HYSYS |", "|---|---|---|",
         "| courbe de distillation | ASTM D1160 ou distillation simulée ASTM D7169 | découpage de l'huile en pseudo-composants |",
         "| masse volumique à 15 °C | ASTM D4052 | calage des pseudo-composants |",
         "| viscosité à 40 et 100 °C | ASTM D445 | calage des propriétés de transport |",
         "| teneur en eau | ASTM D6304 (Karl Fischer) ou D95 | composition de l'alimentation |",
         "| eau et sédiments | ASTM D1796 (centrifugation) ou méthode équivalente du laboratoire | composition de l'alimentation |",
         "| point éclair | ASTM D93 | contrôle de la dilution par le carburant et du produit |",
         "| chlore total | ASTM D5384 au dépistage, confirmation au laboratoire | lots exclus de la simulation |", "",
         "Tant que ces données manquent, les cas ci-dessous utilisent les fractions supposées du lot 5. Les méthodes citées sont les méthodes usuelles des laboratoires pétroliers ; "
         "le laboratoire retenu confirmera celles qu'il pratique.", "",
         "## Modèle de simulation", "",
         "### Composants et thermodynamique", "",
         "- eau (composant pur de la bibliothèque) ;",
         "- fractions légères : pseudo-composants d'une coupe de type gasoil (dilution de l'huile moteur par le carburant) ;",
         "- huile de base : pseudo-composants issus de la courbe de distillation du laboratoire ;",
         "- sédiments : composant solide hypothétique, ou séparation imposée dans un séparateur de composants ;",
         "- modèle thermodynamique proposé : Peng-Robinson, à confirmer par le promoteur selon les recommandations d'AspenTech pour les mélanges eau et hydrocarbures.", "",
         "### Schéma de procédé", "",
         "| Ordre | Opération HYSYS | Fonction | Spécification de départ |", "|---|---|---|---|",
         f"| 1 | séparateur de composants | décanteur : eau libre et sédiments | {pct(val('H-103'))} de l'eau (H-103), {pct(val('H-104'))} des sédiments (H-104), {nombre(val('H-111'), 1)} kg d'huile entraînée par kg de sédiment (H-111) |",
         f"| 2 | réchauffeur | chauffage de l'huile | sortie à {nombre(val('H-106'))} °C (H-106), entrée à {nombre(val('H-109'))} °C (H-109) |",
         "| 3 | séparateur sous vide | déshydratation | pression absolue : variable d'étude, la valeur du fournisseur retenu servant de référence |",
         "| 4 | refroidisseur et séparateur triphasique | condensation des vapeurs | séparation de l'eau et des fractions légères ; incondensables vers la pompe à vide |",
         "| 5 | séparateur de composants | filtration fine | particules résiduelles |", "",
         f"Critère de produit : eau résiduelle d'au plus {pct(val('H-105'), 1)} (H-105).", "",
         "## Cas de calcul", "",
         "| Cas | Qualité | Eau | Sédiments | Fractions légères | Volume (L/an) | Débit (L/h, un poste) |", "|---|---|---:|---:|---:|---:|---:|"]
    for c in cas:
        L.append(f"| {c['cas']} | {c['qualite']} | {pct(c['eau'], 1)} | {pct(c['sediments'], 1)} | {pct(c['legers'], 1)} | {nombre(c['volume_l_an'])} | {nombre(c['debit_l_h'], 1)} |")
    L += ["", f"Débits sur un poste de {procede.HEURES_POSTE} heures et {nombre(val('H-110'))} jours par an (H-110). Fichier des cas : `cas_de_calcul.csv`. "
          "Balayages utiles en plus : température de 60 à 80 °C (H-106) et pression du séparateur sous vide.", "",
          "## Résultats attendus", "",
          "Pour chaque cas et chaque courant : débit massique, température, pression, fractions d'eau, de légers, d'huile et de solides, puissance des équipements. "
          "Format : `retour_simulation_modele.csv` (une ligne par cas et par courant).", "",
          "| Courant | Bilan simplifié, qualité moyenne (kg pour 1 000 kg) |", "|---|---:|",
          f"| eau décantée | {nombre(b['moyennement contaminée']['eau_decant'], 1)} |",
          f"| boues | {nombre(b['moyennement contaminée']['boues'], 1)} |",
          f"| eau évaporée sous vide | {nombre(b['moyennement contaminée']['eau_evap'], 1)} |",
          f"| fractions légères condensées | {nombre(b['moyennement contaminée']['legers'], 1)} |",
          f"| produit | {nombre(b['moyennement contaminée']['produit'], 1)} |", "",
          "## Critères d'acceptation", "",
          "1. bouclage massique de chaque cas à moins de 0,1 % ;",
          f"2. eau résiduelle du produit d'au plus {pct(val('H-105'), 1)} ;",
          "3. écart de rendement avec le bilan simplifié expliqué cas par cas ; au-delà de 5 points, les hypothèses H-100 à H-113 sont révisées ;",
          "4. puissance de chauffe comparée à l'énergie du bilan simplifié (kWh par tonne).", "",
          "## Passage à AutoCAD Plant 3D", "",
          "- liste des équipements : repère, service, dimensions et puissance tirées de HYSYS ;",
          "- liste des lignes : diamètre, matériau, fluide, température et pression de calcul ;",
          "- schéma de procédé et d'instrumentation : sécurités de surchauffe, de niveau et de manque de vide (cahier des charges E2) ;",
          "- implantation du centre de transit : cuves sur rétention, aire de dépotage, distances de sécurité ; les règles de dimensionnement des rétentions sont à confirmer "
          "dans la réglementation camerounaise des établissements classés [S-35] ;",
          "- exports : liste des équipements et des lignes en tableau, vues en PDF, pour le dossier technique et l'évaluation environnementale.", ""]
    return "\n".join(L) + "\n"


def construire():
    SIM.mkdir(exist_ok=True)
    (SIM / "base_simulation_hysys.md").write_text(document(), encoding="utf-8")
    cas = cas_de_calcul()
    with (SIM / "cas_de_calcul.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cas[0]))
        w.writeheader()
        w.writerows(cas)
    with (SIM / "retour_simulation_modele.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLONNES)
        for courant in COURANTS:
            w.writerow([cas[0]["cas"], courant] + [""] * (len(COLONNES) - 2))
    for cas_id, r_sim, r_ref in comparer():
        print(f"{cas_id} : rendement HYSYS {r_sim:.3f}, bilan simplifie {r_ref:.3f}")


if __name__ == "__main__":
    construire()
    print("Base de simulation HYSYS generee")
