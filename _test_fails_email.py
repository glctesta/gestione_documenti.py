# -*- coding: utf-8 -*-
"""
_test_fails_email.py
--------------------
Sends a real-data test of the FAIL daily email report to a fixed address.
Bypasses anti-duplication and recipient lookup — use only for manual testing.

Usage:
    py _test_fails_email.py
"""
import sys, os, logging

# ── ensure the project root is on the path ─────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s — %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("TraceabilityRS")

# ── connect to DB (same creds as main.py) ──────────────────────────────────
from config_manager import ConfigManager
import pyodbc

config_mgr    = ConfigManager(key_file='encryption_key.key', config_file='db_config.enc')
db_credentials = config_mgr.load_config()

CONN_STR = (
    f"DRIVER={db_credentials['driver']};"
    f"SERVER={db_credentials['server']};"
    f"DATABASE={db_credentials['database']};"
    f"UID={db_credentials['username']};"
    f"PWD={db_credentials['password']};"
    "MARS_Connection=Yes;TrustServerCertificate=Yes"
)

conn = pyodbc.connect(CONN_STR, autocommit=True)
logger.info("Connessione DB stabilita.")

# ── minimal db wrapper expected by run_fails_daily_email ──────────────────
class _FakeDb:
    def __init__(self, connection):
        self.conn = connection
        self.conn_str = CONN_STR

db = _FakeDb(conn)

# ── import the email module ────────────────────────────────────────────────
import fails_daily_email as fde
import utils
import datetime

# ── patch: force recipients to test address only ──────────────────────────
TEST_RECIPIENT = 'gianluca.testa@vandewiele.com'

_orig_get_recipients = utils.get_email_recipients
def _patched_recipients(conn_arg, attribute=None):
    logger.info(f"[TEST] Recipient override → {TEST_RECIPIENT}  (original attr={attribute})")
    return [TEST_RECIPIENT]
utils.get_email_recipients = _patched_recipients

# ── patch: bypass the anti-duplication INSERT ─────────────────────────────
_orig_claim = fde._claim_send_slot
def _patched_claim(conn_arg, key):
    logger.info(f"[TEST] _claim_send_slot bypassed (key={key})")
    return True
fde._claim_send_slot = _patched_claim

# ── run ───────────────────────────────────────────────────────────────────
logger.info(f"Invio email di test a {TEST_RECIPIENT} …")
fde.run_fails_daily_email(db)
logger.info("Fatto.")

# ── restore (just in case the module is reused in the same process) ───────
utils.get_email_recipients = _orig_get_recipients
fde._claim_send_slot       = _orig_claim

conn.close()
