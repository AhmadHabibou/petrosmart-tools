# Tournées et coût complet par litre

Fichier généré par `06_logistique/tournees.py` (OR-Tools, problème de tournées avec capacité). Statut : supposé (H-48, H-01, H-88, H-120 à H-138), distances partiellement sourcées.

## Réseau

- Coefficient de détour calé sur deux paires sourcées : 1,30 (Yaoundé-Bertoua et Douala-Bertoua [S-75][S-76]) ; valeur retenue H-120 : 1,30.
- Douala-Yaoundé est déduit de Douala-Bertoua moins Yaoundé-Bertoua, en supposant l'itinéraire par Yaoundé : 239 km.
- Dépôt et déchargement : Douala, où sont situés les collecteurs et éliminateurs identifiés [S-06][S-07]. Capacité de la citerne : 13 390 L [S-29].
- Clients : 15 sites forestiers (H-97 central), répartis de manière supposée : Bertoua 4, Batouri 4, Abong-Mbang 3, Yokadouma 4 ; 50 km de piste par site (H-121) ; 2 500 L par enlèvement.

## Tournées optimisées (un cycle d'enlèvement, scénario central)

| Tournée | Sites | km route | km piste | Litres | Jours saison sèche | Jours saison des pluies |
|---|---|---:|---:|---:|---:|---:|
| 1 | Yokadouma, Yokadouma, Yokadouma, Yokadouma, Bertoua | 1 643 | 500 | 12 500 | 7 | 9 |
| 2 | Abong-Mbang, Abong-Mbang, Abong-Mbang, Bertoua, Bertoua | 1 368 | 500 | 12 500 | 7 | 8 |
| 3 | Batouri, Batouri, Batouri, Batouri, Bertoua | 1 344 | 500 | 12 500 | 7 | 8 |

## Coût complet par litre collecté en forêt (FCFA/L)

| Option de flotte | Saison sèche | Saison des pluies |
|---|---:|---:|
| Achat neuf (coûts fixes imputés à 100 % à la forêt) | 215 | 220 |
| Achat d'occasion (coûts fixes imputés à 100 % à la forêt) | 210 | 215 |
| Location avec chauffeur (carburant en sus) | 237 | 275 |
| Sous-traitance à un collecteur agréé (H-48 par enlèvement) | 200 | 200 |

Base annuelle : 23 420 km, 84 jours d'équipage en saison sèche (100 en saison des pluies), 150 000 L collectés par an.
Les coûts fixes d'un camion possédé sont imputés en totalité à la forêt : ils baissent si le camion sert aussi à la collecte urbaine.

## Collecte urbaine (Douala ou Yaoundé)

Coût variable par litre (carburant, entretien, équipage, hors coûts fixes du véhicule) : 40 FCFA/L pour 2 400 L collectés par jour (H-135 à H-137). La valeur de travail H-85 du lot 8 était de 40 FCFA/L.

Option la moins chère en saison sèche : Sous-traitance à un collecteur agréé (H-48 par enlèvement).

