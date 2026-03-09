# -*- coding: utf-8 -*-
"""
GUI per la sezione Regole del modulo Ospiti.
Menu: Operazioni → Personale → Ospiti → Settings → Regole
Tab 1: Configurazione (firmatari, email, contratti)
Tab 2: Storico (processi eseguiti, documenti, rilancio)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
import os
import tempfile

logger = logging.getLogger("TraceabilityRS")


class GuestRulesWindow(tk.Toplevel):
    """Finestra Regole per la configurazione e gestione rapporti attività."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name

        self.title(self.lang.get('guest_rules_title', 'Regole Ospiti — Rapporti Attività'))
        self.geometry('1050x650')
        self.transient(parent)
        self.grab_set()

        self._settings_vars = {}
        self._contract_data = {}  # {iid: contract_info_id}

        self._build_ui()
        self._load_settings()
        self._load_contracts()
        self._load_reports()

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    # ================================================================
    # BUILD UI
    # ================================================================
    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Tab 1: Configurazione
        self._build_config_tab(notebook)
        # Tab 2: Storico
        self._build_history_tab(notebook)

    # ----------------------------------------------------------------
    # TAB 1 — CONFIGURAZIONE
    # ----------------------------------------------------------------
    def _build_config_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text=self.lang.get('tab_config', '⚙ Configurazione'))

        # --- Firmatari VR ---
        vr_frame = ttk.LabelFrame(tab,
            text=self.lang.get('config_vr_signatory', 'Firmatario Vandewiele Romania (Chi Richiede)'),
            padding=10)
        vr_frame.pack(fill='x', pady=(0, 10))

        self._add_setting_row(vr_frame, 0, 'chi_richiede',
            self.lang.get('lbl_name', 'Nome e Cognome:'))
        self._add_setting_row(vr_frame, 1, 'chi_richiede_titolo',
            self.lang.get('lbl_title', 'Funzione/Titolo:'))
        self._add_setting_row(vr_frame, 2, 'chi_richiede_email',
            'Email:')

        # --- Firmatario società esterna ---
        ext_frame = ttk.LabelFrame(tab,
            text=self.lang.get('config_ext_signatory', 'Firmatario Società Esterna (Chi Invia)'),
            padding=10)
        ext_frame.pack(fill='x', pady=(0, 10))

        self._add_setting_row(ext_frame, 0, 'chi_invia',
            self.lang.get('lbl_name', 'Nome e Cognome:'))
        self._add_setting_row(ext_frame, 1, 'chi_invia_titolo',
            self.lang.get('lbl_title', 'Funzione/Titolo:'))
        self._add_setting_row(ext_frame, 2, 'chi_invia_email',
            'Email:')

        # Bottone Salva Settings
        ttk.Button(tab, text=self.lang.get('btn_save_settings', '💾 Salva Impostazioni'),
                   command=self._save_settings).pack(pady=5, anchor='w')

        # --- Contratti ---
        contract_frame = ttk.LabelFrame(tab,
            text=self.lang.get('config_contracts', 'Contratti Società Fatturanti'),
            padding=10)
        contract_frame.pack(fill='both', expand=True, pady=(10, 0))

        # TreeView contratti
        cols = ('id', 'company', 'contract_no', 'contract_date', 'description')
        self.contract_tree = ttk.Treeview(contract_frame, columns=cols,
                                           show='headings', height=5, selectmode='browse')
        self.contract_tree.heading('id', text='ID')
        self.contract_tree.heading('company', text=self.lang.get('col_company', 'Società'))
        self.contract_tree.heading('contract_no', text=self.lang.get('col_contract_no', 'N. Contratto'))
        self.contract_tree.heading('contract_date', text=self.lang.get('col_contract_date', 'Data'))
        self.contract_tree.heading('description', text=self.lang.get('col_description', 'Descrizione'))

        self.contract_tree.column('id', width=40, anchor='center')
        self.contract_tree.column('company', width=200)
        self.contract_tree.column('contract_no', width=120)
        self.contract_tree.column('contract_date', width=100, anchor='center')
        self.contract_tree.column('description', width=300)

        self.contract_tree.pack(fill='both', expand=True)
        self.contract_tree.bind('<<TreeviewSelect>>', self._on_contract_select)

        # Form contratto
        cf = ttk.Frame(contract_frame, padding=5)
        cf.pack(fill='x', pady=(5, 0))

        ttk.Label(cf, text=self.lang.get('col_company', 'Società:')).grid(
            row=0, column=0, sticky='w', padx=3)
        self.contract_company_var = tk.StringVar()
        self.contract_company_combo = ttk.Combobox(cf, textvariable=self.contract_company_var,
                                                    width=25, state='readonly')
        self.contract_company_combo.grid(row=0, column=1, padx=3, sticky='w')

        ttk.Label(cf, text=self.lang.get('col_contract_no', 'N. Contratto:')).grid(
            row=0, column=2, sticky='w', padx=3)
        self.contract_no_var = tk.StringVar()
        ttk.Entry(cf, textvariable=self.contract_no_var, width=15).grid(
            row=0, column=3, padx=3, sticky='w')

        ttk.Label(cf, text=self.lang.get('col_contract_date', 'Data:')).grid(
            row=0, column=4, sticky='w', padx=3)
        self.contract_date_var = tk.StringVar()
        ttk.Entry(cf, textvariable=self.contract_date_var, width=12).grid(
            row=0, column=5, padx=3, sticky='w')

        ttk.Label(cf, text=self.lang.get('col_description', 'Desc:')).grid(
            row=1, column=0, sticky='w', padx=3, pady=3)
        self.contract_desc_var = tk.StringVar()
        ttk.Entry(cf, textvariable=self.contract_desc_var, width=60).grid(
            row=1, column=1, columnspan=5, padx=3, pady=3, sticky='ew')

        btn_cf = ttk.Frame(cf)
        btn_cf.grid(row=2, column=0, columnspan=6, sticky='w', pady=5)
        ttk.Button(btn_cf, text=self.lang.get('btn_new', '➕ Nuovo'),
                   command=self._new_contract).pack(side='left', padx=3)
        ttk.Button(btn_cf, text=self.lang.get('btn_save', '💾 Salva'),
                   command=self._save_contract).pack(side='left', padx=3)

    def _add_setting_row(self, parent, row, setting_key, label_text):
        """Aggiunge una riga di setting."""
        ttk.Label(parent, text=label_text).grid(
            row=row, column=0, sticky='w', padx=5, pady=3)
        var = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=var, width=50)
        entry.grid(row=row, column=1, padx=5, pady=3, sticky='ew')
        parent.columnconfigure(1, weight=1)
        self._settings_vars[setting_key] = var

    # ----------------------------------------------------------------
    # TAB 2 — STORICO
    # ----------------------------------------------------------------
    def _build_history_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=10)
        notebook.add(tab, text=self.lang.get('tab_history', '📋 Storico Rapporti'))

        # Toolbar
        toolbar = ttk.Frame(tab)
        toolbar.pack(fill='x', pady=(0, 5))

        ttk.Button(toolbar, text=self.lang.get('btn_generate', '🔄 Genera Documenti'),
                   command=self._generate_for_selected).pack(side='left', padx=3)
        ttk.Button(toolbar, text=self.lang.get('btn_send_email', '📧 Invia Email'),
                   command=self._send_email_for_selected).pack(side='left', padx=3)
        ttk.Button(toolbar, text=self.lang.get('btn_download_docs', '📥 Scarica Documenti'),
                   command=self._download_documents).pack(side='left', padx=3)
        ttk.Button(toolbar, text=self.lang.get('btn_refresh', '🔄 Aggiorna'),
                   command=self._load_reports).pack(side='right', padx=3)

        # TreeView rapporti
        cols = ('id', 'guest', 'company', 'period', 'doc_date', 'email_sent', 'created')
        self.report_tree = ttk.Treeview(tab, columns=cols, show='headings',
                                         height=15, selectmode='browse')
        self.report_tree.heading('id', text='ID')
        self.report_tree.heading('guest', text=self.lang.get('col_guest_name', 'Ospite'))
        self.report_tree.heading('company', text=self.lang.get('col_company', 'Società'))
        self.report_tree.heading('period', text=self.lang.get('col_period', 'Periodo'))
        self.report_tree.heading('doc_date', text=self.lang.get('col_report_date', 'Data Rapporto'))
        self.report_tree.heading('email_sent', text=self.lang.get('col_email_sent', 'Email Inviata'))
        self.report_tree.heading('created', text=self.lang.get('col_created', 'Creato'))

        self.report_tree.column('id', width=40, anchor='center')
        self.report_tree.column('guest', width=180)
        self.report_tree.column('company', width=180)
        self.report_tree.column('period', width=150, anchor='center')
        self.report_tree.column('doc_date', width=100, anchor='center')
        self.report_tree.column('email_sent', width=140, anchor='center')
        self.report_tree.column('created', width=140, anchor='center')

        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=self.report_tree.yview)
        self.report_tree.configure(yscrollcommand=scrollbar.set)
        self.report_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self._report_data = {}  # {iid: report_id}

    # ================================================================
    # DATA LOADING
    # ================================================================
    def _load_settings(self):
        """Carica i settings dal DB."""
        for key in ['chi_richiede', 'chi_richiede_titolo', 'chi_richiede_email',
                     'chi_invia', 'chi_invia_titolo', 'chi_invia_email']:
            try:
                cursor = self.db.conn.cursor()
                cursor.execute(
                    "SELECT [value] FROM traceability_rs.dbo.Settings WHERE atribute = ?",
                    (key,))
                row = cursor.fetchone()
                cursor.close()
                if row and key in self._settings_vars:
                    self._settings_vars[key].set(row[0] or '')
            except Exception as e:
                logger.error(f"Errore lettura setting '{key}': {e}")

    def _load_contracts(self):
        """Carica i contratti delle società fatturanti."""
        try:
            self.contract_tree.delete(*self.contract_tree.get_children())
            self._contract_data = {}

            # Carica combo società
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT VisitorPlanToChargeID, CompanyName
                FROM Employee.dbo.VisitorPlanToCharges
                WHERE MustCharged = 1 AND CompanyName IS NOT NULL
                ORDER BY CompanyName
            """)
            companies = []
            self._charge_ids = {}  # {CompanyName: VisitorPlanToChargeID}
            for row in cursor.fetchall():
                companies.append(row.CompanyName)
                self._charge_ids[row.CompanyName] = row.VisitorPlanToChargeID
            self.contract_company_combo['values'] = companies

            # Carica contratti esistenti
            cursor.execute("""
                SELECT vci.VisitorContractInfoId, vpc.CompanyName,
                       vci.ContractNumber, vci.ContractDate, vci.ContractDescription
                FROM Employee.dbo.VisitorContractInfo vci
                INNER JOIN Employee.dbo.VisitorPlanToCharges vpc
                    ON vci.VisitorPlanToChargeID = vpc.VisitorPlanToChargeID
                ORDER BY vpc.CompanyName
            """)
            for row in cursor.fetchall():
                date_str = row.ContractDate.strftime('%d/%m/%Y') if row.ContractDate else ''
                iid = self.contract_tree.insert('', 'end', values=(
                    row.VisitorContractInfoId,
                    row.CompanyName or '',
                    row.ContractNumber or '',
                    date_str,
                    row.ContractDescription or ''
                ))
                self._contract_data[iid] = row.VisitorContractInfoId
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento contratti: {e}")

    def _load_reports(self):
        """Carica lo storico dei rapporti generati."""
        try:
            self.report_tree.delete(*self.report_tree.get_children())
            self._report_data = {}

            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT var.VisitorActivityReportId, v.GuestName, v.CompanyName,
                       v.StartVisit, v.EndVisit,
                       var.ActivityReportDate, var.EmailSentDate, var.CreatedAt
                FROM Employee.dbo.VisitorActivityReports var
                INNER JOIN Employee.dbo.Visitors v ON var.VisitorId = v.VisitorId
                ORDER BY var.CreatedAt DESC
            """)
            for row in cursor.fetchall():
                start_str = row.StartVisit.strftime('%d/%m/%Y') if row.StartVisit else ''
                end_str = row.EndVisit.strftime('%d/%m/%Y') if row.EndVisit else ''
                period = f"{start_str} — {end_str}"
                doc_date = row.ActivityReportDate.strftime('%d/%m/%Y') if row.ActivityReportDate else ''
                email_str = row.EmailSentDate.strftime('%d/%m/%Y %H:%M') if row.EmailSentDate else '❌'
                created_str = row.CreatedAt.strftime('%d/%m/%Y %H:%M') if row.CreatedAt else ''

                iid = self.report_tree.insert('', 'end', values=(
                    row.VisitorActivityReportId,
                    row.GuestName or '',
                    row.CompanyName or '',
                    period,
                    doc_date,
                    email_str,
                    created_str
                ))
                self._report_data[iid] = row.VisitorActivityReportId
            cursor.close()
            logger.info(f"Caricati {len(self._report_data)} rapporti attività")
        except Exception as e:
            logger.error(f"Errore caricamento rapporti: {e}")

    # ================================================================
    # SETTINGS ACTIONS
    # ================================================================
    def _save_settings(self):
        """Salva tutti i settings nel DB."""
        try:
            cursor = self.db.conn.cursor()
            for key, var in self._settings_vars.items():
                value = var.get().strip()
                cursor.execute("""
                    IF EXISTS (SELECT 1 FROM traceability_rs.dbo.Settings WHERE atribute = ?)
                        UPDATE traceability_rs.dbo.Settings SET [value] = ? WHERE atribute = ?
                    ELSE
                        INSERT INTO traceability_rs.dbo.Settings (atribute, [value]) VALUES (?, ?)
                """, (key, value, key, key, value))
            self.db.conn.commit()
            cursor.close()
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('settings_saved', 'Impostazioni salvate con successo.'))
            logger.info("Settings firmatari salvati")
        except Exception as e:
            logger.error(f"Errore salvataggio settings: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")

    # ================================================================
    # CONTRACT ACTIONS
    # ================================================================
    def _on_contract_select(self, event=None):
        sel = self.contract_tree.selection()
        if not sel:
            return
        values = self.contract_tree.item(sel[0], 'values')
        self.contract_company_var.set(values[1])
        self.contract_no_var.set(values[2])
        self.contract_date_var.set(values[3])
        self.contract_desc_var.set(values[4])

    def _new_contract(self):
        self.contract_tree.selection_remove(*self.contract_tree.selection())
        self.contract_company_var.set('')
        self.contract_no_var.set('')
        self.contract_date_var.set('')
        self.contract_desc_var.set('')

    def _save_contract(self):
        company = self.contract_company_var.get().strip()
        contract_no = self.contract_no_var.get().strip()
        date_str = self.contract_date_var.get().strip()
        desc = self.contract_desc_var.get().strip()

        if not company:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_company', 'Selezionare una società.'))
            return

        charge_id = self._charge_ids.get(company)
        if not charge_id:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                'Società non trovata.')
            return

        contract_date = None
        if date_str:
            try:
                from datetime import datetime
                contract_date = datetime.strptime(date_str, '%d/%m/%Y').date()
            except ValueError:
                messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                    self.lang.get('invalid_date', 'Formato data non valido (GG/MM/AAAA).'))
                return

        try:
            cursor = self.db.conn.cursor()
            sel = self.contract_tree.selection()
            if sel and sel[0] in self._contract_data:
                # UPDATE
                contract_id = self._contract_data[sel[0]]
                cursor.execute("""
                    UPDATE Employee.dbo.VisitorContractInfo
                    SET ContractNumber = ?, ContractDate = ?, ContractDescription = ?,
                        VisitorPlanToChargeID = ?
                    WHERE VisitorContractInfoId = ?
                """, (contract_no or None, contract_date, desc or None,
                      charge_id, contract_id))
                logger.info(f"Aggiornato contratto ID={contract_id}")
            else:
                # INSERT
                cursor.execute("""
                    INSERT INTO Employee.dbo.VisitorContractInfo
                        (VisitorPlanToChargeID, ContractNumber, ContractDate, ContractDescription)
                    VALUES (?, ?, ?, ?)
                """, (charge_id, contract_no or None, contract_date, desc or None))
                logger.info(f"Nuovo contratto per {company}")

            self.db.conn.commit()
            cursor.close()
            messagebox.showinfo(self.lang.get('success', 'Successo'),
                self.lang.get('data_saved', 'Dati salvati con successo.'))
            self._load_contracts()
        except Exception as e:
            logger.error(f"Errore salvataggio contratto: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")

    # ================================================================
    # REPORT ACTIONS
    # ================================================================
    def _get_selected_report_id(self):
        sel = self.report_tree.selection()
        if not sel:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_record', 'Selezionare un record dalla lista.'))
            return None
        return self._report_data.get(sel[0])

    def _generate_for_selected(self):
        """Rilancia la generazione documenti per il report selezionato."""
        report_id = self._get_selected_report_id()
        if not report_id:
            return

        if not messagebox.askyesno(self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_regenerate',
                'Rigenerare i documenti? I precedenti saranno sovrascritti.')):
            return

        try:
            from guest_activity_reports import GuestActivityReportGenerator

            # Recupera visitor_id dal report
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT VisitorId, ActivityDescription
                FROM Employee.dbo.VisitorActivityReports
                WHERE VisitorActivityReportId = ?
            """, (report_id,))
            row = cursor.fetchone()
            cursor.close()

            if not row:
                return

            # Rigenera
            gen = GuestActivityReportGenerator(self.db)
            # Elimina il vecchio report
            cursor = self.db.conn.cursor()
            cursor.execute("""
                DELETE FROM Employee.dbo.VisitorActivityReports
                WHERE VisitorActivityReportId = ?
            """, (report_id,))
            self.db.conn.commit()
            cursor.close()

            new_id = gen.process_visitor(row.VisitorId,
                                          activity_description=row.ActivityDescription or '',
                                          created_by=self.user_name)
            if new_id:
                messagebox.showinfo(self.lang.get('success', 'Successo'),
                    self.lang.get('docs_regenerated', 'Documenti rigenerati con successo.'))
                self._load_reports()
            else:
                messagebox.showerror(self.lang.get('error', 'Errore'),
                    self.lang.get('generation_failed', 'Errore nella generazione.'))
        except Exception as e:
            logger.error(f"Errore rigenerazione: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")

    def _send_email_for_selected(self):
        """Invia email per il report selezionato."""
        report_id = self._get_selected_report_id()
        if not report_id:
            return

        if not messagebox.askyesno(self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_send_report', 'Inviare il rapporto via email?')):
            return

        try:
            from guest_activity_reports import GuestActivityReportGenerator
            gen = GuestActivityReportGenerator(self.db)
            success = gen.send_activity_email(report_id)
            if success:
                messagebox.showinfo(self.lang.get('success', 'Successo'),
                    self.lang.get('email_sent_ok', 'Email inviata con successo.'))
                self._load_reports()
            else:
                messagebox.showerror(self.lang.get('error', 'Errore'),
                    self.lang.get('email_send_failed', 'Errore nell\'invio email.'))
        except Exception as e:
            logger.error(f"Errore invio email rapporto: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")

    def _download_documents(self):
        """Scarica i documenti Word del report selezionato."""
        report_id = self._get_selected_report_id()
        if not report_id:
            return

        try:
            folder = filedialog.askdirectory(
                title=self.lang.get('select_folder', 'Seleziona cartella'))
            if not folder:
                return

            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT var.RequestLetterDoc, var.AcceptanceLetterDoc, var.ActivityReportDoc,
                       v.GuestName
                FROM Employee.dbo.VisitorActivityReports var
                INNER JOIN Employee.dbo.Visitors v ON var.VisitorId = v.VisitorId
                WHERE var.VisitorActivityReportId = ?
            """, (report_id,))
            row = cursor.fetchone()
            cursor.close()

            if not row:
                return

            guest_name = (row.GuestName or 'guest').replace(' ', '_')
            saved = 0

            for doc_name, doc_bytes in [
                (f'Richiesta_Intervento_{guest_name}.docx', row.RequestLetterDoc),
                (f'Accettazione_{guest_name}.docx', row.AcceptanceLetterDoc),
                (f'Rapporto_Attivita_{guest_name}.docx', row.ActivityReportDoc)
            ]:
                if doc_bytes:
                    filepath = os.path.join(folder, doc_name)
                    with open(filepath, 'wb') as f:
                        f.write(doc_bytes)
                    saved += 1

            messagebox.showinfo(self.lang.get('success', 'Successo'),
                f"{saved} {self.lang.get('docs_downloaded', 'documenti scaricati in')} {folder}")
            logger.info(f"Scaricati {saved} documenti per report {report_id}")

        except Exception as e:
            logger.error(f"Errore download documenti: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")
