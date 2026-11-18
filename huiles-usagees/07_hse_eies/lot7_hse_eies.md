# Lot 7 : HSE et environnement

Méthodes : matrice probabilité × gravité (`matrice_risques_hse.md`, générée par le code), borne haute par bilan matière pour les émissions (`emissions.md`), pyramide de Minto pour la conclusion.

**Rôles mobilisés :** expert HSE et risques industriels, environnementaliste EIES Cameroun, chimiste analyste, contre-expert.

## 1. Conclusion

Aux étapes 1 et 2, les risques majeurs de la société sont routiers et liés aux interventions chez le client : déversement en transport, lot contaminé, nettoyage de cuve en espace confiné. Douze risques sont analysés : onze sont à réduire avant mesures, un seul le reste après mesures, le déversement en transport routier (criticité 8). Ce risque justifie la sous-traitance du transport jusqu'à l'étape 3 et une assurance de responsabilité environnementale dès le premier contrat (lot 13). Certitude : supposé, notes à réévaluer après le pilote.

Pour la combustion du produit chez les clients (étape 4), le risque principal tient aux métaux, au chlore et aux PCB contenus dans l'huile, que le prétraitement F2 ne retire pas. Une borne haute d'émission est calculable dès les premières analyses, sans hypothèse sur l'installation de l'acheteur.

## 2. Analyse des risques du site et du transport

Le registre et la matrice sont dans `matrice_risques_hse.md`. Points saillants :

- **Transport (R01, R02).** Les tournées forestières durent environ une semaine, dont une partie sur piste (lot 6). Le renversement d'une citerne de 13 390 L en forêt est l'accident le plus grave plausible. Mesures : chauffeur formé, interdiction de conduite de nuit sur piste, suivi GPS (obligatoire selon [S-38]), kit antipollution, procédure d'alerte.
- **Lot contaminé (R04).** Un seul fût de solvant chloré ou d'huile de transformateur contamine une citerne entière. Mesure : dépistage systématique avant pompage (procédure d'acceptation du lot 4 bis).
- **Nettoyage de cuve (R06).** C'est le risque de gravité maximale pour le personnel. Mesure : nettoyage depuis l'extérieur par pompage et filtration ; entrée en cuve interdite sans permis, détection de gaz, ventilation et surveillant.
- **Centre de transit (R07, R08, étape 3).** Incendie de cuvette et pollution des sols. Les mesures sont à dimensionner par l'étude de dangers exigée pour l'établissement classé (lot 2).

## 3. Plan d'opération interne (étape 3, centre de transit)

Le plan d'opération interne sera finalisé avec l'étude de dangers. Sa structure :

1. **Objet et champ :** scénarios d'incendie de cuvette, de déversement en réception, de fuite de cuve et d'accident de transport à proximité du site.
2. **Organisation :** directeur des opérations internes (gérant), responsable d'intervention (chef de site), équipiers formés, liste d'astreinte.
3. **Alerte :** numéros des sapeurs-pompiers, de la délégation régionale du MINEPDED, de la commune et de l'assureur ; message d'alerte type.
4. **Fiches réflexes par scénario :** actions dans les 5, 15 et 60 premières minutes.
5. **Moyens :** extincteurs, émulseur, absorbants, obturateurs, pompes de reprise, équipements de protection.
6. **Fin d'alerte et retour d'expérience :** fiche d'incident (lot 4 bis), analyse des causes, mesures correctives.
7. **Exercices :** au moins un exercice par an, dont un avec les secours extérieurs.

Pour les interventions chez les clients (étapes 1 et 2), une version simplifiée est intégrée à la procédure « intervention en cas de déversement » du lot 15.

## 4. Mesures de prévention transverses

- **EPI :** gants nitrile, lunettes, vêtements à manches longues, chaussures de sécurité, protection respiratoire pour le nettoyage de cuve.
- **Formation :** risques des huiles usagées et des hydrocarbures, transport de matières dangereuses, espace confiné, premiers secours, lutte contre le feu ; certification NEBOSH IGC du promoteur comme référence du système.
- **Hygiène :** lavage des mains, vestiaire, interdiction de manger sur le poste, suivi médical du personnel exposé.
- **Matériel :** liaison équipotentielle au pompage, flexibles contrôlés, rétention sous les raccords.
- **Traçabilité :** bordereau et registre (lot 15), fûts identifiés par QR code (lot 16).

## 5. Note de cadrage de l'évaluation environnementale

**À confier à un bureau d'études agréé autre que HIKMA**, en application de la contrainte d'éthique (lot 11).

**Objet.** Évaluation environnementale du centre de transit (étape 3) et, le cas échéant, de l'unité de prétraitement (étape 4), au titre du décret n°2013/0171/PM du 14 février 2013 [S-33].

