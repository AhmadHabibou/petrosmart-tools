# Formulaires de terrain : import dans KoboToolbox

Les classeurs de ce dossier sont générés par `04b_validation_terrain/construire_formulaires_kobo.py` au format XLSForm, et validés par pyxform à chaque génération.

## Contenu

| Classeur | Usage |
|---|---|
| `enquete_garages.xlsx` | enquête des 30 garages et flottes (lot 4), questions 1 à 20 et observations, avec position GPS et photo |
| `fiche_prospect.xlsx` | prospection commerciale |
| `pilote_journal_tournee.xlsx` | journal des tournées d'enlèvement du pilote |
| `pilote_purification_gasoil.xlsx` | interventions de purification du gasoil, avec signature du client |
| `chaine_tracabilite_echantillons.xlsx` | prélèvement et chaîne de traçabilité des échantillons, avec signatures |
| `resultats_analyses.xlsx` | saisie des résultats de laboratoire et décision d'acceptation des lots |
| `fiche_incident.xlsx` | incidents HSE |
| `releve_sanctions.xlsx` | relevé des sanctions des exploitants |
| `essai_combustion_mesures.xlsx` | mesures d'essai de combustion (étape 4 seulement) |

## Mise en service

1. Créer un compte sur le serveur KoboToolbox choisi (serveur mondial ou serveur européen).
2. Pour chaque classeur : nouveau projet, importer un XLSForm, puis déployer.
3. Sur les téléphones : installer KoboCollect (ou ODK Collect), se connecter au serveur, télécharger les formulaires. La saisie fonctionne sans réseau ; les fiches partent à la reconnexion.
4. Exporter les données en CSV : les noms de colonnes sont ceux des fiches de `formulaires/`, sans les listes de choix entre parenthèses.

## À ajuster avant le terrain

- tous les champs sont obligatoires, sauf les notes, les photos, les positions et les questions conditionnelles : rendre facultatifs ceux qui bloqueraient la saisie ;
- vérifier les listes de choix de l'enquête des garages avec l'enquêteur après deux entretiens tests ;
- les conditions d'usage et les limites du compte gratuit KoboToolbox sont à vérifier sur le site de KoboToolbox.
