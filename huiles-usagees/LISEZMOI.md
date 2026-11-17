# Projet de collecte et de valorisation des huiles usagées et du gasoil au Cameroun

**État au 17/11/2026 : livraison intermédiaire (phase A).** Lots livrés : 0, 1 et 4 bis, avec les registres et le socle de calcul. Les lots 2 à 17 restent à produire. Ce fichier sera réécrit en version finale avec la synthèse du lot 17.

## Conclusion provisoire en cinq lignes

1. Le projet n'est ni validé ni invalidé : les preuves décisives (volumes réels, qualité des huiles, acheteur, statut légal de la valorisation) sont de terrain.
2. Le promoteur peut encaisser dès le premier mois avec trois activités sous 500 000 FCFA de dépenses : formation en atelier, analyse d'huile en service, apport d'affaires à un collecteur agréé.
3. Tant que la société n'a pas de permis, elle ne transporte aucun déchet dangereux : le pilote sous-traite l'enlèvement à un collecteur agréé.
4. Une unité de traitement d'au moins 7 000 t/an a été commandée par Valtech Energy pour Kribi ; son statut doit être éclairci avant tout choix de modèle.
5. L'arrêté n°001/MINEPDED cite la valorisation dans la définition du permis, mais son chapitre sur les déchets dangereux ne la vise pas : la réponse écrite du MINEPDED conditionne le modèle « unité de traitement ».

## Modèle recommandé

Non tranché avant le lot 8. Orientation provisoire : démarrage par le service (conformité, purification du gasoil) et la sous-traitance de la collecte, sans unité de traitement propre.

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
4. `00_registres/` : décisions, questions ouvertes, hypothèses, sources

## Lundi prochain

1. Envoyer trois lettres : HIKMA (Q-10), MINEFOP (Q-07), MINEPDED (Q-01, Q-03, Q-17).
2. Demander les devis : SGS Cameroun et deux laboratoires (Q-05), Bocom International et SECA (Q-18), distributeur Parker (Q-16).
3. Déposer le dossier de création de la société au CFCE (Q-08).
4. Faire 10 appels de prospection avec le script du lot 0, en commençant par les flottes urbaines et les concessionnaires.
5. Transmettre au chef de projet les PDF officiels des textes réglementaires (Q-02) pour le lot 2.

## Reproduire les calculs

```
cd huiles-usagees
python3 run_all.py      # régénère les fichiers chiffrés et contrôle les tirets
python3 -m pytest -q tests
```

ou `make` puis `make test`. Dépendances : Python 3.11 ou plus, bibliothèque standard seulement à ce stade.

## Limites de cette livraison

1. Le réseau de travail bloque le téléchargement des PDF officiels : les textes réglementaires et l'article de référence [S-01] sont connus par extraits.
2. Toutes les valeurs économiques du lot 0 et des budgets du lot 4 bis sont des hypothèses sans devis.
3. Les acheteurs de combustible, les laboratoires et les loueurs d'équipement au Cameroun restent à identifier et à confirmer.
