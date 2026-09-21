# -*- coding: utf-8 -*-
"""
display_launcher.py — Launcher per i monitor di reparto kanban (porta 6505).

Legge display_config.json nella stessa directory (se mancante usa i default:
WIP / deposito 1 / localhost). Costruisce l'URL del display e apre il browser:
Chrome in modalità kiosk se trovato, altrimenti il browser predefinito.

Configurazione (display_config.json):
  {
    "area": "WIP",            // "WIP" | "REPAIR"
    "deposit": 1,             // quale deposito
    "server": "192.168.10.72",// host del display server
    "port": 6505,
    "fullscreen": true        // true = Chrome --kiosk (se Chrome disponibile)
  }

Avvio sul monitor:  pythonw wip_kanban\\display_launcher.py  (o doppio click)
"""
import os
import sys
import json
import shutil
import logging
import subprocess
import webbrowser

logger = logging.getLogger("WipKanban")

CONFIG_FILENAME = "display_config.json"

DEFAULT_CONFIG = {
    "area": "WIP",
    "deposit": 1,
    "server": "localhost",
    "port": 6505,
    "fullscreen": True,
}

# Percorsi standard dove cercare Chrome su Windows
CHROME_CANDIDATES = [
    os.path.join(os.environ.get("PROGRAMFILES", r"C:\Program Files"), "Google", "Chrome", "Application", "chrome.exe"),
    os.path.join(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"), "Google", "Chrome", "Application", "chrome.exe"),
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "Application", "chrome.exe"),
]


def config_path():
    base = os.path.dirname(os.path.abspath(__file__))
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    return os.path.join(base, CONFIG_FILENAME)


def load_config():
    path = config_path()
    if not os.path.isfile(path):
        logger.info("%s assente: uso i default %s", CONFIG_FILENAME, DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logger.error("Errore lettura %s (%s): uso i default", path, e)
        return dict(DEFAULT_CONFIG)
    merged = dict(DEFAULT_CONFIG)
    merged.update({k: v for k, v in data.items() if v is not None})
    return merged


def find_chrome():
    """Percorso di Chrome se disponibile, altrimenti None."""
    for candidate in CHROME_CANDIDATES:
        if candidate and os.path.isfile(candidate):
            return candidate
    # shutil.which su PATH / variabili d'ambiente
    for name in ("chrome.exe", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    return None


def build_url(cfg):
    return "http://{server}:{port}/display?area={area}&deposit={deposit}".format(
        server=cfg["server"], port=int(cfg["port"]),
        area=cfg["area"].upper(), deposit=int(cfg["deposit"]))


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
    cfg = load_config()
    url = build_url(cfg)
    logger.info("Apertura display %s", url)

    chrome = find_chrome()
    if chrome and cfg.get("fullscreen", True):
        # Kiosk: fullscreen senza controlli, come da richiesta monitor di reparto.
        subprocess.Popen([chrome, "--kiosk", "--incognito",
                          "--disable-session-crashed-bubble", "--no-first-run", url])
    elif chrome:
        subprocess.Popen([chrome, url])
    else:
        webbrowser.open(url)


if __name__ == "__main__":
    main()
