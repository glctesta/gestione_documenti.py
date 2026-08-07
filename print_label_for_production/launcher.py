# -*- coding: utf-8 -*-
"""
launcher.py — Lancia le pagine web di Etichette Produzione da DocumentManagement.

Genera un token monouso nel database e apre il browser di default con l'URL.
"""
import uuid
import webbrowser
import logging

from . import server_config

logger = logging.getLogger("PrintLabelProduction")

PERMISSION_KEY = "gestione_stampa_etichette_produzione"


def _issue_token(db, user_id, user_name, page, permission=PERMISSION_KEY):
    token = uuid.uuid4().hex
    ok = db.execute_query(
        """INSERT INTO Traceability_RS.ind.PrintLabelWebSessions
           (Token, UserId, UserName, Permission, Page, IssuedAt, ExpiresAt)
           VALUES (?, ?, ?, ?, ?, GETDATE(), DATEADD(MINUTE, ?, GETDATE()))""",
        (token, user_id, user_name, permission, page, server_config.load_config()["token_ttl_minutes"]),
    )
    if not ok:
        raise RuntimeError("Impossibile emettere il token di accesso web")
    logger.info("Token emesso per pagina %s, utente %s", page, user_name)
    return token


def _open_browser(page_path):
    cfg = server_config.load_config()
    url = f"http://{cfg['server_host_ip']}:{cfg['server_port']}/{page_path}"
    logger.info("Apertura browser: %s", url)
    webbrowser.open(url)


def open_bom_page(db, user_id, user_name, lang='it'):
    """Apre la pagina Gestione BOM nel browser di default."""
    token = _issue_token(db, user_id, user_name, "bom")
    _open_browser(f"bom?token={token}&lang={lang}")


def open_printers_page(db, user_id, user_name, lang='it'):
    """Apre la pagina Gestione stampanti nel browser di default."""
    token = _issue_token(db, user_id, user_name, "printers")
    _open_browser(f"printers?token={token}&lang={lang}")
