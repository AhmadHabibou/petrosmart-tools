"""Point d'entree du serveur.

Developpement : python 16_application/wsgi.py   (http://127.0.0.1:8000)
Production : gunicorn -w 2 -b 127.0.0.1:8000 wsgi:app (voir GUIDE_INSTALLATION.md)
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tracabilite import creer_app  # noqa: E402

app = creer_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
