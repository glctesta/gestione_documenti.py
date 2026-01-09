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
        self.geometry("500x450")
        self.resizable(False, False)

        # Variabili per i campi di input
        self.user_id_var = tk.StringVar()
        self.badge_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.cnp_var = tk.StringVar()

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
            'Inserire almeno uno dei seguenti campi per recuperare le credenziali:'
        )
        instruction_label = ttk.Label(
            main_frame,
            text=instruction_text,
            wraplength=450,
            justify=tk.LEFT
        )
        instruction_label.pack(pady=(0, 15))

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

        # Email
        ttk.Label(
            fields_frame,
            text=self.lang.get('label_work_email', 'Email Aziendale:')
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

        # Bind Enter
        self.bind('<Return>', lambda e: self._recover_password())

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

        # Verifica che almeno un campo sia compilato
        if not any([user_id, badge, name, email, cnp]):
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('password_recovery_empty_fields', 'Inserire almeno un campo per effettuare la ricerca')
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
                error_msg = self.lang.get(
                    'password_recovery_no_email',
                    'Non è possibile recuperare la password perché nel database dei dipendenti '
                    'NON è stata registrata una WorkEmail valida per questo utente.'
                )
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    error_msg
                )
                return

            # Invia email con le credenziali
            self._send_recovery_email(username, password, work_email, employee_name, badge_no, cnp_code)

        except Exception as e:
            logger.error(f"Errore nel recupero password: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('recovery_error', 'Errore durante il recupero')}: {e}"
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
            
            # Chiudi la finestra
            self.destroy()

        except Exception as e:
            logger.error(f"Errore nell'invio dell'email di recupero: {e}", exc_info=True)
            error_msg = self.lang.get('email_send_error', 'Errore durante l\'invio dell\'email')
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{error_msg}: {e}"
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
