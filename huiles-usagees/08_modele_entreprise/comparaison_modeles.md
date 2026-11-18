# Comparaison chiffrée des modèles d'entreprise

Fichier généré par `08_modele_entreprise/comparaison.py`. Montants en M FCFA. Flux annuels non endettés, années 0 à 5. Statut : supposé (hypothèses H-80 à H-99 et premier business plan [S-29]).

## Indicateurs par scénario

### Scénario pessimiste

| Modèle | Capital année 0 | Besoin de financement maximal | VAN 5 ans sans valeur terminale | VAN avec valeur terminale | CA année 5 | Résultat net année 5 |
|---|---:|---:|---:|---:|---:|---:|
| M1 | 25,0 | 369,8 | -253,6 | -500,0 | 32,8 | -79,3 |
| M2 | 25,0 | 719,8 | -483,9 | -1 012,8 | 25,4 | -178,6 |
| M3 | 97,0 | 700,3 | -505,3 | -785,3 | 158,4 | -122,7 |
| M4 | 7,0 | 287,7 | -196,2 | -374,6 | 9,6 | -55,2 |
| M5 | 7,0 | 396,8 | -265,8 | -542,0 | 32,8 | -84,7 |

### Scénario base

| Modèle | Capital année 0 | Besoin de financement maximal | VAN 5 ans sans valeur terminale | VAN avec valeur terminale | CA année 5 | Résultat net année 5 |
|---|---:|---:|---:|---:|---:|---:|
| M1 | 15,0 | 58,9 | -26,7 | 68,0 | 112,5 | 25,6 |
| M2 | 15,0 | 200,1 | -154,0 | -182,5 | 145,0 | -20,6 |
| M3 | 87,0 | 236,0 | -112,0 | 241,4 | 320,5 | 70,4 |
| M4 | 4,0 | 94,6 | -72,5 | -77,1 | 45,0 | -2,2 |
| M5 | 4,0 | 63,6 | -34,8 | 43,1 | 112,5 | 22,7 |

### Scénario optimiste

| Modèle | Capital année 0 | Besoin de financement maximal | VAN 5 ans sans valeur terminale | VAN avec valeur terminale | CA année 5 | Résultat net année 5 |
|---|---:|---:|---:|---:|---:|---:|
| M1 | 10,0 | 10,0 | 318,4 | 1 068,3 | 357,5 | 224,2 |
| M2 | 10,0 | 39,5 | 356,7 | 1 283,1 | 502,5 | 271,5 |
| M3 | 82,0 | 82,0 | 394,8 | 1 712,9 | 681,0 | 362,5 |
| M4 | 2,0 | 12,2 | 160,2 | 570,0 | 198,8 | 123,3 |
| M5 | 2,0 | 5,5 | 314,5 | 1 053,1 | 357,5 | 222,4 |

La valeur terminale est une rente perpétuelle sans croissance du flux d'exploitation de l'année 5, actualisée à 15 %. Les scénarios combinent toutes les bornes défavorables (pessimiste) ou favorables (optimiste) : ce sont des enveloppes, pas des cas probables.

## Point mort en nombre de clients forestiers (scénario de base)

| Modèle | Contribution annuelle par client | Clients nécessaires pour couvrir les charges fixes de structure |
|---|---:|---:|
| M1 | 5,14 | 7,8 |
| M4 | 2,64 | 15,2 |
| M5 | 5,14 | 8,9 |

Test du contre-expert, contrat de conformité à 3 M FCFA par an : M1 : contribution 2,14 M FCFA, point mort 18,7 clients ; M5 : contribution 2,14 M FCFA, point mort 21,5 clients.

M2 et M3 ont la même contribution par client que M1, plus des charges fixes propres au traitement (H-90, H-91) que seuls les volumes d'huiles peuvent couvrir.

## Sensibilité du modèle 3 au prix du combustible (scénario de base)

| Prix du combustible (FCFA/L) | VAN avec valeur terminale |
|---:|---:|
| 250 | -59,1 |
| 331 | 106,8 |
| 400 | 241,4 |

250 FCFA/L : seuil du premier business plan [S-29] ; 331 FCFA/L : prix moyen converti des carburants et lubrifiants importés en 2025 (`04_marche/gisement.md`) ; 400 FCFA/L : H-04.

## Matrice multicritère

Notes de 1 (défavorable) à 5 (favorable). Les quatre premiers critères chiffrés sont mis à l'échelle entre le meilleur et le moins bon modèle ; les autres sont des jugements d'expert justifiés dans `lot8_modele_entreprise.md`.

| Critère | Poids | M1 | M2 | M3 | M4 | M5 |
|---|---:|---:|---:|---:|---:|---:|
| Capital initial (année 0) | 20 % | 4,5 | 4,5 | 1,0 | 5,0 | 5,0 |
| Besoin de financement maximal | 15 % | 5,0 | 1,8 | 1,0 | 4,2 | 4,9 |
| Délai avant revenu propre | 10 % | 4,6 | 1,7 | 1,0 | 4,6 | 5,0 |
| Risque réglementaire | 15 % | 4,0 | 2,0 | 1,0 | 4,0 | 4,0 |
| Dépendance aux hypothèses non vérifiées | 15 % | 3,0 | 2,0 | 1,0 | 3,0 | 3,0 |
| Marge (VAN avec valeur terminale) | 10 % | 3,4 | 1,0 | 5,0 | 2,0 | 3,1 |
| Croissance par étapes | 10 % | 4,0 | 3,0 | 1,0 | 3,0 | 5,0 |
| Adéquation au profil du promoteur | 5 % | 5,0 | 4,0 | 3,0 | 3,0 | 5,0 |
| **Score pondéré** | | **4,14** | **2,54** | **1,50** | **3,79** | **4,35** |

Valeurs brutes des critères chiffrés :

| Critère | M1 | M2 | M3 | M4 | M5 |
|---|---:|---:|---:|---:|---:|
| Capital année 0 (M FCFA) | 15,0 | 15,0 | 87,0 | 4,0 | 4,0 |
| Besoin de financement (M FCFA) | 58,9 | 200,1 | 236,0 | 94,6 | 63,6 |
| Délai avant revenu propre (mois) | 2,0 | 10,1 | 12,1 | 2,0 | 1,0 |
| VAN avec valeur terminale (M FCFA) | 68,0 | -182,5 | 241,4 | -77,1 | 43,1 |

Classement : M5 (4,35), M1 (4,14), M4 (3,79), M2 (2,54), M3 (1,50).

