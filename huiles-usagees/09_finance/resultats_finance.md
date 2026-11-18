# Résultats du modèle financier mensuel

Fichier généré par `09_finance/rapport_finance.py`. Trajectoire retenue (D-09) : M5 jusqu'à la porte de l'étape 1, puis M1. Montants en M FCFA. Statut : supposé (hypothèses listées dans `modele_financier.xlsx`, feuille Hypotheses).

## Scénarios

| Indicateur | Pessimiste | Base | Optimiste |
|---|---:|---:|---:|
| VAN à 5 ans, sans valeur terminale | -190,3 | 9,0 | 321,8 |
| VAN avec valeur terminale | -361,0 | 137,4 | 1 053,0 |
| TRI (flux disponibles) | non défini | 27,5 % | non défini |
| Besoin de financement maximal (flux disponibles cumulés) | 270,7 | 33,6 | 0,0 |
| Trésorerie minimale après apport et emprunt | -267,1 | -8,5 | 20,0 |
| Point mort (EBITDA positif durablement) | non atteint | mois 20 | mois 1 |
| Délai de récupération (cumul durablement positif) | non atteint | mois 50 | mois 1 |
| Mois de passage en M1 | mois 28 | mois 20 | mois 17 |
| DSCR minimal annuel | -12,15 | -2,02 | 11,88 |
| Chiffre d'affaires de l'année 5 | 32,6 | 110,2 | 341,1 |
| Résultat net de l'année 5 | -58,6 | 34,1 | 216,8 |

Les scénarios pessimiste et optimiste combinent toutes les bornes défavorables ou favorables : ce sont des enveloppes. La distribution réaliste est donnée par le Monte-Carlo.

## Compte de résultat et trésorerie annuels (scénario de base)

| Poste | Année 1 | Année 2 | Année 3 | Année 4 | Année 5 |
|---|---:|---:|---:|---:|---:|
| Clients forestiers en fin d'année | 2,0 | 5,2 | 8,5 | 11,8 | 15,0 |
| Chiffre d'affaires | 18,8 | 37,2 | 56,4 | 83,3 | 110,2 |
| dont contrats de conformité | 9,0 | 22,6 | 42,1 | 61,6 | 81,1 |
| dont purification du gasoil | 2,2 | 5,6 | 10,5 | 15,4 | 20,3 |
| dont commission urbaine | 0,0 | 1,4 | 3,9 | 6,4 | 8,9 |
| dont activités d'amorçage | 7,6 | 7,6 | 0,0 | 0,0 | 0,0 |
| Charges d'exploitation | 21,5 | 40,6 | 44,7 | 52,4 | 60,1 |
| EBITDA | -2,7 | -3,4 | 11,7 | 30,9 | 50,1 |
| Amortissements | 0,6 | 1,8 | 3,8 | 3,8 | 3,8 |
| Intérêts | 0,0 | 0,8 | 2,0 | 1,4 | 0,8 |
| Impôt | 0,4 | 0,8 | 1,2 | 5,6 | 11,4 |
| Résultat net | -3,7 | -6,8 | 4,7 | 20,1 | 34,1 |
| Investissements | 4,0 | 15,0 | 0,0 | 0,0 | 0,0 |
| Flux de trésorerie disponible | -10,5 | -23,1 | 7,9 | 21,5 | 34,9 |
| Trésorerie de fin d'année | -0,5 | -5,7 | -4,1 | 11,1 | 39,7 |
| Créances clients (BFR) en fin d'année | 3,8 | 8,2 | 11,5 | 15,9 | 20,4 |
| Capital restant dû en fin d'année | 0,0 | 18,7 | 14,3 | 9,5 | 4,0 |

DSCR par année (EBITDA moins impôt, divisé par le service de la dette) : année 2 : -2,02 ; année 3 : 1,66 ; année 4 : 4,02 ; année 5 : 6,15.
Apport ou ligne de trésorerie supplémentaire nécessaire pour que la trésorerie reste positive en scénario de base : 8,5 M FCFA, en plus de l'apport de 10,0 M FCFA (H-157) et de l'emprunt de 20,0 M FCFA (H-158).
Écart maximal du bilan (actif moins passif) sur 60 mois : 0,000000 FCFA.

