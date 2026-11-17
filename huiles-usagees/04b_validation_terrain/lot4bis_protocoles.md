# Lot 4 bis : protocoles de validation sur le terrain

Ces quatre protocoles sont prêts à exécuter. Ils produisent les preuves qu'aucune étude documentaire ne remplace : volumes réels, qualité réelle des huiles, acceptation du combustible par un acheteur, poids réel des sanctions. Le budget de chaque protocole est généré par `budget_protocoles.py` dans `budget_protocoles.md` (cas central : 8,87 M FCFA pour les quatre). Les formulaires de saisie sont dans `formulaires/` au format CSV (séparateur point-virgule, ouvrable dans Excel).

Règle d'arbitrage appliquée : on loue ou on sous-traite pendant le pilote, on n'achète qu'après la porte de décision (annexe A du cahier des charges [S-29]).

## 1. Préalable réglementaire commun

**Rôle : juriste en droit de l'environnement camerounais.**

La société n'a pas de permis environnemental. L'arrêté n°001/MINEPDED du 15 octobre 2012 soumet à permis la collecte, le transport et le stockage des déchets dangereux [S-02] (connu par extrait). Trois conséquences :

1. pendant le pilote, l'enlèvement et le transport des huiles usagées sont réalisés par un collecteur agréé, sous son bordereau (décision D-05) ;
2. les échantillons de 100 mL à 1 L prélevés pour analyse restent sous la responsabilité du producteur jusqu'à leur remise au laboratoire, avec une chaîne de traçabilité signée ;
3. la fabrication d'un lot de combustible pour l'essai n°3 n'est faite que par un partenaire qui détient le titre adéquat, ou après autorisation écrite du MINEPDED (Q-17).

La purification du gasoil (protocole n°1) porte sur un carburant en service, pas sur un déchet. Les eaux et boues retirées des cuves, elles, sont des déchets dangereux : elles suivent la filière du collecteur agréé. Certitude : probable.

## 2. Protocole n°1 : pilote commercial de 3 mois chez 2 clients forestiers

### 2.1 Objectif et critère de réussite

Mesurer, chez deux clients forestiers ou UTB, les volumes réels d'huiles usagées, le coût réel d'une tournée, le temps passé et le consentement à payer pour un contrat de conformité.

**Critère de réussite principal :** un contrat signé pour l'année suivante avec au moins un des deux clients.

**Critères secondaires (seuils de décision du chef de projet) :**

| Mesure | Seuil | Raison |
|---|---|---|
| Volume d'huiles usagées mesuré par client sur 3 mois | au moins 2 500 L, soit le quart de H-01 | sinon le gisement forestier par client est surestimé et le modèle forêt se dégrade |
| Coût réel d'une tournée sous-traitée | au plus la valeur haute de H-48 | sinon le coût par litre en forêt invalide la collecte forestière en propre |
| Prix accepté par le client pour l'année suivante | couvre le coût complet mesuré plus 20 % | marge minimale de travail, à confirmer au lot 9 |
| Incidents avec déversement | zéro | condition de crédibilité commerciale |

### 2.2 Sélection des deux clients

Critères : chantier accessible en saison sèche, atelier d'entretien sur place, cuve de gasoil d'au moins 10 000 L, accord de la direction pour communiquer les achats de lubrifiants des 12 derniers mois, accord écrit de HIKMA (Q-10). Les candidats sont pris dans la liste du promoteur [S-29].

### 2.3 Déroulé

| Semaine | Activité | Responsable | Formulaire |
|---|---|---|---|
| 0 | convention de pilote signée (prix forfaitaire, durée, données partagées) ; contrat de sous-traitance avec le collecteur agréé | promoteur | contrat (lot 15) |
| 1 | visite d'état initial : inventaire des fûts, du stockage, des engins, des achats de lubrifiants ; photos ; prélèvement d'échantillons (protocole n°2) | promoteur | `fiche_prospect.csv`, `chaine_tracabilite_echantillons.csv` |
| 1 | fourniture de fûts étiquetés et d'un kit antipollution, ouverture du registre | promoteur | registre (lot 15) |
| 2 à 12 | purification du gasoil et nettoyage de cuve, une intervention par mois et par client | promoteur et technicien | `pilote_purification_gasoil.csv` |
| 4, 8, 12 | enlèvement des huiles par le collecteur, présence du promoteur, pesée ou jaugeage, bordereau | collecteur, promoteur | `pilote_journal_tournee.csv` |
| tout au long | tout événement anormal | promoteur | `fiche_incident.csv` |
| 12 | rapport de pilote au client (volumes, coûts, conformité), proposition de contrat annuel | promoteur | rapport (lot 15) |
| 13 | décision du client | client | contrat |

