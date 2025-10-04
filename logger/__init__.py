# logger/__init__.py
import logging
import os
import sys
from logging.config import fileConfig

def _try_fileconfig(cfg_path):
    try:
        if cfg_path and os.path.exists(cfg_path):
            fileConfig(cfg_path, disable_existing_loggers=False)
            logging.getLogger(__name__).info("Loaded logging config from: %s", cfg_path)
            return True
    except Exception as e:
        logging.getLogger(__name__).warning("Failed to load logging config %s: %s", cfg_path, e)
    return False

def configure_logging(debug=False):
    # 1) Percorso accanto al modulo (sviluppo)
    pkg_dir = os.path.dirname(__file__)
    candidates = [os.path.join(pkg_dir, 'logging.conf')]

    # 2) Percorso dentro il bundle PyInstaller (se incluso come dati)
    meipass = getattr(sys, '_MEIPASS', None)
    if meipass:
        # Se hai incluso il file con destinazione 'logger', sarà qui:
        candidates.append(os.path.join(meipass, 'logger', 'logging.conf'))
        # In alcuni setup potrebbe essere direttamente nella root del bundle
        candidates.append(os.path.join(meipass, 'logging.conf'))

    for path in candidates:
        if _try_fileconfig(path):
            return

    # 3) Fallback: basicConfig
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )
    logging.getLogger(__name__).warning("logging.conf not found. Using basicConfig (level=%s).", "DEBUG" if debug else "INFO")

# Configura subito in modo sicuro
try:
    configure_logging(debug=False)
except Exception:
    logging.basicConfig(level=logging.INFO)