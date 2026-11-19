# Projet de collecte et de valorisation des huiles usagées et du gasoil au Cameroun

**Livraison du 18 novembre 2026. Lots 0 à 17 livrés.** Ce fichier est généré par `17_synthese/construire_synthese.py`.

## Conclusion en cinq lignes

1. Go conditionnel : créer la société et lancer un pilote payant de trois mois, sans achat d'équipement ni demande de permis à ce stade.
2. Le marché porteur est le service de conformité payé par les forestiers : collecter en forêt coûte 200 à 237 FCFA/L, que seul le producteur peut payer.
3. Le scénario de base donne une VAN à 5 ans de 9,0 M FCFA, un TRI de 27,5 % et un point mort d'environ 8 clients sous contrat.
4. Le risque est de démarrage : VAN à 5 ans négative dans 29,5 % des 10 000 tirages, trésorerie tendue en année 2.
5. L'unité de fabrication de combustible est gelée : statut légal du produit non tranché, aucun acheteur confirmé, gisement national probablement surestimé.

## Modèle recommandé

Trajectoire par étapes (décision D-09) : démarrage à faible capital (purificateur loué, enlèvements sous-traités à un collecteur titulaire, contrat annuel de conformité), passage en prestataire équipé à 4 contrats et 3 mois d'EBITDA positif, permis propre à 320 000 L/an, traitement seulement aux conditions de D-06.

## Budget de démarrage

- amorçage : au plus 500 000 FCFA avant le premier encaissement ;
- six premiers mois : 16,64 M FCFA de décaissements, besoin maximal de 9,84 M FCFA (`14_plan_action/budget_preoperationnel.md`) ;
- fonds propres et quasi-fonds propres d'environ 20 M FCFA ; équipements en crédit-bail (environ 15,0 M FCFA) ; besoin au 90e centile de 45,6 M FCFA.

## Cinq questions ouvertes à régler sur le terrain

1. Q-10 : HIKMA signe-t-elle la charte de prévention des conflits d'intérêts ?
2. Q-01 et Q-21 : le permis couvre-t-il la valorisation, et quand l'huile traitée cesse-t-elle d'être un déchet ? (réponse écrite du MINEPDED)
3. H-80 : quel prix annuel les forestiers acceptent-ils pour le contrat de conformité ? (pilote)
4. Q-18 : quel collecteur titulaire accepte de sous-traiter les enlèvements en forêt, et à quel prix ?
5. Q-11 : l'unité de Valtech Energy à Kribi fonctionne-t-elle, et achète-t-elle les huiles ?

Liste complète : `00_registres/questions_ouvertes.md`.

## Ordre de lecture

1. `17_synthese/livrables/` : note Go/No Go, business plan, document de projet institutionnel, business plan bancaire, présentations (banque, forestiers)
2. `00b_amorcage/lot0_amorcage.md` et `14_plan_action/lot14_plan_action.md` : ce qu'il faut faire tout de suite
3. `04b_validation_terrain/lot4bis_protocoles.md` : les preuves de terrain
4. `02_reglementaire/`, `03_benchmark/`, `04_marche/`, `04c_extensions/` : le diagnostic
5. `08_modele_entreprise/`, `05_technique/`, `06_logistique/`, `07_hse_eies/`, `09_finance/` : le modèle et ses chiffres
6. `10_organisation/`, `11_juridique/`, `12_parties_prenantes/`, `13_risques/` : l'exécution
7. `15_kit_operationnel/docx/` et `pdf/` : les documents prêts à l'emploi ; `16_application/` : l'application
8. `00_registres/` : sources, hypothèses, questions ouvertes, décisions

## Lundi

1. Envoyer les quatre lettres du kit (A2) : HIKMA, MINEPDED, MINMIDT, MINEFOP.
2. Demander les devis : laboratoires (SGS Cameroun et deux autres), Bocom International et SECA, distributeur Parker ou loueur, deux assureurs, deux crédit-bailleurs (lettre B4 du kit).
3. Déposer le dossier de la SARL au CFCE (statuts J1 relus par un avocat).
4. Faire dix appels de prospection avec le script K4, en commençant par les flottes urbaines et les concessionnaires.
5. Lancer l'enquête des 30 garages et ouvrir le tour de table des comptes courants.

## Reproduire

```
cd huiles-usagees
pip install -r requirements.txt -r 16_application/requirements.txt
python3 run_all.py        # régénère tous les chiffres, le kit et la synthèse ; contrôle les tirets
make test                 # tests du dépôt et de l'application
```

## Limites de la livraison

1. Le réseau de travail a bloqué les PDF officiels et OpenStreetMap : textes réglementaires lus par extraits, distances reconstruites.
2. Aucune donnée de terrain, aucun devis, aucun entretien : les hypothèses décisives restent « supposées » jusqu'au pilote.
3. Les documents juridiques sont des projets à faire relire par un avocat ou un notaire camerounais.
