# -*- coding: utf-8 -*-
"""
launcher.py — Lancia le pagine Kanban da DocumentManagement.

Genera un token monouso in WipKanbanWebSessions e apre il browser.
Richiede l'oggetto db di DocumentManagement (metodi execute_query e
get_employee_hire_history_id, come il launcher di print_label_for_production).
"""
import uuid
import webbrowser
import logging

from . import server_config

logger = logging.getLogger("WipKanban")


def _issue_token(db, user_id, user_name, page, permission):
    token = uuid.uuid4().hex
    ok = db.execute_query(
        """INSERT INTO Traceability_RS.ind.WipKanbanWebSessions
           (Token, UserId, UserName, Permission, Page, IssuedAt, ExpiresAt)
           VALUES (?, ?, ?, ?, ?, GETDATE(), DATEADD(MINUTE, ?, GETDATE()))""",
        (token, user_id, user_name, permission, page, server_config.load_config()["token_ttl_minutes"]),
    )
    if not ok:
        raise RuntimeError("Impossibile emettere il token di accesso kanban")
    logger.info("Token kanban emesso per pagina %s, utente %s", page, user_name)
    return token


def _open_browser(page_path):
    cfg = server_config.load_config()
    url = f"http://{cfg['server_host_ip']}:{cfg['server_port']}/{page_path}"
    logger.info("Apertura browser: %s", url)
    webbrowser.open(url)


def _resolve_user_id(db, user_id):
    """Restituisce un user_id numerico (UserId INT in WipKanbanWebSessions)."""
    if isinstance(user_id, int):
        return user_id
    if isinstance(user_id, str) and user_id.isdigit():
        return int(user_id)
    if hasattr(db, "get_employee_hire_history_id"):
        numeric_id = db.get_employee_hire_history_id(user_id)
        if numeric_id:
            return numeric_id
    raise ValueError(f"Impossibile risolvere l'ID numerico per l'utente {user_id!r}")


def open_load_page(db, user_id, user_name, lang="it"):
    """Apre la pagina Carica schede (richiede permesso 'crea_kanBan_produzione')."""
    numeric_id = _resolve_user_id(db, user_id)
    token = _issue_token(db, numeric_id, user_name, "kanban_load", "crea_kanBan_produzione")
    _open_browser(f"kanban/load?token={token}&lang={lang}")


def open_pick_page(db, user_id, user_name, lang="it"):
    """Apre la pagina Preleva schede (simple login, operazioni auditate)."""
    numeric_id = _resolve_user_id(db, user_id)
    token = _issue_token(db, numeric_id, user_name, "kanban_pick", "wip_kanban_pick")
    _open_browser(f"kanban/pick?token={token}&lang={lang}")


def open_report_page(lang="it"):
    """Apre la pagina Report schede: pubblica, nessun token ne' db richiesti."""
    _open_browser(f"kanban/report?lang={lang}")
