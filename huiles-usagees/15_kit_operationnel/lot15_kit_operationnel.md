# Lot 15 : kit opérationnel

Le kit est prêt à imprimer ou à compléter : 37 documents en `.docx` (dossier `docx/`) et en `.pdf` (dossier `pdf/`), plus deux classeurs Excel à formules. Les sources éditables sont au format Markdown dans `sources/`. Une seule commande régénère l'ensemble : `python3 15_kit_operationnel/construire_kit.py` (également appelée par `run_all.py`).

**Mise en forme.** Charte typographique retenue en D-02 : A4, Arial, marges de 2,5 / 2,5 / 3 / 2 cm, titres en bleu marine, tableaux à en-tête coloré répété, champs à compléter surlignés en jaune, en-tête et pied de page avec « Page X sur Y ». Aucune marque HIKMA. Noms de fichiers au format « AAAA-MM-JJ Projet Document », sans tiret bas.

## Inventaire

| Code | Document | Usage |
|---|---|---|
| A1 | Demande de permis environnemental, pré-remplie | dépôt au MINEPDED à l'étape 3 |
| A2 | Lettres types aux administrations (MINEPDED, MINMIDT, MINEFOP, HIKMA) | semaine 1 du plan des 100 jours |
| A3 | Dossier d'établissement classé | après réponse sur la classe (Q-22) |
| A4 | Lettre de demande d'accès aux données de sanctions | protocole 4 bis n°4 |
| B1 | Cahiers des charges des sept équipements | achats |
| B2 | Demandes de prix en français et en anglais, une par équipement (E1 à E7) | achats |
| B3 | Grille de comparaison des offres (Excel, score pondéré par formules) | achats |
| P0 à P7 | Procédures : acceptation des lots, réception et échantillonnage, analyse, traitement, chargement et transport, déversement, nettoyage de cuve, purification du gasoil | exploitation |
| F1 à F5 | Bordereau de suivi, registre des entrées et sorties, fiche d'analyse, fiche d'incident, étiquettes de fûts | exploitation |
| C1 à C4 | Contrats : conformité forestier, achat d'huiles urbaines, vente de combustible, transport sous-traité | commercial et achats |
| J1 à J3 | Projet de statuts, projet de pacte d'associés, charte de prévention des conflits d'intérêts (lot 11) | création |
| K1 à K5 | Grille tarifaire, proposition commerciale type, plaquette, argumentaire et script d'appel, plan de prospection des 50 premières cibles | commercial |
| T1 | Tableau de bord des indicateurs (Excel : volumes, taux de récupération, coût par litre, marge, incidents, lots refusés) | pilotage |

## Traçabilité des chiffres

Les prix de la grille tarifaire viennent des hypothèses du modèle financier ; la correspondance est dans `grille_tarifaire_tracabilite.md`. Les cibles du tableau de bord renvoient aux décisions et lots qui les fixent (onglet Synthèse). Les montants réglementaires (frais d'étude, caution) restent marqués « à confirmer » tant que le texte officiel n'a pas été lu (Q-01).

## Contre-expertise

**Rôle : contre-expert.**

1. **Les modèles de contrats ne sont pas relus par un avocat.** Clauses de responsabilité, de non-sollicitation et de suspension à valider en droit camerounais et OHADA.
2. **Le bordereau et le registre ne reprennent pas encore le modèle officiel.** S'il existe un formulaire réglementaire, il prévaut.
3. **Le plan de prospection ne nomme que 8 cibles sur 50.** Les 42 autres dépendent de la liste du MINFOF et de l'enquête terrain.

**Ce que la synthèse change en conséquence.** Relecture juridique des contrats C1 et C4 inscrite au budget de démarrage. Alignement du bordereau F1 sur le modèle officiel dès réception du texte. Obtention de la liste des titres d'exploitation au MINFOF ajoutée à la semaine 2 du plan des 100 jours.

## Points faibles

1. Aucun document n'a été testé sur le terrain.
2. Les demandes de prix ne peuvent pas citer de prix plafonds : aucun devis n'a été obtenu.
3. Les étiquettes de fûts sont des maquettes ; l'impression des QR codes se fait par l'application du lot 16.
