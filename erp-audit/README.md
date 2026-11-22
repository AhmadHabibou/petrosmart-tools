# Audit ERP avant commercialisation

Banc d'audit HIKMA : un module a la fois, regard d'expert senior du domaine, tests mono-utilisateur puis multi-utilisateurs simultanes, fiche de cloture validee avant passage au module suivant.

## Regles

- instance de recette uniquement, jamais de production ni de donnees reelles ;
- compte administrateur dedie a l'audit (ex. `audit.hikma`), distinct des comptes personnels ;
- aucun identifiant dans le depot ni dans la conversation ;
- tout parametre reglementaire de `referentiels/` porte sa source et un statut (`a_valider` tant qu'un expert certifie ne l'a pas confirme) ;
- tests de securite seulement avec l'autorisation ecrite de l'editeur.

## Ordre des modules

| N | Module | Expert simule | Statut |
|---|---|---|---|
| 1 | Parametrage, utilisateurs et droits | auditeur SI | a demarrer |
| 2 | Comptabilite generale | expert-comptable SYSCOHADA | en attente |
| 3 | Ventes et facturation | responsable ADV | en attente |
| 4 | Achats | responsable achats | en attente |
| 5 | Stocks | responsable logistique | en attente |
| 6 | Tresorerie et banque | tresorier | en attente |
| 7 | Immobilisations | expert-comptable | en attente |
| 8 | Paie et RH | gestionnaire de paie senior | en attente |
| 9 | Etats financiers et fiscalite | expert-comptable et fiscaliste | en attente |

## Arborescence

- `referentiels/` : regles attendues (YAML, source et statut) ;
- `oracles/` : calculateurs independants de l'ERP ;
- `scenarios/` : cas metier par module ;
- `tests/e2e`, `tests/api` : pilotage de l'interface (Playwright) et des API ;
- `tests/concurrence` : sessions simultanees multi-profils ;
- `tests/invariants` : controles de coherence sur les donnees ;
- `tests/generatifs` : cas generes en masse (Hypothesis) ;
- `securite/` : Semgrep, scans, controle des droits ;
- `perf/` : montee en charge (k6) ;
- `rapport/` : registre des anomalies et fiches de cloture par module.

## Outils

Python : pytest, hypothesis, pyyaml, requests, python-docx, semgrep. Node : playwright (Chromium preinstalle). Binaire : k6.

## Configuration

Copier `config.example.yaml` en `config.yaml` (ignore par git) et renseigner l'adresse de recette. Les identifiants passent par les variables d'environnement `ERP_USER` et `ERP_PASSWORD`, jamais par un fichier.