## Analyse de sensibilité (tornado, VAN avec valeur terminale)

VAN de base : 137,4 M FCFA. Chaque hypothèse est placée à sa borne basse puis haute, les autres restant centrales.

| Hypothèse | Libellé | VAN à la borne basse | VAN à la borne haute | Amplitude |
|---|---|---:|---:|---:|
| H-97 | Clients forestiers sous contrat en année 5 | 31,4 | 293,3 | 261,9 |
| H-80 | Prix annuel du contrat de conformité par client forestier (fûts, kits, registre, formation, 4 enlèvements, rapport PGES) | 45,2 | 286,8 | 241,7 |
| H-48 | Pilote : coût d'une tournée d'enlèvement sous-traitée à un collecteur agréé | 178,4 | 66,8 | 111,7 |
| H-88 | Enlèvements d'huiles par client forestier et par an | 163,0 | 86,1 | 76,9 |
| H-82 | Interventions de purification du gasoil par client forestier et par an | 118,7 | 194,0 | 75,3 |
| H-81 | Prix d'une intervention de purification du gasoil et nettoyage de cuve | 107,7 | 182,6 | 74,8 |
| H-83 | Valeur nette des huiles remises à un valorisateur titulaire (négatif : la société paie) | 112,7 | 162,5 | 49,8 |
| H-153 | Frais généraux (bureau, téléphone, comptable externe, déplacements commerciaux), à partir du mois 4 | 156,6 | 112,2 | 44,4 |
| H-161 | Marge nette mensuelle des activités d'amorçage (lot 0), sur les 24 premiers mois | 130,2 | 156,8 | 26,6 |
| H-150 | Rémunération chargée du gérant, à partir du mois 13 | 145,7 | 120,9 | 24,8 |
| H-87 | Coût des consommables par intervention de purification (cartouches, filtres, absorbants) | 146,5 | 125,3 | 21,2 |
| H-155 | Délai de paiement des clients | 144,7 | 130,1 | 14,6 |

## Simulation de Monte-Carlo (10 000 tirages)

Lois triangulaires (borne basse, valeur centrale, borne haute) sur H-01, H-21, H-48, H-80, H-81, H-82, H-83, H-87, H-88, H-96, H-97, H-150, H-151, H-152, H-153, H-154, H-155, H-161. Graine fixe : résultats reproductibles.

| Résultat | Valeur |
|---|---:|
| Probabilité de VAN à 5 ans négative (sans valeur terminale) | 29,5 % |
| Probabilité de VAN avec valeur terminale négative | 2,3 % |
| VAN avec valeur terminale, 10e centile | 58,0 |
| VAN avec valeur terminale, médiane | 154,1 |
| VAN avec valeur terminale, 90e centile | 293,6 |
| Besoin de financement maximal au 90e centile | 45,6 |

## Scénario de guerre des prix

À partir du mois 25, un concurrent ou le circuit informel offre l'enlèvement gratuit : le prix des contrats baisse de 30 % (H-162) et la commission urbaine disparaît.

| Indicateur | Base | Guerre des prix |
|---|---:|---:|
| VAN à 5 ans | 9,0 | -23,6 |
| VAN avec valeur terminale | 137,4 | 26,9 |
| Besoin de financement maximal | 33,6 | 38,6 |
| Résultat net de l'année 5 | 34,1 | 10,6 |

## Comparaison avec les modèles du lot 8 (comparateur annuel, scénario de base)

| Modèle | Besoin de financement | VAN avec valeur terminale |
|---|---:|---:|
| M1 (annuel) | 58,9 | 68,0 |
| M2 (annuel) | 200,1 | -182,5 |
| M3 (annuel) | 236,0 | 241,4 |
| M4 (annuel) | 94,6 | -77,1 |
| M5 (annuel) | 63,6 | 43,1 |
| Trajectoire M5 puis M1 (mensuel) | 33,6 | 137,4 |

Le modèle mensuel fait monter les charges de structure avec les embauches et ajoute la marge des activités d'amorçage : son besoin de financement est plus faible que celui des comparateurs annuels à charges fixes pleines.

