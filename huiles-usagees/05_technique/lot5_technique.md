# Lot 5 : technique et simulation du procédé

Méthodes : matrice multicritère des filières (`matrice_filieres.md`), simulation Python du bilan matière et énergie (`bilan_procede.md`), pyramide de Minto pour la conclusion.

**Rôles mobilisés :** ingénieur procédés, raffinage et régénération ; chimiste analyste ; expert HSE ; contre-expert.

## 1. Conclusion

Le lot 5 sert le modèle retenu en D-09 : jusqu'à l'étape 3, la société n'a besoin que d'un purificateur de gasoil, d'un kit de prélèvement et de dépistage, et d'un accès à un laboratoire. La filière de traitement en tête de la matrice est la remise des huiles à un valorisateur existant (F6, score 4,30). La filière à préparer pour l'étape 4 est la décantation suivie de déshydratation sous vide (F2) : elle a été simulée. Certitude : probable sur le choix, supposé sur les valeurs.

Deux résultats de la simulation changent les hypothèses du premier business plan :

1. **Le rendement dépend surtout de la qualité de l'huile entrante.** Il va de 65 % pour une huile très contaminée à 96 % pour une huile peu contaminée (`bilan_procede.md`). Le rendement de 80 % du business plan n'est valable que pour une huile moyennement contaminée, avant les refus de lots chlorés ou contenant des PCB.
2. **La capacité n'est pas une contrainte.** Le plus petit purificateur de la série TYA (10 L/min, soit 600 L/h [S-74]) traite en un poste les volumes du seuil de D-06 et ceux du premier business plan. L'investissement du premier business plan (166 M FCFA [S-29]) est surdimensionné par rapport à la matière première disponible.

## 2. Comparaison des filières

Le détail chiffré est dans `matrice_filieres.md`.

- **F6, remise à un valorisateur existant (4,30).** Aucun capital, aucune énergie. Les autorisations portent sur le valorisateur. Le risque est commercial : il faut un valorisateur titulaire qui accepte les huiles (Q-11). Seule filière compatible avec les étapes 1 à 3.
- **F1, décantation et filtration simples (3,90).** Très peu coûteuse et robuste. Elle laisse l'eau émulsionnée et dissoute ainsi que les fractions légères : produit de qualité faible, point éclair non maîtrisé.
- **F2, décantation puis déshydratation sous vide (3,55).** Ajoute un purificateur sous vide de quelques milliers à quelques dizaines de milliers de dollars [S-74]. Elle maîtrise l'eau et relève le point éclair en retirant les légers. Elle n'enlève ni les métaux, ni le chlore, ni les produits d'oxydation.
- **F3, terre adsorbante activée (2,70).** Le procédé publié au Cameroun utilise une montmorillonite activée [S-01]. Il améliore la qualité mais produit des terres usées chargées d'huile et de métaux, déchets dangereux à éliminer. Pas d'industrialisation connue (lot 3).
- **F4, distillation sous vide (2,30).** Produit un distillat de meilleure qualité, mais avec un capital et une énergie élevés, des résidus lourds à éliminer et un risque d'autorisation accru. Le volume disponible ne la justifie pas. Pour cette raison, aucun modèle DWSIM n'a été construit : la filière n'est pas retenue.
- **F5, re-raffinage (1,95).** Exclu au lot 4 ter : gisement inférieur au seuil de rentabilité [S-67].

## 3. Simulation du procédé F2

Le modèle (`procede.py`) enchaîne :

1. une décantation de 24 à 72 h qui retire une part de l'eau libre (H-103) et des sédiments (H-104), avec de l'huile entraînée dans les boues (H-111) ;
2. un chauffage à 60 à 80 °C (H-106) puis une déshydratation sous vide jusqu'à une eau résiduelle de 0,1 à 0,5 % (H-105), qui vaporise l'eau restante et les fractions légères (H-102).

