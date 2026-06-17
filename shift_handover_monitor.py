# -*- coding: utf-8 -*-
"""
shift_handover_monitor.py
Monitor background per i PC Capo Turno.

- Polling ogni 60s
- Finestra alert 15 min prima della fine turno (15:15, 23:15, 07:15)
- Popup "Compila consegna" se non esiste report per turno+data+reparto
- Popup "Conferma lettura" se il report esiste ma non è confermato
- Email alert se il capo entrante non conferma entro 30 min dall'inizio turno
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
import socket
import os
import json
import winsound
import time
import threading
from datetime import datetime, date, timedelta
from business_days import is_business_day, get_next_business_day

logger = logging.getLogger('TraceabilityRS')

POLL_INTERVAL_MS   = 60_000    # polling ogni 60s
ALERT_WINDOW_MIN   = 15        # minuti prima della fine turno: apre alert "compila"
CONFIRM_GRACE_MIN  = 30        # minuti dopo inizio turno: se non confermato → email
ALERT_CUTOFF_HM    = (10, 0)   # oltre le 10:00 del primo giorno lavorativo successivo
                               # alla ShiftDate non si invia più l'alert di mancata conferma

# Tabelle di log per garantire un solo invio (anche con più PC Capo Turno e tra riavvii)
MONTHLY_REPORT_LOG_TABLE = 'Employee.dbo.ShiftHandoverMonthlyReportLog'
ALERT_LOG_TABLE          = 'Employee.dbo.ShiftHandoverAlertLog'

# ─── File marker workstation ─────────────────────────────────────────────────
_LOCALAPPDATA = os.environ.get('LOCALAPPDATA', os.path.expanduser('~\\AppData\\Local'))
SCT_HOST_FILE = os.path.join(_LOCALAPPDATA, 'sct_host.json')


def is_shift_leader_workstation():
    """Restituisce True se questo PC è configurato come Capo Turno."""
    return os.path.isfile(SCT_HOST_FILE)


def _read_sct_host():
    """Legge sct_host.json → {'department': str, 'shifts': [1,2,3]}."""
    try:
        with open(SCT_HOST_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"sct_host.json non leggibile: {e}")
        return {}


# ─── Logica turni ────────────────────────────────────────────────────────────
# (fine_h, fine_m) per ogni turno
SHIFT_ENDS = {
    1: (15, 30),
    2: (23, 30),
    3: (7,  30),
}

MORNING_START_HM = (7, 30)
MORNING_DEADLINE_HM = (8, 0)


def _get_active_shifts(host_cfg):
    """Restituisce i numeri di turno abilitati su questo PC."""
    shifts = host_cfg.get('shifts', [1, 2])
    # Turno 3 solo se esplicitamente in shifts
    return [s for s in shifts if s in SHIFT_ENDS]


def _shift_alert_window(shift_num, now_dt):
    """
    Restituisce (in_window, shift_date) se ora è nella finestra di alert
    (ALERT_WINDOW_MIN prima della fine turno).
    Per il turno 3 (fine 07:30) la ShiftDate è il giorno precedente.
    """
    end_h, end_m = SHIFT_ENDS[shift_num]
    # Calcola ora di fine turno oggi
    if shift_num == 3:
        # Fine alle 07:30 del giorno CORRENTE → turno iniziato ieri sera
        end_dt = now_dt.replace(hour=end_h, minute=end_m, second=0, microsecond=0)
        shift_date = (now_dt - timedelta(days=1)).date()
    else:
        end_dt = now_dt.replace(hour=end_h, minute=end_m, second=0, microsecond=0)
        shift_date = now_dt.date()

    alert_start = end_dt - timedelta(minutes=ALERT_WINDOW_MIN)
    alert_end   = end_dt + timedelta(minutes=5)   # piccola tolleranza post-fine

    in_window = alert_start <= now_dt <= alert_end
    return in_window, shift_date


def _get_previous_business_day(ref_date, country_code='RO'):
    """Restituisce il giorno lavorativo precedente rispetto a ref_date."""
    d = ref_date - timedelta(days=1)
    for _ in range(31):
        if is_business_day(d, country_code=country_code):
            return d
        d -= timedelta(days=1)
    return ref_date - timedelta(days=1)


def _alert_cutoff(shift_date, country_code='RO'):
    """Limite oltre il quale NON si invia più l'alert di mancata conferma.

    È fissato alle 10:00 del primo giorno lavorativo SUCCESSIVO alla ShiftDate.
    Conseguenze (coerenti con la regola richiesta):
      - turno del giorno in corso: alert valido fino alle 10:00 del giorno dopo;
      - giorno precedente: valido solo se siamo entro le 10:00;
      - venerdì: valido fino alle 10:00 del lunedì (o primo giorno lavorativo).
    """
    if isinstance(shift_date, datetime):
        shift_date = shift_date.date()
    next_bd = get_next_business_day(shift_date, country_code=country_code)
    return datetime.combine(next_bd, datetime.min.time()).replace(
        hour=ALERT_CUTOFF_HM[0], minute=ALERT_CUTOFF_HM[1])


def _is_deferred_shift2_mode(shift_num, active_shifts):
    """Turno 2 senza turno 3: popup/warning rinviati al mattino lavorativo successivo."""
    return shift_num == 2 and 3 not in active_shifts


def _is_morning_window(now_dt):
    """Finestra valida per popup mattutino: 07:30-08:00 inclusi."""
    start = now_dt.replace(hour=MORNING_START_HM[0], minute=MORNING_START_HM[1], second=0, microsecond=0)
    end = now_dt.replace(hour=MORNING_DEADLINE_HM[0], minute=MORNING_DEADLINE_HM[1], second=0, microsecond=0)
    return start <= now_dt <= end


def _next_shift_start(shift_num, ref_date, active_shifts=None):
    """Restituisce datetime di inizio del turno SUCCESSIVO (per calcolo grazia conferma).

    Il turno successivo inizia alla stessa ora in cui finisce quello corrente:
      - Turno 1 finisce 15:30 → Turno 2 inizia 15:30 (stesso giorno)
      - Turno 2 finisce 23:30 → Turno 3 inizia 23:30 (stesso giorno)
      - Turno 3 finisce 07:30 → Turno 1 inizia 07:30 (giorno SUCCESSIVO a ref_date)
    """
    # Caso speciale richiesto: turno 2 senza turno 3 attivo.
    # L'inizio turno "successivo" è alle 07:30 del primo giorno lavorativo successivo.
    if shift_num == 2 and active_shifts is not None and 3 not in active_shifts:
        next_bd = get_next_business_day(ref_date, country_code='RO')
        return datetime.combine(next_bd, datetime.min.time()).replace(hour=MORNING_START_HM[0], minute=MORNING_START_HM[1])

    # Nota: next_starts corrisponde a SHIFT_ENDS, cioè la fine del turno corrente
    # coincide con l'inizio del turno successivo.
    next_starts = {1: (15, 30), 2: (23, 30), 3: (7, 30)}
    h, m = next_starts.get(shift_num, (15, 30))
    if shift_num == 3:
        # Il turno 3 finisce all'07:30 del giorno successivo a shift_date
        next_date = ref_date + timedelta(days=1)
    else:
        next_date = ref_date
    return datetime.combine(next_date, datetime.min.time()).replace(hour=h, minute=m)


def _fetch_one(db, sql, params=()):
    try:
        if hasattr(db, 'fetch_one'):
            return db.fetch_one(sql, params)
        with db._lock:
            db.cursor.execute(sql, params)
            return db.cursor.fetchone()
    except Exception as e:
        logger.error(f"Monitor fetch_one: {e}")
        return None


def _get_alert_recipients(db):
    """Legge destinatari email da traceability_rs.dbo.settings."""
    try:
        import utils
        return utils.get_email_recipients(db.conn, 'sys_email_Allert_Shift')
    except Exception as e:
        logger.warning(f"Impossibile leggere sys_email_Allert_Shift: {e}")
        return []


# ─── Monitor ─────────────────────────────────────────────────────────────────
class ShiftHandoverMonitor:
    """Polling background; attivo solo sui PC con sct_host.json."""

    def __init__(self, master, db, lang):
        self.master   = master
        self.db       = db
        self.lang     = lang
        self.hostname = socket.gethostname()
        self._running = True
        self._popup_open = False
        self._email_sent_for = set()  # (shift_num, shift_date) già notificati

        host_cfg = _read_sct_host()
        self._department = host_cfg.get('department', '')
        self._active_shifts = _get_active_shifts(host_cfg)

        logger.info(f"ShiftHandoverMonitor avviato: dept={self._department} shifts={self._active_shifts}")
        self._poll()

    def stop(self):
        self._running = False

    def _poll(self):
        if not self._running:
            return
        try:
            self._check()
        except Exception as e:
            logger.error(f"ShiftHandoverMonitor poll error: {e}", exc_info=True)
        finally:
            if self._running:
                self.master.after(POLL_INTERVAL_MS, self._poll)

    def _check(self):
        if self._popup_open:
            return

        # Ri-verifica ad ogni ciclo: se la workstation è stata disattivata
        # (sct_host.json rimosso), interrompi subito senza mostrare popup.
        if not is_shift_leader_workstation():
            return

        # Aggiorna la config in caso di cambiamenti (es. cambio sezione/turni)
        host_cfg = _read_sct_host()
        self._department    = host_cfg.get('department', self._department)
        self._active_shifts = _get_active_shifts(host_cfg)

        now = datetime.now()

        # Report mensile (primo giorno del mese / primo avvio del mese nuovo)
        self._maybe_send_monthly_report(now)

        for shift_num in self._active_shifts:
            deferred_shift2 = _is_deferred_shift2_mode(shift_num, self._active_shifts)

            if deferred_shift2:
                # Nessun turno 3: il controllo del turno 2 passa al mattino del
                # primo giorno lavorativo successivo (es. venerdì -> lunedì).
                if not is_business_day(now.date(), country_code='RO'):
                    continue
                shift_date = _get_previous_business_day(now.date(), country_code='RO')
                in_window = _is_morning_window(now)
            else:
                in_window, shift_date = _shift_alert_window(shift_num, now)

            if in_window:
                # Controlla se esiste già un report
                row = _fetch_one(self.db, """
                    SELECT HandoverReportId, IsConfirmed
                    FROM Employee.dbo.ShiftHandoverReports
                    WHERE ShiftDate = ? AND ShiftNumber = ? AND Department = ?
                """, (shift_date, shift_num, self._department))

                if row is None:
                    # Nessun report → popup "compila"
                    self._show_compile_popup(shift_num, shift_date)
                    return
                elif not row[1]:
                    # Report non ancora confermato: potrebbe servire conferma
                    # (mostriamo popup conferma solo fuori dalla finestra di compilazione
                    #  del turno precedente, cioè all'inizio del turno successivo)
                    pass  # gestito sotto

            # Controlla mancata conferma 30 min dopo inizio turno successivo
            key = (shift_num, shift_date)
            if key not in self._email_sent_for:
                row = _fetch_one(self.db, """
                    SELECT HandoverReportId, IsConfirmed, CompiledBy, OpenIssues
                    FROM Employee.dbo.ShiftHandoverReports
                    WHERE ShiftDate = ? AND ShiftNumber = ? AND Department = ?
                """, (shift_date, shift_num, self._department))

                if row and not row[1]:
                    next_start = _next_shift_start(shift_num, shift_date)
                    if deferred_shift2:
                        next_start = _next_shift_start(shift_num, shift_date, active_shifts=self._active_shifts)
                    grace_end  = next_start + timedelta(minutes=CONFIRM_GRACE_MIN)
                    cutoff     = _alert_cutoff(shift_date)
                    # Invia SOLO se: superata la grazia E non oltre il limite.
                    # Così si notifica il giorno in corso, il giorno precedente
                    # entro le 10:00 e il venerdì entro le 10:00 del lunedì,
                    # evitando alert per cambi turno di giorni più vecchi.
                    if grace_end < now <= cutoff:
                        # Claim atomico: previene duplicati tra riavvii dell'app e
                        # tra più PC Capo Turno sullo stesso reparto/turno/data.
                        if self._claim_unconfirmed_alert(shift_num, shift_date):
                            if self._send_unconfirmed_alert(shift_num, shift_date, row[2], row[3]):
                                self._email_sent_for.add(key)            # inviato: non riprovare
                            else:
                                self._release_unconfirmed_alert(shift_num, shift_date)  # ritenta dopo
                        else:
                            # già inviato (da questo o altro PC): evita ulteriori query
                            self._email_sent_for.add(key)

    # ── Popup "Compila consegna" ──────────────────────────────────────────────
    def _show_compile_popup(self, shift_num, shift_date):
        self._popup_open = True
        _play_alert()
        L = self.lang.get

        popup = tk.Toplevel(self.master)
        popup.title(L('sct_popup_title', '\u26a0\ufe0f  CAMBIO TURNO \u2014 Compila la consegna!'))
        popup.geometry('480x240')
        popup.attributes('-topmost', True)
        popup.configure(bg='#e74c3c')
        popup.grab_set()

        main = ttk.Frame(popup, padding=20)
        main.pack(expand=True, fill='both')

        ttk.Label(main,
            text='\u26a0\ufe0f  ' + L('sct_popup_header', '\u00c8 ora di compilare la consegna turno!'),
            font=('Segoe UI', 13, 'bold'), foreground='#c0392b'
        ).pack(pady=(0, 8))

        dept_lbl = L('sct_popup_dept', 'Reparto')
        shift_lbl = L('sct_popup_shift', 'Turno')
        date_lbl  = L('sct_popup_date', 'Data')
        ttk.Label(main,
            text=(f"{dept_lbl}: {self._department}\n"
                  f"{shift_lbl}: {shift_num}   |   {date_lbl}: {shift_date.strftime('%d/%m/%Y')}"),
            font=('Segoe UI', 10)
        ).pack(pady=(0, 16))

        btn = ttk.Frame(main)
        btn.pack(fill='x')

        def on_open():
            self._popup_open = False
            popup.destroy()
            self._open_handover_window(preselect_shift=shift_num)

        def on_later():
            self._popup_open = False
            popup.destroy()

        ttk.Button(btn, text='\u270f\ufe0f  ' + L('sct_popup_btn_open', 'Apri Cambio Turno'), command=on_open).pack(
            side='left', expand=True, fill='x', padx=(0, 5))
        ttk.Button(btn, text='\u23f3  ' + L('sct_popup_btn_later', 'Dopo'), command=on_later).pack(
            side='left', expand=True, fill='x', padx=(5, 0))

        popup.protocol('WM_DELETE_WINDOW', on_later)

    # ── Popup "Conferma lettura" ──────────────────────────────────────────────
    def show_confirm_popup(self, shift_num, shift_date, report_id):
        """Chiamato dall'esterno (o dal poll) per richiedere la conferma di lettura."""
        if self._popup_open:
            return
        self._popup_open = True
        _play_alert()
        L = self.lang.get

        popup = tk.Toplevel(self.master)
        popup.title('\U0001f4cb  ' + L('sct_popup_confirm_title', 'CAMBIO TURNO \u2014 Leggi la consegna!'))
        popup.geometry('480x200')
        popup.attributes('-topmost', True)
        popup.grab_set()

        main = ttk.Frame(popup, padding=20)
        main.pack(expand=True, fill='both')

        ttk.Label(main,
            text='\U0001f4cb  ' + L('sct_popup_confirm_header', 'Leggi e conferma la consegna del turno precedente!'),
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=(0, 10))

        dept_lbl  = L('sct_popup_dept',  'Reparto')
        shift_lbl = L('sct_popup_shift', 'Turno')
        ttk.Label(main,
            text=f"{dept_lbl}: {self._department}  |  {shift_lbl}: {shift_num}  |  {shift_date.strftime('%d/%m/%Y')}"
        ).pack()

        btn = ttk.Frame(main)
        btn.pack(fill='x', pady=16)

        def on_open():
            self._popup_open = False
            popup.destroy()
            self._open_handover_window(preselect_shift=shift_num)

        def on_later():
            self._popup_open = False
            popup.destroy()

        ttk.Button(btn, text='\U0001f4d6  ' + L('sct_popup_btn_open_confirm', 'Apri e Conferma'), command=on_open).pack(
            side='left', expand=True, fill='x', padx=(0, 5))
        ttk.Button(btn, text='\u23f3  ' + L('sct_popup_btn_later', 'Dopo'), command=on_later).pack(
            side='left', expand=True, fill='x', padx=(5, 0))

        popup.protocol('WM_DELETE_WINDOW', on_later)

    # ── Apertura finestra handover ────────────────────────────────────────────
    def _open_handover_window(self, preselect_shift=None):
        try:
            from shift_handover_gui import open_shift_handover
            # Prende l'utente corrente dall'app
            current_user = getattr(self.master, 'last_authenticated_user_name', '') or ''
            open_shift_handover(
                self.master, self.db, self.lang, current_user,
                preselect_dept=self._department,
                preselect_shift=preselect_shift
            )
        except Exception as e:
            logger.error(f"Errore apertura ShiftHandoverWindow dal monitor: {e}", exc_info=True)

    # ── Dedup persistente alert (anti-duplicati tra riavvii e tra PC) ─────────
    def _claim_unconfirmed_alert(self, shift_num, shift_date):
        """Prenota l'invio dell'alert per (data, turno, reparto). Ritorna True solo
        se questo PC ha ottenuto il claim ora; False se già presente/inviato."""
        try:
            with self.db._lock:
                self.db.cursor.execute(f"""
                    INSERT INTO {ALERT_LOG_TABLE} (ShiftDate, ShiftNumber, Department, SentByComputer)
                    SELECT ?, ?, ?, ?
                    WHERE NOT EXISTS (
                        SELECT 1 FROM {ALERT_LOG_TABLE}
                        WHERE ShiftDate = ? AND ShiftNumber = ? AND Department = ?
                    )
                """, (shift_date, shift_num, self._department, self.hostname,
                      shift_date, shift_num, self._department))
                claimed = self.db.cursor.rowcount == 1
                self.db.conn.commit()
            return claimed
        except Exception as e:
            # Race / violazione PK con altro PC → consideriamo già inviato
            logger.info(f"Claim alert non riuscito (t{shift_num} {shift_date} {self._department}): {e}")
            try:
                self.db.conn.rollback()
            except Exception:
                pass
            return False

    def _release_unconfirmed_alert(self, shift_num, shift_date):
        """Rimuove il claim dell'alert (in caso di invio fallito) per ritentare."""
        try:
            with self.db._lock:
                self.db.cursor.execute(
                    f"DELETE FROM {ALERT_LOG_TABLE} "
                    f"WHERE ShiftDate = ? AND ShiftNumber = ? AND Department = ? AND SentByComputer = ?",
                    (shift_date, shift_num, self._department, self.hostname)
                )
                self.db.conn.commit()
        except Exception as e:
            logger.warning(f"Impossibile rilasciare il claim alert: {e}")
            try:
                self.db.conn.rollback()
            except Exception:
                pass

    # ── Email mancata conferma ────────────────────────────────────────────────
    def _send_unconfirmed_alert(self, shift_num, shift_date, compiled_by, open_issues):
        try:
            import utils
            recipients = _get_alert_recipients(self.db)
            if not recipients:
                logger.warning('sys_email_Allert_Shift: nessun destinatario configurato')
                return

            subj = (f"[ALERT] Cambio turno non confermato — "
                    f"{self._department} — Turno {shift_num} — "
                    f"{shift_date.strftime('%d/%m/%Y')}")

            body = f"""
<html><body style="font-family:Arial,sans-serif;font-size:12px;">
<h2 style="color:#B71C1C;">⚠️ Cambio turno non confermato</h2>
<p>La consegna del turno <strong>{shift_num}</strong> del <strong>
{shift_date.strftime('%d/%m/%Y')}</strong> per il reparto
<strong>{self._department}</strong> <b>non è stata confermata</b>
entro {CONFIRM_GRACE_MIN} minuti dall'inizio del turno successivo.</p>
<table style="border-collapse:collapse;font-size:12px;border:1px solid #ddd;">
  <tr style="background:#FFCDD2;"><td style="padding:6px 12px;font-weight:bold;">Reparto</td>
      <td style="padding:6px 12px;">{self._department}</td></tr>
  <tr><td style="padding:6px 12px;font-weight:bold;">Turno</td>
      <td style="padding:6px 12px;">{shift_num}</td></tr>
  <tr style="background:#FFCDD2;"><td style="padding:6px 12px;font-weight:bold;">Data</td>
      <td style="padding:6px 12px;">{shift_date.strftime('%d/%m/%Y')}</td></tr>
  <tr><td style="padding:6px 12px;font-weight:bold;">Compilato da</td>
      <td style="padding:6px 12px;">{compiled_by or '—'}</td></tr>
  <tr style="background:#FFCDD2;"><td style="padding:6px 12px;font-weight:bold;">Problemi aperti</td>
      <td style="padding:6px 12px;">{(open_issues or 'Nessuno').replace(chr(10),'<br/>')}</td></tr>
</table>
<p style="margin-top:16px;color:#555;">
  Verificare che il capo turno entrante abbia preso visione delle informazioni.<br/>
  Generato automaticamente da TraceabilityRS — {datetime.now().strftime('%d/%m/%Y %H:%M')}
</p>
</body></html>"""

            utils.send_email(recipients, subj, body, is_html=True)
            logger.info(f"Alert mancata conferma inviato: turno={shift_num} dept={self._department}")
            return True
        except Exception as e:
            logger.error(f"Errore invio email alert cambio turno: {e}", exc_info=True)
            return False

    # ── Report mensile cambi turno ────────────────────────────────────────────
    def _maybe_send_monthly_report(self, now):
        """Il primo giorno del mese (o al primo avvio nel nuovo mese) invia il
        report mensile sui cambi turno del mese precedente + rolling da inizio
        anno. L'invio avviene UNA SOLA volta grazie al claim atomico sulla
        tabella di log, anche se sono attivi più PC Capo Turno."""
        try:
            # Invio previsto "il primo del mese"; finestra dei primi giorni per
            # robustezza (PC spento il 1°, weekend/festivi a inizio mese).
            if now.day > 5:
                return

            # Mese da riportare = mese precedente rispetto a 'now'
            first_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            report_month = (first_of_month - timedelta(days=1)).replace(day=1).date()

            # Claim atomico: solo il primo PC che inserisce la riga invia il report
            if not self._claim_monthly_report(report_month):
                return

            try:
                recipients = _get_alert_recipients(self.db)
                if not recipients:
                    logger.warning('Report mensile cambi turno: nessun destinatario configurato')
                    self._release_monthly_report(report_month)
                    return

                stats = self._compute_monthly_stats(report_month)
                html = _build_monthly_report_html(report_month, stats)
                subj = f"[Report Mensile] Cambi Turno — {_month_label(report_month)}"

                import utils
                logo = os.path.join(os.path.dirname(__file__), 'Logo.png')
                attachments = [('inline', logo, 'company_logo')] if os.path.exists(logo) else None

                utils.send_email(recipients, subj, html, is_html=True, attachments=attachments)
                self._update_monthly_report_recipients(report_month, len(recipients))
                logger.info(
                    f"Report mensile cambi turno inviato per {report_month:%Y-%m} "
                    f"a {len(recipients)} destinatari"
                )
            except Exception as e:
                # Invio fallito: rilascia il claim così verrà ritentato al prossimo poll
                logger.error(f"Errore invio report mensile cambi turno: {e}", exc_info=True)
                self._release_monthly_report(report_month)
        except Exception as e:
            logger.error(f"Errore _maybe_send_monthly_report: {e}", exc_info=True)

    def _claim_monthly_report(self, report_month):
        """Prenota l'invio del report per il mese dato. Ritorna True se questo PC
        ha ottenuto il claim (riga inserita ora), False se già presente/inviato."""
        try:
            with self.db._lock:
                self.db.cursor.execute(f"""
                    INSERT INTO {MONTHLY_REPORT_LOG_TABLE} (ReportMonth, SentByComputer)
                    SELECT ?, ?
                    WHERE NOT EXISTS (
                        SELECT 1 FROM {MONTHLY_REPORT_LOG_TABLE} WHERE ReportMonth = ?
                    )
                """, (report_month, self.hostname, report_month))
                claimed = self.db.cursor.rowcount == 1
                self.db.conn.commit()
            return claimed
        except Exception as e:
            # Es. violazione PK per race con un altro PC → consideriamo già inviato
            logger.info(f"Claim report mensile non riuscito ({report_month:%Y-%m}): {e}")
            try:
                self.db.conn.rollback()
            except Exception:
                pass
            return False

    def _release_monthly_report(self, report_month):
        """Rimuove il claim (in caso di invio fallito) per consentire un nuovo tentativo."""
        try:
            with self.db._lock:
                self.db.cursor.execute(
                    f"DELETE FROM {MONTHLY_REPORT_LOG_TABLE} WHERE ReportMonth = ? AND SentByComputer = ?",
                    (report_month, self.hostname)
                )
                self.db.conn.commit()
        except Exception as e:
            logger.warning(f"Impossibile rilasciare il claim report mensile: {e}")
            try:
                self.db.conn.rollback()
            except Exception:
                pass

    def _update_monthly_report_recipients(self, report_month, count):
        try:
            with self.db._lock:
                self.db.cursor.execute(
                    f"UPDATE {MONTHLY_REPORT_LOG_TABLE} SET RecipientCount = ? WHERE ReportMonth = ?",
                    (count, report_month)
                )
                self.db.conn.commit()
        except Exception:
            try:
                self.db.conn.rollback()
            except Exception:
                pass

    def _compute_monthly_stats(self, report_month):
        """Calcola le statistiche di compliance sui cambi turno per il mese e
        per il rolling da inizio anno (fino a fine mese di riferimento)."""
        # Intervalli [inizio, fineEsclusa)
        month_start = report_month
        if report_month.month == 12:
            month_end = date(report_month.year + 1, 1, 1)
        else:
            month_end = date(report_month.year, report_month.month + 1, 1)
        ytd_start = date(report_month.year, 1, 1)
        ytd_end = month_end  # YTD fino a fine mese di riferimento incluso

        agg_sql = """
            SELECT
                COUNT(*)                                          AS Total,
                SUM(CASE WHEN IsConfirmed = 1 THEN 1 ELSE 0 END)  AS Confirmed,
                SUM(CASE WHEN IsConfirmed = 0 THEN 1 ELSE 0 END)  AS NotConfirmed
            FROM Employee.dbo.ShiftHandoverReports
            WHERE ShiftDate >= ? AND ShiftDate < ?
        """
        by_dept_sql = """
            SELECT Department,
                   COUNT(*)                                          AS Total,
                   SUM(CASE WHEN IsConfirmed = 1 THEN 1 ELSE 0 END)  AS Confirmed,
                   SUM(CASE WHEN IsConfirmed = 0 THEN 1 ELSE 0 END)  AS NotConfirmed
            FROM Employee.dbo.ShiftHandoverReports
            WHERE ShiftDate >= ? AND ShiftDate < ?
            GROUP BY Department
            ORDER BY Department
        """
        by_shift_sql = """
            SELECT ShiftNumber,
                   COUNT(*)                                          AS Total,
                   SUM(CASE WHEN IsConfirmed = 1 THEN 1 ELSE 0 END)  AS Confirmed,
                   SUM(CASE WHEN IsConfirmed = 0 THEN 1 ELSE 0 END)  AS NotConfirmed
            FROM Employee.dbo.ShiftHandoverReports
            WHERE ShiftDate >= ? AND ShiftDate < ?
            GROUP BY ShiftNumber
            ORDER BY ShiftNumber
        """

        def _row_to_dict(r):
            return {
                'total': int(r.Total or 0),
                'confirmed': int(r.Confirmed or 0),
                'not_confirmed': int(r.NotConfirmed or 0),
            }

        stats = {}
        with self.db._lock:
            cur = self.db.cursor
            cur.execute(agg_sql, (month_start, month_end))
            stats['month'] = _row_to_dict(cur.fetchone())
            cur.execute(agg_sql, (ytd_start, ytd_end))
            stats['ytd'] = _row_to_dict(cur.fetchone())

            cur.execute(by_dept_sql, (month_start, month_end))
            stats['by_dept'] = [
                {'key': (r.Department or '—'), **_row_to_dict(r)} for r in cur.fetchall()
            ]
            cur.execute(by_shift_sql, (month_start, month_end))
            stats['by_shift'] = [
                {'key': f"Turno {r.ShiftNumber}", **_row_to_dict(r)} for r in cur.fetchall()
            ]
        return stats


