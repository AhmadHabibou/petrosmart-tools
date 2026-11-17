# Matrice multicritère des activités d'amorçage

Fichier généré par `00b_amorcage/matrice_amorcage.py` : ne pas éditer à la main.

Méthode : matrice multicritère (filtre éliminatoire puis notation pondérée).

## Filtre éliminatoire

| Piste | dépenses avant encaissement <= 500 000 FCFA | premier encaissement < 3 mois | pas d'autorisation lourde | pas de conflit d'intérêts | pas de stock payé d'avance | Résultat |
|---|---|---|---|---|---|---|
| A1 Apporteur d'affaires d'un collecteur agréé | oui | oui | oui | oui | oui | retenue |
| A2 Analyse d'huile en service (kits prépayés, laboratoire partenaire) | oui | oui | oui | oui | oui | retenue |
| A3 Kits antipollution, absorbants, bacs, fûts sur commande | oui | oui | oui | oui | oui | retenue |
| A4 Huile de chaîne biodégradable (agent ou dépôt-vente) | à vérifier | oui | oui | oui | à vérifier | écartée : statut d'agent ou de dépôt-vente non confirmé par STIHL Cameroun [S-16] (Q-09) |
| A5 Formation des mécaniciens et chefs d'atelier, chez le client | oui | oui | oui | oui | oui | retenue |
| A6 Abonnement à l'application de traçabilité seule | oui | NON | oui | oui | oui | écartée : application non livrée (lot 16) : premier encaissement au-delà de 3 mois |
| A7 Audit de la gestion du carburant | oui | oui | oui | NON | oui | écartée : prestation d'audit concurrente de HIKMA auprès des mêmes clients ; demande non vérifiée |
| A8 Contenu de formation en ligne | oui | oui | oui | oui | oui | retenue |
| A9 Prix, concours, incubateurs, subventions | oui | NON | oui | oui | oui | écartée : aucun appel ouvert et sourcé au 17/11/2026 [S-21][S-22] ; veille mensuelle maintenue |
| A10 Courtage de lots d'huiles via la Bourse nationale des déchets | oui | à vérifier | à vérifier | oui | oui | écartée : plateforme non opérationnelle confirmée [S-10][S-11] ; statut du courtier au regard du permis inconnu (Q-03) |
| A11 Prestation de purification du gasoil avec unité louée | NON | oui | oui | oui | oui | écartée : location d'unité estimée au-dessus du plafond (H-47) : traitée dans le pilote 4 bis n°1 |

Dépenses communes avant premier encaissement (H-30, H-31, H-32) : 200 000 FCFA à 500 000 FCFA, valeur centrale 325 000 FCFA, pour un plafond de 500 000 FCFA. Statut : supposé.

## Notation pondérée

Poids : revenu net 12 mois 35 %, temps du promoteur 20 % (5 = peu de temps), apport au projet principal 45 %. La note de revenu va de 1 à 5, proportionnelle au revenu central.

| Rang | Piste | Revenu net 12 mois bas | central | haut | Note revenu | Note temps | Note apport | Score |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | A5 Formation des mécaniciens et chefs d'atelier, chez le client | 1,60 | 4,80 | 12,00 | 5,00 | 2 | 5 | 4,40 |
| 2 | A2 Analyse d'huile en service (kits prépayés, laboratoire partenaire) | 0,60 | 1,80 | 6,00 | 2,50 | 3 | 5 | 3,73 |
| 3 | A1 Apporteur d'affaires d'un collecteur agréé | 0,20 | 1,00 | 3,00 | 1,83 | 4 | 5 | 3,69 |
| 4 | A3 Kits antipollution, absorbants, bacs, fûts sur commande | 0,25 | 0,90 | 3,00 | 1,75 | 3 | 4 | 3,01 |
| 5 | A8 Contenu de formation en ligne | 0,15 | 0,50 | 1,50 | 1,42 | 4 | 2 | 2,20 |

Revenus en M FCFA. Statut : supposé (hypothèses H-20 à H-29).

## Test de robustesse : poids égaux

| Rang | Piste | Score |
|---|---|---:|
| 1 | A5 Formation des mécaniciens et chefs d'atelier, chez le client | 4,00 |
| 2 | A1 Apporteur d'affaires d'un collecteur agréé | 3,61 |
| 3 | A2 Analyse d'huile en service (kits prépayés, laboratoire partenaire) | 3,50 |
| 4 | A3 Kits antipollution, absorbants, bacs, fûts sur commande | 2,92 |
| 5 | A8 Contenu de formation en ligne | 2,47 |

Revenu net cumulé des trois premières pistes sur 12 mois : 2,40 M FCFA (cas bas) à 21,00 M FCFA (cas haut), 7,60 M FCFA en cas central.

Les trois premières pistes sont identiques avec les deux jeux de poids : oui.

## Justification des notes de temps et d'apport

- A1 : temps 4 (quelques rendez-vous par mois, le collecteur exécute) ; apport 5 (apprentissage du métier, données de gisement, relation avec un futur sous-traitant ou partenaire du pilote) ;
- A2 : temps 3 (prélèvement ou formation du client au prélèvement, interprétation des bulletins) ; apport 5 (accès aux intervalles de vidange et aux volumes de chaque engin : donnée directe du gisement forestier) ;
- A3 : temps 3 (cotations, suivi de livraison) ; apport 4 (équipe les sites qui seront ensuite collectés ; prépare l'offre de conformité) ;
- A5 : temps 2 (préparation des modules, 1 jour de session plus le trajet) ; apport 5 (crédibilité HSE, accès aux ateliers, mesure du besoin réel, premiers contrats) ;
- A8 : temps 4 (production unique, puis vente passive) ; apport 2 (notoriété ; peu de contact direct avec les producteurs d'huiles).