**Catégorie.** À faire confirmer par écrit par le MINEPDED au regard de l'arrêté n°00001/MINEPDED du 8 février 2016 [S-34] (Q-23) : notice d'impact environnemental pour un centre de transit, étude d'impact sommaire ou détaillée pour une unité de traitement. Si une notice suffit, son contenu suit l'arrêté n°0002/MINEPDED du 9 février 2016 [S-42].

**Contenu attendu :**

- description du projet, avec les bilans de `05_technique/bilan_procede.md` ;
- état initial : sol, eaux souterraines et de surface, air, bruit, riverains, usages du site ;
- analyse des variantes : remise à un valorisateur, prétraitement, choix du site ;
- impacts : déversements, émissions de COV et d'odeurs au dépotage et à la déshydratation, eaux huileuses, boues, trafic de camions, risques d'accident ;
- émissions indirectes chez les acheteurs du combustible (section 6) ;
- consultation des riverains et de la commune ;
- plan de gestion environnementale et sociale : mesures, indicateurs, responsables, coûts, calendrier de surveillance.

**Données fournies par la société :** résultats des protocoles 4 bis, procédures du lot 15, registre des risques du présent lot.

**Livrable et calendrier :** termes de référence soumis au MINEPDED, puis rapport ; délai réaliste de 3 à 12 mois selon la catégorie (H-71, `02_reglementaire/calendrier.md`).

## 6. Émissions lors de la combustion du produit chez les clients

**Polluants à considérer.**

- **Métaux** (plomb, zinc, cadmium, chrome, nickel, cuivre) issus des additifs, de l'usure des moteurs et, pour le plomb, d'anciennes essences : ils ne sont ni retirés par la déshydratation, ni détruits par la combustion.
- **Chlore**, qui forme de l'acide chlorhydrique et favorise la formation de dioxines et furannes en combustion mal maîtrisée.
- **PCB**, interdits dans le produit (procédure d'acceptation).
- **Soufre** (SO2), **oxydes d'azote**, **monoxyde de carbone**, **particules** et **hydrocarbures aromatiques polycycliques**, qui dépendent de la qualité de la combustion.

**Référence.** L'EPA traite la combustion des huiles usagées dans la section 1.11 de l'AP-42 : le plomb émis y est exprimé en proportion de la teneur en plomb du combustible, et l'acide chlorhydrique fait l'objet d'un tableau propre [S-77]. Les valeurs numériques n'ont pas pu être lues : elles sont à intégrer quand le document sera accessible.

**Méthode retenue.** Borne haute par bilan matière (`emissions.md`) : tout le métal contenu dans le combustible est supposé émis. Pour 100 000 L brûlés, chaque tranche de 100 mg/kg de métal dans le combustible correspond au plus à 9 kg émis. La borne est ensuite affinée par la mesure à la cheminée lors de l'essai de combustion (protocole 4 bis n°3).

**Conséquence commerciale.** Le combustible ne peut être vendu qu'à des installations à combustion maîtrisée (fours, chaudières industrielles avec réglage de l'excès d'air), jamais à des usages domestiques ou artisanaux. Le contrat de vente transfère à l'acheteur la responsabilité de ses propres émissions, sans dispenser la société de déclarer les teneurs de chaque lot.

## 7. Contre-expertise

**Rôle : contre-expert.**

1. **Hypothèse fragile : les notes de probabilité.** Elles sont attribuées sans historique d'accidents ; le pilote doit les recaler.
2. **Hypothèse fragile : le collecteur sous-traitant applique les mêmes règles.** Si son chauffeur verse les huiles en route, c'est la réputation de la société qui est atteinte, et peut-être sa responsabilité.
3. **Hypothèse fragile : les teneurs en métaux sont faibles.** Des huiles moteur de parcs anciens peuvent porter des teneurs élevées, et rendre le produit invendable comme combustible.

Scénario d'échec : un déversement d'une citerne sous-traitée dans un cours d'eau proche d'un village forestier. Le client forestier, la société et le collecteur sont mis en cause ; le contrat de conformité est perdu et la réputation atteinte au moment où la société cherche ses premiers clients.

**Ce que la synthèse change en conséquence.** Le contrat de sous-traitance (lot 15) impose au collecteur des exigences HSE écrites, un suivi GPS partagé, une assurance et un droit d'audit. La société souscrit sa propre assurance de responsabilité civile environnementale avant le premier enlèvement (lot 13).

## 8. Points faibles du livrable

1. Les notes de probabilité et de gravité ne reposent sur aucune donnée d'accident locale.
2. Les facteurs d'émission de l'AP-42 n'ont pas pu être lus ; seule une borne haute est proposée.
3. Le plan d'opération interne et l'étude de dangers restent à finaliser sur un site réel.
