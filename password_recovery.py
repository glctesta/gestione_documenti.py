# -*- coding: utf-8 -*-
"""
Modulo per il recupero della password.
Consente agli utenti di recuperare le proprie credenziali tramite email.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
import os
import base64

logger = logging.getLogger("TraceabilityRS")


class PasswordRecoveryWindow(tk.Toplevel):
    """
    Finestra per il recupero password.
    L'utente può inserire uno o più campi per identificarsi e ricevere
    le credenziali via email.
    """

    def __init__(self, parent, db_handler, lang_manager):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager

        self.title(self.lang.get('password_recovery_title', 'Recupera Password'))
        self.geometry("800x580")
        self.resizable(True, True)

        # Variabili per i campi di input
        self.user_id_var = tk.StringVar()
        self.badge_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.cnp_var = tk.StringVar()

        # Recupero per operatore SENZA email aziendale (richiede autorizzazione capo reparto)
        self.for_other_var = tk.BooleanVar(value=False)
        self._authorized_for_other = False
        self._auth_user = None
        self.other_userid_var = tk.StringVar()
        self.other_name_var = tk.StringVar()
        self.other_dest_email_var = tk.StringVar()
        self.other_frame = None

        self._create_widgets()

    def _create_widgets(self):
        """Crea i widget della finestra"""
        # Frame principale
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_label = ttk.Label(
            main_frame,
            text=self.lang.get('password_recovery_header', 'Recupero Credenziali'),
            font=("Helvetica", 14, "bold")
        )
        header_label.pack(pady=(0, 15))

        # Istruzioni
        instruction_text = self.lang.get(
            'password_recovery_instructions',
            "Inserire l'email aziendale (OBBLIGATORIA). Gli altri campi sono opzionali e "
            "servono solo a restringere la ricerca. Le credenziali saranno inviate all'email aziendale registrata."
        )
        instruction_label = ttk.Label(
            main_frame,
            text=instruction_text,
            wraplength=450,
            justify=tk.LEFT
        )
        instruction_label.pack(pady=(0, 15))

        # Checkbox: recupero per operatore senza email aziendale
        self.for_other_check = ttk.Checkbutton(
            main_frame,
            text=self.lang.get('recovery_for_other_checkbox',
                               'Recupero per un operatore SENZA email aziendale (richiede autorizzazione)'),
            variable=self.for_other_var,
            command=self._on_toggle_for_other
        )
        self.for_other_check.pack(anchor=tk.W, pady=(0, 10))

        # Frame per i campi di input
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # ID Utente
        ttk.Label(
            fields_frame,
            text=self.lang.get('label_user_id', 'ID Utente:')
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Entry(
            fields_frame,
            textvariable=self.user_id_var,
            width=35
        ).grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(10, 0))

        # Numero Badge
        ttk.Label(
            fields_frame,
            text=self.lang.get('label_badge_number', 'Numero Badge:')
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        ttk.Entry(
            fields_frame,
            textvariable=self.badge_var,
            width=35
        ).grid(row=1, column=1, sticky=tk.EW, pady=5, padx=(10, 0))

        # Nome e Cognome
        ttk.Label(
            fields_frame,
            text=self.lang.get('label_full_name', 'Nome e Cognome:')
        ).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        ttk.Entry(
            fields_frame,
            textvariable=self.name_var,
            width=35
        ).grid(row=2, column=1, sticky=tk.EW, pady=5, padx=(10, 0))

        # Email (OBBLIGATORIA)
        ttk.Label(
            fields_frame,
            text=self.lang.get('label_work_email_required', 'Email Aziendale (obbligatoria):'),
            foreground="#b00020"
        ).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        ttk.Entry(
            fields_frame,
            textvariable=self.email_var,
            width=35
        ).grid(row=3, column=1, sticky=tk.EW, pady=5, padx=(10, 0))

        # CNP (Codice Numerico Personale)
        ttk.Label(
            fields_frame,
            text=self.lang.get('label_cnp', 'CNP:')
        ).grid(row=4, column=0, sticky=tk.W, pady=5)
        
        ttk.Entry(
            fields_frame,
            textvariable=self.cnp_var,
            width=35
        ).grid(row=4, column=1, sticky=tk.EW, pady=5, padx=(10, 0))

        # Configura ridimensionamento colonne
        fields_frame.columnconfigure(1, weight=1)

        # Label di stato
        self.status_label = ttk.Label(
            main_frame,
            text="",
            foreground="blue",
            font=("Helvetica", 9, "italic"),
            wraplength=450,
            justify=tk.LEFT
        )
        self.status_label.pack(fill=tk.X, pady=(10, 10))

        # Frame per i bottoni
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            button_frame,
            text=self.lang.get('button_recover', 'Recupera'),
            command=self._recover_password
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text=self.lang.get('button_cancel', 'Annulla'),
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)

        # Frame (nascosto) per il recupero a favore di operatori senza email aziendale
        self._build_other_frame(main_frame)

        # Bind Enter
        self.bind('<Return>', lambda e: self._recover_password())

    # ── Recupero per operatore senza email aziendale ────────────────────────────
    def _build_other_frame(self, parent):
        """Crea (nascosto) il pannello per cercare le credenziali di un operatore
        senza email aziendale, per UserID oppure Cognome+Nome."""
        self.other_frame = ttk.LabelFrame(
            parent,
            text=self.lang.get('recovery_other_title',
                               'Operatore senza email aziendale (mostra credenziali a schermo)'),
            padding=10)

        row = ttk.Frame(self.other_frame)
        row.pack(fill=tk.X, pady=(0, 6))
        ttk.Label(row, text=self.lang.get('recovery_other_userid', 'UserID:')).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 6), pady=3)
        ttk.Entry(row, textvariable=self.other_userid_var, width=22).grid(
            row=0, column=1, sticky=tk.W, pady=3)
        ttk.Label(row, text=self.lang.get('recovery_other_name', 'oppure Cognome e Nome:')).grid(
            row=0, column=2, sticky=tk.W, padx=(14, 6), pady=3)
        ttk.Entry(row, textvariable=self.other_name_var, width=28).grid(
            row=0, column=3, sticky=tk.W, pady=3)
        # Indirizzo email a cui inviare le credenziali (l'operatore non ha email aziendale)
        ttk.Label(row, text=self.lang.get('recovery_other_dest_email', 'Invia a (email):')).grid(
            row=1, column=0, sticky=tk.W, padx=(0, 6), pady=3)
        ttk.Entry(row, textvariable=self.other_dest_email_var, width=40).grid(
            row=1, column=1, columnspan=3, sticky=tk.W, pady=3)
        ttk.Button(row, text=self.lang.get('recovery_other_search', '🔍 Cerca e invia credenziali'),
                   command=self._search_other).grid(row=0, column=4, rowspan=2, padx=(14, 0), pady=3)

        cols = ('employee', 'cdc', 'subcdc', 'function', 'user', 'pass')
        self.other_tree = ttk.Treeview(self.other_frame, columns=cols, show='headings', height=6)
        for c, h, w in (
                ('employee', self.lang.get('recovery_other_col_employee', 'Dipendente'), 190),
                ('cdc', self.lang.get('recovery_other_col_cdc', 'Reparto'), 140),
                ('subcdc', self.lang.get('recovery_other_col_subcdc', 'Sotto-reparto'), 140),
                ('function', self.lang.get('recovery_other_col_function', 'Funzione'), 140),
                ('user', self.lang.get('recovery_other_col_user', 'UserID'), 110),
                ('pass', self.lang.get('recovery_other_col_pass', 'Password'), 120)):
            self.other_tree.heading(c, text=h)
            self.other_tree.column(c, width=w, anchor='w')
        self.other_tree.tag_configure('pw', foreground='#0066cc')
        vsb = ttk.Scrollbar(self.other_frame, orient='vertical', command=self.other_tree.yview)
        self.other_tree.configure(yscrollcommand=vsb.set)
        self.other_tree.pack(side='left', fill=tk.BOTH, expand=True)
        vsb.pack(side='right', fill='y')

    def _on_toggle_for_other(self):
        """Al click sul checkbox: se attivato, richiede l'autorizzazione (capo reparto)
        con chiave 'recupera_password_per altri' e mostra il pannello."""
        if not self.for_other_var.get():
            self._authorized_for_other = False
            if self.other_frame:
                self.other_frame.pack_forget()
            return

        if self._authorized_for_other:
            self._show_other_frame()
            return

        master = self.master
        if not hasattr(master, '_execute_authorized_action'):
            messagebox.showerror(self.lang.get('error', 'Errore'),
                                 self.lang.get('recovery_no_auth', 'Autorizzazione non disponibile.'),
                                 parent=self)
            self.for_other_var.set(False)
            return

        def cb():
            self._authorized_for_other = True
            self._auth_user = getattr(master, 'last_authenticated_user_name', None)
            self._show_other_frame()

        ok = master._execute_authorized_action('recupera_password_per_altri', cb)
        if not ok or not self._authorized_for_other:
            # non autorizzato o login annullato
            self.for_other_var.set(False)

    def _show_other_frame(self):
        if self.other_frame and not self.other_frame.winfo_ismapped():
            self.other_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        try:
            self.geometry("960x640")
        except Exception:
            pass

    def _search_other(self):
        """Cerca le credenziali dell'operatore per UserID o Cognome+Nome e le mostra."""
        if not self._authorized_for_other:
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                   self.lang.get('recovery_not_authorized',
                                                 'Autorizzazione richiesta.'), parent=self)
            return
        userid = self.other_userid_var.get().strip() or None
        name = self.other_name_var.get().strip() or None
        if not userid and not name:
            messagebox.showinfo(self.lang.get('info', 'Info'),
                                self.lang.get('recovery_other_need_input',
                                              'Inserire UserID oppure Cognome e Nome.'), parent=self)
            return
        # Email di destinazione OBBLIGATORIA: le credenziali vengono inviate lì (in rumeno)
        dest_email = self.other_dest_email_var.get().strip()
        import re as _re
        if not dest_email or not _re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', dest_email):
            messagebox.showwarning(self.lang.get('warning', 'Attenzione'),
                                   self.lang.get('recovery_other_dest_required',
                                                 "Inserire un indirizzo email valido a cui inviare le credenziali."),
                                   parent=self)
            return

        query = """
            DECLARE @NameUser NVARCHAR(50) = ?;
            DECLARE @UserId NVARCHAR(20) = ?;
            SELECT
                e.EmployeeSurname + ' ' + e.EmployeeName AS Employee,
                cc.CdcDescription,
                cs.SubCdcDescription,
                f.FunctionDescription,
                k.nomeuser,
                k.pass AS Pwd
            FROM employee.dbo.EmployeeHireHistory h
            INNER JOIN employee.dbo.Employees e ON h.EmployeeId = e.EmployeeId
            INNER JOIN employee.dbo.EmployeeCdcStories ecs
                ON ecs.EmployeeHireHistoryId = h.EmployeeHireHistoryId
            INNER JOIN employee.dbo.CdcSub cs ON ecs.SubCdcId = cs.SubCdcId
            INNER JOIN employee.dbo.CostCenters cc ON cs.CdcId = cc.CdcId
            INNER JOIN employee.dbo.Functions f ON ecs.FunctionId = f.FunctionId
            INNER JOIN resetservices.dbo.tbuserkey k ON e.EmployeeId = k.idanga
            WHERE h.EmployeerId = 2
              AND h.EndWorkDate IS NULL
              AND ecs.DateOut IS NULL
              AND (
                (@NameUser IS NOT NULL AND e.EmployeeSurname + ' ' + e.EmployeeName = @NameUser)
                OR
                (@UserId IS NOT NULL AND k.nomeuser = @UserId)
              )
            ORDER BY cs.SubCdcDescription, f.FunctionCode,
                     e.EmployeeSurname + ' ' + e.EmployeeName;
        """
        try:
            self.db.cursor.execute(query, name, userid)
            rows = self.db.cursor.fetchall()
        except Exception as e:
            logger.error(f"Recupero password per altri: {e}", exc_info=True)
            messagebox.showerror(self.lang.get('error', 'Errore'), str(e), parent=self)
            return

        self.other_tree.delete(*self.other_tree.get_children())
        if not rows:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('password_recovery_not_found',
                              'Nessun utente trovato con i criteri specificati'), parent=self)
            return
        for r in rows:
            self.other_tree.insert('', 'end', values=(
                r.Employee or '', r.CdcDescription or '', r.SubCdcDescription or '',
                r.FunctionDescription or '', r.nomeuser or '', r.Pwd or ''), tags=('pw',))
        logger.info("Recupero password per altri: autorizzato da '%s', criteri userid=%r nome=%r, %d risultati",
                    self._auth_user, userid, name, len(rows))

        # Invio email in rumeno all'indirizzo fornito
        self._send_other_email_ro(rows, dest_email)

    def _send_other_email_ro(self, rows, dest_email):
        """Invia le credenziali trovate all'indirizzo fornito, con testo in RUMENO."""
        try:
            import utils
            html = self._create_other_email_html_ro(rows)
            utils.send_email(
                recipients=[dest_email],
                subject='Recuperare parolă - Traceability RS',
                body=html,
                is_html=True)
            logger.info("Recupero password per altri: email (RO) inviata a %s (%d righe), autorizzato da '%s'",
                        dest_email, len(rows), self._auth_user)
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('recovery_other_email_sent',
                              'Credenziali inviate a: {0}').format(dest_email),
                parent=self)
        except Exception as e:
            logger.error(f"Recupero password per altri - invio email: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('recovery_other_email_error', 'Invio email non riuscito')}:\n{e}",
                parent=self)

    def _create_other_email_html_ro(self, rows):
        """Corpo HTML in RUMENO con le credenziali trovate (una o più righe)."""
        logo_base64 = self._get_logo_base64()
        righe = ""
        for r in rows:
            righe += (
                "<tr>"
                f"<td style='padding:6px 10px;border-bottom:1px solid #eee'>{r.Employee or ''}</td>"
                f"<td style='padding:6px 10px;border-bottom:1px solid #eee'>{r.CdcDescription or ''}</td>"
                f"<td style='padding:6px 10px;border-bottom:1px solid #eee'>{r.SubCdcDescription or ''}</td>"
                f"<td style='padding:6px 10px;border-bottom:1px solid #eee'>{r.FunctionDescription or ''}</td>"
                f"<td style='padding:6px 10px;border-bottom:1px solid #eee;font-family:Courier New,monospace'>{r.nomeuser or ''}</td>"
                f"<td style='padding:6px 10px;border-bottom:1px solid #eee;font-family:Courier New,monospace'>{r.Pwd or ''}</td>"
                "</tr>")
        logo_html = (f'<img src="data:image/png;base64,{logo_base64}" alt="Logo" style="max-width:180px">'
                     if logo_base64 else '')
        return f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;color:#333;max-width:680px;margin:0 auto;padding:20px">
    <div style="text-align:center;border-bottom:3px solid #0066cc;padding-bottom:16px;margin-bottom:24px">
        {logo_html}
        <h2 style="color:#0066cc;margin-top:12px">Recuperare parolă</h2>
    </div>
    <p>Bună ziua,</p>
    <p>Mai jos găsiți datele de autentificare solicitate:</p>
    <table style="border-collapse:collapse;width:100%;font-size:13px;margin:16px 0">
        <tr style="background:#0066cc;color:#fff">
            <th style="padding:8px 10px;text-align:left">Angajat</th>
            <th style="padding:8px 10px;text-align:left">Departament</th>
            <th style="padding:8px 10px;text-align:left">Sub-departament</th>
            <th style="padding:8px 10px;text-align:left">Funcție</th>
            <th style="padding:8px 10px;text-align:left">Utilizator</th>
            <th style="padding:8px 10px;text-align:left">Parolă</th>
        </tr>
        {righe}
    </table>
    <p style="background:#fff3cd;border-left:4px solid #ffc107;padding:12px;border-radius:5px">
        Vă rugăm să păstrați aceste date în siguranță și să schimbați parola la prima autentificare.
    </p>
    <div style="text-align:center;font-size:12px;color:#777;margin-top:26px;padding-top:16px;border-top:1px solid #ddd">
        <p>Acesta este un email automat. Vă rugăm să nu răspundeți la acest mesaj.</p>
        <p><strong>Traceability RS</strong> &copy; {self._get_current_year()}</p>
    </div>