### 2.4 Appareillage

| Besoin | Solution de référence | Alternative 1 | Alternative 2 | Choix pour le pilote |
|---|---|---|---|---|
| Purification du gasoil | Parker DFC14WS25VVX1 [S-28] | location d'une unité auprès d'un prestataire de nettoyage de cuves (à identifier, Q-16) | prestation complète sous-traitée à un prestataire de nettoyage de cuves | location ou achat d'une seule unité selon le devis (H-47) ; disponibilité des cartouches à vérifier avant tout engagement |
| Mesure des volumes enlevés | jaugeage des fûts et du camion du collecteur | pesée sur bascule du collecteur | comptage des fûts pleins | jaugeage croisé avec le bordereau du collecteur |
| Test d'eau dans le gasoil avant et après | pâte de détection d'eau sur jauge | test de crépitement sur plaque chauffante (qualitatif) | Karl Fischer en laboratoire | pâte de détection, plus 2 échantillons au laboratoire |
| Kit antipollution | achat sur commande (A3) | dépôt-vente fournisseur | fourniture par le client | achat sur commande payé par le client |

### 2.5 Budget et calendrier

Budget : voir `budget_protocoles.md`, protocole n°1. Une partie est refacturée aux clients par la convention de pilote : le prix forfaitaire est fixé après réception des devis H-47 et H-48. Calendrier : 13 semaines, à démarrer en saison sèche pour l'accès aux chantiers.

## 3. Protocole n°2 : campagne d'échantillonnage et d'analyse

### 3.1 Objectif et critère de réussite

Caractériser la qualité réelle des huiles en forêt et en ville, mesurer la fréquence des lots contaminés (chlore, PCB) et alimenter le bilan matière du lot 5.

**Critères de réussite :** 12 échantillons analysés avec chaîne de traçabilité complète (8 en forêt, 4 en ville, dans la fourchette de 10 à 15 du cahier des charges) ; résultats de laboratoire accrédité pour au moins 10 d'entre eux ; corrélation du dépistage Clor-D-Tect avec le chlore mesuré au laboratoire sur tous les échantillons dépistés positifs.

### 3.2 Plan d'échantillonnage

| Origine | Nombre | Points de prélèvement |
|---|---|---|
| Chantiers forestiers | 5 | fût de stockage d'atelier, carter d'engin à la vidange |
| UTB | 3 | fût de stockage, cuve de récupération |
| Garages et flottes de Douala | 2 | cuve ou fût de vidange |
| Garages et flottes de Yaoundé | 2 | cuve ou fût de vidange |

### 3.3 Mode opératoire de prélèvement

1. Port des EPI : gants nitrile, lunettes, vêtement à manches longues.
2. Identification du contenant, photo, coordonnées GPS.
3. Homogénéisation si possible (roulage du fût), sinon prélèvement sur toute la hauteur.
4. Prélèvement à l'échantillonneur COLIWASA ou à la canne de prélèvement de fût (référence Koehler K27400 [S-28]), selon les principes de la norme ASTM D4057 sur l'échantillonnage manuel des produits pétroliers (référence normative, contenu non relu dans cette mission).
5. Remplissage de deux flacons en verre ambré de 500 mL avec bouchon à joint PTFE : un pour le laboratoire, un conservé en réserve 6 mois.
6. Sur place : dépistage des halogènes au Clor-D-Tect 1000 (méthode ASTM D5384, seuil de réponse à 1 000 ppm de chlore [S-28]) et test qualitatif d'eau par crépitement.
7. Étiquetage, scellé numéroté, saisie dans `chaine_tracabilite_echantillons.csv`, signatures du producteur et du préleveur.
8. Conservation à l'abri de la lumière et de la chaleur, transport en caisse étanche avec absorbant.

### 3.4 Paramètres et méthodes de laboratoire

