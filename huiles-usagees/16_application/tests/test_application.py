from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tracabilite import creer_app  # noqa: E402
from demo import creer_demo  # noqa: E402

H = {"X-Token": "secret"}


@pytest.fixture()
def client(tmp_path):
    app = creer_app({"BASE": str(tmp_path / "t.sqlite"), "TOKEN": "secret", "TESTING": True})
    return app.test_client()


def _post(c, url, data):
    return c.post(url, json=data, headers=H)


def _base(c):
    cid = _post(c, "/api/clients", {"nom": "Client test"}).get_json()["id"]
    sid = _post(c, "/api/sites", {"client_id": cid, "nom": "Site test"}).get_json()["id"]
    fid = _post(c, "/api/futs", {"code": "F-1", "site_id": sid}).get_json()["id"]
    eid = _post(c, "/api/enlevements", {"site_id": sid, "date_prevue": "2026-12-01"}).get_json()["id"]
    return cid, sid, fid, eid


def test_authentification_obligatoire(client):
    assert client.get("/api/clients").status_code == 401
    assert client.get("/api/clients", headers=H).status_code == 200


def test_interface_servie(client):
    r = client.get("/")
    assert r.status_code == 200 and b"Tra" in r.data
    assert client.get("/sw.js").status_code == 200


def test_champs_obligatoires(client):
    r = _post(client, "/api/clients", {"type": "forestier"})
    assert r.status_code == 400 and "nom" in r.get_json()["erreur"]


def test_parcours_complet(client):
    cid, sid, fid, eid = _base(client)
    r = _post(client, f"/api/enlevements/{eid}/realiser", {"volume_l": 2500, "depistage": "negatif", "fut_ids": [fid], "date": "2026-12-01"})
    assert r.status_code == 200 and r.get_json()["bordereau"] == "BSD-2026-0001"
    futs = client.get("/api/futs", headers=H).get_json()
    assert futs[0]["statut"] == "enleve"
    pdf = client.get(f"/api/enlevements/{eid}/bordereau.pdf", headers=H)
    assert pdf.status_code == 200 and pdf.data[:4] == b"%PDF"
    lot = client.get("/api/lots", headers=H).get_json()[0]
    assert lot["statut"] == "accepte_provisoire" and lot["volume_l"] == 2500
    assert _post(client, "/api/analyses", {"lot_id": lot["id"], "chlore_ppm": 300, "pcb_detecte": False}).get_json()["decision"] == "accepte"
    stock = client.get("/api/stock", headers=H).get_json()
    assert stock[0]["stock_l"] == 2500
    v = _post(client, "/api/ventes", {"date": "2026-12-10", "acheteur": "Acheteur test", "lot_id": lot["id"], "volume_l": 1000, "prix_l": 300})
    assert v.status_code == 201
    assert client.get("/api/stock", headers=H).get_json()[0]["stock_l"] == 1500
    rap = client.get(f"/api/clients/{cid}/rapport/2026.pdf", headers=H)
    assert rap.status_code == 200 and rap.data[:4] == b"%PDF"
    tdb = client.get("/api/tableau_de_bord", headers=H).get_json()
    assert tdb["enlevements_realises"] == 1 and tdb["volume_enleve_l"] == 2500 and tdb["volume_vendu_l"] == 1000


def test_lot_refuse_si_chlore_ou_pcb(client):
    _, _, _, eid = _base(client)
    _post(client, f"/api/enlevements/{eid}/realiser", {"volume_l": 100, "depistage": "positif"})
    lot = client.get("/api/lots", headers=H).get_json()[0]
    assert lot["statut"] == "en_attente"
    assert _post(client, "/api/analyses", {"lot_id": lot["id"], "chlore_ppm": 1000, "pcb_detecte": False}).get_json()["decision"] == "refuse"
    v = _post(client, "/api/ventes", {"date": "2026-12-10", "acheteur": "X", "lot_id": lot["id"], "volume_l": 10, "prix_l": 300})
    assert v.status_code == 400


def test_vente_limitee_au_stock(client):
    _, _, _, eid = _base(client)
    _post(client, f"/api/enlevements/{eid}/realiser", {"volume_l": 100, "depistage": "negatif"})
    lot = client.get("/api/lots", headers=H).get_json()[0]
    _post(client, "/api/analyses", {"lot_id": lot["id"], "chlore_ppm": 10, "pcb_detecte": False})
    r = _post(client, "/api/ventes", {"date": "2026-12-10", "acheteur": "X", "lot_id": lot["id"], "volume_l": 500, "prix_l": 300})
    assert r.status_code == 400 and "stock insuffisant" in r.get_json()["erreur"]


def test_depistage_obligatoire(client):
    _, _, _, eid = _base(client)
    r = _post(client, f"/api/enlevements/{eid}/realiser", {"volume_l": 100})
    assert r.status_code == 400


def test_synchronisation_hors_ligne_idempotente(client):
    ops = [{"op_id": "op1", "type": "creer", "table": "clients", "data": {"id": "cX", "nom": "Saisi hors ligne"}},
           {"op_id": "op2", "type": "creer", "table": "sites", "data": {"id": "sX", "client_id": "cX", "nom": "Site hors ligne"}},
           {"op_id": "op3", "type": "creer", "table": "enlevements", "data": {"id": "eX", "site_id": "sX", "date_prevue": "2026-12-02"}},
           {"op_id": "op4", "type": "realiser", "table": "enlevements", "data": {"id": "eX", "volume_l": 900, "depistage": "negatif"}}]
    r1 = _post(client, "/api/sync", {"operations": ops}).get_json()["resultats"]
    assert [x["statut"] for x in r1] == ["ok"] * 4
    r2 = _post(client, "/api/sync", {"operations": ops}).get_json()["resultats"]
    assert [x["statut"] for x in r2] == ["deja_recu"] * 4
    assert len(client.get("/api/clients", headers=H).get_json()) == 1
    assert len(client.get("/api/lots", headers=H).get_json()) == 1


def test_synchronisation_signale_les_erreurs(client):
    r = _post(client, "/api/sync", {"operations": [{"op_id": "e1", "type": "realiser", "data": {"id": "inconnu", "volume_l": 1, "depistage": "negatif"}}]})
    assert r.get_json()["resultats"][0]["statut"] == "erreur"


def test_qr_code(client):
    _, _, fid, _ = _base(client)
    r = client.get(f"/api/futs/{fid}/qr.svg", headers=H)
    assert r.status_code == 200 and b"<svg" in r.data


def test_donnees_de_demonstration_marquees_fictives(tmp_path):
    chemin = tmp_path / "demo.sqlite"
    creer_demo(chemin)
    app = creer_app({"BASE": str(chemin), "TOKEN": ""})
    c = app.test_client()
    clients = c.get("/api/clients").get_json()
    assert clients and all(x["fictif"] == 1 and "DEMO" in x["nom"] for x in clients)
    tdb = c.get("/api/tableau_de_bord").get_json()
    assert tdb["enlevements_realises"] == 3 and tdb["lots"].get("refuse") == 1
