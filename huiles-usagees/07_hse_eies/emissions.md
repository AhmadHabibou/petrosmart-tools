# Émissions de métaux lors de la combustion : méthode de borne haute

Fichier généré par `07_hse_eies/risques_hse.py`.

Les facteurs d'émission de l'EPA pour la combustion des huiles usagées (AP-42, section 1.11 [S-77]) expriment le plomb émis en proportion de la teneur en plomb du combustible ; leurs valeurs n'ont pas pu être lues. En attendant, la borne haute suppose que tout le métal contenu dans le combustible sort à la cheminée. Elle se calcule sans hypothèse sur l'installation de l'acheteur, à partir des résultats de laboratoire du protocole 4 bis n°2.

Formule : émission (kg) = teneur (mg/kg) × 10⁻⁶ × volume brûlé (L) × masse volumique (H-60, 0,90 kg/L).

| Teneur du combustible en métal (mg/kg) | Émission maximale pour 1 000 L brûlés (g) | Pour 100 000 L brûlés (kg) |
|---:|---:|---:|
| 10 | 9,0 | 0,90 |
| 50 | 45,0 | 4,50 |
| 100 | 90,0 | 9,00 |
| 500 | 450,0 | 45,00 |
| 1 000 | 900,0 | 90,00 |

Aucune teneur n'est supposée ici : la colonne de gauche est une échelle de lecture. Les teneurs réelles viendront des analyses ASTM D5185.