# ─── Helpers ─────────────────────────────────────────────────────────────────
_MONTH_NAMES_IT = ['', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
                   'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']


def _month_label(d):
    return f"{_MONTH_NAMES_IT[d.month]} {d.year}"


def _rate(confirmed, total):
    return (confirmed / total * 100.0) if total else 0.0


def _rate_color(pct):
    if pct >= 95:
        return '#2E7D32'   # verde
    if pct >= 80:
        return '#F9A825'   # ambra
    return '#C62828'       # rosso


def _build_monthly_report_html(report_month, stats):
    """Costruisce l'HTML del report mensile cambi turno (con logo inline)."""
    m = stats['month']
    y = stats['ytd']
    m_rate = _rate(m['confirmed'], m['total'])
    y_rate = _rate(y['confirmed'], y['total'])

    def _summary_card(title, data, subtitle):
        pct = _rate(data['confirmed'], data['total'])
        return f"""
        <td style="padding:10px;">
          <div style="border:1px solid #e0e0e0;border-radius:8px;padding:16px;background:#fafafa;">
            <div style="font-size:12px;color:#777;text-transform:uppercase;letter-spacing:.5px;">{title}</div>
            <div style="font-size:11px;color:#999;margin-bottom:8px;">{subtitle}</div>
            <table style="width:100%;font-size:13px;">
              <tr><td style="color:#555;padding:2px 0;">Totale consegne</td><td style="text-align:right;font-weight:bold;">{data['total']}</td></tr>
              <tr><td style="color:#2E7D32;padding:2px 0;">Confermate</td><td style="text-align:right;font-weight:bold;color:#2E7D32;">{data['confirmed']}</td></tr>
              <tr><td style="color:#C62828;padding:2px 0;">Non confermate</td><td style="text-align:right;font-weight:bold;color:#C62828;">{data['not_confirmed']}</td></tr>
            </table>
            <div style="margin-top:10px;text-align:center;">
              <span style="font-size:26px;font-weight:bold;color:{_rate_color(pct)};">{pct:.1f}%</span>
              <div style="font-size:11px;color:#999;">tasso di conferma</div>
            </div>
          </div>
        </td>"""

    def _breakdown_rows(items):
        if not items:
            return '<tr><td colspan="5" style="padding:10px;text-align:center;color:#999;">Nessun dato</td></tr>'
        rows = []
        for it in items:
            pct = _rate(it['confirmed'], it['total'])
            rows.append(f"""
            <tr>
              <td style="padding:8px 12px;border-bottom:1px solid #eee;">{it['key']}</td>
              <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:center;">{it['total']}</td>
              <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:center;color:#2E7D32;">{it['confirmed']}</td>
              <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:center;color:#C62828;">{it['not_confirmed']}</td>
              <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:center;font-weight:bold;color:{_rate_color(pct)};">{pct:.1f}%</td>
            </tr>""")
        return ''.join(rows)

    def _breakdown_table(title, items):
        return f"""
        <h3 style="color:#37474F;margin:24px 0 8px 0;font-size:15px;">{title}</h3>
        <table style="width:100%;border-collapse:collapse;font-size:13px;border:1px solid #e0e0e0;">
          <tr style="background:#37474F;color:#fff;">
            <th style="padding:8px 12px;text-align:left;">Voce</th>
            <th style="padding:8px 12px;">Consegne</th>
            <th style="padding:8px 12px;">Confermate</th>
            <th style="padding:8px 12px;">Non conf.</th>
            <th style="padding:8px 12px;">% Conferma</th>
          </tr>
          {_breakdown_rows(items)}
        </table>"""

    now_str = datetime.now().strftime('%d/%m/%Y %H:%M')

    return f"""
<html><body style="font-family:'Segoe UI',Arial,sans-serif;color:#333;margin:0;padding:0;background:#f4f6f8;">
  <div style="max-width:720px;margin:0 auto;padding:20px;">
    <div style="background:#fff;border-radius:10px;overflow:hidden;border:1px solid #e0e0e0;">
      <div style="border-bottom:3px solid #37474F;padding:18px 24px;">
        <table width="100%"><tr>
          <td style="font-size:20px;font-weight:bold;color:#37474F;">
            Report Mensile &mdash; Cambi Turno
          </td>
          <td style="text-align:right;">
            <img src="cid:company_logo" alt="Vandewiele" style="width:120px;height:auto;"/>
          </td>
        </tr></table>
        <div style="font-size:14px;color:#777;margin-top:4px;">Periodo: <strong>{_month_label(report_month)}</strong></div>
      </div>

      <div style="padding:20px 24px;">
        <p style="font-size:14px;line-height:1.6;">
          Riepilogo della compliance dei cambi turno: numero di consegne registrate,
          confermate e non confermate dal capo turno entrante. La colonna
          <em>Non confermate</em> rappresenta i cambi turno che hanno generato un alert di ritardo.
        </p>

        <table width="100%" style="margin:8px 0;"><tr>
          {_summary_card('Mese di riferimento', m, _month_label(report_month))}
          {_summary_card('Rolling da inizio anno', y, f'01/01/{report_month.year} → {_month_label(report_month)}')}
        </tr></table>

        {_breakdown_table('Dettaglio per reparto (mese)', stats['by_dept'])}
        {_breakdown_table('Dettaglio per turno (mese)', stats['by_shift'])}

        <p style="font-size:13px;color:#555;margin-top:24px;line-height:1.6;">
          Tasso di conferma mese: <strong style="color:{_rate_color(m_rate)};">{m_rate:.1f}%</strong> &nbsp;|&nbsp;
          Rolling YTD: <strong style="color:{_rate_color(y_rate)};">{y_rate:.1f}%</strong>
        </p>
      </div>

      <div style="padding:14px 24px;border-top:1px solid #eee;background:#fafafa;">
        <p style="font-size:11px;color:#999;line-height:1.5;margin:0;">
          Report generato automaticamente da TraceabilityRS il {now_str}.<br/>
          &copy; {datetime.now().year} Vandewiele Romania &mdash; All rights reserved.
        </p>
      </div>
    </div>
  </div>
</body></html>"""


# ─── Suoni ───────────────────────────────────────────────────────────────────
def _play_alert():
    def _beep():
        try:
            for _ in range(3):
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                time.sleep(0.4)
        except Exception:
            pass
    threading.Thread(target=_beep, daemon=True).start()
