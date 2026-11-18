# Lot 9 : finance et simulations

Méthodes : modèle mensuel sur 60 mois (`modele_mensuel.py`), scénarios, tornado, Monte-Carlo de 10 000 tirages, scénario de stress ; pyramide de Minto pour la conclusion. Résultats : `resultats_finance.md`. Classeur : `modele_financier.xlsx`.

**Rôles mobilisés :** analyste financier et banquier de PME, juriste OHADA et fiscaliste, entrepreneur PME en Afrique centrale, contre-expert.

## 1. Conclusion

La trajectoire retenue (M5 puis M1) est rentable dans le scénario de base, mais tendue en trésorerie les deux premières années. Certitude : supposé, tant que le pilote n'a pas mesuré le prix du contrat et le rythme de signature.

1. **Rentabilité.** VAN à 5 ans légèrement positive (9 M FCFA), TRI de 27,5 %, VAN de 137 M FCFA avec valeur terminale. La société atteint son point mort d'exploitation au mois 20 et un résultat net de 34 M FCFA en année 5 pour 15 clients forestiers.
2. **Risque.** Sur 10 000 tirages, la VAN à 5 ans est négative dans 29,5 % des cas, mais la VAN avec valeur terminale ne l'est que dans 2,3 % des cas. Le projet perd peu de valeur à long terme ; son risque est surtout un risque de démarrage.
3. **Trésorerie.** Avec un apport de 10 M FCFA et un emprunt de 20 M FCFA, la trésorerie descend à -8,5 M FCFA en année 2. Il faut donc environ 20 M FCFA de fonds propres et quasi-fonds propres au démarrage, ou une ligne de trésorerie équivalente. Au 90e centile, le besoin de financement atteint 45,6 M FCFA.
4. **Dette.** Placé au passage en M1 (mois 20), l'emprunt tombe dans une année où l'EBITDA est encore négatif : DSCR de -2,02 en année 2, puis 1,66 en année 3. Un banquier refusera ce calendrier. L'achat des équipements doit donc être financé par crédit-bail, ou différé jusqu'à trois mois consécutifs d'EBITDA positif.
5. **Leviers.** Le tornado confirme le lot 8 : le nombre de clients (H-97) et le prix du contrat (H-80) dominent, devant le coût de l'enlèvement sous-traité (H-48). Une guerre des prix qui ferait baisser les contrats de 30 % rend la VAN à 5 ans négative (-23,6 M FCFA), sans tuer le projet (VAN avec valeur terminale de 26,9 M FCFA).

Les chiffres ci-dessus sont générés dans `resultats_finance.md` et contrôlés par les tests.

## 2. Structure du modèle

