# Bilan matière et énergie du prétraitement

Fichier généré par `05_technique/procede.py`. Base : 1 000 kg d'huile usagée entrante. Filière simulée : décantation et filtration, puis déshydratation sous vide (F2). Statut : supposé (H-100 à H-113).

| Grandeur (kg ou kWh) | peu contaminée | moyennement contaminée | très contaminée |
|---|---:|---:|---:|
| Huile entrante | 1 000,0 | 1 000,0 | 1 000,0 |
| Eau libre décantée | 15,0 | 60,0 | 150,0 |
| Boues (sédiments et huile entraînée) | 9,0 | 36,0 | 90,0 |
| Eau évaporée sous vide | 3,1 | 18,3 | 48,7 |
| Fractions légères condensées | 10,0 | 30,0 | 60,0 |
| Produit déshydraté | 962,9 | 855,7 | 651,3 |
| Rendement en produit | 96,3 % | 85,6 % | 65,1 % |
| Énergie électrique (kWh/t) | 32,5 | 44,4 | 67,4 |
| Coût de l'énergie (FCFA/t) | 3 250 | 4 441 | 6 735 |
| Écart de bouclage (kg) | 0,000 | 0,000 | 0,000 |

Le premier business plan retenait un rendement de 80 % (H-05). La simulation donne 65,1 % à 96,3 % selon la qualité, avant toute perte de lot refusé (chlore, PCB).

## Dimensionnement

| Volume traité (L/an) | Débit requis (L/h, 1 poste) | Plus petit TYA suffisant (L/min) |
|---:|---:|---:|
| 320 000 | 174 | 10 |
| 1 050 000 | 571 | 10 |
| 1 200 000 | 652 | 20 |

320 000 L/an : seuil de collecte de D-06 ; ligne 2 : collecte urbaine haute (H-96) et 25 clients forestiers (H-97 haut) ; 1 200 000 L/an : collecte urbaine du premier business plan (H-02). Le plus petit modèle de la gamme TYA (10 L/min, soit 600 L/h) [S-74] couvre tous les cas sur un poste : le débit n'est pas une contrainte, la matière première l'est.

