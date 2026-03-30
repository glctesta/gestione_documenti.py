"""
Modulo per la gestione dei programmi esterni (External IPs).
- ExternalIpsManagerWindow: finestra CRUD sulla tabella Employee.dbo.ExternalIps
- BrowserLauncherWindow:    scelta programma e apertura nel browser
"""
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import logging
import threading
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class ExternalIpsManagerWindow(tk.Toplevel):
    """Finestra CRUD per gestire IP/Programmi esterni (Employee.dbo.ExternalIps)."""

    QUERY_ACTIVE = """
        SELECT [ExternalIpID], [ExternalIP], [Port], [ProgramName]
        FROM [Employee].[dbo].[ExternalIps]
        WHERE [DateOut] IS NULL
        ORDER BY [ProgramName]
    """

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang

        self.title(self.lang.get('ext_programs_setup_title', 'SetUp IP - Programmi Esterni'))
        self.geometry('750x500')
        self.resizable(True, True)

        self._create_widgets()
        self._load_data()

        self.transient(parent)
        self.grab_set()

    # ── Widget ──────────────────────────────────────────────────────────
    def _create_widgets(self):
        # Bottoni azione
        actions = ttk.Frame(self)
        actions.pack(fill=tk.X, padx=8, pady=(8, 4))

        ttk.Button(actions, text=self.lang.get('add', 'Aggiungi'),
                   command=self._add).pack(side=tk.LEFT, padx=4)
        ttk.Button(actions, text=self.lang.get('edit', 'Modifica'),
                   command=self._edit).pack(side=tk.LEFT, padx=4)
        ttk.Button(actions, text=self.lang.get('delete', 'Elimina'),
                   command=self._soft_delete).pack(side=tk.LEFT, padx=4)
        ttk.Button(actions, text=self.lang.get('refresh', 'Aggiorna'),
                   command=self._load_data).pack(side=tk.LEFT, padx=4)

        # Treeview
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'IP', 'Port', 'Program'),
            show='headings',
            yscrollcommand=vsb.set
        )
        vsb.config(command=self.tree.yview)

        self.tree.heading('ID', text='ID')
        self.tree.heading('IP', text='IP')
        self.tree.heading('Port', text='Port')
        self.tree.heading('Program', text=self.lang.get('ext_program_name', 'Programma'))

        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('IP', width=200)
        self.tree.column('Port', width=80, anchor=tk.CENTER)
        self.tree.column('Program', width=250)

        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    # ── Dati ────────────────────────────────────────────────────────────
    def _load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            self.db.cursor.execute(self.QUERY_ACTIVE)
            for row in self.db.cursor.fetchall():
                self.tree.insert('', tk.END, values=(
                    row.ExternalIpID, row.ExternalIP, row.Port, row.ProgramName
                ))
        except Exception as e:
            logger.error(f"Errore caricamento ExternalIps: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('load_error', 'Errore caricamento')}: {e}",
                parent=self
            )

    # ── CRUD ────────────────────────────────────────────────────────────
    def _add(self):
        dialog = _ExternalIpDialog(self, self.db, self.lang, mode='add')
        self.wait_window(dialog)
        if dialog.result:
            self._load_data()

    def _edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('ext_select_row', 'Seleziona un record da modificare'),
                parent=self
            )
            return
        vals = self.tree.item(sel[0])['values']
        data = {'ID': vals[0], 'IP': vals[1], 'Port': vals[2], 'Program': vals[3]}
        dialog = _ExternalIpDialog(self, self.db, self.lang, mode='edit', data=data)
        self.wait_window(dialog)
        if dialog.result:
            self._load_data()

    def _soft_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('ext_select_row', 'Seleziona un record da eliminare'),
                parent=self
            )
            return
        vals = self.tree.item(sel[0])['values']
        rec_id = vals[0]
        program = vals[3]

        if not messagebox.askyesno(
            self.lang.get('confirm_delete', 'Conferma Eliminazione'),
            f"{self.lang.get('ext_confirm_delete', 'Disattivare il programma')} '{program}'?",
            parent=self
        ):
            return

        try:
            ip_val = vals[1]
            port_val = vals[2]
            self.db.cursor.execute(
                "UPDATE [Employee].[dbo].[ExternalIps] SET [DateOut] = GETDATE() WHERE [ExternalIpID] = ?",
                (rec_id,)
            )
            self.db.conn.commit()

            # Invia notifica email in background
            _send_ip_change_notification(
                self.db, 'deactivated', program, str(ip_val), str(port_val)
            )

            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('ext_deleted_ok', 'Programma disattivato'),
                parent=self
            )
            self._load_data()
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)


