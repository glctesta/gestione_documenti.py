# -*- coding: utf-8 -*-
"""
background_notification_service.py

Servizio di notifiche popup che gira in background nella sessione utente Windows.
Non richiede che il programma principale (main.py) sia avviato.

Si attiva SOLO sui PC che hanno una workstation configurata tramite il
programma principale (file JSON in %LOCALAPPDATA%). Se la workstation viene
disattivata, il relativo monitor si ferma automaticamente entro il prossimo
ciclo di polling.

I popup usano una finestra tkinter principale nascosta; i monitor esistenti
vengono riutilizzati quasi senza modifiche.
"""
import argparse
import logging
import os
import sys
import threading
import time
from collections import defaultdict
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pyodbc
import tkinter as tk
from tkinter import ttk

# ---------------------------------------------------------------------------
#  Configurazione logging
# ---------------------------------------------------------------------------
LOG_DIR = Path(os.environ.get("LOCALAPPDATA", ".")) / "TraceabilityRS" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "background_notifications.log"

logger = logging.getLogger("BackgroundNotificationService")
logger.setLevel(logging.DEBUG)

_fmt = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    "%Y-%m-%d %H:%M:%S",
)
_fh = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
_fh.setFormatter(_fmt)
logger.addHandler(_fh)

_ch = logging.StreamHandler(sys.stdout)
_ch.setFormatter(_fmt)
logger.addHandler(_ch)


# ---------------------------------------------------------------------------
#  Gestione redirect stdout/stderr (come main.py, in modo leggero)
# ---------------------------------------------------------------------------
_STDOUT_FILE = None
_STDERR_FILE = None

try:
    if getattr(sys, "stdout", None) is None:
        _STDOUT_FILE = open(LOG_DIR / "stdout.log", "w", buffering=1, encoding="utf-8")
        sys.stdout = _STDOUT_FILE
    if getattr(sys, "stderr", None) is None:
        _STDERR_FILE = open(LOG_DIR / "stderr.log", "w", buffering=1, encoding="utf-8")
        sys.stderr = _STDERR_FILE
except Exception:
    pass


# ---------------------------------------------------------------------------
#  Database minimale compatibile con i monitor esistenti
# ---------------------------------------------------------------------------
class BackgroundDatabase:
    """Wrapper pyodbc con l'interfaccia usata dai monitor (fetch_one/fetch_all,
    execute_query, cursor, conn, _lock)."""

    def __init__(self, conn_str: str):
        self.conn_str = conn_str
        self.conn = None
        self._lock = threading.RLock()
        self._tls = threading.local()
        self.last_error_details = ""
        self.engine = None
        self.npi_engine = None
        self._connect()

    def _connect(self) -> bool:
        with self._lock:
            try:
                if self.conn is not None:
                    try:
                        self.conn.close()
                    except Exception:
                        pass
                self.conn = pyodbc.connect(self.conn_str, timeout=30, autocommit=False)
                self._tls.cursor_entry = None
                self.last_error_details = ""
                logger.info("Connessione al database stabilita")
                return True
            except Exception as e:
                self.last_error_details = str(e)
                logger.error("Connessione al database fallita: %s", e)
                return False

    def _ensure_connection(self):
        try:
            if self.conn is None:
                return self._connect()
            # Test leggero; se fallisce riconnettiamo
            self.conn.cursor().execute("SELECT 1").fetchone()
        except Exception as e:
            logger.warning("Connessione DB persa, tentativo riconnessione: %s", e)
            return self._connect()
        return True

    @property
    def cursor(self):
        """Cursore thread-local: stesso pattern della classe Database di main.py.
        I monitor che fanno 'self.db.cursor.execute(...)' e poi
        'self.db.cursor.fetchall()' devono ottenere lo stesso cursore."""
        self._ensure_connection()
        conn = self.conn
        entry = getattr(self._tls, 'cursor_entry', None)
        if entry is not None:
            owner, cur = entry
            if cur is not None and owner is conn:
                return cur
        cur = conn.cursor()
        self._tls.cursor_entry = (conn, cur)
        return cur

    @cursor.setter
    def cursor(self, value):
        if value is None:
            self._tls.cursor_entry = None
        else:
            self._tls.cursor_entry = (self.conn, value)

    def execute_query(self, query: str, params=()) -> bool:
        """Esegue una query che non restituisce righe; ritorna True/False."""
        try:
            self._ensure_connection()
            with self._lock:
                cur = self.conn.cursor()
                cur.execute(query, params)
                self.conn.commit()
                cur.close()
            return True
        except Exception as e:
            logger.error("execute_query fallita: %s", e)
            return False

    def fetch_one(self, query: str, params=()):
        try:
            self._ensure_connection()
            with self._lock:
                cur = self.conn.cursor()
                cur.execute(query, params)
                row = cur.fetchone()
                cur.close()
            return row
        except Exception as e:
            logger.error("fetch_one fallita: %s", e)
            return None

    def fetch_all(self, query: str, params=()):
        try:
            self._ensure_connection()
            with self._lock:
                cur = self.conn.cursor()
                cur.execute(query, params)
                rows = cur.fetchall()
                cur.close()
            return rows
        except Exception as e:
            logger.error("fetch_all fallita: %s", e)
            return []

    def disconnect(self):
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            logger.warning("Errore chiusura connessione: %s", e)
        self.conn = None


