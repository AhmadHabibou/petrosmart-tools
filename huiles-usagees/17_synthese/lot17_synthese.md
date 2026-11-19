# Lot 17 : synthèse

Méthode : pyramide de Minto. Tous les chiffres de la synthèse sont lus dans les modèles et fichiers générés par `construire_synthese.py` ; aucun n'est recopié à la main.

## Livrables

| Livrable | Fichier source | Versions |
|---|---|---|
| Business plan de synthèse (scénario de base avec emprunt ; pour la banque, le business plan bancaire le remplace) | `business_plan.md` | `livrables/` en .docx et .pdf |
| Document de projet institutionnel (trame des documents de projet présentés aux administrations : fiche signalétique, contexte, marché, impacts, technique, finances, cadre réglementaire, appui attendu) | `bp_institutionnel.md`, généré par `construire_business_plans.py` | `livrables/` en .docx et .pdf |
| Business plan bancaire (demande chiffrée, structure en crédit-bail et fonds propres, comptes, ratios de couverture, Monte-Carlo sur la structure demandée, garanties, conditions de décaissement) | `bp_banque.md`, généré par `construire_business_plans.py` | `livrables/` en .docx et .pdf |
| Dossier technique des équipements (annexe des deux business plans : principes de fonctionnement avec trois schémas, fiches E1 à E7, matériel de terrain, exigences HSE, plan d'acquisition) | `05_technique/dossier_equipements.md`, généré par `05_technique/construire_dossier_equipements.py` | `livrables/` en .docx et .pdf |
| Note Go/No Go (deux pages) | `note_go_no_go.md` | `livrables/` en .docx et .pdf |
| Présentation pour une banque (12 diapositives, même structure de financement que le business plan bancaire) | généré par `construire_business_plans.py` | `livrables/` en .pptx et .pdf |
| Présentation pour les clients forestiers (8 diapositives) | généré par le script | `livrables/` en .pptx et .pdf |
| LISEZMOI du dépôt | généré par le script | `LISEZMOI.md` |

## Contrôles avant livraison

| Contrôle | Résultat | Moyen |
|---|---|---|
| Chaque chiffre de la synthèse renvoie à une source ou une hypothèse | oui : chiffres lus dans les modèles ; toute référence [S-xx] ou [H-xx] existe dans les registres | test `test_sources_citees_existent`, `test_hypotheses_citees_existent`, `test_synthese_concordante` |
| `run_all.py` régénère toutes les simulations sans erreur | oui | `python3 run_all.py` |
| Les tests de l'application passent | oui, 12 tests dont un test navigateur | `make test` |
| Les totaux concordent entre les fichiers | oui sur les chiffres cités dans les rapports rédigés | tests `test_chiffres_lot*` |
| Aucune entreprise, personne, référence ou étude de cas inventée | les entreprises nommées viennent des sources du registre ou du cahier des charges ; les données de démonstration de l'application portent le préfixe « DEMO » et la mention « fictif » | revue manuelle, test `test_donnees_de_demonstration_marquees_fictives` |
| Aucun tiret long ni moyen | oui | contrôle automatique de `run_all.py` et test `test_aucun_tiret_long` |
| Note Go/No Go de deux pages, présentations de 12 et 8 diapositives | oui | test `test_synthese_formats` |

## Contre-expertise de la synthèse

**Rôle : contre-expert.**

1. **Hypothèse fragile : le prix du contrat (H-80).** Toute la valeur de la recommandation en dépend ; il n'a pas été mesuré.
2. **Hypothèse fragile : la lecture réglementaire.** La recommandation de démarrer sans permis repose sur une lecture d'extraits ; une réponse écrite du MINEPDED peut la remettre en cause.
3. **Hypothèse fragile : la neutralité de HIKMA.** Le premier cercle de clients est celui de HIKMA ; sans charte signée, la cible principale disparaît.

Scénario d'échec de l'ensemble : HIKMA refuse la charte, le MINEPDED exige un permis pour le service de conformité, et le pilote se heurte à un prix accepté de moitié inférieur à H-80. Dans ce cas, la note Go/No Go conduit au No Go dès la porte 1, avec des pertes limitées au budget d'amorçage et aux protocoles de terrain engagés.

**Ce que la synthèse change en conséquence.** La décision est un Go conditionnel et non un Go ferme ; les trois points ci-dessus sont des conditions de la porte 1.

## Points faibles de la synthèse

1. Les chiffres sont générés à partir d'hypothèses supposées pour l'essentiel : ils montrent la cohérence du modèle, pas sa validation.
2. Les présentations sont sobres et sans visuels de terrain ; elles devront être enrichies de photos et de résultats du pilote.
3. La note Go/No Go ne chiffre pas le coût d'un No Go à chaque porte.