# ═══════════════════════════════════════════════════════════════════════
class _ExternalIpDialog(tk.Toplevel):
    """Dialog per aggiungere / modificare un ExternalIp."""

    def __init__(self, parent, db, lang, mode='add', data=None):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.mode = mode
        self.data = data
        self.result = False

        title = (self.lang.get('ext_add_title', 'Aggiungi Programma Esterno')
                 if mode == 'add'
                 else self.lang.get('ext_edit_title', 'Modifica Programma Esterno'))
        self.title(title)
        self.geometry('400x220')
        self.resizable(False, False)

        self._create_widgets()
        if mode == 'edit' and data:
            self._populate()

        self.transient(parent)
        self.grab_set()

    def _create_widgets(self):
        f = ttk.Frame(self, padding=16)
        f.pack(fill=tk.BOTH, expand=True)

        ttk.Label(f, text='IP:').grid(row=0, column=0, sticky=tk.W, pady=4)
        self.ip_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.ip_var, width=30).grid(row=0, column=1, sticky=tk.EW, padx=6, pady=4)

        ttk.Label(f, text='Port:').grid(row=1, column=0, sticky=tk.W, pady=4)
        self.port_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.port_var, width=30).grid(row=1, column=1, sticky=tk.EW, padx=6, pady=4)

        ttk.Label(f, text=self.lang.get('ext_program_name', 'Programma:')).grid(row=2, column=0, sticky=tk.W, pady=4)
        self.prog_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.prog_var, width=30).grid(row=2, column=1, sticky=tk.EW, padx=6, pady=4)

        btn = ttk.Frame(f)
        btn.grid(row=3, column=0, columnspan=2, pady=16)
        ttk.Button(btn, text=self.lang.get('save', 'Salva'), command=self._save).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn, text=self.lang.get('cancel', 'Annulla'), command=self.destroy).pack(side=tk.LEFT, padx=6)

        f.columnconfigure(1, weight=1)

    def _populate(self):
        self.ip_var.set(self.data['IP'])
        self.port_var.set(self.data['Port'])
        self.prog_var.set(self.data['Program'])

    def _save(self):
        ip = self.ip_var.get().strip()
        port = self.port_var.get().strip()
        prog = self.prog_var.get().strip()

        if not ip or not port or not prog:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('ext_all_fields_required', 'Tutti i campi sono obbligatori'),
                parent=self
            )
            return

        try:
            if self.mode == 'add':
                self.db.cursor.execute(
                    "INSERT INTO [Employee].[dbo].[ExternalIps] ([ExternalIP], [Port], [ProgramName]) VALUES (?, ?, ?)",
                    (ip, port, prog)
                )
            else:
                self.db.cursor.execute(
                    "UPDATE [Employee].[dbo].[ExternalIps] SET [ExternalIP]=?, [Port]=?, [ProgramName]=? WHERE [ExternalIpID]=?",
                    (ip, port, prog, self.data['ID'])
                )
            self.db.conn.commit()
            self.result = True

            # Invia notifica email in background
            if self.mode == 'add':
                _send_ip_change_notification(
                    self.db, 'added', prog, ip, port
                )
            else:
                old_vals = self.data or {}
                _send_ip_change_notification(
                    self.db, 'modified', prog, ip, port,
                    old_values={
                        'IP': str(old_vals.get('IP', '')),
                        'Port': str(old_vals.get('Port', '')),
                        'Program': str(old_vals.get('Program', ''))
                    }
                )

            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('ext_saved_ok', 'Salvato con successo'),
                parent=self
            )
            self.destroy()
        except Exception as e:
            self.db.conn.rollback()
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)