# ---------------------------------------------------------------------------
#  Language manager minimale
# ---------------------------------------------------------------------------
class BackgroundLanguageManager:
    """Carica le traduzioni da Traceability_rs.dbo.AppTranslations; se non riesce
    usa i testi di default passati ai monitor."""

    def __init__(self, db: BackgroundDatabase, default_language: str = "ro"):
        self.db = db
        self.current_language = default_language.lower()
        self.translations = defaultdict(dict)
        self._load()

    def _load(self):
        try:
            rows = self.db.fetch_all(
                "SELECT LanguageCode, TranslationKey, TranslationValue "
                "FROM Traceability_rs.dbo.AppTranslations"
            )
            for lang, key, value in rows or []:
                self.translations[lang.lower()][key] = value
            logger.info("Caricate %s traduzioni per %s lingue",
                        len(rows or []), len(self.translations))
        except Exception as e:
            logger.warning("Impossibile caricare traduzioni: %s", e)

    def get(self, key, *args):
        lang_map = self.translations.get(self.current_language, {})
        has_translation = key in lang_map
        translated_text = lang_map.get(key, key)

        format_args = args
        if not has_translation and args and isinstance(args[0], str):
            translated_text = args[0]
            format_args = args[1:]

        if format_args:
            try:
                return translated_text.format(*format_args)
            except (IndexError, KeyError, ValueError, TypeError):
                return translated_text
        return translated_text

    def get_raw(self, key):
        return self.translations.get(self.current_language, {}).get(key, key)

    def set_language(self, lang_code):
        self.current_language = lang_code.lower()


# ---------------------------------------------------------------------------
#  Costanti
# ---------------------------------------------------------------------------
LOCAL_APPDATA = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))

MARKERS = {
    "wh": ("wh_host.json", "indirect_materials_wh_monitor", "WHMonitor"),
    "requester": ("wh_host.json", "indirect_materials_wh_monitor", "RequesterMonitor"),
    "purchasing": ("purchasing_host.json", "indirect_materials_purchasing_monitor", "PurchasingMonitor"),
    "shift_handover": ("sct_host.json", "shift_handover_monitor", "ShiftHandoverMonitor"),
    "touchup": ("touchup_host.json", "touchup_monitor", "TouchUpMonitor"),
    "kit": ("kit_host.json", "kit_popup_monitor", "KitPopupMonitor"),
    "label_scrap": ("labelscrap_print_host.json", "label_scrap_monitor", "LabelScrapMonitor"),
    "shipment": ("shipment_host.json", "orders.shipment_monitor", "ShipmentMonitor"),
}

