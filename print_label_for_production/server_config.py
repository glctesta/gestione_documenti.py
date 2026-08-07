# -*- coding: utf-8 -*-
"""
server_config.py — Configurazione del web server Etichette Produzione.

Legge/crea `print_label_server_config.json` nella stessa directory dell'eseguibile
(o nella root del progetto in sviluppo). Se il file non esiste viene creato con i
default.
"""
import os
import sys
import json
import shutil
import tempfile
import logging
import secrets

logger = logging.getLogger("PrintLabelProduction")

CONFIG_FILENAME = "print_label_server_config.json"

DEFAULT_CONFIG = {
    "server_host_ip": "192.168.10.72",
    "server_port": 5015,
    "token_ttl_minutes": 5,
    "session_lifetime_minutes": 30,
    "session_secret": None,
}


def app_base_dir() -> str:
    """Directory dell'eseguibile (frozen) o root del progetto (sviluppo)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def config_path() -> str:
    return os.path.join(app_base_dir(), CONFIG_FILENAME)


def load_config() -> dict:
    path = config_path()
    if not os.path.isfile(path):
        logger.info("%s assente: creo con i default in %s", CONFIG_FILENAME, path)
        save_config(dict(DEFAULT_CONFIG))
        return dict(DEFAULT_CONFIG)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logger.error("Errore lettura %s (%s): uso i default", path, e)
        return dict(DEFAULT_CONFIG)

    merged = dict(DEFAULT_CONFIG)
    merged.update({k: v for k, v in data.items() if v is not None})

    if not merged.get("session_secret"):
        merged["session_secret"] = secrets.token_hex(32)
        try:
            save_config(merged)
        except Exception as e:
            logger.warning("Impossibile salvare session_secret generato: %s", e)

    return merged


def save_config(cfg: dict) -> None:
    path = config_path()
    dir_ = os.path.dirname(path)
    os.makedirs(dir_, exist_ok=True)
    if os.path.isfile(path):
        try:
            shutil.copy2(path, path + ".bak")
        except Exception:
            pass
    with tempfile.NamedTemporaryFile("w", delete=False, dir=dir_, encoding="utf-8") as tf:
        json.dump(cfg, tf, ensure_ascii=False, indent=2)
        tmp = tf.name
    os.replace(tmp, path)


def base_url(cfg: dict = None) -> str:
    cfg = cfg or load_config()
    return f"http://{cfg['server_host_ip']}:{cfg['server_port']}"


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    c = load_config()
    print("Config path:", config_path())
    print(json.dumps(c, ensure_ascii=False, indent=2))
    print("base_url:", base_url(c))
