# -*- coding: utf-8 -*-
"""
server_config.py — Configurazione della Kit Dashboard web.

Legge/crea `kit_server_config.json` nella **stessa directory dell'eseguibile**
(accanto a main.exe / db_config.enc). Se il file non esiste viene creato con i
valori di default (decisione D6). Scrittura atomica (tmp -> replace) con backup.
"""

import os
import sys
import json
import shutil
import tempfile
import logging

logger = logging.getLogger("KitDashboard")

CONFIG_FILENAME = "kit_server_config.json"

DEFAULT_CONFIG = {
    "server_host_ip": "192.168.10.72",
    "server_port": 8090,
    "sync_interval_minutes": 5,
    "heartbeat_seconds": 60,
    "controller_takeover_minutes": 3,
    "health_path": "/health",
    "alert_targets": ["KIT_PREP"],
    "email_setting": "Sys_email_Kit_materiali",
    "history_default_days": 3,
    "pthm_phase_id": 4,            # IdPhase 'PTHM' (dbo.Phases)
    "pthm_phase_name": "PTHM",     # match esatto nel file di pianificazione (escl. 'PTHM SELECTIVE')
    "eta_fallback_minutes_per_item": 1.5,  # usato se lo storico è insufficiente
    # Percorso del file di pianificazione. UNC (non lettera mappata) così funziona
    # anche se il server gira come SYSTEM (senza login → niente T:). Vuoto = usa
    # il default di fai_autocheck (T:\Planning).
    "planning_path": r"\\192.168.10.110\InternalApplications\Planning",
}


def app_base_dir() -> str:
    """Directory dell'eseguibile (frozen) o root del progetto (sviluppo)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    # dev: la root del progetto è il parent della cartella del package kit_dashboard
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def config_path() -> str:
    return os.path.join(app_base_dir(), CONFIG_FILENAME)


def load_config() -> dict:
    """Carica la config; se assente la crea con i default. Le chiavi mancanti
    vengono completate con i default (forward-compatibile)."""
    path = config_path()
    if not os.path.isfile(path):
        logger.info("kit_server_config.json assente: creo con i default in %s", path)
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logger.error("Errore lettura %s (%s): uso i default", path, e)
        return dict(DEFAULT_CONFIG)

    merged = dict(DEFAULT_CONFIG)
    merged.update({k: v for k, v in data.items() if v is not None})
    # Se il file era incompleto, riscrivilo completo (best-effort)
    if set(merged) != set(data):
        try:
            save_config(merged)
        except Exception:
            pass
    return merged


def save_config(cfg: dict) -> None:
    """Scrittura atomica con backup del file precedente."""
    path = config_path()
    dir_ = os.path.dirname(path)
    os.makedirs(dir_, exist_ok=True)
    if os.path.isfile(path):
        try:
            shutil.copy2(path, path + ".bak")
        except Exception:
            pass
    with tempfile.NamedTemporaryFile("w", delete=False, dir=dir_,
                                     encoding="utf-8") as tf:
        json.dump(cfg, tf, ensure_ascii=False, indent=2)
        tmp = tf.name
    os.replace(tmp, path)


CATEGORY_SERVER_DOWN = "KIT_DASHBOARD_DOWN"

# Flag locale (per-PC) per silenziare l'avviso "server non raggiungibile".
_MUTE_DIR = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
_MUTE_FILE = os.path.join(_MUTE_DIR, "kit_dashboard_alert_muted.flag")


def is_alert_muted() -> bool:
    """True se su questo PC l'avviso 'server down' è stato silenziato."""
    return os.path.isfile(_MUTE_FILE)


def set_alert_muted(muted: bool) -> None:
    """Attiva/disattiva il silenziamento dell'avviso su questo PC."""
    try:
        if muted:
            os.makedirs(_MUTE_DIR, exist_ok=True)
            with open(_MUTE_FILE, "w", encoding="utf-8") as f:
                f.write("muted\n")
        elif os.path.isfile(_MUTE_FILE):
            os.remove(_MUTE_FILE)
    except Exception as e:
        logger.warning("set_alert_muted fallito: %s", e)


def base_url(cfg: dict = None) -> str:
    cfg = cfg or load_config()
    return f"http://{cfg['server_host_ip']}:{cfg['server_port']}"


def health_url(cfg: dict = None) -> str:
    cfg = cfg or load_config()
    return base_url(cfg) + cfg.get("health_path", "/health")


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    c = load_config()
    print("Config path:", config_path())
    print(json.dumps(c, ensure_ascii=False, indent=2))
    print("base_url:", base_url(c))
