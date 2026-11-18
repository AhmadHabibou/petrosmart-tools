# Lot 16 : application de traçabilité

**Rôles mobilisés :** développeur logiciel, chimiste analyste (règles d'acceptation), expert HSE, contre-expert.

## 1. Conclusion

L'application est fonctionnelle et testée : 12 tests automatisés, dont un test de bout en bout dans Chromium qui saisit un client hors ligne et vérifie sa synchronisation au retour du réseau. Elle couvre les neuf modules demandés et applique les règles de la procédure d'acceptation des lots. Elle tourne sur un serveur virtuel d'entrée de gamme avec une base SQLite.

## 2. Architecture

- **Serveur :** Python, Flask, SQLite (`tracabilite/`) ; API JSON protégée par jeton ; PDF générés par ReportLab ; QR codes par segno.
- **Interface :** page web unique pour téléphone (`tracabilite/static/`), installable sur l'écran d'accueil ; service worker pour le fonctionnement hors ligne ; file d'attente locale des saisies, rejouée par `/api/sync`.
- **Synchronisation :** chaque saisie porte un identifiant unique créé sur le téléphone ; le serveur ignore une opération déjà reçue. Rejouer la file deux fois ne crée donc aucun doublon (test `test_synchronisation_hors_ligne_idempotente`).

## 3. Couverture des modules

| Module demandé | Réalisation |
|---|---|
| Clients et sites | onglet Clients et sites ; coordonnées GPS et distance de piste |
| Fûts identifiés par QR code | onglet Fûts ; `/api/futs/<id>/qr.svg` |
| Planification et suivi des enlèvements | onglet Enlèvements ; statuts planifié et réalisé |
| Bordereaux PDF | `/api/enlevements/<id>/bordereau.pdf`, numérotation BSD-année-numéro |
| Stocks au centre de transit | mouvements d'entrée et de sortie par lot ; `/api/stock` |
| Lots, analyses et traitement | lot créé à chaque enlèvement ; décision automatique à l'analyse ; table des traitements |
| Ventes de combustible | onglet Ventes, limité aux lots acceptés et au stock |
| Rapport annuel par client | `/api/clients/<id>/rapport/<année>.pdf` |
| Tableau de bord | onglet Tableau de bord ; `/api/tableau_de_bord` |

## 4. Lancer, tester, démontrer

```bash
cd huiles-usagees/16_application
pip install -r requirements.txt
python -m pytest -q tests        # 12 tests
python demo.py demo.sqlite       # base de démonstration aux données fictives
TRACABILITE_BASE=demo.sqlite python wsgi.py   # http://127.0.0.1:8000
```

Guides : `GUIDE_INSTALLATION.md` (serveur virtuel, HTTPS, sauvegardes) et `GUIDE_UTILISATEUR.md`.

## 5. Contre-expertise

**Rôle : contre-expert.**

1. **Sécurité par jeton unique.** Tous les utilisateurs partagent un jeton ; un téléphone perdu impose de le changer pour tous. Des comptes individuels seront nécessaires au-delà de trois ou quatre utilisateurs.
2. **Stockage local du navigateur.** Si l'utilisateur vide les données du navigateur avant la synchronisation, les saisies en attente sont perdues.
3. **Conformité du bordereau.** Le bordereau PDF suit le modèle du kit (F1), pas un modèle officiel, qui n'a pas été trouvé.

**Ce que la synthèse change en conséquence.** Comptes individuels et journal des modifications au programme de l'année 2. Consigne écrite de synchronisation quotidienne dans le guide utilisateur. Bordereau aligné sur le modèle officiel dès sa réception (Q-01).

## 6. Points faibles

1. Pas de gestion des droits par rôle ni de journal d'audit des modifications.
2. L'abonnement de l'application à des tiers (piste A6 du lot 0) supposerait une base par client et une facturation : non développés.
3. Les traitements (étape 4) sont enregistrables par l'API mais n'ont pas d'écran dédié.