# ═══════════════════════════════════════════════════════════════════════
class BrowserLauncherWindow(tk.Toplevel):
    """Finestra per selezionare un programma esterno e aprirlo nel browser."""

    QUERY_ACTIVE = """
        SELECT [ExternalIpID], [ExternalIP], [Port], [ProgramName]
        FROM [Employee].[dbo].[ExternalIps]
        WHERE [DateOut] IS NULL
        ORDER BY [ProgramName]
    """

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.programs = []  # lista di dict

        self.title(self.lang.get('ext_browser_title', 'Apri Programma Esterno'))
        self.geometry('450x180')
        self.resizable(False, False)

        self._create_widgets()
        self._load_programs()

        self.transient(parent)
        self.grab_set()

    def _create_widgets(self):
        f = ttk.Frame(self, padding=20)
        f.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            f,
            text=self.lang.get('ext_select_program', 'Seleziona un programma:'),
            font=('Helvetica', 10)
        ).pack(anchor=tk.W, pady=(0, 8))

        self.combo_var = tk.StringVar()
        self.combo = ttk.Combobox(f, textvariable=self.combo_var, state='readonly', width=50)
        self.combo.pack(fill=tk.X, pady=(0, 16))

        btn_frame = ttk.Frame(f)
        btn_frame.pack()

        ttk.Button(
            btn_frame,
            text=self.lang.get('ext_open_browser_btn', '🌐 Apri nel Browser'),
            command=self._open_browser
        ).pack(side=tk.LEFT, padx=6)

        ttk.Button(
            btn_frame,
            text=self.lang.get('cancel', 'Annulla'),
            command=self.destroy
        ).pack(side=tk.LEFT, padx=6)

    def _load_programs(self):
        try:
            self.db.cursor.execute(self.QUERY_ACTIVE)
            self.programs = []
            display_values = []
            for row in self.db.cursor.fetchall():
                entry = {
                    'id': row.ExternalIpID,
                    'ip': row.ExternalIP,
                    'port': row.Port,
                    'name': row.ProgramName
                }
                self.programs.append(entry)
                display_values.append(row.ProgramName)
            self.combo['values'] = display_values
            if display_values:
                self.combo.current(0)
        except Exception as e:
            logger.error(f"Errore caricamento programmi: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)

    def _open_browser(self):
        idx = self.combo.current()
        if idx < 0 or not self.programs:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('ext_select_program', 'Seleziona un programma'),
                parent=self
            )
            return

        prog = self.programs[idx]
        url = f"http://{prog['ip']}:{prog['port']}"
        logger.info(f"Apertura browser: {url} ({prog['name']})")
        webbrowser.open(url)


# ═══════════════════════════════════════════════════════════════════════
# Notifica email per modifiche IP
# ═══════════════════════════════════════════════════════════════════════

