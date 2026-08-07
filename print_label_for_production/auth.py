# -*- coding: utf-8 -*-
"""
auth.py — Validazione token monouso e gestione sessione per il web server.
"""
import functools
import logging
from datetime import datetime

from flask import session, request, abort, redirect

from . import server_config, db

logger = logging.getLogger("PrintLabelProduction")

SESSION_USER_KEY = "plp_user"


def validate_token(token: str, expected_page: str):
    """Valida un token monouso e restituisce i dati utente, oppure None."""
    conn = db.get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """SELECT UserId, UserName, Permission, Page, UsedAt, ExpiresAt
               FROM Traceability_RS.ind.PrintLabelWebSessions
               WHERE Token = ?""",
            (token,),
        )
        row = cur.fetchone()
        if not row:
            return None

        user_id, user_name, permission, page, used_at, expires_at = row

        if used_at is not None or expires_at < datetime.now():
            return None
        if page != expected_page:
            return None
        if permission != "gestione_stampa_etichette_produzione":
            return None

        cur.execute(
            "UPDATE Traceability_RS.ind.PrintLabelWebSessions SET UsedAt = GETDATE() WHERE Token = ?",
            (token,),
        )
        conn.commit()
        return {"user_id": user_id, "user_name": user_name, "permission": permission}
    finally:
        conn.close()


def set_session(user: dict):
    cfg = server_config.load_config()
    session.permanent = True
    session[SESSION_USER_KEY] = user


def get_session_user():
    return session.get(SESSION_USER_KEY)


def require_page_token_or_session(page: str):
    """Decoratore: richiede token valido in URL o sessione già attiva."""
    def decorator(view):
        @functools.wraps(view)
        def wrapper(*args, **kwargs):
            user = get_session_user()
            if user:
                return view(*args, **kwargs)

            token = request.args.get("token") or request.form.get("token")
            if not token:
                abort(403)
            user = validate_token(token, page)
            if not user:
                abort(403)
            set_session(user)
            return view(*args, **kwargs)
        return wrapper
    return decorator