- **Horizon :** 60 mois ; flux mensuels ; impôt calculé par exercice.
- **Activité :** 2 clients pilotes du mois 4 au mois 12, puis progression linéaire jusqu'à H-97 au mois 60. Revenus : contrats de conformité, purification du gasoil, valeur des huiles remises, commission sur les volumes urbains apportés à un partenaire, marge des activités d'amorçage pendant 24 mois.
- **Passage de M5 à M1 :** au premier mois à partir du mois 13 où la société compte au moins 4 clients (porte de l'étape 1 du lot 8). Les loyers s'arrêtent, les équipements sont achetés, l'emprunt est débloqué.
- **Charges :** enlèvements sous-traités (le lot 6 montre que la sous-traitance est l'option la moins chère à ce volume), consommables, salaires progressifs (technicien au mois 4, gérant et commercial au mois 13), frais généraux, assurances.
- **Fiscalité :** impôt sur les sociétés à 25 % du bénéfice (H-99), avec un minimum de perception de 2,2 % du chiffre d'affaires [S-29] ; report des déficits sur 4 ans, règle de travail à confirmer (Q-31). La TVA n'est pas modélisée : elle est neutre sur le résultat, mais pèse sur la trésorerie si les clients paient en retard.
- **Bilan :** immobilisations nettes, créances, trésorerie à l'actif ; apports, résultats cumulés, emprunt et dettes fournisseurs au passif. L'écart actif moins passif est nul sur les 60 mois.
- **Classeur Excel :** les lignes d'exploitation, de BFR, de flux et de trésorerie sont des formules liées à la feuille Hypotheses. Les amortissements, intérêts, impôts et flux de financement sont des valeurs calculées par Python, en italique. Une ligne de contrôle compare la trésorerie des formules et celle de Python : après recalcul par LibreOffice, l'écart est nul (test automatisé).

## 3. Plan de financement recommandé

| Besoin | Montant de travail | Source recommandée |
|---|---|---|
| Démarrage, loyers, salaires du technicien, BFR des premiers contrats | apport de 10 M FCFA (H-157) plus environ 8,5 M FCFA de quasi-fonds propres ou de ligne de trésorerie | apport du promoteur et d'associés (lot 11), avances clients via un paiement trimestriel d'avance des contrats |
| Équipements du passage en M1 (purificateur, véhicule léger, H-92) | 15 M FCFA | crédit-bail plutôt qu'emprunt, pour éviter un service de la dette en année 2 |
| Croissance (années 3 à 5) | selon la trajectoire | crédit bancaire à moyen terme, garanti si possible |

Le paiement trimestriel d'avance des contrats de conformité est le levier le moins coûteux : il supprime une grande part du BFR (20 M FCFA de créances en fin d'année 5 en scénario de base, avec un délai de paiement de 60 jours).

## 4. Sources de financement identifiées

Les conditions précises (taux, garanties, éligibilité) n'ont pas été obtenues : chaque piste doit être confirmée par un rendez-vous.

- **Crédit bancaire aux PME.** Le coût moyen du crédit aux PME est de 11,85 % selon des données de la BEAC reprises par la presse [S-78] ; c'est la valeur centrale de H-159. Les PME accèdent difficilement au crédit faute de garanties [S-78].
- **Garantie.** La Caisse des dépôts et consignations du Cameroun (CDEC) et l'African Guarantee Fund ont mis en place un dispositif de 5 milliards de FCFA pour les PME, et la CDEC teste un crédit de long terme aux PME [S-79]. C'est la piste à ouvrir en premier pour réduire les garanties demandées par la banque.
- **Lignes vertes.** Attijariwafa bank et l'AFD ont mobilisé 15 millions d'euros pour les PME vertes au Cameroun [S-80]. Un projet de gestion des déchets dangereux peut y prétendre, sous réserve des critères d'éligibilité de la ligne.
- **Lignes PME de bailleurs.** La Banque islamique de développement a accordé une ligne de 95 millions d'euros à quatre banques camerounaises pour les PME, et la SFI a financé Afriland First Bank à hauteur de 37 milliards de FCFA pour les PME [S-81].
- **Crédit-bail.** Les PME de la zone CEMAC s'orientent vers le crédit-bail face aux difficultés d'accès au crédit (presse, [S-78]) ; aucune offre n'a été consultée (Q-35).
- **Subventions et prix.** Aucun appel ouvert n'a été trouvé au 17/11/2026 (lot 0). Veille maintenue.

## 5. Contre-expertise

**Rôle : contre-expert.**

Les trois hypothèses les plus fragiles :

1. **H-97 et H-80, 15 clients à 6 M FCFA en année 5.** Ensemble, elles expliquent l'essentiel de la variance de la VAN. Aucune n'est mesurée.
2. **H-161, la marge des activités d'amorçage pendant 24 mois.** Elle couvre une partie des pertes des deux premières années. Si le promoteur n'a pas le temps de mener le lot 0 et le pilote en parallèle, cette marge disparaît.
3. **Le délai de paiement des clients (H-155).** Des grands comptes forestiers payant à 90 jours ou plus, avec une TVA avancée, creusent la trésorerie au-delà du besoin calculé.

Scénario d'échec : la signature des contrats prend deux fois plus de temps que prévu (8 clients en année 5), et le prix se fixe à 4 M FCFA. La société reste sous son point mort, consomme ses fonds propres en 18 mois et ne peut pas rembourser un emprunt contracté trop tôt.

**Ce que la synthèse change en conséquence.**

- La porte de l'étape 1 du lot 8 est complétée : passer en M1 exige, en plus de 4 contrats signés, trois mois consécutifs d'EBITDA positif.
- L'achat d'équipements se finance par crédit-bail, pas par emprunt.
- Le contrat de conformité est facturé trimestriellement d'avance.
- La note Go/No Go du lot 17 reprendra le seuil de 20 M FCFA de fonds propres et quasi-fonds propres au démarrage.

## 6. Points faibles du livrable

1. Toutes les hypothèses d'activité sont supposées ; les salaires seront remplacés par des salaires de marché sourcés au lot 10.
2. La TVA, les acomptes d'impôt et les règles exactes du report déficitaire ne sont pas modélisés (Q-31).
3. Les lois triangulaires du Monte-Carlo sont indépendantes : en réalité, un prix de contrat élevé réduit probablement le nombre de clients, ce qui élargit la dispersion réelle.
