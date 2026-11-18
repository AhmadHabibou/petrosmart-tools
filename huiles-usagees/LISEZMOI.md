# Projet de collecte et de valorisation des huiles usagées et du gasoil au Cameroun

**État au 18/11/2026 : livraison intermédiaire (phases A, B et C).** Lots livrés : 0, 1, 2, 3, 4, 4 bis, 4 ter et 8, avec les registres et le socle de calcul. Décisions de viabilité (D-06) et de modèle (D-09) prises. Les lots 5, 6, 7 et 9 à 17 restent à produire. Ce fichier sera réécrit en version finale avec la synthèse du lot 17.

## Conclusion provisoire en cinq lignes

1. Go conditionnel (D-06) : le projet est viable comme service de conformité et de collecte payé par les producteurs, pas encore comme fabricant de combustible.
2. Le promoteur peut encaisser dès le premier mois avec trois activités sous 500 000 FCFA de dépenses : formation en atelier, analyse d'huile en service, apport d'affaires à un collecteur agréé.
3. Tant que la société n'a pas de permis, elle ne transporte aucun déchet dangereux : le pilote sous-traite l'enlèvement à un collecteur agréé.
4. Le gisement national de 70 000 t/an est probablement surestimé (environ 11 M L/an par le parc en cas central) et aucun acheteur de combustible n'est confirmé.
5. Le permis déchets peut couvrir la valorisation, mais le statut légal du combustible vendu n'est pas tranché : l'unité de traitement est gelée jusqu'à une réponse écrite du MINEPDED.

## Modèle recommandé

Trajectoire par étapes (D-09) : démarrage en modèle à faible capital (purificateur loué, enlèvements sous-traités, contrat de conformité), passage en prestataire équipé quand au moins 4 contrats annuels sont signés, permis propre en année 3, traitement seulement aux conditions de D-06. Point mort : environ 8 à 9 clients forestiers sous contrat (`08_modele_entreprise/comparaison_modeles.md`).

## Budget de démarrage

- Amorçage (lot 0) : au plus 500 000 FCFA avant le premier encaissement (`00b_amorcage/matrice_amorcage.md`).
- Preuves de terrain (lot 4 bis) : voir `04b_validation_terrain/budget_protocoles.md`, en partie refacturé aux clients pilotes.

## Cinq questions ouvertes à régler sur le terrain

1. Q-01 : la valorisation en combustible est-elle couverte par le permis « déchets dangereux » ?
2. Q-10 : HIKMA accepte-t-elle par écrit la prospection de ses clients, et à quelles conditions ?
3. Q-11 : l'unité de Valtech Energy à Kribi fonctionne-t-elle, et à quel prix achète-t-elle les huiles ?
4. Q-05 : quel laboratoire accrédité, à quel prix et en quel délai ?
5. Q-18 : un collecteur agréé accepte-t-il de monter en forêt, et à quel prix ?

La liste complète est dans `00_registres/questions_ouvertes.md`.

## Ordre de lecture

1. `01_cadrage/lot1_cadrage.md`
2. `00b_amorcage/lot0_amorcage.md`, puis `matrice_amorcage.md`
3. `04b_validation_terrain/lot4bis_protocoles.md`, `procedure_acceptation_lots.md`, `budget_protocoles.md`
4. `02_reglementaire/lot2_reglementaire.md`, puis `calendrier.md`
5. `03_benchmark/lot3_benchmark.md`
6. `04_marche/lot4_marche.md`, `gisement.md`, `questionnaire_garages.md`
7. `04c_extensions/lot4ter_extensions.md`, puis `matrice_extensions.md`
8. `08_modele_entreprise/lot8_modele_entreprise.md`, puis `comparaison_modeles.md`
9. `00_registres/` : décisions (D-06, D-09), questions ouvertes, hypothèses, sources

## Lundi prochain

1. Envoyer trois lettres : HIKMA (Q-10), MINEFOP (Q-07), MINEPDED (Q-01, Q-03, Q-17, Q-21, Q-23).
2. Demander les devis : SGS Cameroun et deux laboratoires (Q-05), Bocom International et SECA (Q-18), distributeur Parker (Q-16).
3. Déposer le dossier de création de la société au CFCE (Q-08).
4. Faire 10 appels de prospection avec le script du lot 0, en commençant par les flottes urbaines et les concessionnaires.
5. Transmettre au chef de projet les PDF officiels des textes réglementaires (Q-02) pour confirmer le lot 2 ; lancer l'enquête de 30 garages (`04_marche/questionnaire_garages.md`).

## Reproduire les calculs

```
cd huiles-usagees
python3 run_all.py      # régénère les fichiers chiffrés et contrôle les tirets
python3 -m pytest -q tests
```

ou `make` puis `make test`. Dépendances : Python 3.11 ou plus et `pip install -r requirements.txt` (OR-Tools, NumPy, openpyxl, pytest).

## Limites de cette livraison

1. Le réseau de travail bloque le téléchargement des PDF officiels : les textes réglementaires et l'article de référence [S-01] sont connus par extraits.
2. Toutes les valeurs économiques du lot 0 et des budgets du lot 4 bis sont des hypothèses sans devis.
3. Les acheteurs de combustible, les laboratoires et les loueurs d'équipement au Cameroun restent à identifier et à confirmer.
