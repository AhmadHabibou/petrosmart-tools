# Base de simulation du prétraitement : Aspen HYSYS et AutoCAD Plant 3D

Fichier généré par `05_technique/base_simulation.py` à partir du bilan simplifié du lot 5 (`05_technique/bilan_procede.md`).

## Objet

Remplacer le bilan matière et énergie simplifié du lot 5 (hypothèses H-100 à H-113, statut supposé) par une simulation rigoureuse du prétraitement : décantation, chauffage, déshydratation sous vide, condensation, filtration. La simulation sert à trois choses : vérifier le rendement en produit et la consommation d'énergie, dimensionner les équipements de l'étape 4, et fournir les débits et compositions des rejets (eau huileuse, fractions légères, boues) à l'évaluation environnementale du centre de transit.

Priorité : l'étape 4 reste soumise à la décision D-06. La simulation n'a de valeur qu'avec une huile caractérisée au laboratoire : elle se fait après l'échantillonnage du protocole de terrain (lot 4 bis).

## Partage du travail

| Tâche | Qui |
|---|---|
| caractérisation de l'huile au laboratoire (analyses ci-dessous) | laboratoire, sur les échantillons du lot 4 bis |
| construction du cas HYSYS, choix des pseudo-composants, calcul des cas | promoteur (licence Aspen HYSYS sur son poste) |
| préparation des cas, contrôle des résultats, mise à jour des hypothèses H-100 à H-113 et des documents | Claude, dans le dépôt |
| liste des équipements et des lignes, schéma de procédé, implantation en AutoCAD Plant 3D | promoteur, à partir des résultats HYSYS |
| intégration des dimensions et des rejets dans le dossier technique et l'évaluation environnementale | Claude, dans le dépôt |

Échange : le promoteur exporte les tableaux de courants au format de `retour_simulation_modele.csv` et les dépose dans `05_technique/simulation/retour_simulation.csv`, par envoi du fichier ou par un dossier partagé de son poste. La fonction `comparer()` confronte alors chaque cas au bilan simplifié.

## Données d'entrée à obtenir du laboratoire

| Grandeur | Méthode | Usage dans HYSYS |
|---|---|---|
| courbe de distillation | ASTM D1160 ou distillation simulée ASTM D7169 | découpage de l'huile en pseudo-composants |
| masse volumique à 15 °C | ASTM D4052 | calage des pseudo-composants |
| viscosité à 40 et 100 °C | ASTM D445 | calage des propriétés de transport |
| teneur en eau | ASTM D6304 (Karl Fischer) ou D95 | composition de l'alimentation |
| eau et sédiments | ASTM D1796 (centrifugation) ou méthode équivalente du laboratoire | composition de l'alimentation |
| point éclair | ASTM D93 | contrôle de la dilution par le carburant et du produit |
| chlore total | ASTM D5384 au dépistage, confirmation au laboratoire | lots exclus de la simulation |

Tant que ces données manquent, les cas ci-dessous utilisent les fractions supposées du lot 5. Les méthodes citées sont les méthodes usuelles des laboratoires pétroliers ; le laboratoire retenu confirmera celles qu'il pratique.

## Modèle de simulation

### Composants et thermodynamique

- eau (composant pur de la bibliothèque) ;
- fractions légères : pseudo-composants d'une coupe de type gasoil (dilution de l'huile moteur par le carburant) ;
- huile de base : pseudo-composants issus de la courbe de distillation du laboratoire ;
- sédiments : composant solide hypothétique, ou séparation imposée dans un séparateur de composants ;
- modèle thermodynamique proposé : Peng-Robinson, à confirmer par le promoteur selon les recommandations d'AspenTech pour les mélanges eau et hydrocarbures.

### Schéma de procédé