</body>
</html>"""

    def _normalize_badge(self, badge):
        """Normalizza il numero badge aggiungendo zeri davanti se necessario"""
        if not badge:
            return None
        
        badge = badge.strip()
        if len(badge) < 10:
            badge = badge.zfill(10)  # Aggiunge zeri a sinistra fino a 10 caratteri
        
        return badge

    def _recover_password(self):
        """Esegue il recupero password"""
        # Ottieni i valori dai campi
        user_id = self.user_id_var.get().strip() if self.user_id_var.get().strip() else None
        badge = self._normalize_badge(self.badge_var.get())
        name = self.name_var.get().strip() if self.name_var.get().strip() else None
        email = self.email_var.get().strip() if self.email_var.get().strip() else None
        cnp = self.cnp_var.get().strip() if self.cnp_var.get().strip() else None

        # L'unico campo OBBLIGATORIO è l'email aziendale. Gli altri sono opzionali
        # e servono solo a restringere la ricerca.
        if not email:
            self.status_label.config(
                text=self.lang.get('recovery_email_required',
                                   "L'email aziendale è obbligatoria per il recupero password."),
                foreground="red"
            )
            return
        import re
        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            self.status_label.config(
                text=self.lang.get('recovery_email_invalid', 'Formato email non valido.'),
                foreground="red"
            )
            return

        try:
            # Esegui la query
            query = """
                DECLARE @IdUser nvarchar(40) = ?
                DECLARE @WorkEmail nvarchar(100) = ?
                DECLARE @EmployeeName nvarchar(100) = ?
                DECLARE @BadgeNo nvarchar(15) = ?
                DECLARE @CNP nvarchar(13) = ?

                SELECT 
                    U.nomeuser,
                    U.Pass, 
                    a.WorkEmail, 
                    e.EmployeeSurname + ' ' + e.EmployeeName AS EmployeeName, 
                    b.NoBadge, 
                    e.employeenid AS CNP 
                FROM resetservices.dbo.tbuserkey U 
                INNER JOIN employee.dbo.employees e ON e.employeeid = u.idanga 
                INNER JOIN employee.dbo.EmployeeHireHistory H 
                    ON h.employeeid = e.EmployeeId 
                    AND h.employeerid = 2 
                    AND h.EndWorkDate IS NULL 
                INNER JOIN employee.dbo.EmployeeAddress A 
                    ON a.EmployeeId = e.EmployeeId 
                    AND a.dateout IS NULL
                INNER JOIN employee.dbo.EmployeeBadgeHistory BH 
                    ON bh.EmployeeHireHistoryId = h.EmployeeHireHistoryId 
                    AND bh.dateout IS NULL
                INNER JOIN employee.dbo.badges B 
                    ON b.BadgeId = BH.BadgeID
                WHERE u.nomeuser = IIF(@iduser IS NOT NULL, @iduser, u.nomeuser)
                    AND u.nota = IIF(@EmployeeName IS NOT NULL, @EmployeeName, u.nota)
                    AND b.NoBadge = IIF(@BadgeNo IS NOT NULL, @BadgeNo, b.NoBadge)
                    AND a.workemail = IIF(@WorkEmail IS NOT NULL, @WorkEmail, a.workemail)
                    AND e.EmployeeNID = IIF(@CNP IS NOT NULL, @CNP, e.EmployeeNID)
                    AND u.nomeuser = IIF(@iduser IS NULL AND @WorkEmail IS NULL AND @EmployeeName IS NULL AND @BadgeNo IS NULL AND @CNP IS NULL, 'x', U.nomeuser)
            """

            self.db.cursor.execute(query, user_id, email, name, badge, cnp)
            result = self.db.cursor.fetchone()

            if not result:
                messagebox.showwarning(
                    self.lang.get('warning', 'Attenzione'),
                    self.lang.get('password_recovery_not_found', 'Nessun utente trovato con i criteri specificati')
                )
                return

            # Estrai i dati
            username = result.nomeuser
            password = result.Pass
            work_email = result.WorkEmail
            employee_name = result.EmployeeName
            badge_no = result.NoBadge
            cnp_code = result.CNP

            # Verifica se l'email è presente
            if not work_email or work_email.strip() == '':
                self.status_label.config(
                    text=self.lang.get(
                        'password_recovery_no_email',
                        'Non è possibile recuperare la password perché nel database dei dipendenti '
                        'NON è stata registrata una WorkEmail valida per questo utente.'
                    ),
                    foreground="red"
                )
                return

            # Mostra messaggio di stato: dati trovati, preparazione email
            status_msg = self.lang.get(
                'preparing_email',
                'Dati trovati! Preparazione email in corso...'
            )
            self.status_label.config(text=status_msg, foreground="green")
            self.update()  # Forza l'aggiornamento della UI

            # Invia email con le credenziali
            self._send_recovery_email(username, password, work_email, employee_name, badge_no, cnp_code)

        except Exception as e:
            logger.error(f"Errore nel recupero password: {e}", exc_info=True)
            self.status_label.config(
                text=f"{self.lang.get('recovery_error', 'Errore durante il recupero')}: {e}",
                foreground="red"
            )

    def _send_recovery_email(self, username, password, work_email, employee_name, badge_no, cnp_code):
        """Invia l'email con le credenziali recuperate"""
        try:
            # Prepara l'oggetto dell'email
            subject = self.lang.get(
                'password_recovery_email_subject',
                'Recupero Credenziali - Traceability RS'
            )

            # Prepara il corpo HTML dell'email
            html_body = self._create_email_html(username, password, employee_name, badge_no, cnp_code)

            # Invia l'email
            import utils
            utils.send_email(
                recipients=[work_email],
                subject=subject,
                body=html_body,
                is_html=True
            )

            # Mostra messaggio di conferma
            success_msg_template = self.lang.get(
                'password_recovery_email_sent',
                'Le credenziali sono state inviate all\'indirizzo email: {0}'
            )
            success_msg = success_msg_template.format(work_email)
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                success_msg
            )

            logger.info(f"Email di recupero password inviata a {work_email} per utente {username}")
            
            # Chiudi la finestra dopo la conferma
            self.destroy()

        except Exception as e:
            logger.error(f"Errore nell'invio dell'email di recupero: {e}", exc_info=True)
            error_msg = self.lang.get('email_send_error', 'Errore durante l\'invio dell\'email')
            self.status_label.config(
                text=f"{error_msg}: {e}",
                foreground="red"
            )

    def _create_email_html(self, username, password, employee_name, badge_no, cnp_code):
        """Crea il corpo HTML dell'email con formattazione professionale"""
        
        # Converti il logo in base64 per incorporarlo nell'email
        logo_base64 = self._get_logo_base64()

        # Traduzi le etichette
        greeting = self.lang.get('email_greeting', 'Gentile')
        credentials_header = self.lang.get('email_credentials_header', 'Ecco le tue credenziali di accesso:')
        username_label = self.lang.get('email_username_label', 'Nome utente')
        password_label = self.lang.get('email_password_label', 'Password')
        badge_label = self.lang.get('email_badge_label', 'Numero Badge')
        cnp_label = self.lang.get('email_cnp_label', 'CNP')
        footer_text = self.lang.get(
            'email_footer_text',
            'Questa è un\'email automatica. Per favore non rispondere a questo messaggio.'
        )

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #0066cc;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .logo {{
            max-width: 200px;
            height: auto;
        }}
        .content {{
            background-color: #f9f9f9;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .credentials {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            border-left: 4px solid #0066cc;
            margin: 20px 0;
        }}
        .credential-item {{
            margin: 15px 0;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        .credential-item:last-child {{
            border-bottom: none;
        }}
        .label {{
            font-weight: bold;
            color: #0066cc;
            display: inline-block;
            width: 150px;
        }}
        .value {{
            color: #333;
            font-family: 'Courier New', monospace;
            background-color: #f0f0f0;
            padding: 3px 8px;
            border-radius: 3px;
        }}
        .security-note {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .footer {{
            text-align: center;
            font-size: 12px;
            color: #777;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="header">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo" class="logo">
        <h2 style="color: #0066cc; margin-top: 15px;">{self.lang.get('password_recovery_email_subject', 'Recupero Credenziali')}</h2>
    </div>
    
    <div class="content">
        <p><strong>{greeting} {employee_name},</strong></p>
        <p>{credentials_header}</p>
        
        <div class="credentials">
            <div class="credential-item">
                <span class="label">{username_label}:</span>
                <span class="value">{username}</span>
            </div>
            <div class="credential-item">
                <span class="label">{password_label}:</span>
                <span class="value">{password}</span>
            </div>
            <div class="credential-item">
                <span class="label">{badge_label}:</span>
                <span class="value">{badge_no}</span>
            </div>
            <div class="credential-item">
                <span class="label">{cnp_label}:</span>
                <span class="value">{cnp_code}</span>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>{footer_text}</p>
        <p style="margin-top: 10px;">
            <strong>Traceability RS</strong> &copy; {self._get_current_year()}
        </p>
    </div>
</body>
</html>
"""
        return html

    def _get_logo_base64(self):
        """Legge il logo e lo converte in base64 per incorporarlo nell'email"""
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
            
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as f:
                    logo_data = f.read()
                    return base64.b64encode(logo_data).decode('utf-8')
            else:
                logger.warning(f"Logo non trovato: {logo_path}")
                return ""
        except Exception as e:
            logger.error(f"Errore nella lettura del logo: {e}")
            return ""

    def _get_current_year(self):
        """Restituisce l'anno corrente"""
        from datetime import datetime
        return datetime.now().year
