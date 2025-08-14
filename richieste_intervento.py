# richieste_intervento.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog  # Import simpledialog
from datetime import datetime
# Importa il nuovo file utils.py
import utils


# In richieste_intervento.py

# In richieste_intervento.py

class AddNewSparePartWindow(tk.Toplevel):
    """Finestra per aggiungere un nuovo materiale di ricambio al catalogo."""

    def __init__(self, parent, db, lang):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.new_part_id = None

        self.title(self.lang.get('add_new_material_title', "Aggiungi Nuovo Materiale"))
        self.geometry("500x300")
        self.transient(parent)

        # Variabili
        self.part_number_var = tk.StringVar()
        self.code_var = tk.StringVar()

        self._create_widgets()

        # --- CORREZIONE PRINCIPALE ---
        # Forziamo la finestra a ricevere il focus dal sistema operativo
        self.focus_force()

        # Ora che la finestra ha il focus, rendiamola modale
        self.grab_set()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)

        # 1. Codice Materiale (MaterialPartNumber) - Obbligatorio
        ttk.Label(frame, text=self.lang.get('material_part_number_label', "Codice Materiale (*):")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.part_number_entry = ttk.Entry(frame, textvariable=self.part_number_var)
        self.part_number_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)

        # 2. Nome Materiale (MaterialCode) - Opzionale
        ttk.Label(frame, text=self.lang.get('material_code_label', "Nome Materiale:")).grid(row=1, column=0, sticky=tk.W, pady=5)
        # --- SECONDA CORREZIONE MINORE ---
        # Assegniamo anche questo Entry a una variabile di istanza
        self.code_entry = ttk.Entry(frame, textvariable=self.code_var)
        self.code_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)

        # 3. Descrizione (MaterialDescription) - Opzionale, usiamo un Text widget
        ttk.Label(frame, text=self.lang.get('material_description_label', "Descrizione:")).grid(row=2, column=0, sticky=tk.NW, pady=5)
        self.description_text = tk.Text(frame, height=5, wrap=tk.WORD)
        self.description_text.grid(row=2, column=1, sticky=tk.EW, pady=5)

        # Pulsanti
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=1, sticky=tk.E, pady=(20, 0))

        ttk.Button(button_frame, text=self.lang.get('save_button', "Salva"), command=self._save_new_part).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('cancel_button', "Annulla"), command=self.destroy).pack(side=tk.LEFT)

        # Mettiamo il cursore nel primo campo
        self.part_number_entry.focus_set()

    def _save_new_part(self):
        part_number = self.part_number_var.get().strip()
        code = self.code_var.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()

        if not part_number:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('error_part_number_required', "Il Codice Materiale è obbligatorio."),
                                 parent=self)
            return

        new_id = self.db.add_new_spare_part(part_number, code, description)

        if new_id:
            messagebox.showinfo(self.lang.get('success_title', "Successo"),
                                self.lang.get('info_new_part_saved', "Nuovo materiale salvato con successo."),
                                parent=self)
            self.new_part_id = new_id
            self.destroy()
        else:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('error_saving_part', "Impossibile salvare il nuovo materiale.") + f"\n\n{self.db.last_error_details}",
                                 parent=self)

