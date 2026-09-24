# -*- coding: utf-8 -*-
"""
usage_stats_gui.py — Statistiche mensili di utilizzo delle form.

Legge Traceability_RS.eqp.UsersLogs (già popolata da main.py a ogni login /
apertura form) e mostra, per il mese selezionato, quante volte ogni form è
stata aperta e da quanti utenti distinti. Serve a decidere quali funzionalità
mantenere e quali rimuovere.

Il campo Activity contiene valori eterogenei:
  - chiavi di traduzione del menu (es. 'submenu_assign') per le azioni con
    autorizzazione (_execute_authorized_action);
  - nomi di funzione (es. 'open_scrap_validation_with_login') per il login
    semplice (_execute_simple_login).
_resolve_activity_label() normalizza entrambi in un'etichetta leggibile.
"""
import os
import logging
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
import calendar

logger = logging.getLogger(__name__)

# Voce di log da escludere: è la finestra statistica stessa.
SELF_ACTIVITY = 'open_usage_statistics_with_login'

_MONTHS = {
    'it': ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
           'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'],
    'en': list(calendar.month_name)[1:],
    'ro': ['ianuarie', 'februarie', 'martie', 'aprile', 'mai', 'iunie',
           'iulie', 'august', 'septembrie', 'octombrie', 'noiembrie', 'decembrie'],
    'de': ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
           'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
    'sv': ['januari', 'februari', 'mars', 'april', 'maj', 'juni',
           'juli', 'augusti', 'september', 'oktober', 'november', 'december'],
}


def open_usage_statistics(parent, db, lang):
    UsageStatisticsWindow(parent, db, lang)


