"""
kit_notifications.py
Notifiche Email + Popup del modulo Kit Preparation — Sprint 3
(spec docs/PlanRespect_KitPreparation_Spec_v1.2.md §7).

- Email: destinatari da traceability_rs.dbo.settings, Atribute =
  'Sys_email_Kit_materiali' (utils.get_email_recipients); invio in thread
  per non bloccare la UI, SEMPRE dopo il commit della transazione.
- Popup: righe in kit_popup_queue (categoria DIRECT_MATERIAL), consumate
  dal monitor in-app (kit_popup_monitor.py). I target di ruolo sono
  configurati esplicitamente per postazione (kit_workstation_config.py):
    'KIT_PREP' -> postazione Formazione Kit (kit_prep_host.json)
    'KIT_PROD' -> postazione Ricezione Kit Produzione (kit_prod_host.json)
  oppure l'hostname del richiedente per le notifiche punto-a-punto.
Le funzioni queue_popup_* ricevono un cursor e NON committano.
"""
import logging
import socket
import threading

import utils

logger = logging.getLogger("PlanMonitor")

EMAIL_SETTING = 'Sys_email_Kit_materiali'
CATEGORY = 'DIRECT_MATERIAL'
# Target di ruolo (postazioni configurate via kit_workstation_config.py)
TARGET_KIT_PREP = 'KIT_PREP'   # Formazione Kit
TARGET_KIT_PROD = 'KIT_PROD'   # Ricezione Kit Produzione


def queue_popup(cursor, target: str, title: str, message: str,
                order_number: str = None, category: str = CATEGORY) -> None:
    cursor.execute("""
        INSERT INTO Traceability_RS.dbo.kit_popup_queue
            (category, target, title, message, order_number)
        VALUES (?, ?, ?, ?, ?)
    """, (category, target, title[:200], message[:1000],
          order_number[:30] if order_number else None))


def send_kit_email_async(conn, subject: str, body: str) -> None:
    """Invia l'email ai destinatari di Sys_email_Kit_materiali in un thread.
    Chiamare DOPO il commit. Errori solo loggati (non bloccanti)."""
    try:
        recipients = utils.get_email_recipients(conn, EMAIL_SETTING)
    except Exception as e:
        logger.error("Lettura destinatari %s fallita: %s", EMAIL_SETTING, e)
        return
    if not recipients:
        logger.warning("Nessun destinatario in %s: email NON inviata (%s)",
                       EMAIL_SETTING, subject)
        return

    def _send():
        try:
            utils.send_email(recipients, subject, body)
        except Exception as e:
            logger.error("Invio email kit fallito (%s): %s", subject, e)

    threading.Thread(target=_send, daemon=True).start()


def current_hostname() -> str:
    return socket.gethostname()


# ───────────────────── Template notifiche (§7.3) ──────────────────────── #

def verify_fail_pf_messages(orders_compact: str, codes: list) -> dict:
    codes_txt = '\n'.join(codes) if codes else '-'
    subject = f"[ALERT] Verifica Kit NON CONFORME — Ordine {orders_compact}"
    body = (f"La verifica di ingresso in Preformatura per l'ordine {orders_compact}\n"
            f"ha rilevato discrepanze.\n\n"
            f"Codici non conformi:\n{codes_txt}\n\n"
            f"La lista di prelievo è stata RIAPERTA.\n"
            f"Accedi al sistema (Prelievo Magazzino Kit) per effettuare le correzioni.")
    popup_msg = (f"Ordine {orders_compact}: verifica fallita in ingresso preformatura. "
                 f"Codici non conformi: {', '.join(codes) if codes else '-'}. "
                 f"Lista di prelievo RIAPERTA.")
    return {'subject': subject, 'body': body,
            'popup_title': f"⚠ Verifica Kit NON CONFORME — {orders_compact}",
            'popup_msg': popup_msg}


def material_request_messages(order_number: str, phase: str, material_code: str,
                              qty, requester: str, note: str) -> dict:
    subject = f"[RICHIESTA] Materiale aggiuntivo richiesto — Ordine {order_number}"
    body = (f"{requester} ha richiesto materiale aggiuntivo per l'ordine {order_number}\n"
            f"da fase: {phase}\n\n"
            f"Materiale: {material_code}\n"
            f"Quantità: {qty}\n"
            f"Motivazione: {note or '-'}\n\n"
            f"Accedi al sistema (scheda Richieste Materiale) per confermare il prelievo.")
    popup_msg = (f"{requester} richiede {qty} x {material_code} "
                 f"per ordine {order_number} (fase {phase}). Motivo: {note or '-'}")
    return {'subject': subject, 'body': body,
            'popup_title': f"🔔 Richiesta materiale — {order_number}",
            'popup_msg': popup_msg}


def verify_fail_prod_messages(orders_compact: str, codes: list) -> dict:
    """Caso B §5.3.2: kit incompleto al ricevimento linea -> avvisare la
    preformatura (attori della fase precedente)."""
    codes_txt = '\n'.join(codes) if codes else '-'
    subject = f"[ALERT] Ordine NON avanzabile — kit incompleto — {orders_compact}"
    body = (f"Ordine {orders_compact} non avanzabile: kit incompleto in "
            f"ricevimento linea di produzione.\n\n"
            f"Codici non conformi:\n{codes_txt}\n\n"
            f"L'ordine è in stato BLOCKED_MISSING_MATERIAL.\n"
            f"Verificare la consegna effettuata dalla preformatura.")
    popup_msg = (f"Ordine {orders_compact} non avanzabile: kit incompleto in "
                 f"ricevimento linea. Codici: {', '.join(codes) if codes else '-'}")
    return {'subject': subject, 'body': body,
            'popup_title': f"⛔ Ordine bloccato — kit incompleto — {orders_compact}",
            'popup_msg': popup_msg}


def material_ready_messages(order_number: str, material_code: str, qty) -> dict:
    return {
        'popup_title': f"📦 Materiale pronto — {order_number}",
        'popup_msg': (f"Materiale {material_code} (qty {qty}) disponibile "
                      f"per prelievo in magazzino — ordine {order_number}"),
    }


def request_cancelled_messages(order_number: str, material_code: str,
                               reason: str) -> dict:
    return {
        'popup_title': f"↩ Richiesta annullata — {order_number}",
        'popup_msg': (f"La richiesta di {material_code} per l'ordine {order_number} "
                      f"è stata annullata: {reason}. Evitare il prelievo."),
    }