def _send_ip_change_notification(db, change_type, program_name, ip, port, old_values=None):
    """
    Invia una notifica email professionale a tutti gli utenti SKILL attivi
    quando un IP esterno viene aggiunto, modificato o disattivato.

    Args:
        db: Database handler
        change_type: 'added', 'modified', 'deactivated'
        program_name: Nome del programma
        ip: Indirizzo IP corrente
        port: Porta corrente
        old_values: dict con IP/Port/Program precedenti (solo per 'modified')
    """
    def _do_send():
        try:
            from email_connector import EmailSender

            # 1. Query destinatari
            cursor = db.conn.cursor()
            cursor.execute("""
                SELECT e.employeename + ' ' + e.employeesurname AS Employee,
                       aa.WorkEmail
                FROM [Employee].[sks].[AppUsers] A
                INNER JOIN Employee.dbo.EmployeeHireHistory H
                    ON a.employeeid = h.employeeHireHistoryId
                    AND h.EndWorkDate IS NULL AND h.EmployeeRId = 2
                INNER JOIN Employee.dbo.Employees e
                    ON e.employeeid = h.employeeid AND a.IsActive = 1
                INNER JOIN Employee.dbo.EmployeeAddress AA
                    ON AA.EmployeeId = e.employeeid AND aa.DateOut IS NULL
                WHERE LEN(ISNULL(aa.WorkEmail, '')) > 0
            """)
            rows = cursor.fetchall()
            cursor.close()

            if not rows:
                logger.warning("IP change notification: nessun destinatario trovato")
                return

            emails = [r.WorkEmail.strip() for r in rows if r.WorkEmail and r.WorkEmail.strip()]
            if not emails:
                return

            # 2. Costruisci contenuto email
            change_label = {
                'added': 'New Program Added',
                'modified': 'Program Configuration Updated',
                'deactivated': 'Program Deactivated'
            }.get(change_type, 'Configuration Change')

            subject = f"System Update: External Program Configuration Change \u2014 {program_name}"

            # Dettagli modifica
            if change_type == 'modified' and old_values:
                details_html = f"""
                <table style="border-collapse: collapse; width: 100%; margin: 15px 0;">
                    <tr style="background-color: #f8f9fa;">
                        <th style="padding: 10px 15px; text-align: left; border: 1px solid #dee2e6; color: #495057;">Field</th>
                        <th style="padding: 10px 15px; text-align: left; border: 1px solid #dee2e6; color: #495057;">Previous Value</th>
                        <th style="padding: 10px 15px; text-align: left; border: 1px solid #dee2e6; color: #495057;">New Value</th>
                    </tr>
                    <tr>
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6; font-weight: bold;">Program Name</td>
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6;">{old_values.get('Program', '')}</td>
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6;">{program_name}</td>
                    </tr>
                    <tr style="background-color: #f8f9fa;">
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6; font-weight: bold;">IP Address</td>
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6;">{old_values.get('IP', '')}</td>
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6;">{ip}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6; font-weight: bold;">Port</td>
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6;">{old_values.get('Port', '')}</td>
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6;">{port}</td>
                    </tr>
                </table>
                """
            else:
                details_html = f"""
                <table style="border-collapse: collapse; width: 100%; margin: 15px 0;">
                    <tr style="background-color: #f8f9fa;">
                        <th style="padding: 10px 15px; text-align: left; border: 1px solid #dee2e6; color: #495057;">Field</th>
                        <th style="padding: 10px 15px; text-align: left; border: 1px solid #dee2e6; color: #495057;">Value</th>
                    </tr>
                    <tr>
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6; font-weight: bold;">Program Name</td>
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6;">{program_name}</td>
                    </tr>
                    <tr style="background-color: #f8f9fa;">
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6; font-weight: bold;">IP Address</td>
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6;">{ip}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6; font-weight: bold;">Port</td>
                        <td style="padding: 10px 15px; border: 1px solid #dee2e6;">{port}</td>
                    </tr>
                </table>
                """

            now_str = datetime.now().strftime('%B %d, %Y at %H:%M')

            body_html = f"""
            <html>
            <body style="font-family: 'Segoe UI', Arial, sans-serif; color: #333; margin: 0; padding: 0;">
                <div style="max-width: 650px; margin: 0 auto; padding: 20px;">
                    <!-- Header with logo -->
                    <div style="border-bottom: 3px solid #0056b3; padding-bottom: 15px; margin-bottom: 20px;">
                        <table width="100%" cellpadding="0" cellspacing="0">
                            <tr>
                                <td style="font-size: 22px; font-weight: bold; color: #0056b3;">
                                    External Program Configuration
                                </td>
                                <td style="text-align: right;">
                                    <img src="cid:company_logo" alt="Vandewiele" 
                                         style="width: 120px; height: auto;" />
                                </td>
                            </tr>
                        </table>
                    </div>

                    <!-- Change type badge -->
                    <div style="background-color: {'#28a745' if change_type == 'added' else '#ffc107' if change_type == 'modified' else '#dc3545'};
                                color: {'#fff' if change_type != 'modified' else '#333'};
                                display: inline-block; padding: 6px 16px; border-radius: 4px;
                                font-weight: bold; font-size: 13px; margin-bottom: 15px;">
                        {change_label.upper()}
                    </div>

                    <p style="font-size: 14px; line-height: 1.6;">
                        Dear Colleague,
                    </p>
                    <p style="font-size: 14px; line-height: 1.6;">
                        This is to inform you that a configuration change has been made to the 
                        external programs registry on <strong>{now_str}</strong>. 
                        Please find the details below:
                    </p>

                    {details_html}

                    {'<p style="font-size: 14px; line-height: 1.6;">You can access the program directly using the link below:</p><p style="text-align: center; margin: 20px 0;"><a href="http://' + ip + ':' + port + '" style="background-color: #0056b3; color: #ffffff; padding: 12px 28px; text-decoration: none; border-radius: 5px; font-size: 14px; font-weight: bold; display: inline-block;">&#x1F517; Open ' + program_name + ' &mdash; http://' + ip + ':' + port + '</a></p>' if change_type != 'deactivated' else ''}

                    <p style="font-size: 14px; line-height: 1.6;">
                        If you have any questions or need assistance accessing this program, 
                        please contact your department supervisor or the IT department.
                    </p>

                    <!-- Footer -->
                    <div style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #dee2e6;">
                        <p style="font-size: 11px; color: #888; line-height: 1.5;">
                            This is an automated notification generated by the TraceabilityRS system.
                            Please do not reply to this email.<br/>
                            &copy; {datetime.now().year} Vandewiele Romania &mdash; All rights reserved.
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """

            # 3. Invia email
            sender = EmailSender()
            sender.save_credentials("Accounting@Eutron.it", "9jHgFhSs7Vf+")

            primary_to = emails[0]
            cc_list = emails[1:] if len(emails) > 1 else None

            attachments = []
            logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
            if os.path.exists(logo_path):
                attachments.append(('inline', logo_path, 'company_logo'))

            sender.send_email(
                to_email=primary_to,
                subject=subject,
                body=body_html,
                is_html=True,
                attachments=attachments if attachments else None,
                cc_emails=cc_list
            )

            logger.info(
                f"IP change notification sent: {change_type} '{program_name}' "
                f"to {len(emails)} recipients"
            )

        except Exception as e:
            logger.error(f"Errore invio notifica modifica IP: {e}", exc_info=True)

    # Esegui in background thread
    t = threading.Thread(target=_do_send, daemon=True)
    t.start()


# ═══════════════════════════════════════════════════════════════════════
# Entry-point richiamati da main.py
# ═══════════════════════════════════════════════════════════════════════
def open_external_ips_manager(parent, db, lang):
    """Apre la finestra di gestione IP esterni (SetUp IP)."""
    ExternalIpsManagerWindow(parent, db, lang)


def open_browser_launcher(parent, db, lang):
    """Apre la finestra per selezionare e aprire un programma nel browser."""
    BrowserLauncherWindow(parent, db, lang)
