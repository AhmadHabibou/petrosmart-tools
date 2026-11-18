# Guide d'installation de l'application de traçabilité

## 1. Ce qu'il faut

- un serveur virtuel Linux d'entrée de gamme (1 processeur, 1 Go de mémoire, 20 Go de disque) chez un hébergeur au choix, avec Ubuntu 22.04 ou 24.04 ;
- un nom de domaine (par exemple `suivi.[domaine].cm`) pointant vers l'adresse du serveur ;
- un accès SSH.

L'application tient dans un seul processus Python avec une base SQLite : aucun serveur de base de données n'est nécessaire.

## 2. Installation

```bash
sudo apt update && sudo apt install -y python3-venv nginx certbot python3-certbot-nginx git
sudo useradd -m -s /bin/bash tracabilite
sudo -u tracabilite -i
git clone [adresse du dépôt] depot
cd depot/huiles-usagees/16_application
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q tests          # les tests doivent passer
exit
```

## 3. Configuration

Créer le fichier `/etc/tracabilite.env` (lisible par root et par l'utilisateur `tracabilite` seulement) :

```
TRACABILITE_BASE=/home/tracabilite/donnees/tracabilite.sqlite
TRACABILITE_TOKEN=[jeton long et aléatoire, par exemple produit par : openssl rand -hex 24]
TRACABILITE_SOCIETE=[Dénomination de la société]
```

```bash
sudo -u tracabilite mkdir -p /home/tracabilite/donnees
sudo chmod 640 /etc/tracabilite.env && sudo chgrp tracabilite /etc/tracabilite.env
```

## 4. Service systemd

Fichier `/etc/systemd/system/tracabilite.service` :

```
[Unit]
Description=Application de traçabilité des huiles usagées
After=network.target

[Service]
User=tracabilite
WorkingDirectory=/home/tracabilite/depot/huiles-usagees/16_application
EnvironmentFile=/etc/tracabilite.env
ExecStart=/home/tracabilite/depot/huiles-usagees/16_application/.venv/bin/gunicorn -w 2 -b 127.0.0.1:8000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload && sudo systemctl enable --now tracabilite
```

## 5. Nginx et HTTPS

Fichier `/etc/nginx/sites-available/tracabilite` :

```
server {
    server_name suivi.[domaine].cm;
    location / { proxy_pass http://127.0.0.1:8000; proxy_set_header Host $host; proxy_set_header X-Forwarded-Proto $scheme; }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/tracabilite /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d suivi.[domaine].cm
```

Le HTTPS est obligatoire : le mode hors ligne du navigateur (service worker) ne fonctionne qu'en HTTPS.

## 6. Sauvegarde

Sauvegarde quotidienne de la base, conservée 30 jours (crontab de l'utilisateur `tracabilite`) :

```
15 2 * * * sqlite3 /home/tracabilite/donnees/tracabilite.sqlite ".backup /home/tracabilite/donnees/sauvegarde-$(date +\%F).sqlite" && find /home/tracabilite/donnees -name 'sauvegarde-*.sqlite' -mtime +30 -delete
```

Copier aussi chaque semaine une sauvegarde hors du serveur (stockage en ligne ou ordinateur du gérant).

## 7. Démonstration

Pour une base de démonstration, aux données **fictives** et marquées comme telles :

```bash
python demo.py /home/tracabilite/donnees/demo.sqlite
```

Ne jamais mélanger la base de démonstration et la base réelle.

## 8. Mise à jour

```bash
sudo -u tracabilite -i
cd depot && git pull && cd huiles-usagees/16_application && . .venv/bin/activate && pip install -r requirements.txt && python -m pytest -q tests
exit
sudo systemctl restart tracabilite
```
