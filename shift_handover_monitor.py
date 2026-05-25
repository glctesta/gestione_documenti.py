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

logger = logging.getLogger('TraceabilityRS')

POLL_INTERVAL_MS   = 60_000    # polling ogni 60s
ALERT_WINDOW_MIN   = 15        # minuti prima della fine turno: apre alert "compila"
CONFIRM_GRACE_MIN  = 30        # minuti dopo inizio turno: se non confermato → email

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


def _next_shift_start(shift_num, ref_date):
    """Restituisce datetime di inizio del turno SUCCESSIVO (per calcolo grazia conferma).

    Il turno successivo inizia alla stessa ora in cui finisce quello corrente:
      - Turno 1 finisce 15:30 → Turno 2 inizia 15:30 (stesso giorno)
      - Turno 2 finisce 23:30 → Turno 3 inizia 23:30 (stesso giorno)
      - Turno 3 finisce 07:30 → Turno 1 inizia 07:30 (giorno SUCCESSIVO a ref_date)
    """
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
        for shift_num in self._active_shifts:
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
                    grace_end  = next_start + timedelta(minutes=CONFIRM_GRACE_MIN)
                    if now > grace_end:
                        self._send_unconfirmed_alert(shift_num, shift_date, row[2], row[3])
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
        except Exception as e:
            logger.error(f"Errore invio email alert cambio turno: {e}", exc_info=True)


# ─── Helpers ─────────────────────────────────────────────────────────────────
def _play_alert():
    def _beep():
        try:
            for _ in range(3):
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                time.sleep(0.4)
        except Exception:
            pass
    threading.Thread(target=_beep, daemon=True).start()