# Kit usa due marker separati, ma noi lo avviamo se almeno uno dei due esiste.
KIT_PREP_MARKER = "kit_prep_host.json"
KIT_PROD_MARKER = "kit_prod_host.json"

POLL_INTERVAL_MS = 30_000


# ---------------------------------------------------------------------------
#  Orchestratore
# ---------------------------------------------------------------------------
class MonitorOrchestrator:
    def __init__(self, master: tk.Tk, db: BackgroundDatabase, lang: BackgroundLanguageManager):
        self.master = master
        self.db = db
        self.lang = lang
        self._running = True
        self._active = {}   # name -> monitor instance
        self._schedule_next()

    def _marker_path(self, filename: str) -> str:
        return os.path.join(LOCAL_APPDATA, filename)

    def _is_active(self, name: str) -> bool:
        if name == "kit":
            return (os.path.isfile(self._marker_path(KIT_PREP_MARKER)) or
                    os.path.isfile(self._marker_path(KIT_PROD_MARKER)))
        marker, _, _ = MARKERS[name]
        return os.path.isfile(self._marker_path(marker))

    def _start(self, name: str):
        if name in self._active:
            return
        try:
            _, module_name, class_name = MARKERS[name]
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            monitor = cls(self.master, self.db, self.lang)
            self._active[name] = monitor
            logger.info("Monitor avviato: %s", name)
        except Exception as e:
            logger.error("Errore avvio monitor %s: %s", name, e, exc_info=True)

    def _stop(self, name: str):
        monitor = self._active.pop(name, None)
        if monitor is None:
            return
        try:
            monitor.stop()
            logger.info("Monitor fermato: %s", name)
        except Exception as e:
            logger.error("Errore fermata monitor %s: %s", name, e, exc_info=True)

    def _tick(self):
        if not self._running:
            return
        try:
            for name in MARKERS:
                if self._is_active(name):
                    self._start(name)
                else:
                    self._stop(name)
        except Exception as e:
            logger.error("Errore ciclo orchestratore: %s", e, exc_info=True)
        finally:
            self._schedule_next()

    def _schedule_next(self):
        if self._running:
            self.master.after(POLL_INTERVAL_MS, self._tick)

    def stop(self):
        self._running = False
        for name in list(self._active):
            self._stop(name)


# ---------------------------------------------------------------------------
#  Finestra stato (opzionale)
# ---------------------------------------------------------------------------
class StatusWindow:
    def __init__(self, root: tk.Tk, orchestrator: MonitorOrchestrator):
        self.root = root
        self.orchestrator = orchestrator
        self.window = tk.Toplevel(root)
        self.window.title("TraceabilityRS - Notification Service")
        self.window.geometry("420x260")
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

        main = ttk.Frame(self.window, padding=15)
        main.pack(expand=True, fill="both")

        ttk.Label(main, text="Servizio notifiche in esecuzione",
                  font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))

        self.status_var = tk.StringVar(value="Inizializzazione...")
        ttk.Label(main, textvariable=self.status_var, wraplength=380,
                  justify="left").pack(expand=True, fill="both")

        ttk.Button(main, text="Esci", command=self._on_close).pack(pady=(10, 0))
        self._update()

    def _on_close(self):
        logger.info("Chiusura richiesta dalla finestra di stato")
        self.orchestrator.stop()
        self.root.quit()
        self.root.destroy()

    def _update(self):
        if not self.orchestrator._running:
            return
        active = ", ".join(sorted(self.orchestrator._active.keys())) or "nessuno"
        self.status_var.set(
            f"Monitor attivi: {active}\n"
            f"Ultimo controllo: {datetime.now().strftime('%H:%M:%S')}"
        )
        self.window.after(1_000, self._update)


# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------
def _build_db() -> BackgroundDatabase:
    from database_config import DatabaseConfig

    cfg = DatabaseConfig()
    conn_str = cfg.get_connection_string()
    db = BackgroundDatabase(conn_str)
    if db.conn is None:
        raise RuntimeError("Impossibile connettersi al database")
    return db


