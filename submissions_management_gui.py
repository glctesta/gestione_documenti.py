import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import tempfile
import logging
from PIL import Image, ImageTk

logger = logging.getLogger("TraceabilityRS")


class SubmissionsManagementWindow(tk.Toplevel):
    """Finestra gestione segnalazioni assegnate"""

    def __init__(self, parent, db, lang, current_user):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.current_user = current_user

        self.title(lang.get('submissions_management_title', "Gestione Segnalazioni"))
        self.geometry("1000x700")
        self.transient(parent)
        self.grab_set()

        # Dati
        self.submissions_data = {}
        self.current_submission_id = None
        self.current_assignment_id = None
        self.attachments = []  # Lista file da allegare

        # Variabili
        self.submission_var = tk.StringVar()
        self.activity_desc_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.status_note_var = tk.StringVar()

        self._create_widgets()
        self._load_submissions()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        # === SEZIONE 1: Selezione Segnalazione ===
        sel_frame = ttk.LabelFrame(main_frame, text=self.lang.get('select_submission', "Seleziona Segnalazione"),
                                   padding="10")
        sel_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(sel_frame, text=self.lang.get('submission', "Segnalazione:")).pack(side="left", padx=(0, 5))
        self.submission_combo = ttk.Combobox(sel_frame, textvariable=self.submission_var,
                                             state="readonly", width=60)
        self.submission_combo.pack(side="left", fill="x", expand=True)
        self.submission_combo.bind("<<ComboboxSelected>>", self._on_submission_selected)

        # === SEZIONE 2: Dettagli Segnalazione ===
        details_frame = ttk.LabelFrame(main_frame, text=self.lang.get('submission_details', "Dettagli"), padding="10")
        details_frame.pack(fill="both", expand=True, pady=(0, 10))
        details_frame.columnconfigure(1, weight=1)

        row = 0
        # Tipo
        ttk.Label(details_frame, text=self.lang.get('type', "Tipo:")).grid(row=row, column=0, sticky="w", pady=2)
        self.type_label = ttk.Label(details_frame, text="", font=("", 9, "bold"))
        self.type_label.grid(row=row, column=1, sticky="w", pady=2)

        row += 1
        # Titolo
        ttk.Label(details_frame, text=self.lang.get('title', "Titolo:")).grid(row=row, column=0, sticky="w", pady=2)
        self.title_label = ttk.Label(details_frame, text="", wraplength=600)
        self.title_label.grid(row=row, column=1, sticky="w", pady=2)

        row += 1
        # Descrizione
        ttk.Label(details_frame, text=self.lang.get('description', "Descrizione:")).grid(row=row, column=0, sticky="nw",
                                                                                         pady=2)
        self.desc_text = tk.Text(details_frame, height=4, width=70, state="disabled", wrap="word")
        self.desc_text.grid(row=row, column=1, sticky="ew", pady=2)

        row += 1
        # Segnalatore
        ttk.Label(details_frame, text=self.lang.get('reporter', "Segnalatore:")).grid(row=row, column=0, sticky="w",
                                                                                      pady=2)
        self.reporter_label = ttk.Label(details_frame, text="")
        self.reporter_label.grid(row=row, column=1, sticky="w", pady=2)

        row += 1
        # Stato corrente
        ttk.Label(details_frame, text=self.lang.get('current_status', "Stato:")).grid(row=row, column=0, sticky="w",
                                                                                      pady=2)
        self.status_label = ttk.Label(details_frame, text="", foreground="blue")
        self.status_label.grid(row=row, column=1, sticky="w", pady=2)

        row += 1
        # Allegato originale
        ttk.Label(details_frame, text=self.lang.get('attachment', "Allegato:")).grid(row=row, column=0, sticky="w",
                                                                                     pady=2)
        self.attachment_btn = ttk.Button(details_frame, text=self.lang.get('view_attachment', "Visualizza"),
                                         command=self._view_original_attachment, state="disabled")
        self.attachment_btn.grid(row=row, column=1, sticky="w", pady=2)

        # === SEZIONE 3: Attività Svolte ===
        activities_frame = ttk.LabelFrame(main_frame,
                                          text=self.lang.get('activities_done', "Attività Svolte o in Corso"),
                                          padding="10")
        activities_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Treeview attività
        cols = ("id", "note", "descrizione", "data")
        self.activities_tree = ttk.Treeview(activities_frame, columns=cols, show="headings", height=5)
        self.activities_tree.heading("id", text="ID")
        self.activities_tree.heading("note", text=self.lang.get('notes', "Note"))
        self.activities_tree.heading("descrizione", text=self.lang.get('activity', "Attività"))
        self.activities_tree.heading("data", text=self.lang.get('date', "Data"))

        self.activities_tree.column("id", width=50, anchor="center")
        self.activities_tree.column("note", width=150)
        self.activities_tree.column("descrizione", width=350)
        self.activities_tree.column("data", width=120, anchor="center")

        self.activities_tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(activities_frame, orient="vertical", command=self.activities_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.activities_tree.configure(yscrollcommand=scrollbar.set)

        self.activities_tree.bind("<Double-1>", self._view_activity_attachment)

        # === SEZIONE 4: Nuova Attività ===
        new_activity_frame = ttk.LabelFrame(main_frame, text=self.lang.get('new_activity', "Nuova Attività"),
                                            padding="10")
        new_activity_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(new_activity_frame, text=self.lang.get('activity_description', "Descrizione:")).pack(anchor="w")
        self.activity_entry = ttk.Entry(new_activity_frame, textvariable=self.activity_desc_var, width=80)
        self.activity_entry.pack(fill="x", pady=(2, 5))

        attach_frame = ttk.Frame(new_activity_frame)
        attach_frame.pack(fill="x")

        ttk.Button(attach_frame, text=self.lang.get('add_attachment', "Aggiungi Allegato"),
                   command=self._add_attachment).pack(side="left", padx=(0, 5))

        self.attachments_listbox = tk.Listbox(attach_frame, height=3)
        self.attachments_listbox.pack(side="left", fill="x", expand=True, padx=(0, 5))

        ttk.Button(attach_frame, text=self.lang.get('remove_attachment', "Rimuovi"),
                   command=self._remove_attachment).pack(side="left")

        # === SEZIONE 5: Cambio Stato ===
        status_frame = ttk.LabelFrame(main_frame, text=self.lang.get('change_status', "Cambio Stato"), padding="10")
        status_frame.pack(fill="x", pady=(0, 10))

        row_frame = ttk.Frame(status_frame)
        row_frame.pack(fill="x")

        ttk.Label(row_frame, text=self.lang.get('new_status', "Nuovo Stato:")).pack(side="left", padx=(0, 5))
        self.status_combo = ttk.Combobox(row_frame, textvariable=self.status_var, state="readonly", width=30)
        self.status_combo.pack(side="left", padx=(0, 10))

        ttk.Label(row_frame, text=self.lang.get('note', "Nota:")).pack(side="left", padx=(0, 5))
        self.status_note_entry = ttk.Entry(row_frame, textvariable=self.status_note_var, width=40)
        self.status_note_entry.pack(side="left", fill="x", expand=True)

        # === PULSANTI AZIONE ===
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(btn_frame, text=self.lang.get('save', "Salva"),
                   command=self._save_all).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text=self.lang.get('close', "Chiudi"),
                   command=self.destroy).pack(side="left")

        # Carica status types
        self._load_status_types()

    def _load_submissions(self):
        """Carica segnalazioni assegnate all'utente"""
        if not self.current_user or 'employee_hire_history_id' not in self.current_user:
            messagebox.showerror(self.lang.get('error', "Errore"),
                                 self.lang.get('no_user_id', "ID utente non disponibile"), parent=self)
            return

        rows = self.db.fetch_assigned_submissions(self.current_user['employee_hire_history_id'])
        if not rows:
            messagebox.showinfo(self.lang.get('info', "Info"),
                                self.lang.get('no_submissions', "Nessuna segnalazione assegnata"), parent=self)
            return

        self.submissions_data = {}
        items = []
        for r in rows:
            sid = r.SegnalazioneId
            display = f"{sid} - {r.Titolo} ({r.TipoStato})"
            items.append(display)
            self.submissions_data[display] = {
                'id': sid,
                'tipo': r.NomeTipo,
                'titolo': r.Titolo,
                'descrizione': r.Descrizione or "",
                'segnalatore': r.Segnalatore,
                'stato': r.TipoStato,
                'assegnatario': r.Assegnatario,
                'nome_file': getattr(r, 'NomeFile', None),
                'dati_file': getattr(r, 'DatiFile', None)
            }

        self.submission_combo['values'] = items
        if items:
            self.submission_combo.current(0)
            self._on_submission_selected()

    def _on_submission_selected(self, event=None):
        """Quando l'utente seleziona una segnalazione"""
        sel = self.submission_var.get()
        if not sel or sel not in self.submissions_data:
            return

        data = self.submissions_data[sel]
        self.current_submission_id = data['id']

        # Popola dettagli
        self.type_label.config(text=data['tipo'])
        self.title_label.config(text=data['titolo'])

        self.desc_text.config(state="normal")
        self.desc_text.delete("1.0", "end")
        self.desc_text.insert("1.0", data['descrizione'])
        self.desc_text.config(state="disabled")

        self.reporter_label.config(text=data['segnalatore'])
        self.status_label.config(text=data['stato'])

        # Allegato
        if data['dati_file']:
            self.attachment_btn.config(state="normal")
        else:
            self.attachment_btn.config(state="disabled")

        # Carica attività
        self._load_activities()

        # Recupera assignment ID
        self.current_assignment_id = self.db.get_submission_assignment_id(
            self.current_submission_id,
            self.current_user['employee_hire_history_id']
        )

    def _load_activities(self):
        """Carica attività svolte"""
        for item in self.activities_tree.get_children():
            self.activities_tree.delete(item)

        if not self.current_submission_id:
            return

        rows = self.db.fetch_submission_activities(self.current_submission_id)
        for r in rows:
            has_doc = "📎" if getattr(r, 'Documentazione', None) else ""
            self.activities_tree.insert("", "end", values=(
                r.SegnalazioneSvolgimentoId,
                getattr(r, 'Note', "") or "",
                getattr(r, 'DescrizioneAttivita', "") or "",
                r.DataAzione.strftime("%Y-%m-%d %H:%M") if hasattr(r.DataAzione, 'strftime') else str(r.DataAzione)
            ), tags=(has_doc,))

    def _view_original_attachment(self):
        """Visualizza allegato originale della segnalazione"""
        sel = self.submission_var.get()
        if not sel or sel not in self.submissions_data:
            return

        data = self.submissions_data[sel]
        if not data['dati_file']:
            messagebox.showwarning(self.lang.get('warning', "Attenzione"),
                                   self.lang.get('no_attachment', "Nessun allegato"), parent=self)
            return

        self._open_binary_file(data['dati_file'], data['nome_file'] or "allegato")

    def _view_activity_attachment(self, event=None):
        """Doppio click su attività per vedere allegato"""
        sel = self.activities_tree.selection()
        if not sel:
            return

        svolgimento_id = self.activities_tree.item(sel[0])['values'][0]

        # Query per recuperare allegato
        sql = """
              SELECT [DescrizioneDocumento], [Allegato]
              FROM [Employee].[dbo].[SegnalazioniStatiAllegati]
              WHERE [SegnalazioneSvolgimentoId] = ?; \
              """
        try:
            self.db.cursor.execute(sql, svolgimento_id)
            row = self.db.cursor.fetchone()
            if row and row.Allegato:
                self._open_binary_file(row.Allegato, row.DescrizioneDocumento or "documento")
            else:
                messagebox.showinfo(self.lang.get('info', "Info"),
                                    self.lang.get('no_attachment', "Nessun allegato"), parent=self)
        except Exception as e:
            logger.error(f"Error viewing activity attachment: {e}")
            messagebox.showerror(self.lang.get('error', "Errore"), str(e), parent=self)

    def _open_binary_file(self, binary_data: bytes, filename: str):
        """Salva e apre file binario"""
        try:
            ext = os.path.splitext(filename)[1] if '.' in filename else ""
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                tmp.write(binary_data)
                tmp_path = tmp.name

            os.startfile(tmp_path)  # Windows
        except Exception as e:
            logger.error(f"Error opening file: {e}")
            messagebox.showerror(self.lang.get('error', "Errore"),
                                 self.lang.get('cannot_open_file', f"Impossibile aprire il file: {e}"),
                                 parent=self)

    def _add_attachment(self):
        """Aggiungi allegato per nuova attività"""
        files = filedialog.askopenfilenames(
            title=self.lang.get('select_files', "Seleziona file"),
            filetypes=[
                ("All supported", "*.jpg;*.jpeg;*.png;*.pdf;*.doc;*.docx;*.xls;*.xlsx"),
                ("Images", "*.jpg;*.jpeg;*.png"),
                ("PDF", "*.pdf"),
                ("Word", "*.doc;*.docx"),
                ("Excel", "*.xls;*.xlsx"),
                ("All files", "*.*")
            ]
        )

        for fpath in files:
            if fpath not in [a[0] for a in self.attachments]:
                self.attachments.append((fpath, os.path.basename(fpath)))
                self.attachments_listbox.insert("end", os.path.basename(fpath))

    def _remove_attachment(self):
        """Rimuovi allegato selezionato"""
        sel = self.attachments_listbox.curselection()
        if sel:
            idx = sel[0]
            self.attachments_listbox.delete(idx)
            del self.attachments[idx]

    def _load_status_types(self):
        """Carica tipi stato nel combo"""
        rows = self.db.fetch_submission_status_types()
        self.status_types_data = {}
        items = []
        for r in rows:
            display = r.TipoStato
            items.append(display)
            self.status_types_data[display] = {
                'id': r.SegnalazioniTipoStatoId,
                'chiuso': r.Statochiuso
            }

        self.status_combo['values'] = items

    def _save_all(self):
        """Salva attività e cambio stato"""
        if not self.current_submission_id:
            messagebox.showwarning(self.lang.get('warning', "Attenzione"),
                                   self.lang.get('select_submission_first', "Seleziona una segnalazione"),
                                   parent=self)
            return

        activity_desc = self.activity_desc_var.get().strip()
        new_status = self.status_var.get()
        status_note = self.status_note_var.get().strip()

        if not activity_desc and not new_status:
            messagebox.showwarning(self.lang.get('warning', "Attenzione"),
                                   self.lang.get('nothing_to_save', "Nessuna modifica da salvare"),
                                   parent=self)
            return

        # Verifica chiusura
        if new_status and new_status in self.status_types_data:
            if self.status_types_data[new_status]['chiuso'] == 1:
                if not messagebox.askyesno(self.lang.get('confirm', "Conferma"),
                                           self.lang.get('confirm_close_submission',
                                                         "Stai chiudendo la segnalazione. Confermi?"),
                                           parent=self):
                    return

        try:
            # 1. Inserisci attività
            svolgimento_id = None
            if activity_desc:
                if not self.current_assignment_id:
                    messagebox.showerror(self.lang.get('error', "Errore"),
                                         self.lang.get('no_assignment_id', "ID assegnazione non trovato"),
                                         parent=self)
                    return

                ok, svolgimento_id = self.db.insert_submission_activity(
                    self.current_assignment_id, activity_desc
                )
                if not ok:
                    raise Exception(self.db.last_error_details)

                # 2. Inserisci allegati
                for fpath, fname in self.attachments:
                    with open(fpath, 'rb') as f:
                        file_data = f.read()
                    ok, err = self.db.insert_activity_attachment(svolgimento_id, fname, file_data)
                    if not ok:
                        raise Exception(err)

            # 3. Aggiorna stato
            if new_status:
                tipo_stato_id = self.status_types_data[new_status]['id']
                ok, err = self.db.update_submission_status(
                    self.current_submission_id,
                    tipo_stato_id,
                    status_note,
                    self.current_user.get('username', 'Unknown')
                )
                if not ok:
                    raise Exception(err)

            # 4. Invia email
            self._send_confirmation_email(new_status)

            messagebox.showinfo(self.lang.get('success', "Successo"),
                                self.lang.get('saved_successfully', "Salvato con successo"),
                                parent=self)

            # Reset form
            self.activity_desc_var.set("")
            self.status_note_var.set("")
            self.attachments.clear()
            self.attachments_listbox.delete(0, "end")

            # Ricarica attività
            self._load_activities()

        except Exception as e:
            logger.error(f"Error saving submission management: {e}")
            messagebox.showerror(self.lang.get('error', "Errore"),
                                 f"{self.lang.get('save_error', 'Errore salvataggio')}: {e}",
                                 parent=self)

    def _send_confirmation_email(self, new_status: str):
        """Invia email di conferma"""
        try:
            import utils

            # Recupera destinatari
            recipients = [self.current_user.get('email', '')]
            sys_recipients = utils.get_email_recipients(self.db.conn, 'sys_confirmassignation')
            recipients.extend(sys_recipients)
            recipients = [r for r in recipients if r]  # Rimuovi vuoti

            if not recipients:
                logger.warning("No email recipients found for submission confirmation")
                return

            sel = self.submission_var.get()
            data = self.submissions_data.get(sel, {})

            subject = f"Submission Update: {data.get('titolo', 'N/A')}"
            body = f"""
Dear Team,

The submission "{data.get('titolo', 'N/A')}" has been processed.

- Processed by: {self.current_user.get('username', 'Unknown')}
- New Status: {new_status}

Best regards,
Traceability System
            """

            sender = utils.EmailSender(self.db.conn)
            sender.send_email(recipients, subject, body)
            logger.info(f"Confirmation email sent to: {', '.join(recipients)}")

        except Exception as e:
            logger.error(f"Error sending confirmation email: {e}")
            # Non bloccare il salvataggio se l'email fallisce
