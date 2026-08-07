# -*- coding: utf-8 -*-
"""
db.py — Connessione al database per il web server Etichette Produzione.
"""
import os
import sys
import logging
import pyodbc

logger = logging.getLogger("PrintLabelProduction")


def _project_root() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _conn_str() -> str:
    sys.path.insert(0, _project_root())

    cfg = None
    try:
        from config_manager import ConfigManager
        cfg = ConfigManager(key_file="encryption_key.key", config_file="db_config.enc").load_config()
    except Exception as e:
        logger.warning("ConfigManager non disponibile: %s", e)

    if cfg is None:
        try:
            from database_config import db_config
            conn_str = db_config.get_connection_string()
            logger.info("Connessione tramite database_config.py")
            return conn_str
        except Exception as e:
            logger.warning("database_config.py non disponibile: %s", e)
            raise RuntimeError("Impossibile ottenere la configurazione del database")

    driver = cfg.get("driver", "").strip()
    available = pyodbc.drivers()
    if not driver or driver not in available:
        for d in (
            "ODBC Driver 18 for SQL Server",
            "ODBC Driver 17 for SQL Server",
            "SQL Server Native Client 11.0",
            "SQL Server",
        ):
            if d in available:
                driver = d
                break
        if not driver and available:
            driver = available[0]
    if not driver:
        raise RuntimeError("Nessun driver ODBC per SQL Server trovato")

    # Normalizza il driver per la connection string ODBC
    if not (driver.startswith("{") and driver.endswith("}")):
        driver = "{" + driver + "}"

    logger.info("Uso driver ODBC: %s", driver)
    return (
        f"DRIVER={driver};"
        f"SERVER={cfg['server']};"
        f"DATABASE={cfg['database']};"
        f"UID={cfg['username']};"
        f"PWD={cfg['password']};"
        "MARS_Connection=Yes;"
        "TrustServerCertificate=Yes;"
        "Connection Timeout=30;"
    )


def get_conn(autocommit: bool = False):
    return pyodbc.connect(_conn_str(), autocommit=autocommit)


def row_to_dict(row, cursor):
    if row is None:
        return None
    columns = [desc[0] for desc in cursor.description]
    return {col: (row[i] if i < len(row) else None) for i, col in enumerate(columns)}


def fetch_all_dict(cursor):
    columns = [desc[0] for desc in cursor.description]
    return [{col: row[i] for i, col in enumerate(columns)} for row in cursor.fetchall()]
