# Lot 6 : logistique et optimisation des tournées

Méthodes : optimisation des tournées avec capacité par OR-Tools (`tournees.py`), comparaison des options de flotte par coût complet au litre, pyramide de Minto pour la conclusion.

**Rôles mobilisés :** logisticien transport de matières dangereuses, expert de la filière forêt-bois, expert HSE, contre-expert.

## 1. Conclusion

Collecter en forêt coûte de l'ordre de 200 à 240 FCFA par litre, quelle que soit l'option de flotte (`tournees.md`). C'est quatre fois la valeur la plus haute retenue pour une huile remise à un valorisateur (50 FCFA/L, H-83). La collecte forestière ne s'autofinance donc jamais par la valeur de l'huile : elle doit être payée par le producteur dans le contrat de conformité. Ce résultat confirme le modèle retenu (D-09). Certitude : probable.

Avec 15 clients, la sous-traitance à un collecteur agréé et l'achat d'un camion d'occasion ont des coûts voisins. L'achat ne devient intéressant que si le camion sert aussi à la collecte urbaine, qui absorbe ses coûts fixes. D'où la recommandation : sous-traiter jusqu'à l'étape 3 (permis propre), puis acheter un camion d'occasion partagé entre la forêt et la ville. Certitude : supposé.

## 2. Méthode et limites

**Distances.** Le réseau de travail bloque OpenStreetMap (OSRM, Overpass, Geofabrik). Le graphe routier est construit sur deux distances routières publiées (Yaoundé-Bertoua, 333 km ; Douala-Bertoua, 572 km [S-75]) et sur des distances à vol d'oiseau depuis Bertoua [S-76], corrigées par un coefficient de détour. Ce coefficient, calé sur les deux paires sourcées, vaut 1,30. La fonction `matrice_osrm()` est prévue pour remplacer le graphe par une matrice OSRM dès que le réseau le permet.

**Clients.** Les 15 clients forestiers de l'année 5 (H-97) sont répartis autour de Bertoua, Batouri, Abong-Mbang et Yokadouma. Cette répartition est supposée : la localisation réelle des clients sera saisie dans l'application du lot 16 et le modèle relancé. Les clients de la région du Sud (Sangmélima, Ebolowa) ne sont pas modélisés faute de distances sourcées vers l'Est.

**Pistes et saisons.** Chaque site est à 50 km de piste de sa ville de référence (H-121). La vitesse sur piste baisse de 40 % en saison des pluies (H-124). Les barrières de pluie, qui ferment des routes forestières à la circulation des camions, ne sont pas modélisées : elles peuvent rendre un site inaccessible pendant plusieurs semaines (Q-38).

**Solveur.** OR-Tools résout un problème de tournées avec capacité (citerne de 13 390 L [S-29]), au départ et au retour de Douala, où se trouvent les collecteurs et éliminateurs identifiés [S-06][S-07].

## 3. Résultats

Le solveur regroupe les 15 sites en trois tournées de 5 sites, d'une semaine environ chacune (7 jours en saison sèche, 8 à 9 en saison des pluies), pour 12 500 L par tournée. Sur une année de 4 cycles d'enlèvement, le camion parcourt environ 23 400 km. Les détails sont dans `tournees.md`.

Pour une citerne de 13 390 L, chaque tournée est remplie à environ 93 %. Une citerne plus grande n'apporterait rien sans clients supplémentaires dans la même zone.

## 4. Options de flotte

| Option | Avantage | Inconvénient | Recommandation |
|---|---|---|---|
| Sous-traitance à un collecteur agréé | pas de capital, pas de permis transport propre, coût variable | dépendance au collecteur, qui peut devenir concurrent | étapes 1 et 2 (D-05) |
| Location avec chauffeur | flexibilité | coût le plus élevé, surtout en saison des pluies ; offres non vérifiées | dépannage seulement |
| Achat d'occasion | coût voisin de la sous-traitance, coûts fixes partageables avec la ville | entretien plus lourd (H-138), immobilisations | étape 3, après obtention du permis |
| Achat neuf | fiabilité | capital élevé (H-130) sans gain de coût au litre | non recommandé avant l'année 5 |

**Véhicule léger.** Un pick-up 4x4 sert à la purification du gasoil, aux visites et aux prélèvements. Un Toyota Hilux d'occasion importé de 2020 est estimé à environ 30,6 M FCFA par un site d'aide à l'importation [S-82]. En étape 1, il est loué (modèle M5).

## 5. Collecte urbaine

Le coût variable de la collecte urbaine est d'environ 40 FCFA/L pour 2 400 L collectés par jour (H-135 à H-137), hors coûts fixes du véhicule. Il est cinq fois plus faible qu'en forêt, mais il s'ajoute au prix d'achat des huiles au garage, que le circuit informel fixe (Q-30). Pendant les étapes 1 et 2, la collecte urbaine passe par le partenariat M4 avec un collecteur titulaire.

## 6. Exigences de transport

- autorisation de transport de marchandises dangereuses du MINT et suivi GPS du véhicule [S-37][S-38], à l'étape 3 ;
- citerne compatible avec les huiles usagées, signalisation, extincteurs, kit antipollution et trousse de premiers secours à bord ;
- formation du chauffeur aux matières dangereuses et à l'intervention en cas de déversement (lot 10) ;
- interdiction de conduite de nuit sur piste et durée de travail limitée (H-126) ;
- bordereau de suivi à chaque enlèvement.

L'accord ADR n'a pas de valeur obligatoire démontrée au Cameroun (lot 2) ; il sert de référence de bonne pratique.

## 7. Contre-expertise

**Rôle : contre-expert.**

1. **Hypothèse fragile : 50 km de piste par site.** Certains chantiers sont à plus de 100 km de la route revêtue. Le coût au litre augmente alors fortement, et le temps de tournée dépasse une semaine.
2. **Hypothèse fragile : les sites sont accessibles toute l'année.** Les barrières de pluie peuvent imposer de concentrer les enlèvements en saison sèche, avec des stocks plus importants chez le client.
3. **Hypothèse fragile : un collecteur agréé de Douala accepte des tournées d'une semaine à l'Est au prix H-48 (Q-18).**

Scénario d'échec : en saison des pluies, plusieurs chantiers deviennent inaccessibles ; les fûts débordent chez le client, un déversement survient, et le client est sanctionné alors qu'il paie un contrat de conformité.

**Ce que la synthèse change en conséquence.** Le contrat de conformité prévoit une capacité de stockage tampon chez le client (fûts sur rétention pour au moins un trimestre), un calendrier d'enlèvement calé sur la saison sèche et un enlèvement d'urgence facturé à part. Les coordonnées GPS et l'état des pistes de chaque client sont relevés pendant le pilote.

## 8. Points faibles du livrable

1. Les distances viennent d'un graphe reconstruit, et non d'une matrice OSRM ; la répartition des clients est supposée.
2. Les prix des camions, de la location et de la sous-traitance ne viennent d'aucun devis.
3. Les barrières de pluie et l'état réel des pistes ne sont pas modélisés.
