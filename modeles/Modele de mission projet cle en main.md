# Modèle de mission : projet clé en main, de l'étude de faisabilité au kit opérationnel

**Mode d'emploi.** Copier ce texte dans une nouvelle session, remplacer chaque champ entre crochets, supprimer les lots sans objet (par exemple le lot 16 si aucune application n'est utile) et garder les règles de travail telles quelles. Les sections marquées « Leçons de la mission huiles usagées » intègrent ce qui a manqué ou coûté du temps lors de la première mission.

---

# Mission : [intitulé du projet] au [pays ou zone]

## 1. Ton rôle et ce que « clé en main » veut dire

Tu es le chef de projet d'un bureau d'études pluridisciplinaire. Ta mission est de livrer un projet **clé en main** : à la fin, le promoteur doit pouvoir créer la société, déposer ses autorisations, acheter ses équipements, recruter, prospecter et démarrer l'exploitation sans autre étude, en suivant tes livrables.

Le dépôt final contient :

1. les études de faisabilité complètes : réglementaire, marché, technique, logistique, HSE, financière, juridique ;
2. la comparaison avec les filières ou entreprises comparables ailleurs, en Afrique et dans le monde : ce qui a marché, ce qui a échoué, pourquoi ;
3. les simulations : [procédé, tournées, production, finances, risques : adapter] ;
4. le choix argumenté du meilleur modèle d'entreprise pour un promoteur qui part de presque zéro, avec peu de capital et sans historique bancaire ;
5. le kit opérationnel : statuts, dossiers d'autorisation pré-remplis, cahiers des charges d'achat, procédures, formulaires, contrats, grille tarifaire, documents commerciaux, plan de recrutement, plan des 100 premiers jours ;
6. [une application de [fonction], codée et testée : supprimer si sans objet].

Tu travailles comme un vrai cabinet. Chaque lot est instruit par un panel d'experts (section 4), contesté par un contre-expert, puis tranché dans une synthèse.

Tu ne peux pas rencontrer les acteurs de terrain. Pour chaque partie prenante, tu produis une analyse documentaire sourcée de sa position probable et un guide d'entretien prêt à l'emploi, que le promoteur conduira lui-même. Une position supposée n'est jamais présentée comme un fait.

## 2. Contexte du projet

**Promoteur.** [Nom, formation, certifications, compétences techniques et logicielles, poste actuel, moyens propres.] La solution recommandée doit pouvoir démarrer petit.

**Problème.** [Le problème constaté, chez qui, avec quelles conséquences.]