| Ordre | Opération HYSYS | Fonction | Spécification de départ |
|---|---|---|---|
| 1 | séparateur de composants | décanteur : eau libre et sédiments | 75 % de l'eau (H-103), 90 % des sédiments (H-104), 1,0 kg d'huile entraînée par kg de sédiment (H-111) |
| 2 | réchauffeur | chauffage de l'huile | sortie à 70 °C (H-106), entrée à 27 °C (H-109) |
| 3 | séparateur sous vide | déshydratation | pression absolue : variable d'étude, la valeur du fournisseur retenu servant de référence |
| 4 | refroidisseur et séparateur triphasique | condensation des vapeurs | séparation de l'eau et des fractions légères ; incondensables vers la pompe à vide |
| 5 | séparateur de composants | filtration fine | particules résiduelles |

Critère de produit : eau résiduelle d'au plus 0,2 % (H-105).

## Cas de calcul

| Cas | Qualité | Eau | Sédiments | Fractions légères | Volume (L/an) | Débit (L/h, un poste) |
|---|---|---:|---:|---:|---:|---:|
| bas-320k | peu contaminée | 2,0 % | 0,5 % | 1,0 % | 320 000 | 173,9 |
| bas-1050k | peu contaminée | 2,0 % | 0,5 % | 1,0 % | 1 050 000 | 570,7 |
| bas-1200k | peu contaminée | 2,0 % | 0,5 % | 1,0 % | 1 200 000 | 652,2 |
| central-320k | moyennement contaminée | 8,0 % | 2,0 % | 3,0 % | 320 000 | 173,9 |
| central-1050k | moyennement contaminée | 8,0 % | 2,0 % | 3,0 % | 1 050 000 | 570,7 |
| central-1200k | moyennement contaminée | 8,0 % | 2,0 % | 3,0 % | 1 200 000 | 652,2 |
| haut-320k | très contaminée | 20,0 % | 5,0 % | 6,0 % | 320 000 | 173,9 |
| haut-1050k | très contaminée | 20,0 % | 5,0 % | 6,0 % | 1 050 000 | 570,7 |
| haut-1200k | très contaminée | 20,0 % | 5,0 % | 6,0 % | 1 200 000 | 652,2 |

Débits sur un poste de 8 heures et 230 jours par an (H-110). Fichier des cas : `cas_de_calcul.csv`. Balayages utiles en plus : température de 60 à 80 °C (H-106) et pression du séparateur sous vide.

## Résultats attendus

Pour chaque cas et chaque courant : débit massique, température, pression, fractions d'eau, de légers, d'huile et de solides, puissance des équipements. Format : `retour_simulation_modele.csv` (une ligne par cas et par courant).

| Courant | Bilan simplifié, qualité moyenne (kg pour 1 000 kg) |
|---|---:|
| eau décantée | 60,0 |
| boues | 36,0 |
| eau évaporée sous vide | 18,3 |
| fractions légères condensées | 30,0 |
| produit | 855,7 |

## Critères d'acceptation

1. bouclage massique de chaque cas à moins de 0,1 % ;
2. eau résiduelle du produit d'au plus 0,2 % ;
3. écart de rendement avec le bilan simplifié expliqué cas par cas ; au-delà de 5 points, les hypothèses H-100 à H-113 sont révisées ;
4. puissance de chauffe comparée à l'énergie du bilan simplifié (kWh par tonne).

## Passage à AutoCAD Plant 3D

- liste des équipements : repère, service, dimensions et puissance tirées de HYSYS ;
- liste des lignes : diamètre, matériau, fluide, température et pression de calcul ;
- schéma de procédé et d'instrumentation : sécurités de surchauffe, de niveau et de manque de vide (cahier des charges E2) ;
- implantation du centre de transit : cuves sur rétention, aire de dépotage, distances de sécurité ; les règles de dimensionnement des rétentions sont à confirmer dans la réglementation camerounaise des établissements classés [S-35] ;
- exports : liste des équipements et des lignes en tableau, vues en PDF, pour le dossier technique et l'évaluation environnementale.