# ---------------------------------------------------------------------------
#  Launcher del programma principale dai popup del servizio
# ---------------------------------------------------------------------------
def _find_main_executable():
    """Trova l'eseguibile principale o lo script main.py.

    Ordine di ricerca:
      1. Variabile d'ambiente TRACEABILITY_RS_MAIN_EXE
      2. TraceabilityRS.exe nella root del progetto
      3. TraceabilityRS.exe in dist/ o dist/DocumentManagement/
      4. main.py nella root del progetto
    """
    env = os.environ.get("TRACEABILITY_RS_MAIN_EXE")
    if env and os.path.isfile(env):
        return env, None

    candidates = [
        Path.cwd() / "TraceabilityRS.exe",
        Path.cwd() / "dist" / "TraceabilityRS.exe",
        Path.cwd() / "dist" / "DocumentManagement" / "TraceabilityRS.exe",
        Path.cwd() / "main.py",
    ]
    for c in candidates:
        if c.exists():
            if c.suffix.lower() == ".py":
                return None, c
            return str(c), None
    return None, None


def _launch_main_application():
    """Avvia il programma principale TraceabilityRS se non e' gia' aperto.

    I monitor che aprono finestre dal popup (spedizioni, touch-up, cambio turno)
    possono usare questo metodo attraverso il master Tk.
    """
    exe, py = _find_main_executable()
    if exe:
        try:
            subprocess.Popen([exe], shell=False)
            logger.info("Programma principale avviato da popup: %s", exe)
        except Exception as e:
            logger.error("Errore avvio programma principale: %s", e)
        return

    if py:
        python = sys.executable
        # Preferisce python.exe a pythonw.exe per main.py cosi' eventuali errori
        # in console sono visibili in fase di test.
        if python.lower().endswith("pythonw.exe"):
            python_exe = Path(python).with_name("python.exe")
            if python_exe.exists():
                python = str(python_exe)
        try:
            subprocess.Popen([python, str(py)], shell=False)
            logger.info("Programma principale avviato da popup: %s %s", python, py)
        except Exception as e:
            logger.error("Errore avvio programma principale: %s", e)
        return

    logger.error("Impossibile trovare il programma principale (TraceabilityRS.exe o main.py)")


def main():
    parser = argparse.ArgumentParser(
        description="Servizio notifiche popup TraceabilityRS"
    )
    parser.add_argument(
        "--show-window", action="store_true",
        help="Mostra una finestra di stato con il bottone di uscita"
    )
    parser.add_argument(
        "--lang", default="ro",
        help="Codice lingua per le traduzioni (default: ro)"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Avvio Background Notification Service")
    logger.info("=" * 60)

    root = tk.Tk()
    root.withdraw()
    root.title("TraceabilityRS Background Service")

    # Metodi usati dai monitor per aprire il programma principale dal popup,
    # quando TraceabilityRS non e' gia' in esecuzione.
    root._open_shipment_confirmation = _launch_main_application
    root._open_touchup_response = _launch_main_application
    root._open_shift_handover = _launch_main_application

    try:
        db = _build_db()
    except Exception as e:
        logger.critical("Impossibile avviare il servizio: %s", e)
        sys.exit(1)

    lang = BackgroundLanguageManager(db, default_language=args.lang)
    orchestrator = MonitorOrchestrator(root, db, lang)

    if args.show_window:
        StatusWindow(root, orchestrator)
    else:
        logger.info("Finestra principale nascosta; usa --show-window per visualizzare lo stato")

    def _on_signal():
        logger.info("Segnale di chiusura ricevuto")
        orchestrator.stop()
        db.disconnect()
        root.quit()
        root.destroy()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        _on_signal()
    finally:
        orchestrator.stop()
        db.disconnect()
        if _STDOUT_FILE:
            try:
                _STDOUT_FILE.close()
            except Exception:
                pass
        if _STDERR_FILE:
            try:
                _STDERR_FILE.close()
            except Exception:
                pass
        logger.info("Servizio terminato")


if __name__ == "__main__":
    main()
