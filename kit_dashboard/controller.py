# -*- coding: utf-8 -*-
"""
controller.py — Watcher della Kit Dashboard lato programma desktop.

Architettura "server indipendente": il web server gira come processo autonomo
sul PC 192.168.10.72 (avviato da Scheduled Task al boot) e fa da sé il sync
ogni 5 minuti. Il programma desktop NON avvia né chiude il server.

Questo controller, avviato su ogni PC da main.py, fa solo da **watcher**:
  - ping periodico di /health del server
  - se il server è DOWN → alert (popup KIT_PREP + email) con dedup atomico
    (decisione D2 = solo alert, nessun rilancio remoto).

Thread daemon, connessione DB propria (non usa quella della GUI).
"""
import socket
import logging
import threading
import time

logger = logging.getLogger("KitDashboard")


class KitDashboardController:
    def __init__(self, cfg: dict = None):
        from . import server_config
        self.cfg = cfg or server_config.load_config()
        self.hostname = socket.gethostname()
        self._running = False
        self._thread = None
        self._conn = None
        self._down_since = None

    # ------------------------------------------------------------------ #
    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, name="KitDashboardWatcher",
                                        daemon=True)
        self._thread.start()
        logger.info("KitDashboardController (watcher) avviato su %s (server=%s:%s)",
                    self.hostname, self.cfg.get("server_host_ip"), self.cfg.get("server_port"))

    def stop(self):
        self._running = False

    # ------------------------------------------------------------------ #
    def _open_conn(self):
        import pyodbc
        from config_manager import ConfigManager
        c = ConfigManager(key_file="encryption_key.key", config_file="db_config.enc").load_config()
        return pyodbc.connect(
            f"DRIVER={c['driver']};SERVER={c['server']};DATABASE={c['database']};"
            f"UID={c['username']};PWD={c['password']};MARS_Connection=Yes;TrustServerCertificate=Yes",
            autocommit=True,
        )

    def _conn_ok(self):
        if self._conn is None:
            self._conn = self._open_conn()
            return
        try:
            self._conn.cursor().execute("SELECT 1")
        except Exception:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = self._open_conn()

    # ------------------------------------------------------------------ #
    def _run(self):
        from . import server_watcher
        heartbeat_s = int(self.cfg.get("heartbeat_seconds", 60))
        tick = max(20, min(heartbeat_s, 60))
        # piccola attesa iniziale: lascia partire il server/app
        slept = 0
        while self._running and slept < 15:
            time.sleep(1); slept += 1

        while self._running:
            try:
                if server_watcher.check_health(self.cfg):
                    self._down_since = None
                else:
                    # HTTP non raggiungibile da questo PC: alza l'alert SOLO se anche
                    # l'heartbeat del server nel DB è vecchio (= server davvero giù).
                    # Evita falsi positivi da proxy/rete del singolo PC.
                    self._conn_ok()
                    if server_watcher.server_heartbeat_fresh(self._conn, self.cfg):
                        logger.info("Dashboard non raggiungibile via HTTP da %s, "
                                    "ma heartbeat DB fresco: server vivo, nessun alert.",
                                    self.hostname)
                    else:
                        server_watcher.handle_down(self._conn, self.cfg)
            except Exception as e:
                logger.error("KitDashboardController watcher errore: %s", e, exc_info=True)
            slept = 0
            while self._running and slept < tick:
                time.sleep(1); slept += 1