class RequestWindow(tk.Toplevel):
    """Finestra per richiedere parti di ricambio o interventi."""

    def __init__(self, parent, db, lang, user_name, equipment_id, equipment_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.equipment_id = equipment_id
        self.equipment_name = equipment_name

        # --- Variabili ripulite ---
        self.spare_parts_data = {}
        self.spare_part_var = tk.StringVar()
        self.quantity_var = tk.StringVar(value="1")  # Imposta la quantità di default a 1

        self.title(self.lang.get('request_window_title', "Crea Richiesta Parti/Intervento"))
        self.geometry("650x400")  # Leggermente più larga per un layout migliore
        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        self._load_spare_parts()

    def _create_widgets(self):
        """Crea e posiziona i widget con un layout corretto."""

        # 1. Crea un frame principale con padding
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 2. Configura la griglia per espandersi correttamente
        # La colonna 1 (dove sono i campi di input) si espanderà con la finestra
        main_frame.columnconfigure(1, weight=1)
        # La riga 3 (dove sono le note) si espanderà verticalmente
        main_frame.rowconfigure(3, weight=1)

        # --- Etichetta per la macchina ---
        machine_label_text = self.lang.get('request_for_machine', "Richiesta per la macchina:")
        ttk.Label(main_frame, text=machine_label_text, font=("Helvetica", 10, "bold")).grid(row=0, column=0,
                                                                                            sticky=tk.W, pady=(0, 5))
        ttk.Label(main_frame, text=self.equipment_name, font=("Helvetica", 10)).grid(row=0, column=1, columnspan=2,
                                                                                     sticky=tk.W, pady=(0, 5))

        # --- Selezione parte di ricambio ---
        ttk.Label(main_frame, text=self.lang.get('spare_part_label', "Parte di Ricambio:")).grid(row=1, column=0,
                                                                                                 sticky=tk.W, padx=5,
                                                                                                 pady=5)

        # Frame interno per il combobox e il pulsante "Nuovo..."
        part_frame = ttk.Frame(main_frame)
        part_frame.grid(row=1, column=1, sticky=tk.EW, pady=5)
        part_frame.columnconfigure(0, weight=1)  # Il combobox si espande

        self.spare_parts_combo = ttk.Combobox(part_frame, textvariable=self.spare_part_var, state='readonly', height=10)
        self.spare_parts_combo.grid(row=0, column=0, sticky=tk.EW)

        new_part_button = ttk.Button(part_frame, text=self.lang.get('new_material_button', "Nuovo..."),
                                     command=self._open_add_new_part_window)
        new_part_button.grid(row=0, column=1, padx=(5, 0))

        # --- Quantità ---
        ttk.Label(main_frame, text=self.lang.get('quantity_label', "Quantità:")).grid(row=2, column=0, sticky=tk.W,
                                                                                      padx=5, pady=5)
        self.quantity_entry = ttk.Entry(main_frame, textvariable=self.quantity_var, width=10)
        self.quantity_entry.grid(row=2, column=1, sticky=tk.W, pady=5)  # sticky=W per allinearlo a sx

        # --- Note ---
        ttk.Label(main_frame, text=self.lang.get('notes_label', "Note:")).grid(row=3, column=0, sticky=tk.NW, padx=5,
                                                                               pady=5)

        # Frame per il campo di testo con scrollbar
        notes_frame = ttk.Frame(main_frame)
        notes_frame.grid(row=3, column=1, sticky="nsew", pady=5)
        notes_frame.rowconfigure(0, weight=1)
        notes_frame.columnconfigure(0, weight=1)

        self.notes_text = tk.Text(notes_frame, height=6, wrap=tk.WORD)
        self.notes_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(notes_frame, orient=tk.VERTICAL, command=self.notes_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.notes_text.config(yscrollcommand=scrollbar.set)

        # --- Pulsante di salvataggio ---
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, sticky=tk.E, pady=(15, 0))

        self.save_button = ttk.Button(button_frame, text=self.lang.get('save_request_button', "Invia Richiesta"),
                                      command=self._save_request)
        self.save_button.pack()

    # I tuoi altri metodi (_load_spare_parts, _open_add_new_part_window, _save_request) rimangono qui...
    # Assicurati che il metodo _save_request esista o crealo.
    def _save_request(self):
        # Logica per salvare la richiesta
        part_selection = self.spare_part_var.get()
        quantity_str = self.quantity_var.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        if not part_selection:
            messagebox.showwarning(self.lang.get('warning_title', "Attenzione"),
                                   self.lang.get('warning_select_part', "Selezionare una parte di ricambio."),
                                   parent=self)
            return

        try:
            quantity = int(quantity_str)
            if quantity <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning(self.lang.get('warning_title', "Attenzione"),
                                   self.lang.get('warning_invalid_quantity',
                                                 "La quantità deve essere un numero intero positivo."), parent=self)
            return

        spare_part_id = self.spare_parts_data.get(part_selection)

        success = self.db.insert_spare_part_request(
            equipment_id=self.equipment_id,
            spare_part_id=spare_part_id,
            quantity=quantity,
            notes=notes,
            requested_by=self.user_name
        )

        if success:
            messagebox.showinfo(self.lang.get('success_title', "Successo"),
                                self.lang.get('info_request_sent', "Richiesta inviata con successo."), parent=self)
            self.destroy()
        else:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 f"{self.lang.get('error_sending_request', 'Impossibile inviare la richiesta.')}\n\n{self.db.last_error_details}",
                                 parent=self)
    def _open_add_new_part_window(self):
        """Apre la finestra per aggiungere un nuovo materiale e gestisce il risultato."""
        add_window = AddNewSparePartWindow(self, self.db, self.lang)
        self.wait_window(add_window)  # Pausa l'esecuzione finché la finestra non è chiusa

        # Dopo che la finestra è stata chiusa, controlliamo se è stato creato un nuovo ID
        newly_created_id = add_window.new_part_id
        if newly_created_id:
            # Se sì, ricarichiamo la lista dei ricambi e la impostiamo sul nuovo valore
            self._load_spare_parts(select_id=newly_created_id)

    # In richieste_intervento.py, dentro la classe RequestWindow

    def _load_spare_parts(self, select_id=None):
        """
        Carica i ricambi dal DB. Se viene fornito select_id,
        tenta di preselezionare quell'elemento nel combobox.
        """
        self.spare_parts_data = {}  # Pulisci i dati vecchi
        spare_parts = self.db.fetch_spare_parts()
        if not spare_parts:
            # Gestisci il caso in cui non ci sono ricambi
            self.spare_parts_combo['values'] = []
            return

        # Costruisci la mappa dei dati e la lista per il display
        display_list = []
        value_to_select = ""
        for part in spare_parts:
            # Assumiamo che MaterialPartNumber e MaterialCode possano essere NULL
            part_number = part.MaterialPartNumber or "N/A"
            part_code = part.MaterialCode or ""
            display_text = f"{part_number} - {part_code}"
            self.spare_parts_data[display_text] = part.SparePartMaterialId
            display_list.append(display_text)

            # Se questo è l'ID che vogliamo selezionare, memorizziamo il testo corrispondente
            if select_id and part.SparePartMaterialId == select_id:
                value_to_select = display_text

        # Popola e ordina il combobox
        self.spare_parts_combo['values'] = sorted(display_list)

        # Se abbiamo un valore da preselezionare, impostalo
        if value_to_select:
            self.spare_part_var.set(value_to_select)

    # NUOVO METODO: Gestisce l'aggiunta di una nuova parte al catalogo
    def _handle_new_part(self, material_part_number):
        """Chiede all'utente di aggiungere una nuova parte (MaterialPartNumber) al catalogo."""

        # Chiedi conferma all'utente
        confirm_msg = self.lang.get('confirm_add_new_part',
                                    "La parte '{0}' non esiste nel catalogo. Vuoi aggiungerla?").format(
            material_part_number)
        if not messagebox.askyesno(self.lang.get('new_part_title', "Nuova Parte"), confirm_msg, parent=self):
            return None

        # Richiesta 1: MaterialCode
        material_code = simpledialog.askstring(self.lang.get('new_part_title', "Nuova Parte"),
                                               self.lang.get('enter_material_code',
                                                             "Inserisci Codice Materiale (Opzionale):"),
                                               parent=self)

        # Richiesta 2: MaterialDescription
        material_description = simpledialog.askstring(self.lang.get('new_part_title', "Nuova Parte"),
                                                      self.lang.get('enter_material_description',
                                                                    "Inserisci Descrizione Materiale (Opzionale):"),
                                                      parent=self)

        # Chiama il metodo DB aggiornato in main.py
        new_id = self.db.add_new_spare_part(material_part_number, material_code, material_description, to_be_revizited=1)

        if new_id:
            messagebox.showinfo(self.lang.get('success_title'),
                                self.lang.get('info_part_added', "Parte aggiunta al catalogo con successo."),
                                parent=self)

            # Ricarica la lista per includere il nuovo elemento
            self._load_spare_parts()

            # Seleziona automaticamente il nuovo elemento nel combo box
            # Dobbiamo ricostruire il testo visualizzato esatto per selezionarlo
            new_display_text = f"{material_part_number} [{material_code or 'N/D'}]"
            if material_description:
                # Assicurati che la formattazione corrisponda a _load_spare_parts
                new_display_text += f" - {material_description[:50]}..."

            # Imposta il valore nel combobox (questo aggiorna anche self.part_var)
            self.part_combo.set(new_display_text)

            return new_id
        else:
            # Qui verrà mostrato l'errore SQL se il DB fallisce (grazie alla correzione in main.py)
            messagebox.showerror(self.lang.get('error_title'), self.lang.get('error_adding_part',
                                                                             "Errore nell'aggiunta della parte al catalogo.") + f"\n{self.db.last_error_details}",
                                 parent=self)
            return None

    # METODO AGGIORNATO: Sostituisci il metodo _submit_request esistente con questo
    def _submit_request(self):
        # Usa .strip() per rimuovere spazi bianchi
        part_selection = self.part_var.get().strip()
        quantity_str = self.quantity_var.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        # 1. Validazione Input Base (Invariata)
        if not part_selection:
            messagebox.showerror(self.lang.get('error_title'),
                                 self.lang.get('error_part_required', "Selezionare o digitare una parte/servizio."),
                                 parent=self)
            return

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(self.lang.get('error_title'),
                                 self.lang.get('error_invalid_quantity', "Inserire una quantità numerica valida (>0)."),
                                 parent=self)
            return

        # 2. Gestione ID Parte (Esistente o Nuova)
        # Controlla se il testo digitato corrisponde esattamente a una voce esistente nel dizionario
        spare_part_id = self.spare_parts_data.get(part_selection)

        if not spare_part_id:
            # L'utente ha digitato un valore non presente nella lista
            # Passiamo il testo digitato (part_selection) come MaterialPartNumber
            spare_part_id = self._handle_new_part(part_selection)

            # Se l'utente ha annullato l'inserimento o se l'inserimento è fallito
            if not spare_part_id:
                return

                # 3. Chiamata DB (Inserimento Richiesta) (Invariata)
        success = self.db.insert_spare_part_request(
            equipment_id=self.equipment_id,
            spare_part_id=spare_part_id,
            quantity=quantity,
            notes=notes,
            requested_by=self.user_name
        )

        if success:
            # 4. Invio Email (Invariata)
            self._send_notification_email(part_selection, quantity, notes)

            messagebox.showinfo(self.lang.get('success_title'),
                                self.lang.get('info_request_submitted', "Richiesta inviata con successo."), parent=self)
            self.destroy()
        else:
            messagebox.showerror(self.lang.get('error_title'), self.db.last_error_details, parent=self)

    # NUOVO METODO: Gestisce la logica di invio email
    def _send_notification_email(self, part_name, quantity, notes):
        """Recupera i destinatari e invia l'email di notifica."""

        # 1. Recupera destinatari dal DB usando il nuovo metodo fetch_setting
        recipients_str = self.db.fetch_setting('SparePartRequest')

        if not recipients_str:
            print(
                "Attenzione: Nessun destinatario email configurato in Settings (SparePartRequest). Email non inviata.")
            return

        # Separa gli indirizzi (gestisce virgola e punto e virgola)
        recipients = [email.strip() for email in recipients_str.replace(';', ',').split(',') if email.strip()]

        # 2. Prepara Oggetto (Localizzato)
        # Usa la chiave di traduzione 'email_request_subject' con placeholder {0} per il nome macchina
        subject_template = self.lang.get('email_request_subject', "Richiesta spare part per macchina {0}")
        subject = subject_template.format(self.equipment_name)

        # 3. Prepara Corpo Email (Localizzazione di base per il corpo)
        body = f"""
{self.lang.get('email_body_intro', "Nuova richiesta di parti di ricambio/intervento inserita.")}

{self.lang.get('select_machine_label')}: {self.equipment_name} (ID: {self.equipment_id})
{self.lang.get('requested_by_label')}: {self.user_name}
{self.lang.get('header_date')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

--- {self.lang.get('request_details_label')} ---
{self.lang.get('select_part_service_label')}: {part_name}
{self.lang.get('quantity_label')}: {quantity}

{self.lang.get('notes_label')}:
{notes}
"""
        # 4. Invia Email usando l'utility
        email_success = utils.send_email(recipients, subject, body)

        if not email_success:
            messagebox.showwarning(self.lang.get('warning_title'), self.lang.get('warn_email_failed',
                                                                                 "La richiesta è stata salvata nel database, ma l'invio dell'email di notifica è fallito. Verificare le impostazioni SMTP o la connessione di rete."),
                                   parent=self)


# Funzione Launcher (Invariata)
def open_request_window(parent, db, lang, user_name, equipment_id, equipment_name):
    RequestWindow(parent, db, lang, user_name, equipment_id, equipment_name)