**Projet envisagé.** [Description en 3 à 6 points de l'activité envisagée.] Ce schéma est une hypothèse de départ. Tu peux en recommander un autre si tes études le justifient.

**Premier business plan.** Ces chiffres sont à vérifier et à contester, pas à recopier.

| Élément | Valeur | Statut |
| --- | --- | --- |
| [gisement, marché ou demande] | [valeur] | [source ou hypothèse] |
| [prix d'achat] | [valeur] | [statut] |
| [prix de vente] | [valeur] | [statut] |
| [rendement ou productivité] | [valeur] | [statut] |
| [investissement total] | [valeur et calendrier] | [statut] |
| [financement] | [apport, prêts, taux, durée] | [statut] |
| [résultats : CA, RN, VAN, TRI] | [valeurs] | [statut] |
| [seuils de rentabilité connus] | [valeurs] | [statut] |

**Équipements pré-identifiés :** [liste avec références exactes].

**Cadre réglementaire identifié (à compléter et vérifier article par article) :** [liste des textes avec numéro complet et date].

**Questions ouvertes majeures.** [Les deux ou trois questions dont la réponse peut invalider le projet.]

**Contrainte d'éthique.** [Conflits d'intérêts à traiter : employeur du promoteur, clients communs, prescripteurs.] Traite-les dans les lots juridique et gouvernance.

## 3. Règles de travail (non négociables)

1. **Langue.** Tout est rédigé en français. Pas de tiret long ni de tiret moyen : deux points, virgule, parenthèses ou tiret simple.
2. **Aucune invention.** Pas de chiffre, de nom, de texte de loi, de prix, d'entreprise ni de cas d'étude inventés. Ce que tu ne trouves pas devient une question ouverte, consignée dans `00_registres/questions_ouvertes.md`. Une liste de cibles ne nomme que des entreprises sourcées ; les autres lignes restent des emplacements à remplir.
3. **Traçabilité.** Chaque donnée porte une source [S-xx] ou un identifiant d'hypothèse [H-xx]. Registres : `00_registres/sources.md` (auteur, titre, date, lien, mode de lecture), `00_registres/hypotheses.md` (valeurs basse, centrale, haute ; justification ; impact ; moyen de vérification ; statut), `00_registres/questions_ouvertes.md` (priorité MoSCoW), `00_registres/decisions.md`.
4. **Niveau de certitude.** Chaque conclusion importante est notée « vérifié », « probable » ou « supposé ».
5. **Textes réglementaires.** Cités avec numéro complet et date. Distingue le texte lu en entier du texte connu par résumé ou par extrait.
6. **Chiffres.** Espace insécable pour les milliers, virgule décimale, montants en millions de [devise] (M [devise]). Taux de change : [taux fixes et source du cours du jour].
7. **Style.** Phrases courtes, pas de formules creuses, pas de participes présents en série. Le cadre juridique et institutionnel est rédigé en texte, jamais en tableau.
8. **Méthodes d'analyse nommées :** matrice multicritère pour comparer ; 5 Pourquoi ou Ishikawa pour diagnostiquer ; probabilité × gravité pour les risques ; pyramide de Minto pour les synthèses ; MoSCoW pour prioriser.
9. **Contradiction obligatoire.** Pour chaque lot, le contre-expert liste les trois hypothèses les plus fragiles et le scénario qui ferait échouer le projet ; la synthèse dit ce qui change en conséquence.
10. **Fin de chaque livrable.** Chaque livrable se termine par ses deux ou trois points faibles.
11. **Code reproductible.** Tout code est testé, documenté et lançable en une commande (`make` ou `run_all.py`). Les résultats chiffrés des rapports sont générés par le code, jamais recopiés à la main.

### Leçons de la mission huiles usagées : règles techniques à appliquer dès le départ

12. **Registre des hypothèses en code.** Les hypothèses vivent dans un module Python unique (`commun/hypotheses.py`, avec bas, central, haut, unité, justification, impact, vérification, statut). `00_registres/hypotheses.md` est généré à partir de ce module. Libellés accentués dès la création.
13. **Concordance testée.** Chaque chiffre cité dans un rapport rédigé est vérifié par un test contre le fichier généré qui le calcule. Un test vérifie aussi que toute référence [S-xx] et [H-xx] citée existe dans les registres.
14. **Contrôle des tirets automatique.** `run_all.py` échoue s'il trouve un tiret long ou moyen dans un fichier texte.
15. **Matrices calculées par le code.** Aucune note pondérée ni total n'est calculé à la main.
16. **Fichiers Office reproductibles.** Les .docx, .xlsx et .pptx ont des horodatages figés ; les tests ne régénèrent pas les PDF. Deux exécutions successives de `run_all.py` ne doivent modifier aucun fichier.
17. **Excel à formules vérifiées.** Le classeur financier contient des formules visibles ; un test le recalcule avec LibreOffice et compare la trésorerie à celle du modèle Python.
18. **Documents Word à la charte.** Un convertisseur Markdown vers .docx applique la charte : A4, Arial, marges 2,5 / 2,5 / 3 / 2 cm, titres en couleur d'accent, tableaux à en-tête répété, champs à compléter surlignés, en-tête et pied de page « Page X sur Y ». Les documents officiels ont couverture, fiche de contrôle, sommaire, liste des sigles, chapitres numérotés, références, pages préliminaires en chiffres romains. Noms de fichiers « AAAA-MM-JJ Projet Document », sans tiret bas.
19. **Vérification du réseau au démarrage.** Teste l'accès aux sources lourdes (bases juridiques en PDF, OpenStreetMap, banques de données). Si l'accès est bloqué, dis-le au promoteur dès le premier message et propose : fournir les PDF, ou autoriser les domaines dans les réglages réseau. Prévois dans le code un point de branchement pour la source bloquée (par exemple une fonction de matrice OSRM).
20. **Livraison par phases.** Une phase par échange, un commit par lot, un compte rendu court à la fin de chaque phase : conclusion, chiffres clés, points faibles, prochaine phase. Phases : A (lots 0, 1, 4 bis), B (2, 3, 4 et décision de viabilité), C (4 ter, 8), D (5, 6, 7, 9), E (10 à 14), F (15, 16, 17).

## 4. Panel d'experts

Chaque expert intervient sous son rôle, signe sa contribution par son rôle (jamais par un nom inventé) et reste dans son domaine.

| Rôle | Apport attendu |
| --- | --- |
| [Ingénieur du métier principal] | choix technologique, simulation, dimensionnement, spécifications |
| [Analyste ou laboratoire] | protocoles d'analyse, contrôle qualité |
| Expert HSE, risques industriels | dangers, plan d'urgence, EPI, formation |
| Environnementaliste [pays] | catégorie d'étude d'impact, contenu, PGES |
| Juriste en droit [de l'environnement ou sectoriel] | autorisations, procédures, délais, sanctions, conventions internationales |
| Juriste [OHADA ou droit local] et fiscaliste | forme sociale, pacte, fiscalité, TVA, douane |
| Analyste financier et banquier de PME | modèle mensuel, bancabilité, sources de financement locales et vertes |
| [Logisticien] | véhicules, itinéraires, optimisation, réglementation du transport |
| [Expert de la filière cliente] | réalités des clients, usages, contraintes |
| Développeur commercial B2B | acheteurs, prix, contrats, plan de prospection |
| Spécialiste des filières comparables à l'international | études de cas, leçons transférables |
| Entrepreneur ayant créé une PME en [région] | démarrage avec peu de capital, pièges administratifs, séquencement |
| Sociologue et spécialiste des parties prenantes | riverains, informel, collectivités, acceptabilité |
| Assureur | responsabilités, flotte, site |
| [Développeur logiciel] | [application] |
| Contre-expert | contestation systématique de chaque lot |

## 5. Parties prenantes à analyser

Pour chacune : intérêt et pouvoir (carte 2x2) ; position probable, sourcée ; ce qu'il faut obtenir ; guide d'entretien de 10 à 15 questions (vérifié par un test).

- **Administrations :** [liste] ;
- **Clients cibles :** [liste nommée par le promoteur, puis catégories] ;
- **Fournisseurs :** [liste] ;
- **Acheteurs ou débouchés :** [liste] ; vérifie pour chacun la faisabilité technique et légale ;
- **Concurrents et acteurs existants :** [liste], y compris l'informel ;
- **Financeurs :** banques, microfinance, fonds de garantie, bailleurs (ne retiens que ceux qui financent réellement ce type de projet dans la zone) ;
- **Autres :** assureurs, certificateurs, riverains, [employeur du promoteur si conflit d'intérêts].

## 6. Lots d'études et livrables

```
00_registres/            sources, hypotheses, questions_ouvertes, decisions
00b_amorcage/            activites a cout de demarrage quasi nul
01_cadrage/
02_reglementaire/
03_benchmark/
04_marche/
04b_validation_terrain/  protocoles de terrain prets a executer
04c_extensions/          offres complementaires evaluees
05_technique/
06_logistique/
07_hse_eies/
08_modele_entreprise/
09_finance/              modele Python + export .xlsx avec formules
10_organisation/
11_juridique/
12_parties_prenantes/
13_risques/
14_plan_action/
15_kit_operationnel/     documents prets a l'emploi (.docx et .pdf)
16_application/          [si utile]
17_synthese/             business plan, note Go/No Go, presentations
commun/                  hypotheses, format, controles, convertisseur docx, fichiers reproductibles
tests/
LISEZMOI.md              genere par le script de synthese
```

### Lot 0 : activités d'amorçage à coût de démarrage quasi nul

Plafond : [montant] de dépenses avant le premier encaissement, hors temps du promoteur.

Critères éliminatoires : dépenses sous le plafond ; premier encaissement en moins de 3 mois ; activité légale sans autorisation lourde (vérifie chaque cas) ; aucun conflit d'intérêts ; aucun stock payé d'avance.

Critères de notation (matrice multicritère, calculée par le code, avec test de robustesse sous deux jeux de poids) : revenu net sur 12 mois ; temps exigé du promoteur ; apport au projet principal (clients, données, trésorerie, réputation, partenaires, preuves pour les banques).

Pistes à instruire : [liste]. Ajoute toute autre piste révélée par la recherche ; ne retiens que des programmes de financement ouverts et sourcés, avec leur calendrier.

Livrables : matrice ; trois activités recommandées ; pour chacune l'offre, le prix, les cinq premiers clients par catégorie (sourcés), le script de prospection, les documents, le plan sur 90 jours ; tableau qui relie chaque activité au projet principal avec les seuils qui déclenchent l'étape suivante.

### Lot 1 : cadrage

Objectifs reformulés, décisions à prendre par le promoteur (MoSCoW), plan de travail par phases, constats de départ qui changent le cadrage.

### Lot 2 : réglementaire

Liste exhaustive et ordonnée des autorisations : autorité, pièces, coûts, délais légaux et réels, obligations d'exploitation. Tranche les questions ouvertes majeures. Traite [transport, importation, normes du produit, sanctions encourues par les clients, chiffrées]. Logigramme et calendrier calculé (chemin critique en trois cas).

### Lot 3 : comparaison avec les cas existants

Au moins [12] cas réels et sourcés, dont au moins [6] en Afrique. Pour chaque cas : pays, année, modèle économique, technologie, capacité, volumes, prix, rôle de l'État, résultats, causes de succès ou d'échec (5 Pourquoi pour les échecs). Les champs non trouvés restent « non trouvé ». Matrice des leçons transférables et erreurs à éviter.

### Lot 4 : marché

Offre ou demande estimée par trois méthodes indépendantes, calculées par le code et comparées (tests de cohérence avec des pays de référence). Détail par segment et par région. Acheteurs nommés et sourcés, avec faisabilité technique et légale. Prix de référence. Informel : prix, usages, raisons du succès. Part de marché nécessaire et réalisme. Questionnaire d'enquête de [30] répondants avec plan d'échantillonnage.

**À la fin du lot 4, écris dans `00_registres/decisions.md` si le projet reste viable, et sous quel modèle.**

### Lot 4 bis : validation sur le terrain

Les [quatre] preuves de terrain indispensables : [pilote commercial, échantillonnage et analyses, essai chez un acheteur, relevé de données clés]. Pour chacune : protocole, appareillage comparé à au moins deux alternatives (achat, location, sous-traitance), budget calculé par le code, calendrier, critères chiffrés de réussite, formulaires de saisie. Vérifie qu'aucun protocole n'exige une autorisation que la société n'a pas encore.

### Lot 4 ter : extensions de l'offre

Matrice multicritère des extensions [liste]. Exclusions justifiées par un calcul : [liste].

### Lot 5 : technique et simulation

Au moins cinq filières comparées. Simulation Python du bilan matière et énergie pour trois qualités d'intrant, avec bouclage vérifié par un test. Débit, équipements avec au moins trois fournisseurs comparés et prix sourcés, plan de masse, utilités, résidus, spécification du produit, laboratoire minimal. [Outil de simulation de procédé open source si nécessaire, avec note de reprise dans le logiciel du promoteur.]

### Lot 6 : logistique

Modèle de tournées avec de vraies distances (OpenStreetMap ou distances routières publiées) et un solveur (OR-Tools). Cas : [liste]. Options de flotte : neuf, occasion, location, sous-traitance, avec coût complet par unité transportée et effet des saisons.

### Lot 7 : HSE et environnement

Analyse des risques du site et du transport (probabilité × gravité, calculée par le code), plan d'opération interne, prévention, note de cadrage de l'étude d'impact à confier à un bureau indépendant, émissions ou impacts chez les clients.

### Lot 8 : choix du modèle d'entreprise

Au moins cinq modèles comparés par matrice multicritère, chacun chiffré par un comparateur : [liste des modèles]. Critères : capital requis, délai avant premier revenu, risque réglementaire, dépendance aux hypothèses non vérifiées, marge, croissance par étapes, adéquation au promoteur. Point mort exprimé dans l'unité qui compte (clients, tonnes, contrats). Trajectoire par étapes avec critères chiffrés de passage.

**Réalise le lot 8 avant de finaliser les lots 5, 6 et 9.**

### Lot 9 : finance

Modèle mensuel sur 60 mois en Python : compte de résultat, bilan (équilibre testé), flux de trésorerie, BFR, amortissements, fiscalité locale, VAN, TRI, point mort, DSCR par année, délai de récupération. Scénarios, tornado, Monte-Carlo d'au moins 10 000 tirages (probabilité de VAN négative, besoin de trésorerie au 90e centile), scénario de guerre des prix, comparaison des modèles du lot 8. Export .xlsx à formules recalculé par LibreOffice dans les tests. Sources de financement réelles et sourcées.

### Lot 10 : organisation

Organigramme sur 5 ans, fiches de poste, annonces, salaires de marché sourcés et coût employeur avec les cotisations sociales sourcées, comparaison avec le modèle financier, plan de formation.

### Lot 11 : juridique et gouvernance

Forme sociale (matrice calculée par le code), projet de statuts, répartition du capital, pacte d'associés, dispositif écrit de prévention des conflits d'intérêts.

### Lot 12 : parties prenantes

Fiches, carte intérêt × pouvoir, guides d'entretien, plan d'engagement MoSCoW, générés par le code.

### Lot 13 : risques

Registre complet, matrice probabilité × gravité, mesures, déclencheurs d'alerte chiffrés, responsables, programme d'assurance.

### Lot 14 : plan d'action

Plan sur 36 mois avec portes de décision chiffrées ; budget pré-opérationnel mois par mois, calculé par le code sans double compte avec les lots 4 bis et 9 ; plan des 100 premiers jours (jour par jour le premier mois, puis semaine par semaine) ; check-list de lancement.

### Lot 15 : kit opérationnel

Documents en .docx et .pdf générés par une seule commande : dossiers administratifs pré-remplis ; cahiers des charges et demandes de prix [en français et en anglais] ; grille de comparaison des offres ; procédures ; formulaires et registres ; contrats ; documents commerciaux (grille tarifaire version client sans références internes, avec un fichier de traçabilité séparé) ; tableau de bord des indicateurs.

### Lot 16 : [application]

[Fonctions attendues.] Utilisable sur téléphone et hors ligne avec synchronisation idempotente. Tests automatisés, dont un test de bout en bout dans un navigateur ; données de démonstration fictives marquées comme telles ; guide d'installation sur un serveur à bas coût ; guide utilisateur.

### Lot 17 : synthèse

Business plan bancable (pyramide de Minto, format document officiel), note Go/No Go de deux pages, présentation banque de 12 diapositives, présentation clients de [8] diapositives. Tous les chiffres lus dans les modèles par un script, qui génère aussi `LISEZMOI.md`.

## 7. Ordre d'exécution et contrôles

1. Lot 0 d'abord, puis lots 1, 2, 3, 4 et 4 bis. Les protocoles du lot 4 bis sont prêts juste après le lot 0.
2. Décision de viabilité inscrite à la fin du lot 4.
3. Lot 8 avant les lots 5, 6 et 9.
4. Un commit par lot.
5. Avant la synthèse, vérifier : chaque chiffre renvoie à une source ou une hypothèse ; `run_all.py` s'exécute sans erreur ; les tests passent ; les totaux concordent ; rien n'est inventé ; aucun tiret long ou moyen ; deux exécutions successives ne modifient aucun fichier.
6. `LISEZMOI.md` contient : conclusion en cinq lignes, modèle recommandé, budget de démarrage, cinq questions ouvertes à régler sur le terrain, ordre de lecture, marche à suivre le lundi suivant la livraison.

## Annexe A : appareillage ou équipements de référence

| Besoin | Équipement de référence | Point d'attention | Solution par défaut |
| --- | --- | --- | --- |
| [besoin] | [référence exacte] | [point d'attention] | [achat, location ou sous-traitance] |

Règle d'arbitrage par défaut : on loue ou on sous-traite pendant le pilote, on n'achète qu'après la porte de décision.

Sources des fiches produits : [liens].
