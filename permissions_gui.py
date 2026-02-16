# permissions_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from utils import get_employee_work_email, send_email


class ViewPermissionsWindow(tk.Toplevel):
    """Finestra per la SOLA VISUALIZZAZIONE dei permessi di un utente."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.title(lang.get('view_permissions_title', "Visualizza Autorizzazioni"))
        self.geometry("700x400")
        self.transient(parent)
        self.grab_set()

        self.employees_data = {}
        self.employee_var = tk.StringVar()

        self._create_widgets()
        self._load_employees()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Filtro per dipendente
        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        filter_frame.columnconfigure(1, weight=1)
        ttk.Label(filter_frame, text=self.lang.get('select_employee_label', "Seleziona Dipendente:")).grid(row=0,
                                                                                                           column=0,
                                                                                                           padx=(0, 5))
        self.employee_combo = ttk.Combobox(filter_frame, textvariable=self.employee_var, state="readonly", height=10)
        self.employee_combo.grid(row=0, column=1, sticky="ew")
        self.employee_combo.bind("<<ComboboxSelected>>", self._load_permissions)

        # Lista permessi
        cols = ('permission',)
        self.tree = ttk.Treeview(main_frame, columns=cols, show="headings")
        self.tree.heading('permission', text=self.lang.get('permission_header', "Menu Autorizzato"))
        self.tree.grid(row=1, column=0, sticky="nsew")

    def _load_employees(self):
        # Riusiamo la funzione esistente per caricare i dipendenti
        employees = self.db.fetch_authorized_employees()
        if employees:
            self.employees_data = {e.Employ: e.EmployeeHireHistoryId for e in employees}
            self.employee_combo['values'] = sorted(list(self.employees_data.keys()))

    def _load_permissions(self, event=None):
        self.tree.delete(*self.tree.get_children())
        employee_name = self.employee_var.get()
        if not employee_name: return

        employee_id = self.employees_data.get(employee_name)
        permissions = self.db.fetch_user_permissions(employee_id)

        if permissions:
            for perm in permissions:
                if perm.MenuKey:  # Mostra solo se esiste una chiave menu
                    self.tree.insert("", "end", values=(perm.MenuKey,))


class ManagePermissionsWindow(tk.Toplevel):
    """Finestra per AGGIUNGERE o RIMUOVERE permessi a un utente."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.title(lang.get('manage_permissions_title', "Gestione Autorizzazioni Speciali"))
        self.geometry("900x500")
        self.transient(parent)
        self.grab_set()

        self.employees_data = {}
        self.available_perms_data = {}
        self.all_available_perms_data = {}
        self.assigned_perms_data = {}
        self.employee_var = tk.StringVar()
        self.menuvalue_filter_var = tk.StringVar()

        # --- NUOVO: Lista per conservare tutti i nomi dei dipendenti per la ricerca ---
        self.all_employee_names = []

        self._create_widgets()
        self._load_employees()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        top_frame.columnconfigure(1, weight=1)
        ttk.Label(top_frame, text=self.lang.get('select_employee_label', "Seleziona o Cerca Dipendente:")).grid(row=0,
                                                                                                                column=0)

        # --- MODIFICATO: state='normal' per permettere la scrittura ---
        self.employee_combo = ttk.Combobox(top_frame, textvariable=self.employee_var, state="normal", height=10)
        self.employee_combo.grid(row=0, column=1, sticky="ew", padx=5)
        self.employee_combo.bind("<<ComboboxSelected>>", self._populate_lists)
        # --- NUOVO: Associa la pressione dei tasti alla funzione di filtro ---
        self.employee_combo.bind('<KeyRelease>', self._filter_employee_combo)

        lists_frame = ttk.Frame(main_frame)
        lists_frame.grid(row=1, column=0, sticky="nsew")
        lists_frame.rowconfigure(0, weight=1)
        lists_frame.columnconfigure(0, weight=1)
        lists_frame.columnconfigure(2, weight=1)

        # Lista Sinistra: Permessi Disponibili
        available_frame = ttk.LabelFrame(lists_frame,
                                         text=self.lang.get('available_perms_label', "Permessi Disponibili"))
        available_frame.grid(row=0, column=0, sticky="nsew")

        menuvalue_filter_frame = ttk.Frame(available_frame)
        menuvalue_filter_frame.pack(fill="x", padx=5, pady=(5, 0))
        ttk.Label(
            menuvalue_filter_frame,
            text=self.lang.get('menuvalue_filter_label', "Filtro MenuValue:")
        ).pack(side=tk.LEFT, padx=(0, 5))
        self.menuvalue_filter_entry = ttk.Entry(
            menuvalue_filter_frame,
            textvariable=self.menuvalue_filter_var
        )
        self.menuvalue_filter_entry.pack(side=tk.LEFT, fill="x", expand=True)
        self.menuvalue_filter_entry.bind('<KeyRelease>', self._apply_menuvalue_filter)

        self.available_list = tk.Listbox(available_frame, selectmode="extended")
        self.available_list.pack(fill="both", expand=True, padx=5, pady=5)

        # Pulsanti Centrali
        btn_frame = ttk.Frame(lists_frame)
        btn_frame.grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text=">>", command=self._grant_permission).pack(pady=5)
        ttk.Button(btn_frame, text="<<", command=self._revoke_permission).pack(pady=5)

        # Lista Destra: Permessi Assegnati
        assigned_frame = ttk.LabelFrame(lists_frame, text=self.lang.get('assigned_perms_label', "Permessi Assegnati"))
        assigned_frame.grid(row=0, column=2, sticky="nsew")
        self.assigned_list = tk.Listbox(assigned_frame, selectmode="extended")
        self.assigned_list.pack(fill="both", expand=True, padx=5, pady=5)

    def _load_employees(self):
        employees = self.db.fetch_authorized_employees()
        if employees:
            self.employees_data = {e.Employ: e.EmployeeHireHistoryId for e in employees}
            # --- NUOVO: Salva la lista completa per la ricerca ---
            self.all_employee_names = sorted(list(self.employees_data.keys()))
            self.employee_combo['values'] = self.all_employee_names

    # --- NUOVO: Metodo per filtrare la lista dei dipendenti ---
    def _filter_employee_combo(self, event):
        typed_text = self.employee_var.get().lower()

        if not typed_text:
            self.employee_combo['values'] = self.all_employee_names
            # Se l'utente cancella il testo, pulisce anche le liste dei permessi
            self.available_list.delete(0, tk.END)
            self.assigned_list.delete(0, tk.END)
            self.available_perms_data.clear()
            self.all_available_perms_data.clear()
            self.menuvalue_filter_var.set("")
            return

        filtered_list = [name for name in self.all_employee_names if typed_text in name.lower()]
        self.employee_combo['values'] = filtered_list

    def _populate_lists(self, event=None):
        self.available_list.delete(0, tk.END)
        self.assigned_list.delete(0, tk.END)
        self.available_perms_data.clear()
        self.all_available_perms_data.clear()
        self.assigned_perms_data.clear()

        employee_name = self.employee_var.get()
        if not employee_name or employee_name not in self.employees_data:
            return  # Non fare nulla se il nome non è valido
        employee_id = self.employees_data[employee_name]

        available = self.db.fetch_available_permissions(employee_id)
        for perm in available:
            self.all_available_perms_data[perm.translationvalue] = perm.Translationkey

        self._apply_menuvalue_filter()

        assigned = self.db.fetch_user_permissions(employee_id)
        for perm in assigned:
            if perm.MenuKey:
                self.assigned_list.insert(tk.END, perm.MenuKey)
                self.assigned_perms_data[perm.MenuKey] = perm.AuthorizedUsedId

    def _apply_menuvalue_filter(self, event=None):
        """Filtra la lista dei permessi disponibili per il campo MenuValue."""
        filter_text = self.menuvalue_filter_var.get().strip().lower()
        self.available_list.delete(0, tk.END)
        self.available_perms_data.clear()

        if not self.all_available_perms_data:
            return

        for menu_value, translation_key in self.all_available_perms_data.items():
            menu_value_str = str(menu_value) if menu_value is not None else ""
            if not filter_text or filter_text in menu_value_str.lower():
                self.available_list.insert(tk.END, menu_value_str)
                self.available_perms_data[menu_value_str] = translation_key

    def _grant_permission(self):
        selections = self.available_list.curselection()
        if not selections: return
        
        employee_name = self.employee_var.get()
        employee_id = self.employees_data[employee_name]

        for i in selections:
            display_name = self.available_list.get(i)
            translation_key = self.available_perms_data[display_name]
            self.db.grant_permission(employee_id, translation_key)

            # Invia email di notifica professionale
            try:
                self._send_permission_notification_email(employee_name, translation_key)
            except Exception as e:
                print(f"Errore invio email notifica permesso: {e}")

        self._populate_lists()

    def _send_permission_notification_email(self, employee_name, menu_key):
        """Invia email di notifica professionale multilingua con logo"""
        try:
            # Recupera l'email del dipendente
            work_email = get_employee_work_email(self.db.conn, employee_name)
            if not work_email:
                print(f"Email non trovata per {employee_name}")
                return

            # Recupera il nome del servizio dalle traduzioni per IT, RO, EN
            service_names = {}
            for lang_code in ['it', 'ro', 'en']:
                query = """
                    SELECT MenuValue 
                    FROM AppTranslations 
                    WHERE TranslationKey = ? AND LanguageCode = ?
                """
                cursor = self.db.conn.cursor()
                cursor.execute(query, (menu_key, lang_code))
                row = cursor.fetchone()
                cursor.close()
                
                if row:
                    service_names[lang_code] = row.MenuValue
                else:
                    service_names[lang_code] = menu_key

            # Costruisci il corpo dell'email in HTML con logo
            html_body = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: 'Segoe UI', Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 650px;
                        margin: 20px auto;
                        background-color: #ffffff;
                        border: 1px solid #e0e0e0;
                        border-radius: 10px;
                        overflow: hidden;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        background: linear-gradient(135deg, #0066cc 0%, #004999 100%);
                        color: white;
                        text-align: center;
                        padding: 30px 20px;
                    }}
                    .logo {{
                        max-width: 180px;
                        height: auto;
                        margin-bottom: 15px;
                    }}
                    .header h2 {{
                        margin: 0;
                        font-size: 20px;
                        font-weight: 300;
                    }}
                    .content {{
                        padding: 30px;
                        background-color: #f9f9f9;
                    }}
                    .service-box {{
                        background-color: #fff;
                        padding: 20px;
                        margin: 20px 0;
                        border-left: 5px solid #0066cc;
                        border-radius: 5px;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    }}
                    .service-name {{
                        font-size: 18px;
                        font-weight: bold;
                        color: #0066cc;
                        margin: 0;
                    }}
                    .language-section {{
                        background-color: white;
                        margin: 15px 0;
                        padding: 20px;
                        border-radius: 5px;
                        border: 1px solid #e8e8e8;
                    }}
                    .language-title {{
                        color: #0066cc;
                        font-weight: bold;
                        font-size: 14px;
                        margin-bottom: 12px;
                        padding-bottom: 8px;
                        border-bottom: 2px solid #e8f4f8;
                    }}
                    .language-section p {{
                        margin: 8px 0;
                        line-height: 1.6;
                    }}
                    .footer {{
                        background-color: #f0f0f0;
                        text-align: center;
                        padding: 20px;
                        font-size: 11px;
                        color: #666;
                        border-top: 1px solid #e0e0e0;
                    }}
                    .footer p {{
                        margin: 5px 0;
                    }}
                    .highlight {{
                        background-color: #e8f4f8;
                        padding: 2px 6px;
                        border-radius: 3px;
                        font-weight: 600;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <img src="cid:logo" class="logo" alt="Company Logo">
                        <h2>Notifica Autorizzazione / Notificare Autorizație / Authorization Notification</h2>
                    </div>
                    
                    <div class="content">
                        <div class="service-box">
                            <p class="service-name">🔐 {service_names.get('it', menu_key)}</p>
                        </div>

                        <div class="language-section">
                            <div class="language-title">🇮🇹 ITALIANO</div>
                            <p>Gentile <span class="highlight">{employee_name}</span>,</p>
                            <p>Le comunichiamo che è stato autorizzato ad accedere al seguente servizio:</p>
                            <p><strong>{service_names.get('it', menu_key)}</strong></p>
                            <p>L'autorizzazione è ora attiva. Può utilizzare il servizio accedendo all'applicazione con le sue credenziali.</p>
                        </div>

                        <div class="language-section">
                            <div class="language-title">🇷🇴 ROMÂNĂ</div>
                            <p>Stimate <span class="highlight">{employee_name}</span>,</p>
                            <p>Vă informăm că ați fost autorizat să accesați următorul serviciu:</p>
                            <p><strong>{service_names.get('ro', menu_key)}</strong></p>
                            <p>Autorizația este acum activă. Puteți utiliza serviciul accesând aplicația cu acreditările dumneavoastră.</p>
                        </div>

                        <div class="language-section">
                            <div class="language-title">🇬🇧 ENGLISH</div>
                            <p>Dear <span class="highlight">{employee_name}</span>,</p>
                            <p>We inform you that you have been authorized to access the following service:</p>
                            <p><strong>{service_names.get('en', menu_key)}</strong></p>
                            <p>The authorization is now active. You can use the service by accessing the application with your credentials.</p>
                        </div>
                    </div>

                    <div class="footer">
                        <p><strong>Questa è una notifica automatica. Si prega di non rispondere a questa email.</strong></p>
                        <p><strong>Aceasta este o notificare automată. Vă rugăm să nu răspundeți la acest email.</strong></p>
                        <p><strong>This is an automated notification. Please do not reply to this email.</strong></p>
                    </div>
                </div>
            </body>
            </html>
            """

            # Percorso del logo
            import os
            logo_path = os.path.join(os.path.dirname(__file__), 'Logo.png')
            
            # Prepara gli allegati con il logo come inline image
            attachments = []
            if os.path.exists(logo_path):
                attachments.append(('Logo.png', logo_path, 'logo'))
            
            # Invia l'email
            send_email(
                recipients=[work_email],
                subject=f"🔐 Nuova Autorizzazione / Autorizație Nouă / New Authorization",
                body=html_body,
                is_html=True
            )

            
            print(f"✓ Email di notifica inviata a {work_email} per autorizzazione: {menu_key}")
            
        except Exception as e:
            print(f"✗ Errore invio email notifica autorizzazione: {e}")
            import traceback
            traceback.print_exc()

    def _revoke_permission(self):
        selections = self.assigned_list.curselection()
        if not selections: return

        for i in selections:
            display_name = self.assigned_list.get(i)
            authorized_user_id = self.assigned_perms_data[display_name]
            self.db.revoke_permission(authorized_user_id)

        self._populate_lists()


# Funzioni Launcher
def open_view_permissions_window(parent, db, lang):
    ViewPermissionsWindow(parent, db, lang)


def open_manage_permissions_window(parent, db, lang):
    ManagePermissionsWindow(parent, db, lang)
