# Guide utilisateur de l'application de traçabilité

## 1. Premier lancement

1. Ouvrir l'adresse de l'application dans le navigateur du téléphone (Chrome recommandé).
2. Menu du navigateur : « Ajouter à l'écran d'accueil ». L'application s'ouvre ensuite comme une application installée.
3. Onglet **Réglages** : saisir le jeton d'accès remis par le gérant, puis « Enregistrer le jeton ».

## 2. Travailler sans réseau

- Le bandeau indique « en ligne » ou « hors ligne ».
- Hors ligne, toutes les saisies sont enregistrées sur le téléphone. Le pied de page affiche le nombre de saisies en attente.
- Au retour du réseau, la synchronisation est automatique ; le bouton **Synchroniser** la force.
- Une saisie refusée par le serveur (par exemple un enlèvement sans dépistage) est signalée par un message : la corriger et la saisir de nouveau.
- Ne pas vider les données du navigateur tant que des saisies sont en attente.

## 3. Modules

| Onglet | Usage |
|---|---|
| Tableau de bord | clients, sites, fûts chez les clients, enlèvements, volume enlevé, stock, taux de lots refusés |
| Clients et sites | créer un client, ses sites (coordonnées GPS, distance de piste) ; télécharger le rapport annuel PDF d'un client |
| Fûts | enregistrer un fût et son site ; afficher et imprimer son QR code pour l'étiquette |
| Enlèvements | planifier ; réaliser (volume, dépistage, date) ; télécharger le bordereau PDF |
| Stock et lots | saisir les résultats de laboratoire ; voir le stock par lot |
| Ventes | réservé à l'étape 4, après réponse du MINEPDED sur le statut du combustible |

## 4. Règles intégrées

- Un enlèvement ne peut pas être validé sans résultat de dépistage des halogènes.
- Un dépistage positif place le lot en quarantaine.
- Une analyse avec 1 000 ppm de chlore ou plus, ou des PCB détectés, refuse le lot.
- Seul un lot accepté peut être vendu, et jamais au-delà du stock.
- Chaque enlèvement réalisé reçoit un numéro de bordereau (BSD-année-numéro) et crée un lot (LOT-année-numéro).

## 5. Rapport annuel client

Onglet **Clients et sites**, colonne « Rapport annuel » : PDF de l'année en cours avec la liste des enlèvements, volumes et bordereaux. C'est un rapport d'activité factuel, pas un audit.

## 6. En cas de problème

- Saisies bloquées en attente : vérifier le jeton dans **Réglages**, puis appuyer sur **Synchroniser**.
- Téléphone perdu : demander au gérant de changer le jeton sur le serveur.
