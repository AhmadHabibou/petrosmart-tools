# Optimisation robuste de la stratégie

Fichier généré par `18_optimisation/optimisation.py`. Méthode : évaluation de chaque stratégie sur les mêmes tirages Monte-Carlo (2 000 pour la recherche, 10 000 pour la confirmation), apport nul pour mesurer les fonds propres requis ; frontière de Pareto entre la VAN avec valeur terminale au 10e centile et les fonds propres requis au 90e centile, sous la contrainte d'une couverture du service financier d'au moins 1,2 en années 3 à 5 dans au moins 80 % des tirages.

## Conclusions

1. **Sous-traiter les enlèvements jusqu'à l'étape 3** (confirme D-10). Le camion propre réduit la VAN avec valeur terminale au 10e centile de 15,1 M FCFA et augmente les fonds propres requis au 90e centile de 29,5 M FCFA.
2. **Fixer la porte d'équipement à 4 contrats.** Elle fait mieux que 6 contrats (49,0 contre 47,6 M FCFA au 10e centile) ; le mois minimal de la porte n'a pas d'effet, car c'est le nombre de contrats qui la déclenche.
3. **Le choix entre crédit-bail et emprunt dépend des offres.** Avec les hypothèses actuelles, l'achat financé par emprunt fait mieux (49,0 contre 40,7 M FCFA au 10e centile) ; le crédit-bail ne l'égale que si ses loyers restent sous 3,88 M FCFA par an (6,00 M FCFA supposés). Mais l'emprunt suppose qu'une banque prête à une société dont la couverture de la dette est négative en année 2 (lot 9) : le crédit-bail (D-11) reste la voie réaliste tant qu'aucune offre de prêt n'est obtenue, et la décision est à revoir à réception des offres B4.
4. **La couverture du service financier est le point faible pour la banque.** Aucune stratégie n'atteint 1,2 en années 3 à 5 dans 80 % des tirages (au mieux 78 %) ; la stratégie retenue y parvient dans 63 % des cas. La seconde tranche de comptes courants du pacte d'associés en est la réponse.
5. **Prix plancher du contrat : 6,62 M FCFA HT par site** pour une VAN à 5 ans positive dans 80 % des tirages.
6. **Mesurer en premier** le nombre de contrats signés et le prix accepté (pilote), puis le prix des enlèvements sous-traités (devis des collecteurs).

Coût variable d'un camion propre : tiré entre 74 et 226 FCFA/L, valeur centrale 123 FCFA/L (carburant, entretien, équipage sur le réseau des 15 clients du lot 6, saisons sèche et des pluies), proportionnel à la fréquence des enlèvements (H-88) ; s'y ajoutent l'assurance et les autorisations (H-133) et l'achat d'occasion (H-131).

## Stratégies évaluées

| Stratégie | VAN 5 ans P10 | VAN 5 ans P50 | VAN 5 ans < 0 | VAN avec VT P10 | Fonds propres requis P50 | Fonds propres requis P90 | Couverture ≥ 1,2 | Admissible |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Achat et emprunt, porte au mois 13 et 4 contrats, enlèvements sous-traités | -18,1 | 17,4 | 27 % | 49,0 | 16,0 | 32,6 | 66 % | non |
| Achat et emprunt, porte au mois 19 et 4 contrats, enlèvements sous-traités | -18,1 | 17,3 | 27 % | 49,0 | 16,4 | 32,6 | 66 % | non |
| Achat et emprunt, porte au mois 13 et 6 contrats, enlèvements sous-traités | -20,1 | 15,8 | 30 % | 47,6 | 17,6 | 33,6 | 68 % | non |
| Achat et emprunt, porte au mois 25 et 6 contrats, enlèvements sous-traités | -20,1 | 15,6 | 30 % | 47,6 | 17,8 | 33,8 | 68 % | non |
| Crédit-bail, enlèvements sous-traités | -18,8 | 16,8 | 27 % | 40,7 | 18,5 | 37,7 | 67 % | non |
| Achat et emprunt, porte au mois 13 et 4 contrats, enlèvements camion propre au mois 37 | -28,7 | 6,9 | 41 % | 33,9 | 37,0 | 62,1 | 66 % | non |
| Achat et emprunt, porte au mois 19 et 4 contrats, enlèvements camion propre au mois 37 | -28,7 | 6,8 | 41 % | 33,9 | 37,0 | 62,1 | 66 % | non |
| Achat et emprunt, porte au mois 13 et 4 contrats, enlèvements camion propre au mois 25 | -29,3 | 7,0 | 41 % | 33,2 | 42,1 | 58,3 | 76 % | non |
| Achat et emprunt, porte au mois 19 et 4 contrats, enlèvements camion propre au mois 25 | -29,3 | 6,8 | 41 % | 33,2 | 42,1 | 58,3 | 76 % | non |
| Achat et emprunt, porte au mois 13 et 6 contrats, enlèvements camion propre au mois 37 | -31,0 | 5,3 | 43 % | 32,2 | 36,9 | 62,5 | 68 % | non |
| Achat et emprunt, porte au mois 25 et 6 contrats, enlèvements camion propre au mois 37 | -31,0 | 5,2 | 43 % | 32,2 | 36,9 | 62,5 | 68 % | non |
| Achat et emprunt, porte au mois 13 et 6 contrats, enlèvements camion propre au mois 25 | -31,1 | 5,4 | 43 % | 30,5 | 44,6 | 60,9 | 78 % | non |
| Achat et emprunt, porte au mois 25 et 6 contrats, enlèvements camion propre au mois 25 | -31,1 | 5,2 | 43 % | 30,5 | 44,6 | 60,9 | 78 % | non |
| Crédit-bail, enlèvements camion propre au mois 37 | -29,3 | 6,3 | 42 % | 24,3 | 42,0 | 67,2 | 67 % | non |
| Crédit-bail, enlèvements camion propre au mois 25 | -29,7 | 6,3 | 42 % | 22,5 | 47,4 | 63,6 | 77 % | non |

