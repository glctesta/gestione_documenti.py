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


def _resolve_user_id(db, user_id):
    """Restituisce un user_id numerico.

    Il login semplice passa lo username (es. 'sa'), mentre la tabella
    PrintLabelWebSessions richiede UserId INT. Se user_id non è numerico,
    cerca l'EmployeeHireHistoryId corrispondente tramite il metodo del DB.
    """
    if isinstance(user_id, int):
        return user_id
    if isinstance(user_id, str) and user_id.isdigit():
        return int(user_id)
    if hasattr(db, "get_employee_hire_history_id"):
        numeric_id = db.get_employee_hire_history_id(user_id)
        if numeric_id:
            return numeric_id
    raise ValueError(f"Impossibile risolvere l'ID numerico per l'utente {user_id!r}")


def open_bom_page(db, user_id, user_name, lang='it'):
    """Apre la pagina Gestione BOM nel browser di default."""
    numeric_id = _resolve_user_id(db, user_id)
    token = _issue_token(db, numeric_id, user_name, "bom")
    _open_browser(f"bom?token={token}&lang={lang}")


def open_printers_page(db, user_id, user_name, lang='it'):
    """Apre la pagina Gestione stampanti nel browser di default."""
    numeric_id = _resolve_user_id(db, user_id)
    token = _issue_token(db, numeric_id, user_name, "printers")
    _open_browser(f"printers?token={token}&lang={lang}")


def open_generic_print_page(db, user_id, user_name, lang='it'):
    """Apre la pagina Stampa generica etichette nel browser di default."""
    numeric_id = _resolve_user_id(db, user_id)
    token = _issue_token(db, numeric_id, user_name, "print_generic")
    _open_browser(f"print/generic?token={token}&lang={lang}")


def open_orders_print_page(db, user_id, user_name, lang='it'):
    """Apre la pagina Stampa etichette per ordini nel browser di default."""
    numeric_id = _resolve_user_id(db, user_id)
    token = _issue_token(db, numeric_id, user_name, "print_orders")
    _open_browser(f"print/orders?token={token}&lang={lang}")