| Paramètre | Méthode de référence | Usage |
|---|---|---|
| Eau | ASTM D6304 (Karl Fischer) | rendement, déshydratation |
| Eau et sédiments | ASTM D4007 (centrifugation) | décantation |
| Point éclair en vase clos | ASTM D93 (Pensky-Martens) | sécurité, spécification du combustible |
| Viscosité à 40 °C | ASTM D445 | spécification, pompabilité |
| Masse volumique à 15 °C | ASTM D4052 ou D1298 | conversion litres et tonnes |
| Chlore total | méthode à préciser par le laboratoire | acceptation des lots, émissions |
| Soufre | ASTM D4294 | émissions de SO2 |
| Métaux (Pb, Zn, Cd, Cr, Ni, Cu) | ASTM D5185 (ICP) | émissions, cendres |
| PCB | méthode chromatographique à préciser par le laboratoire | acceptation des lots |

Les références de normes ASTM sont citées comme normes en vigueur, sans lecture de leur texte dans cette mission. Certitude : probable.

### 3.5 Choix entre achat, location et sous-traitance

| Appareil | Référence [S-28] | Alternative 1 | Alternative 2 | Choix pour la campagne |
|---|---|---|---|---|
| Prélèvement | COLIWASA et Koehler K27400 | canne jetable en polyéthylène | pompe manuelle à vide avec tube | achat de la canne Koehler et de cannes jetables (coût faible, H-45) |
| Dépistage halogènes | Dexsil Clor-D-Tect 1000, 22 USD l'unité [S-14], commande par 10 puis par 20 [S-15] | Dexsil Clor-D-Tect Q4000 (version quantitative, même fabricant) | sans dépistage, chlore au laboratoire pour tous | achat de 20 kits Clor-D-Tect 1000 ; le Clor-N-Oil est écarté car réservé aux huiles diélectriques [S-28] |
| Eau | Megger KF-LAB MkII ou Aquamax KF Portable [S-28] | test de crépitement (qualitatif, quasi gratuit) | Karl Fischer au laboratoire | sous-traitance au laboratoire ; test de crépitement sur place ; achat au-delà de 30 analyses par mois [S-28] |
| Point éclair | Pensky-Martens LMPFT-A102 [S-28] | appareil à petite échelle en vase clos (méthode ASTM D3828) | laboratoire | laboratoire pendant la campagne ; achat à la mise en service de l'unité |

### 3.6 Laboratoires

Aucun laboratoire accrédité n'est confirmé à ce stade pour l'analyse complète d'huile usagée au Cameroun. SGS Cameroun (Douala) propose des services d'analyse d'huile et d'hydrocarbures [S-12], sans précision sur le lieu d'analyse. Action : demande de devis à SGS Cameroun et à deux autres laboratoires (Q-05), en précisant l'accréditation ISO/CEI 17025 pour chaque paramètre, le délai et le lieu d'analyse. Si l'analyse part hors du pays, l'expédition d'échantillons de déchets dangereux exige un transitaire compétent et la vérification des formalités au titre de la convention de Bâle (Q-14).

### 3.7 Procédure d'acceptation et de refus des lots

Livrable associé : `procedure_acceptation_lots.md`.

### 3.8 Calendrier

Semaines 1 à 4 : devis et choix du laboratoire, achat des kits. Semaines 3 à 6 : prélèvements. Semaines 6 à 10 : résultats. Le protocole peut démarrer avant le pilote : il n'exige que l'accord des producteurs.

## 4. Protocole n°3 : essai de combustion chez un acheteur

### 4.1 Objectif et critère de réussite

Montrer qu'un industriel peut brûler le combustible sans dégrader son installation ni ses émissions par rapport à son combustible habituel.

**Critère de réussite :** lettre d'intention de l'acheteur avec un prix. Le seuil de prix retenu est 250 FCFA/L, valeur sous laquelle la VAN du premier business plan devient nulle [S-29]. Ce seuil sera recalculé par le modèle du lot 9.

### 4.2 Préalables

- acheteur identifié au lot 4, dont l'installation est techniquement apte (brûleur pour fioul ou combustible liquide, préchauffage si la viscosité l'exige) et légalement autorisée à brûler ce produit ;
- lot de 200 L fabriqué par un partenaire autorisé, ou autorisation d'essai du MINEPDED (Q-17) ;
- analyse complète du lot avant essai (protocole n°2) : un lot positif au dépistage halogènes ou contenant des PCB n'est jamais brûlé ;
- accord écrit de l'acheteur sur les conditions de sécurité et la responsabilité.

### 4.3 Mode opératoire

