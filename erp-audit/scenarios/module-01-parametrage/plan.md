# Module 1 : parametrage, utilisateurs et droits

Expert simule : auditeur des systemes d'information senior.

## Cartographie
- societe, exercice, devise, plan comptable charge ;
- roles et profils disponibles, granularite des droits (module, ecran, action, champ) ;
- politique de mot de passe, double authentification, expiration de session ;
- journal d'audit : contenu, horodatage, modifiable ou non.

## Tests mono-utilisateur
- creation des 8 comptes de test (config.example.yaml) ;
- chaque profil tente une action hors de ses droits (acces direct par URL, API, bouton masque) ;
- separation des taches : un meme compte peut-il saisir et valider, creer un fournisseur et le payer ;
- modification de ses propres droits par un utilisateur non administrateur ;
- desactivation d'un compte : la session ouverte est-elle coupee.

## Tests simultanes
- deux administrateurs modifient le meme role au meme instant ;
- retrait d'un droit pendant qu'un utilisateur l'exerce ;
- meme compte connecte depuis plusieurs postes ;
- rafale de tentatives de connexion erronees : verrouillage du compte.

## Cloture
Fiche `rapport/modules/module-01.md` : anomalies, verdict, validation par le directeur de mission.
