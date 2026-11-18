"""Schema SQLite et acces aux donnees de l'application de tracabilite."""
import sqlite3
import uuid
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS clients (
    id TEXT PRIMARY KEY, nom TEXT NOT NULL, type TEXT NOT NULL DEFAULT 'forestier',
    contact TEXT, telephone TEXT, fictif INTEGER NOT NULL DEFAULT 0, cree_le TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS sites (
    id TEXT PRIMARY KEY, client_id TEXT NOT NULL REFERENCES clients(id), nom TEXT NOT NULL,
    type TEXT, latitude REAL, longitude REAL, piste_km REAL, cree_le TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS futs (
    id TEXT PRIMARY KEY, code TEXT UNIQUE NOT NULL, site_id TEXT REFERENCES sites(id),
    statut TEXT NOT NULL DEFAULT 'chez_client', contenu TEXT NOT NULL DEFAULT 'huiles usagees',
    cree_le TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS enlevements (
    id TEXT PRIMARY KEY, site_id TEXT NOT NULL REFERENCES sites(id), date_prevue TEXT NOT NULL,
    date_realisee TEXT, statut TEXT NOT NULL DEFAULT 'planifie', transporteur TEXT,
    volume_l REAL, depistage TEXT, bordereau TEXT UNIQUE, cree_le TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS enlevement_futs (
    enlevement_id TEXT NOT NULL REFERENCES enlevements(id), fut_id TEXT NOT NULL REFERENCES futs(id),
    PRIMARY KEY (enlevement_id, fut_id));
CREATE TABLE IF NOT EXISTS lots (
    id TEXT PRIMARY KEY, numero TEXT UNIQUE NOT NULL, enlevement_id TEXT REFERENCES enlevements(id),
    date TEXT NOT NULL, volume_l REAL NOT NULL, statut TEXT NOT NULL DEFAULT 'en_attente', cree_le TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS analyses (
    id TEXT PRIMARY KEY, lot_id TEXT NOT NULL REFERENCES lots(id), date TEXT NOT NULL, laboratoire TEXT,
    chlore_ppm REAL, pcb_detecte INTEGER, eau_pct REAL, point_eclair_c REAL, decision TEXT, cree_le TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS traitements (
    id TEXT PRIMARY KEY, lot_id TEXT NOT NULL REFERENCES lots(id), date TEXT NOT NULL,
    volume_entree_l REAL NOT NULL, volume_sortie_l REAL NOT NULL, cree_le TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS mouvements (
    id TEXT PRIMARY KEY, date TEXT NOT NULL, sens TEXT NOT NULL, volume_l REAL NOT NULL,
    lot_id TEXT REFERENCES lots(id), reference TEXT, cree_le TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS ventes (
    id TEXT PRIMARY KEY, date TEXT NOT NULL, acheteur TEXT NOT NULL, lot_id TEXT REFERENCES lots(id),
    volume_l REAL NOT NULL, prix_l REAL NOT NULL, cree_le TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS operations_sync (op_id TEXT PRIMARY KEY, recu_le TEXT NOT NULL, resultat TEXT);
"""

# Champs modifiables par l'API generique, par table
CHAMPS = {
    "clients": ["nom", "type", "contact", "telephone", "fictif"],
    "sites": ["client_id", "nom", "type", "latitude", "longitude", "piste_km"],
    "futs": ["code", "site_id", "statut", "contenu"],
    "enlevements": ["site_id", "date_prevue", "transporteur", "statut"],
    "ventes": ["date", "acheteur", "lot_id", "volume_l", "prix_l"],
    "traitements": ["lot_id", "date", "volume_entree_l", "volume_sortie_l"],
}
OBLIGATOIRES = {
    "clients": ["nom"], "sites": ["client_id", "nom"], "futs": ["code"], "enlevements": ["site_id", "date_prevue"],
    "ventes": ["date", "acheteur", "volume_l", "prix_l"], "traitements": ["lot_id", "date", "volume_entree_l", "volume_sortie_l"],
}


def maintenant():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def nouvel_id():
    return str(uuid.uuid4())


def connecter(chemin):
    con = sqlite3.connect(chemin, detect_types=sqlite3.PARSE_DECLTYPES)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def initialiser(con):
    con.executescript(SCHEMA)
    con.commit()


def lignes(con, sql, params=()):
    return [dict(r) for r in con.execute(sql, params).fetchall()]
