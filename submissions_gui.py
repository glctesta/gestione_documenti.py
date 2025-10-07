import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import utils

class NewSubmissionWindow(tk.Toplevel):
    """Finestra per l'inserimento di una nuova segnalazione (Near Miss, Idea, etc.)."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.title(lang.get('new_submission_title', "Nuova Segnalazione"))
        self.geometry("700x550")
        self.transient(parent)
        self.grab_set()

        # Dati per i combobox
        self.employees_data = {}
        self.types_data = {}

        # Lista per gli allegati in memoria
        self.attachments = []

        # Variabili Tkinter
        self.employee_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.location_var = tk.StringVar()

        # La sequenza corretta è creare i widget e POI caricarne i dati
        self._create_widgets()
        self._load_combobox_data()

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        main_frame.rowconfigure(5, weight=1)

        # Riga 0: Segnalato da
        ttk.Label(main_frame, text=self.lang.get('submitted_by_label', "Segnalato da (*):")).grid(row=0, column=0,
                                                                                                  sticky="w", padx=5,
                                                                                                  pady=5)
        self.employee_combo = ttk.Combobox(main_frame, textvariable=self.employee_var, state="normal", height=10)
        self.employee_combo.grid(row=0, column=1, columnspan=2, sticky="ew", pady=5)
        # self.employee_combo.bind('<KeyRelease>', self._filter_employee_combo) # Ricerca dinamica (se la vuoi riattivare)

        # Riga 1: Tipo di Segnalazione
        ttk.Label(main_frame, text=self.lang.get('submission_type_label', "Tipo (*):")).grid(row=1, column=0,
                                                                                             sticky="w", padx=5, pady=5)
        self.type_combo = ttk.Combobox(main_frame, textvariable=self.type_var, state="readonly")
        self.type_combo.grid(row=1, column=1, columnspan=2, sticky="ew", pady=5)

        # Riga 2: Titolo
        ttk.Label(main_frame, text=self.lang.get('title_label', "Titolo (*):")).grid(row=2, column=0, sticky="w",
                                                                                     padx=5, pady=5)
        ttk.Entry(main_frame, textvariable=self.title_var).grid(row=2, column=1, columnspan=2, sticky="ew", pady=5)

        # Riga 3: Luogo
        ttk.Label(main_frame, text=self.lang.get('location_label', "Luogo (Opzionale):")).grid(row=3, column=0,
                                                                                               sticky="w", padx=5,
                                                                                               pady=5)
        ttk.Entry(main_frame, textvariable=self.location_var).grid(row=3, column=1, columnspan=2, sticky="ew", pady=5)

        # Riga 4: Descrizione
        ttk.Label(main_frame, text=self.lang.get('description_label', "Descrizione (*):")).grid(row=4, column=0,
                                                                                                sticky="nw", padx=5,
                                                                                                pady=5)
        self.desc_text = tk.Text(main_frame, height=6, wrap=tk.WORD)
        self.desc_text.grid(row=4, column=1, columnspan=2, sticky="nsew", pady=5)

        # Riga 5: Allegati
        attachments_frame = ttk.LabelFrame(main_frame, text=self.lang.get('attachments_label', "Allegati"))
        attachments_frame.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=10)
        attachments_frame.columnconfigure(0, weight=1)
        attachments_frame.rowconfigure(0, weight=1)

        self.attachments_listbox = tk.Listbox(attachments_frame)
        self.attachments_listbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        btn_attach_frame = ttk.Frame(attachments_frame)
        btn_attach_frame.grid(row=0, column=1, sticky="ns", padx=5)
        ttk.Button(btn_attach_frame, text=self.lang.get('add_attachment_button', "Aggiungi..."),
                   command=self._add_attachment).pack()
        ttk.Button(btn_attach_frame, text=self.lang.get('remove_attachment_button', "Rimuovi"),
                   command=self._remove_attachment).pack()

        # Riga 6: Pulsante Salva
        ttk.Button(main_frame, text=self.lang.get('save_submission_button', "Salva Segnalazione"),
                   command=self._save_submission).grid(row=6, column=1, columnspan=2, sticky="e", pady=10)

    def _load_combobox_data(self):
        """Carica i dati iniziali per tutti i combobox."""
        # Carica i dipendenti
        employees = self.db.fetch_authorized_employees()
        if employees:
            self.employees_data = {e.Employ: e.EmployeeHireHistoryId for e in employees}
            self.employee_combo['values'] = sorted(list(self.employees_data.keys()))

        # Carica i tipi di segnalazione usando la lingua corrente
        self._reload_submission_types()

    def _reload_submission_types(self):
        """Ricarica la lista dei tipi di segnalazione in base alla lingua."""
        self.type_var.set("")
        self.types_data.clear()

        current_lang_code = self.lang.current_language
        print(f"DEBUG: Chiamo fetch_submission_types con lang_code: '{current_lang_code}'")  # Ho lasciato il debug

        types = self.db.fetch_submission_types(current_lang_code)

        print(f"DEBUG: Dati ricevuti dal DB: {types}")  # Ho aggiunto un altro debug

        if types:
            self.types_data = {t.NomeTipo: t.TipoSegnalazioneId for t in types}
            self.type_combo['values'] = sorted(list(self.types_data.keys()))
        else:
            # Se non trova dati, svuota esplicitamente la lista
            self.type_combo['values'] = []

    # ... tutti gli altri metodi (_add_attachment, _remove_attachment, _save_submission) rimangono invariati ...
    def _add_attachment(self):
        file_path = filedialog.askopenfilename(parent=self)
        if not file_path: return
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
            file_name = os.path.basename(file_path)
            self.attachments.append({'name': file_name, 'data': file_data})
            self.attachments_listbox.insert(tk.END, file_name)
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile leggere il file: {e}", parent=self)

    def _remove_attachment(self):
        selected_indices = self.attachments_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Attenzione", "Selezionare un allegato da rimuovere.", parent=self)
            return
        index = selected_indices[0]
        del self.attachments[index]
        self.attachments_listbox.delete(index)

    def _save_submission(self):
        employee_name = self.employee_var.get()
        type_name = self.type_var.get()
        title = self.title_var.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        if not all([employee_name, type_name, title, description]):
            messagebox.showerror("Dati Obbligatori Mancanti",
                                 "I campi Segnalato da, Tipo, Titolo e Descrizione sono obbligatori.", parent=self)
            return
        employee_id = self.employees_data[employee_name]
        type_id = self.types_data[type_name]
        location = self.location_var.get().strip()
        success, message = self.db.add_new_submission(
            type_id=type_id, title=title, desc=description,
            location=location, employee_id=employee_id, attachments=self.attachments
        )
        if success:
            messagebox.showinfo("Successo", message, parent=self)
            # INVIO EMAIL al gruppo "Sys_email_submission"
            try:
                recipients = utils.get_email_recipients(self.db.conn, attribute='Sys_email_submission')
                if recipients:
                    subject = "New submission created"
                    body = (
                        "Hello,\n\n"
                        "A new submission has just been created in the system.\n\n"
                        f"Title: {title}\n"
                        f"Submitted by: {employee_name}\n"
                        f"Location: {location or '-'}\n"
                        f"Description:\n{description}\n\n"
                        "Regards,\nSystem"
                    )
                    utils.send_email(recipients=recipients, subject=subject, body=body)
            except Exception as e:
                # Non bloccare l'utente per errore email
                print(f"Warning: email group notification failed: {e}")
            self.destroy()
        else:
            messagebox.showerror("Errore", message, parent=self)


def open_new_submission_form(parent, db, lang):
    NewSubmissionWindow(parent, db, lang)