L'énergie comprend la chaleur sensible, la chaleur latente de l'eau (2 333 kJ/kg vers 70 °C) et celle des légers (H-112), divisées par le rendement du skid (H-108). Le bilan boucle à zéro pour les trois qualités. Les trois qualités sont les bornes basse, centrale et haute de l'eau, des sédiments et des légers (H-100 à H-102), à remplacer par les résultats du protocole 4 bis n°2.

**Reprise dans HYSYS.** Le procédé se modélise avec un séparateur triphasique (décanteur) suivi d'un ballon de flash sous vide chauffé. L'huile se représente par des pseudo-composants issus d'une distillation simulée de l'échantillon, l'eau en composant pur, la dilution par le gasoil en coupe de distillat moyen. Les débits de `bilan_procede.md` servent de cas de validation.

## 4. Équipements et fournisseurs

Les prix sont en dollars, tels que publiés ; leur conversion et les frais d'approche relèvent du lot 9 (H-41, H-42). Aucun délai ni service après-vente en Afrique centrale n'a été confirmé (Q-37).

| Équipement | Étape | Fournisseur ou modèle | Prix publié | Point d'attention | Sources |
|---|---|---|---|---|---|
| Purificateur de gasoil 60 L/min | 1 (location), 2 (achat) | Parker DFC14WS25VVX1 [S-73] ou DFCC14WS10VVX1 [S-92], version 50 Hz à exiger | 6 773,51 USD (prix spécial), hors stock | cartouches de rechange au Cameroun (Q-16) | [S-73] |
| idem | | chariot Racor FBO-14 (même groupe Parker) | non lu | débit à vérifier | [S-84] |
| idem | | FFC 3000, chariot de filtration en location (Royaume-Uni) | non lu | location hors CEMAC, modèle de référence pour un loueur local | [S-84] |
| Purificateur sous vide | 4 | TYA, Tradeeasy | 2 500 USD FOB Chongqing, livraison 25 jours | modèle exact et débit à préciser | [S-74] |
| idem | | TYA 600 L/h, Chongqing TOP | 7 000 USD | | [S-74] |
| idem | | TYA-100 (6 000 L/h), Rexon | 36 500 USD | surdimensionné | [S-74] |
| Point éclair Pensky-Martens | 4 | LMPFT-A102 | non consulté | | [S-28] |
| idem | | Koehler automatique ; Anton Paar PMA 300 ou 500 ; Qualitest QualiFPT-CC-Auto | sur demande | sous-traitance au laboratoire jusqu'à l'étape 4 | [S-83] |
| Dépistage des halogènes | 1 | Dexsil Clor-D-Tect 1000 | 22 USD l'unité | commande par 10 puis par 20 | [S-14][S-15] |
| Prélèvement | 1 | Koehler K27400 et COLIWASA | non consulté | | [S-28] |

Seul un fournisseur a un prix publié pour le purificateur de gasoil : les deux autres prix sont à demander dans les demandes de prix du lot 15.

## 5. Laboratoire minimal

- **Étapes 1 à 3 :** kits Clor-D-Tect, test de crépitement, éprouvettes de décantation, densimètre, pâte de détection d'eau pour le gasoil, conservation des échantillons ; analyses complètes sous-traitées (Q-05).
- **Étape 4 :** ajout d'un appareil Pensky-Martens, d'une centrifugeuse pour l'eau et les sédiments (ASTM D4007), et d'un viscosimètre ; Karl Fischer acheté au-delà de 30 analyses par mois [S-28].

## 6. Spécification proposée du combustible (étape 4)

Proposition à valider avec l'acheteur et à confronter à une norme nationale si elle existe (Q-26). Les références ASTM sont citées sans lecture de leur texte.