1. Mesure de référence : 2 heures de marche sur le combustible habituel, à charge stable.
2. Basculement sur le combustible d'essai (pur ou en mélange, selon l'accord de l'acheteur), 2 heures à la même charge.
3. Retour au combustible habituel, 1 heure.
4. Mesures toutes les 10 minutes : O2, CO, NOx, SO2, température des fumées ; observation de la flamme, de l'encrassement et de l'opacité.
5. Saisie dans `essai_combustion_mesures.csv`. Rapport signé de l'acheteur et du prestataire de mesure.

### 4.4 Appareillage

| Référence [S-28] | Alternative 1 | Alternative 2 | Choix |
|---|---|---|---|
| Testo 350, certifié MCERTS, jusqu'à 6 capteurs, location possible | analyseur portable 4 gaz de gamme inférieure (Testo 340 ou équivalent) | prestataire de mesure des émissions équipé et étalonné | prestataire ou location (H-46) ; certificat d'étalonnage de moins de 6 mois exigé (Q-15) |

### 4.5 Calendrier

Après les résultats du protocole n°2 et l'identification de l'acheteur au lot 4 : semaines 10 à 14.

## 5. Protocole n°4 : relevé des sanctions

### 5.1 Objectif et critère de réussite

Chiffrer les sanctions, mises en demeure et observations d'audit reçues par les clients sur trois ans au titre des huiles et des déchets dangereux. **Critère de réussite :** données obtenues auprès d'au moins 5 entreprises, dont au moins 3 avec des pièces justificatives.

### 5.2 Méthode

1. Lettre de demande d'accès aux données (`lettre_acces_sanctions.md`) adressée à la direction générale, avec engagement de confidentialité et d'anonymisation.
2. Entretien avec le responsable HSE ou environnement.
3. Saisie dans `releve_sanctions.csv`, une ligne par acte.
4. Croisement avec les textes visés : le montant légal maximal de chaque infraction est confronté au montant réellement payé. Les montants légaux des articles 80 à 82 de la loi n°96/12 restent à vérifier dans le texte officiel (Q-19).

### 5.3 Usage

Les résultats servent l'argumentaire commercial et la grille tarifaire du lot 15. Aucun nom de client n'apparaît dans un document commercial sans accord écrit.

### 5.4 Calendrier

Semaines 2 à 8, en parallèle de la prospection du lot 0.

## 6. Contre-expertise

**Rôle : contre-expert.**

Les trois hypothèses les plus fragiles :

1. **Un collecteur agréé accepte de monter en forêt au prix H-48 (Q-18).** Les collecteurs identifiés travaillent à Douala [S-06][S-07]. S'ils refusent ou facturent au-delà de la valeur haute, le pilote ne mesure pas un coût reproductible.
2. **Un laboratoire accrédité est accessible à un coût proche de H-43 (Q-05).** Si l'analyse des PCB et des métaux doit partir hors de la CEMAC, le coût et le délai doublent et la procédure d'acceptation devient lente.
3. **L'essai de combustion peut être autorisé (Q-17).** Si le MINEPDED exige le permis avant tout essai, la preuve n°3 glisse après l'obtention du permis, donc après l'investissement.

Scénario d'échec : le pilote montre un volume réel par client de l'ordre du tiers de H-01, et le dépistage révèle des huiles mélangées à des solvants chlorés dans plusieurs ateliers. La collecte forestière seule ne couvre pas ses coûts, et une part du gisement est inutilisable comme combustible.

**Ce que la synthèse change en conséquence.** Le protocole n°2 démarre avant le pilote, car il ne dépend d'aucun contrat. Les devis Q-05 et Q-18 sont demandés dès la semaine 1. Si Q-17 reçoit une réponse négative, l'essai n°3 est remplacé par une remise d'échantillons à l'acheteur pour analyse dans son propre laboratoire, et la lettre d'intention est demandée sous condition de résultat.

## 7. Points faibles du livrable

1. Tous les postes de budget sont des hypothèses : aucun devis n'a été obtenu, et le total central de 8,87 M FCFA peut varier du simple au triple (voir `budget_protocoles.md`).
2. Aucun laboratoire, loueur d'analyseur ou acheteur de combustible n'est encore confirmé au Cameroun.
3. Les références de normes ASTM sont citées sans lecture de leur texte, et le cadre réglementaire des essais et des échantillons repose sur des textes connus par extrait.