Montants en M FCFA. P10, P50, P90 : 10e, 50e et 90e centiles des tirages. La VAN avec valeur terminale est corrigée du renouvellement des équipements (amortissement de l'année 5 reconduit à perpétuité).

## Frontière de Pareto

**Aucune stratégie ne respecte la contrainte de couverture** (au moins 1,2 dans 80 % des tirages). La frontière ci-dessous est calculée sans cette contrainte ; la probabilité de couverture de chaque stratégie figure dans le tableau précédent.

| Stratégie | VAN avec VT P10 | Fonds propres requis P90 |
|---|---:|---:|
| Achat et emprunt, porte au mois 13 et 4 contrats, enlèvements sous-traités | 49,0 | 32,6 |
| Achat et emprunt, porte au mois 19 et 4 contrats, enlèvements sous-traités | 49,0 | 32,6 |

## Stratégie retenue et confirmation

**Achat et emprunt, porte au mois 13 et 4 contrats, enlèvements sous-traités**, confirmée sur 10 000 tirages : VAN à 5 ans au 10e centile -19,9 M FCFA, médiane 15,0 M FCFA, négative dans 29,7 % des tirages ; VAN avec valeur terminale au 10e centile 45,4 M FCFA ; fonds propres requis 16,5 M FCFA en médiane et 33,9 M FCFA au 90e centile ; couverture d'au moins 1,2 dans 63,2 % des tirages.

Règle de choix : sur la frontière de Pareto (stratégies admissibles, ou toutes si aucune ne l'est), la plus forte VAN avec valeur terminale au 10e centile.

## Correction à reporter au lot 9

La valeur terminale du modèle mensuel ne déduit pas le renouvellement des équipements achetés. Dans le scénario de base (achat et emprunt), la VAN avec valeur terminale de 137,4 M FCFA est surestimée d'environ 12,6 M FCFA. La structure en crédit-bail du business plan bancaire est peu touchée : ses loyers sont déjà dans l'EBITDA.

## Crédit-bail ou emprunt

Le crédit-bail (enlèvements sous-traités) égale la meilleure stratégie d'achat (achat et emprunt, porte au mois 13 et 4 contrats, enlèvements sous-traités) sur la VAN avec valeur terminale au 10e centile si ses loyers ne dépassent pas **3,88 M FCFA par an**, contre 6,00 M FCFA supposés (H-94). Le choix entre crédit-bail (D-11) et emprunt se fera donc sur les offres reçues avec la lettre B4, en tenant compte de l'option d'achat en fin de contrat, que le modèle ignore, et des garanties exigées pour un emprunt.

## Seuil de prix du contrat

Pour la stratégie retenue, la VAN à 5 ans est positive dans au moins 80 % des tirages si le contrat annuel atteint **6,62 M FCFA HT par site**, contre 6,00 M FCFA retenus (H-80). C'est le prix minimal à valider pendant le pilote.

## Ce qu'il faut mesurer en premier

Corrélation de rang entre chaque hypothèse tirée et la VAN avec valeur terminale, stratégie retenue. Plus elle est forte en valeur absolue, plus la mesure de l'hypothèse réduit l'incertitude.

| Hypothèse | Libellé | Corrélation de rang |
|---|---|---:|
| H-97 | Clients forestiers sous contrat en année 5 | 0,60 |
| H-80 | Prix annuel du contrat de conformité par client forestier (fûts, kits, registre, formation, 4 enlèvements, rapport PGES) | 0,56 |
| H-48 | Pilote : coût d'une tournée d'enlèvement sous-traitée à un collecteur agréé | -0,31 |
| H-81 | Prix d'une intervention de purification du gasoil et nettoyage de cuve | 0,21 |
| H-88 | Enlèvements d'huiles par client forestier et par an | -0,19 |
| H-82 | Interventions de purification du gasoil par client forestier et par an | 0,18 |
| H-83 | Valeur nette des huiles remises à un valorisateur titulaire (négatif : la société paie) | 0,11 |
| H-153 | Frais généraux (bureau, téléphone, comptable externe, déplacements commerciaux), à partir du mois 4 | -0,10 |

## Limites

1. Les hypothèses tirées sont pour la plupart « supposées » : l'optimum dit quelle stratégie est la plus robuste à notre ignorance actuelle, pas quelle stratégie gagnera.
2. Le coût du camion propre suppose des tournées organisées comme au lot 6 dès son achat ; avec moins de 15 clients, le coût par litre serait plus élevé.
3. Les leviers commerciaux (prix, effort de vente, recrutement du commercial) ne sont pas optimisés : le modèle ne relie pas ces choix au nombre de clients.
4. Le choix du modèle d'entreprise (M1 à M5) a été fait au lot 8 ; l'optimisation porte sur la trajectoire retenue (D-09).