| Paramètre | Méthode | Valeur proposée | Raison |
|---|---|---|---|
| Eau | ASTM D6304 ou D95 | au plus 0,5 % m/m | combustion stable ; cible du procédé 0,1 à 0,5 % (H-105) |
| Eau et sédiments | ASTM D4007 | au plus 0,5 % v/v | encrassement des brûleurs |
| Point éclair en vase clos | ASTM D93 | au moins 60 °C | sécurité de stockage et de transport |
| Chlore total | méthode du laboratoire | moins de 1 000 ppm | seuil de dépistage [S-28] ; corrosion et émissions de HCl |
| PCB | méthode chromatographique du laboratoire | non détectés | interdiction de valoriser des huiles contaminées |
| Soufre | ASTM D4294 | valeur déclarée | émissions de SO2 |
| Métaux (Pb, Zn, Cd, Cr, Ni, Cu) | ASTM D5185 | valeurs déclarées | émissions (lot 7) |
| Viscosité à 40 °C | ASTM D445 | valeur déclarée | préchauffage du brûleur |
| Masse volumique à 15 °C | ASTM D4052 | valeur déclarée | facturation au poids |

## 7. Plan de masse et utilités du centre de transit (étape 3)

Organisation proposée, à confirmer par l'étude de dangers et l'évaluation environnementale :

- **zone de réception :** quai de dépotage sur dalle étanche reliée à un séparateur d'hydrocarbures, aire d'échantillonnage abritée ;
- **zone de stockage :** cuves d'huiles acceptées et fûts en quarantaine dans une cuvette de rétention, avec une zone séparée pour les lots positifs au dépistage ;
- **zone de traitement (étape 4) :** décanteurs et purificateur sous vide sous abri ventilé, hors zone de stockage ;
- **local technique :** laboratoire minimal, tableau électrique, extincteurs et réserve d'absorbants ;
- **accès :** voie d'entrée et de sortie des camions sans marche arrière.

Utilités : électricité (Eneo et groupe de secours), eau pour le nettoyage et la lutte incendie, aucune vapeur. Rétention et séparateur dimensionnés selon l'étude de dangers ; à défaut de règle camerounaise trouvée, la pratique de référence consiste à retenir au moins le volume de la plus grande cuve.

## 8. Gestion des résidus

| Résidu | Origine | Filière |
|---|---|---|
| Eau huileuse | décantation | séparateur, puis éliminateur titulaire |
| Boues | décantation | éliminateur titulaire |
| Condensat de légers | déshydratation sous vide | mélange au produit si le point éclair reste conforme, sinon éliminateur |
| Cartouches et filtres usagés | purification du gasoil et de l'huile | éliminateur titulaire (extension E1) |
| Lots refusés (chlore, PCB) | réception | éliminateur titulaire, sans dilution |

## 9. Contre-expertise

**Rôle : contre-expert.**

1. **Hypothèse fragile : la qualité moyenne des huiles.** Des huiles de chantier stockées à ciel ouvert peuvent dépasser 20 % d'eau, et le rendement tombe alors sous 65 %.
2. **Hypothèse fragile : un purificateur sous vide à quelques milliers de dollars suffit.** Les prix les plus bas viennent de places de marché, sans garantie de conception pour des huiles moteur très sales.
3. **Hypothèse fragile : un valorisateur accepte les huiles brutes.** F6 n'existe que si Q-11 ou un autre valorisateur répond positivement.

Scénario d'échec : la campagne d'échantillonnage montre que 30 % des lots forestiers sont positifs au dépistage des halogènes, à cause de mélanges avec des solvants d'atelier. Ces lots coûtent leur élimination, et le gisement valorisable se réduit d'autant.

**Ce que la synthèse change en conséquence.** Le contrat de conformité inclut la formation au tri à la source et une clause de prix majoré pour les lots refusés. Le choix du purificateur sous vide passe par un essai sur échantillon réel chez le fournisseur avant toute commande.

## 10. Points faibles du livrable

1. La simulation repose sur des fractions d'eau, de sédiments et de légers supposées.
2. Les prix d'équipements viennent de distributeurs étrangers et de places de marché ; aucun prix rendu Douala ni service après-vente local n'est confirmé.
3. Le plan de masse est fonctionnel, sans dimensions ni implantation sur un terrain réel.
