"""Test de bout en bout dans Chromium (Playwright pour Node) : saisie hors ligne puis synchronisation."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import threading

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tracabilite import creer_app  # noqa: E402

SCRIPT = Path(__file__).with_name("e2e_navigateur.js")


def _playwright_disponible():
    if shutil.which("node") is None:
        return False
    return subprocess.run(["node", "-e", "require('playwright')"], capture_output=True).returncode == 0


@pytest.mark.skipif(not _playwright_disponible(), reason="Node ou Playwright absent")
def test_saisie_hors_ligne_puis_synchronisation(tmp_path):
    from werkzeug.serving import make_server
    app = creer_app({"BASE": str(tmp_path / "n.sqlite"), "TOKEN": "secret"})
    srv = make_server("127.0.0.1", 0, app)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        r = subprocess.run(["node", str(SCRIPT), f"http://127.0.0.1:{srv.server_port}", str(tmp_path / "capture.png")],
                           capture_output=True, text=True, timeout=90)
        assert r.returncode == 0, r.stderr
        res = json.loads(r.stdout.strip().splitlines()[-1])
        assert res["attente"] == "1" and res["visible"] is True
        assert res["largeur"] <= 390
        with app.test_client() as c:
            noms = [x["nom"] for x in c.get("/api/clients", headers={"X-Token": "secret"}).get_json()]
        assert "Client saisi en forêt" in noms
    finally:
        srv.shutdown()