class UsageStatisticsWindow(tk.Toplevel):
    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        L = self.lang.get
        self.title(L('us_title', 'Statistiche uso form'))
        self.geometry('900x600')
        self.transient(parent)
        self._rows = []  # (label, activity_raw, opens, users, pct)
        self._period = (None, None)
        self._build()
        self._load_years()
        self._generate()

    # ── UI ────────────────────────────────────────────────────────────────

    def _build(self):
        L = self.lang.get
        flt = ttk.LabelFrame(self, text=L('filters', 'Filtri'), padding=8)
        flt.pack(fill=tk.X, padx=10, pady=8)

        ttk.Label(flt, text=L('us_month', 'Mese') + ':').pack(side=tk.LEFT, padx=(0, 4))
        self.month_combo = ttk.Combobox(flt, width=16, state='readonly')
        self.month_combo.pack(side=tk.LEFT, padx=(0, 12))

        ttk.Label(flt, text=L('us_year', 'Anno') + ':').pack(side=tk.LEFT, padx=(0, 4))
        self.year_combo = ttk.Combobox(flt, width=8, state='readonly')
        self.year_combo.pack(side=tk.LEFT, padx=(0, 12))

        self.whole_year_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(flt, text=L('us_whole_year', 'Tutto l\'anno'),
                        variable=self.whole_year_var,
                        command=self._toggle_month).pack(side=tk.LEFT, padx=(0, 12))

        ttk.Button(flt, text=L('us_generate', 'Genera'),
                   command=self._generate).pack(side=tk.LEFT, padx=4)
        ttk.Button(flt, text=L('us_excel', '📊 Excel'),
                   command=self._export_excel).pack(side=tk.LEFT, padx=4)

        wrap = ttk.Frame(self)
        wrap.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        cols = ('form', 'key', 'opens', 'users', 'pct')
        self.tree = ttk.Treeview(wrap, columns=cols, show='headings', selectmode='browse')
        for c, t, w, a in (('form', L('us_col_form', 'Form'), 320, 'w'),
                           ('key', L('us_col_key', 'Chiave/Funzione'), 240, 'w'),
                           ('opens', L('us_col_opens', 'Aperture'), 90, 'e'),
                           ('users', L('us_col_users', 'Utenti unici'), 100, 'e'),
                           ('pct', L('us_col_pct', '% del totale'), 100, 'e')):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor=a)
        vsb = ttk.Scrollbar(wrap, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        wrap.rowconfigure(0, weight=1)
        wrap.columnconfigure(0, weight=1)

        self.count_lbl = ttk.Label(self, text='', foreground='#555')
        self.count_lbl.pack(anchor='w', padx=12, pady=(2, 6))

    def _toggle_month(self):
        state = 'disabled' if self.whole_year_var.get() else 'readonly'
        self.month_combo.configure(state=state)

    def _load_years(self):
        """Popola mese/anno; default = mese precedente."""
        L = self.lang.get
        lang_code = getattr(self.lang, 'current_language', 'it')
        month_names = _MONTHS.get(lang_code, _MONTHS['en'])
        self.month_combo['values'] = [
            f'{i + 1:02d} - {name}' for i, name in enumerate(month_names)]

        today = date.today()
        first_of_month = today.replace(day=1)
        prev = date(first_of_month.year - 1, 12, 1) if first_of_month.month == 1 \
            else date(first_of_month.year, first_of_month.month - 1, 1)
        self._default_month = prev.month
        self._default_year = prev.year
        self.month_combo.current(prev.month - 1)

        years = {today.year, prev.year}
        try:
            cur = self.db.conn.cursor()
            cur.execute("SELECT DISTINCT YEAR(DateLog) FROM Traceability_RS.eqp.UsersLogs "
                        "WHERE DateLog IS NOT NULL")
            years.update(int(r[0]) for r in cur.fetchall() if r[0] is not None)
            cur.close()
        except Exception as e:
            logger.warning(f"usage_stats: caricamento anni fallito: {e}")
        self.year_combo['values'] = [str(y) for y in sorted(years, reverse=True)]
        self.year_combo.set(str(prev.year))

    # ── Dati ──────────────────────────────────────────────────────────────

    def _period_bounds(self):
        """Restituisce (data_inizio, data_fine_esclusa) per il periodo selezionato."""
        year = int(self.year_combo.get())
        if self.whole_year_var.get():
            return date(year, 1, 1), date(year + 1, 1, 1)
        month = self.month_combo.current() + 1
        start = date(year, month, 1)
        end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
        return start, end

    def _resolve_activity_label(self, activity):
        """Converte Activity (chiave traduzione o nome funzione) in etichetta leggibile."""
        if not activity:
            return ''
        # Chiave di traduzione nota? (cercata in tutte le lingue caricate)
        try:
            known_keys = set()
            for trans in self.lang.translations.values():
                known_keys.update(trans.keys())
            if activity in known_keys:
                resolved = self.lang.get(activity)
                if resolved and resolved != activity:
                    return resolved
        except Exception as e:
            logger.debug(f"usage_stats: risoluzione traduzione '{activity}' fallita: {e}")
        # Nome funzione open_xxx_with_login → "Xxx"
        name = activity
        if name.startswith('open_'):
            name = name[len('open_'):]
        if name.endswith('_with_login'):
            name = name[:-len('_with_login')]
        name = name.replace('_', ' ').strip()
        return name.title() if name else activity

    def _generate(self):
        L = self.lang.get
        self.tree.delete(*self.tree.get_children())
        self._rows = []
        start, end = self._period_bounds()
        self._period = (start, end)
        try:
            cur = self.db.conn.cursor()
            cur.execute(
                """
                SELECT Activity,
                       COUNT(*) AS Aperture,
                       COUNT(DISTINCT EmployeeHireHistoryId) AS Utenti
                FROM Traceability_RS.eqp.UsersLogs
                WHERE DateLog >= ? AND DateLog < ?
                GROUP BY Activity
                ORDER BY Aperture DESC
                """,
                datetime(start.year, start.month, start.day),
                datetime(end.year, end.month, end.day)
            )
            raw = [(r.Activity, int(r.Aperture or 0), int(r.Utenti or 0))
                   for r in cur.fetchall()]
            cur.close()
        except Exception as e:
            logger.error(f"usage_stats: query fallita: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'),
                                 f"Impossibile leggere i log di utilizzo:\n{e}", parent=self)
            return

        total = sum(n for _, n, _u in raw if _ != SELF_ACTIVITY)
        for activity, opens, users in raw:
            if activity == SELF_ACTIVITY:
                continue
            label = self._resolve_activity_label(activity)
            pct = (opens / total * 100.0) if total else 0.0
            self._rows.append((label, activity, opens, users, pct))
            self.tree.insert('', 'end', values=(
                label, activity, opens, users, f'{pct:.1f}%'))

        if total:
            self.tree.insert('', 'end', values=(
                L('us_total', 'Totale'), '', total,
                sum(u for _, _, _, u, _ in self._rows), '100.0%'),
                tags=('total',))
            self.tree.tag_configure('total', background='#E8E8E8')
        self.count_lbl.config(text=L('us_forms_found',
                                     '{0} form aperte nel periodo (totale aperture: {1})'
                                     ).format(len(self._rows), total))

    # ── Export Excel ──────────────────────────────────────────────────────

    def _export_excel(self):
        L = self.lang.get
        if not self._rows:
            messagebox.showinfo(L('us_title', 'Statistiche uso form'),
                                L('us_no_data', 'Nessun dato da esportare per il periodo selezionato.'),
                                parent=self)
            return
        start, _ = self._period
        suffix = f'{start.year}' if self.whole_year_var.get() \
            else f'{start.year}-{start.month:02d}'
        path = filedialog.asksaveasfilename(
            parent=self,
            defaultextension='.xlsx',
            initialfile=f'statistiche_form_aperte_{suffix}.xlsx',
            filetypes=[('Excel', '*.xlsx')])
        if not path:
            return
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment

            wb = Workbook()
            ws = wb.active
            ws.title = f'{suffix}'

            title = L('us_title', 'Statistiche uso form')
            ws.append([f'{title} — {suffix}'])
            ws.cell(row=1, column=1).font = Font(bold=True, size=13)

            headers = [L('us_col_form', 'Form'), L('us_col_key', 'Chiave/Funzione'),
                       L('us_col_opens', 'Aperture'), L('us_col_users', 'Utenti unici'),
                       L('us_col_pct', '% del totale')]
            ws.append([])
            ws.append(headers)
            hfill = PatternFill('solid', fgColor='D9E1F2')
            for col in range(1, len(headers) + 1):
                cell = ws.cell(row=3, column=col)
                cell.font = Font(bold=True)
                cell.fill = hfill
                cell.alignment = Alignment(horizontal='center')

            for label, activity, opens, users, pct in self._rows:
                ws.append([label, activity, opens, users, f'{pct:.1f}%'])

            total_opens = sum(r[2] for r in self._rows)
            total_users = sum(r[3] for r in self._rows)
            trow = ws.max_row + 1
            ws.append([L('us_total', 'Totale'), '', total_opens, total_users, '100.0%'])
            for col in range(1, len(headers) + 1):
                ws.cell(row=trow, column=col).font = Font(bold=True)

            for col, width in (('A', 40), ('B', 32), ('C', 12), ('D', 14), ('E', 14)):
                ws.column_dimensions[col].width = width

            wb.save(path)
            logger.info(f"usage_stats: export Excel salvato in {path}")
            if messagebox.askyesno(L('us_title', 'Statistiche uso form'),
                                   f"File salvato:\n{path}\n\nAprirlo adesso?",
                                   parent=self):
                os.startfile(path)
        except Exception as e:
            logger.error(f"usage_stats: export Excel fallito: {e}", exc_info=True)
            messagebox.showerror(L('error', 'Errore'),
                                 f"Impossibile salvare il file Excel:\n{e}", parent=self)
