# richieste_intervento.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog  # Import simpledialog
from datetime import datetime
# Importa il nuovo file utils.py
import utils


class RequestWindow(tk.Toplevel):
    """Finestra per richiedere parti di ricambio o interventi."""

    def __init__(self, parent, db, lang, user_name, equipment_id, equipment_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.equipment_id = equipment_id
        self.equipment_name = equipment_name

        self.title(self.lang.get('request_window_title', "Crea Richiesta Parti/Intervento"))
        self.geometry("600x450")
        self.transient(parent)
        self.grab_set()

        self.spare_parts_data = {}
        self.part_var = tk.StringVar()
        self.quantity_var = tk.StringVar(value="1")  # Default a 1

        self._create_widgets()
        self._load_spare_parts()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)

        # --- Informazioni Contesto (Read-Only) ---
        context_frame = ttk.LabelFrame(frame, text=self.lang.get('context_label', "Contesto"), padding="10")
        context_frame.grid(row=0, column=0, columnspan=2, sticky=tk.EW, pady=5)
        context_frame.columnconfigure(1, weight=1)

        ttk.Label(context_frame, text=self.lang.get('select_machine_label')).grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(context_frame, text=self.equipment_name, font=("Helvetica", 10, "bold")).grid(row=0, column=1,
                                                                                                sticky=tk.W, pady=2)

        ttk.Label(context_frame, text=self.lang.get('requested_by_label', "Richiedente:")).grid(row=1, column=0,
                                                                                                sticky=tk.W, pady=2)
        ttk.Label(context_frame, text=self.user_name).grid(row=1, column=1, sticky=tk.W, pady=2)

        # --- Dettagli Richiesta ---
        details_frame = ttk.LabelFrame(frame, text=self.lang.get('request_details_label', "Dettagli Richiesta"),
                                       padding="10")
        details_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=10)
        details_frame.columnconfigure(1, weight=1)

        # 1. Selezione Parte/Servizio
        # Etichetta aggiornata per indicare la possibilità di digitare
        ttk.Label(details_frame,
                  text=self.lang.get('select_part_service_label', "Seleziona o digita Parte/Servizio:")).grid(row=0,
                                                                                                              column=0,
                                                                                                              sticky=tk.W,
                                                                                                              pady=5)
        # MODIFICATO: Rimosso state='readonly' per permettere l'inserimento manuale
        self.part_combo = ttk.Combobox(details_frame, textvariable=self.part_var, height=15)
        self.part_combo.grid(row=0, column=1, sticky=tk.EW, pady=5)

        # 2. Quantità
        ttk.Label(details_frame, text=self.lang.get('quantity_label', "Quantità:")).grid(row=1, column=0, sticky=tk.W,
                                                                                         pady=5)
        self.quantity_entry = ttk.Entry(details_frame, textvariable=self.quantity_var, width=10)
        self.quantity_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        # 3. Note
        ttk.Label(details_frame, text=self.lang.get('notes_label', "Note Aggiuntive:")).grid(row=2, column=0,
                                                                                             sticky=tk.NW, pady=5)
        self.notes_text = tk.Text(details_frame, height=5, wrap=tk.WORD)
        self.notes_text.grid(row=2, column=1, sticky=tk.EW, pady=5)

        # --- Azioni ---
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=1, sticky=tk.E, pady=10)

        save_button = ttk.Button(button_frame, text=self.lang.get('submit_request_button', "Invia Richiesta"),
                                 command=self._submit_request)
        save_button.pack(side=tk.RIGHT, padx=5)
        cancel_button = ttk.Button(button_frame, text=self.lang.get('cancel_button'), command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)

    def _load_spare_parts(self):
        self.spare_parts_data = {}  # Pulisce i dati esistenti prima del ricaricamento
        parts = self.db.fetch_spare_parts()
        if parts:
            for part in parts:
                try:
                    display_text = f"{part.PartName} [{part.PartCode or 'N/D'}]"
                    if part.Description:
                        display_text += f" - {part.Description[:50]}..."

                    self.spare_parts_data[display_text] = part.SparePartId
                except AttributeError as e:
                    print(f"Errore: Colonna mancante nella tabella SparePartMaterials? Dettaglio: {e}")
                    messagebox.showerror("Errore Struttura DB",
                                         f"Errore nel leggere i dati delle parti di ricambio.\n{e}", parent=self)
                    return

            self.part_combo['values'] = list(self.spare_parts_data.keys())
        else:
            messagebox.showwarning(self.lang.get('warning_title'), self.lang.get('warn_no_spare_parts_found',
                                                                                 "Nessuna parte di ricambio trovata nel database."),
                                   parent=self)

    # NUOVO METODO: Gestisce l'aggiunta di una nuova parte al catalogo
    def _handle_new_part(self, part_name):
        """Chiede all'utente di aggiungere una nuova parte al catalogo e restituisce il nuovo ID."""

        # Chiedi conferma all'utente
        confirm_msg = self.lang.get('confirm_add_new_part',
                                    "La parte '{0}' non esiste nel catalogo. Vuoi aggiungerla?").format(part_name)
        if not messagebox.askyesno(self.lang.get('new_part_title', "Nuova Parte"), confirm_msg, parent=self):
            return None

        # Chiedi dettagli aggiuntivi (Codice Parte e Descrizione) usando simpledialog
        part_code = simpledialog.askstring(self.lang.get('new_part_title', "Nuova Parte"),
                                           self.lang.get('enter_part_code', "Inserisci Codice Parte (Opzionale):"),
                                           parent=self)
        description = simpledialog.askstring(self.lang.get('new_part_title', "Nuova Parte"),
                                             self.lang.get('enter_description', "Inserisci Descrizione (Opzionale):"),
                                             parent=self)

        # Chiama il DB per inserire la nuova parte
        new_id = self.db.add_new_spare_part(part_name, part_code, description)

        if new_id:
            messagebox.showinfo(self.lang.get('success_title'),
                                self.lang.get('info_part_added', "Parte aggiunta al catalogo con successo."),
                                parent=self)
            # Ricarica la lista per includere il nuovo elemento
            self._load_spare_parts()
            return new_id
        else:
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

        # 1. Validazione Input Base
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
        spare_part_id = self.spare_parts_data.get(part_selection)

        if not spare_part_id:
            # L'utente ha digitato un valore non presente nella lista
            spare_part_id = self._handle_new_part(part_selection)

            # Se l'utente ha annullato l'inserimento o se l'inserimento è fallito
            if not spare_part_id:
                return

                # 3. Chiamata DB (Inserimento Richiesta)
        success = self.db.insert_spare_part_request(
            equipment_id=self.equipment_id,
            spare_part_id=spare_part_id,
            quantity=quantity,
            notes=notes,
            requested_by=self.user_name
        )

        if success:
            # 4. Invio Email (NUOVA LOGICA)
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