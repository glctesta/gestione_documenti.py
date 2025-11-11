
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import collections.abc
from tkinter import filedialog
import os, sys, tempfile, subprocess

import logging

logger = logging.getLogger(__name__)

class CalibrationsWindow(tk.Toplevel):
    def __init__(self, parent, db_object, language_manager):
        super().__init__(parent)
        self.parent = parent
        self.db = db_object
        self.lang = language_manager

        self.equipment_map = {}
        self.supplier_map = {}
        self.all_supplier_names = []
        self.current_equipment_id = None
        self.current_calibration_id = None  # ID della calibrazione selezionata per modifica

        self.title(self.lang.get('calibrations_title', "Gestione Calibrazioni"))
        self.geometry("650x600")  # Aumentata altezza per il nuovo bottone
        self.transient(parent)
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._create_widgets()
        self._load_initial_data()

        self.selected_pdf_path = None  # PDF scelto per nuovo inserimento
        self.selected_pdf_bytes = None  # bytes del PDF scelto per nuovo inserimento
        self.current_cert_bytes = None  # bytes del certificato dell'ultima calibrazione caricata

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # COMBOBOX MACCHINARI IN TESTA ALLA FORM
        select_frame = ttk.LabelFrame(main_frame, text=self.lang.get('select_equipment', "Seleziona Attrezzatura"),
                                      padding="10")
        select_frame.pack(fill=tk.X, expand=True, pady=(0, 10))
        self.combo_equipment = ttk.Combobox(select_frame, state="readonly", font=('Segoe UI', 10))
        self.combo_equipment.pack(fill=tk.X, expand=True)
        self.combo_equipment.bind("<<ComboboxSelected>>", self._on_equipment_select)

        # BOTTONE MODIFICA (visibile solo quando esiste una calibrazione)
        self.btn_edit_frame = ttk.Frame(main_frame)
        self.btn_edit_frame.pack(fill=tk.X, pady=(0, 10))
        self.btn_edit_calibration = ttk.Button(
            self.btn_edit_frame,
            text=self.lang.get('edit_calibration', "Modifica Calibrazione"),
            command=self._edit_calibration,
            state="disabled"
        )
        self.btn_edit_calibration.pack(side=tk.LEFT)

        self.details_frame = ttk.LabelFrame(main_frame,
                                            text=self.lang.get('calibration_details', "Dettagli Ultima Calibrazione"),
                                            padding="10")
        ttk.Label(self.details_frame, text=self.lang.get('last_calibration_date', "Data ultima calibrazione:")).grid(
            row=0, column=0, sticky="w", pady=2, padx=5)
        self.lbl_last_date = ttk.Label(self.details_frame, text="N/D", font=('Segoe UI', 10, 'bold'))
        self.lbl_last_date.grid(row=0, column=1, sticky="w", pady=2, padx=5)
        ttk.Label(self.details_frame, text=self.lang.get('expiry_date', "Data di scadenza:")).grid(row=1, column=0,
                                                                                                   sticky="w", pady=2,
                                                                                                   padx=5)
        self.lbl_expiry_date = ttk.Label(self.details_frame, text="N/D", font=('Segoe UI', 10, 'bold'))
        self.lbl_expiry_date.grid(row=1, column=1, sticky="w", pady=2, padx=5)

        # Stato certificato + apri
        ttk.Label(self.details_frame, text=self.lang.get('certificate_status', "Stato certificato:")).grid(
            row=2, column=0, sticky="w", pady=2, padx=5)
        self.lbl_cert_status = ttk.Label(self.details_frame, text=self.lang.get('certificate_absent', "Assente"))
        self.lbl_cert_status.grid(row=2, column=1, sticky="w", pady=2, padx=5)
        self.btn_open_cert = ttk.Button(self.details_frame, text=self.lang.get('open_certificate', "Apri certificato"),
                                        command=self._open_certificate, state="disabled")
        self.btn_open_cert.grid(row=2, column=2, sticky="e", pady=2, padx=5)

        self.insert_frame = ttk.LabelFrame(main_frame,
                                           text=self.lang.get('new_calibration_data', "Inserisci Nuova Calibrazione"),
                                           padding="10")
        ttk.Label(self.insert_frame, text=self.lang.get('new_expiry_date', "Nuova data di scadenza:")).grid(row=0,
                                                                                                            column=0,
                                                                                                            sticky="w",
                                                                                                            pady=5,
                                                                                                            padx=5)
        self.entry_new_expiry_date = DateEntry(self.insert_frame, width=18, background='darkblue', foreground='white',
                                               borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_new_expiry_date.grid(row=0, column=1, sticky="w", pady=5, padx=5)

        ttk.Label(self.insert_frame, text=self.lang.get('certifying_body', "Ente certificatore:")).grid(row=1, column=0,
                                                                                                        sticky="w",
                                                                                                        pady=5, padx=5)
        self.combo_cert_body = ttk.Combobox(self.insert_frame, width=35)
        self.combo_cert_body.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        self.combo_cert_body.bind('<KeyRelease>', self._on_supplier_search)
        self.combo_cert_body.bind('<<ComboboxSelected>>', lambda e: self.focus())

        # Sostituisce "Numero certificato" con Upload PDF
        ttk.Label(self.insert_frame, text=self.lang.get('certificate_pdf', "Certificato (PDF):")).grid(row=2,
                                                                                                       column=0,
                                                                                                       sticky="w",
                                                                                                       pady=5, padx=5)
        self.lbl_cert_file = ttk.Label(self.insert_frame,
                                       text=self.lang.get('no_file_selected', "Nessun file selezionato"),
                                       foreground="gray")
        self.lbl_cert_file.grid(row=2, column=1, sticky="w", pady=5, padx=5)
        self.btn_upload_pdf = ttk.Button(self.insert_frame, text=self.lang.get('upload_pdf', "Carica PDF"),
                                         command=self._choose_pdf_file)
        self.btn_upload_pdf.grid(row=2, column=2, sticky="w", pady=5, padx=5)

        self.btn_save = ttk.Button(self.insert_frame, text=self.lang.get('save_button', "Salva"),
                                   command=self._save_calibration)
        self.btn_save.grid(row=3, column=1, sticky="e", pady=10, padx=5)
        self.btn_save.state(["disabled"])  # Disabilitato finché non viene caricato un PDF

    def _load_initial_data(self):
        self._load_equipment_list()
        self._load_suppliers()

    def _load_equipment_list(self):
        try:
            rows = self.db.get_calibratable_equipment()
            if not rows:
                self.combo_equipment['values'] = [
                    self.lang.get('no_equipment_found', "Nessuna attrezzatura da calibrare trovata.")]
                return
            equipment_display_list = [f"{row.InternalName} (Mat: {row.InventoryNumber}) - {row.Brand}" for row in rows]
            self.equipment_map = {f"{row.InternalName} (Mat: {row.InventoryNumber}) - {row.Brand}": row.EquipmentId for
                                  row in rows}
            self.combo_equipment['values'] = equipment_display_list
        except Exception as e:
            messagebox.showerror(self.lang.get('error', "Errore"), f"Impossibile caricare la lista attrezzature:\n{e}",
                                 parent=self)

    def _load_suppliers(self):
        try:
            rows = self.db.get_suppliers()
            if not rows: return
            self.all_supplier_names = sorted([row.SiteName for row in rows])
            self.supplier_map = {row.SiteName: row.IDSite for row in rows}
            self.combo_cert_body['values'] = self.all_supplier_names
        except Exception as e:
            messagebox.showerror(self.lang.get('error', "Errore"), f"Impossibile caricare la lista fornitori:\n{e}",
                                 parent=self)

    def _on_supplier_search(self, event=None):
        value = self.combo_cert_body.get().lower()
        if value == '':
            self.combo_cert_body['values'] = self.all_supplier_names
        else:
            filtered_data = [name for name in self.all_supplier_names if value in name.lower()]
            self.combo_cert_body['values'] = filtered_data

    def _on_equipment_select(self, event=None):
        selected_display_name = self.combo_equipment.get()
        if not selected_display_name: return
        equipment_id = self.equipment_map.get(selected_display_name)
        if equipment_id:
            self.current_equipment_id = equipment_id
            self._load_calibration_data(equipment_id)

    def _load_calibration_data(self, equipment_id):
        try:
            self.insert_frame.pack_forget()
            self.details_frame.pack_forget()
            self.btn_edit_frame.pack_forget()

            # reset stato certificati
            self.current_cert_bytes = None
            self.selected_pdf_path = None
            self.selected_pdf_bytes = None
            self.lbl_cert_file.config(text=self.lang.get('no_file_selected', "Nessun file selezionato"),
                                      foreground="gray")
            self.btn_save.state(["disabled"])
            self.current_calibration_id = None

            row = self.db.get_last_calibration(equipment_id)

            if row:
                self.lbl_last_date.config(text=str(row.CalibratedOn) if row.CalibratedOn else "N/D")
                self.lbl_expiry_date.config(text=str(row.ExpireOn) if row.ExpireOn else "NESSUNA")
                # certificato
                cert = getattr(row, 'NrCertificate', None)
                if cert:
                    try:
                        self.current_cert_bytes = bytes(cert)
                    except Exception:
                        self.current_cert_bytes = cert  # pyodbc può restituire già bytes
                has_cert = bool(self.current_cert_bytes)
                self.lbl_cert_status.config(
                    text=self.lang.get('certificate_present', "Allegato") if has_cert
                    else self.lang.get('certificate_absent', "Assente")
                )
                self.btn_open_cert.configure(state="normal" if has_cert else "disabled")

                # Memorizza l'ID della calibrazione corrente
                self.current_calibration_id = getattr(row, 'CalibrationID', None)

                # Mostra il bottone modifica
                self.btn_edit_calibration.state(["!disabled"])
                self.btn_edit_frame.pack(fill=tk.X, pady=(0, 10))
            else:
                self.lbl_last_date.config(text="Nessuna calibrazione registrata")
                self.lbl_expiry_date.config(text="N/D")
                self.lbl_cert_status.config(text=self.lang.get('certificate_absent', "Assente"))
                self.btn_open_cert.configure(state="disabled")
                self.btn_edit_calibration.state(["disabled"])

            self.details_frame.pack(fill=tk.X, expand=True, pady=10)

            # Mostra sempre il frame di inserimento per nuove calibrazioni
            self.insert_frame.pack(fill=tk.X, expand=True, pady=10)

        except Exception as e:
            messagebox.showerror(self.lang.get('error', "Errore"), f"Impossibile caricare i dati di calibrazione:\n{e}",
                                 parent=self)

    def _edit_calibration(self):
        """Carica i dati della calibrazione corrente nei campi per la modifica"""
        if not self.current_calibration_id:
            return

        try:
            # Recupera i dettagli completi della calibrazione
            calibration_details = self.db.get_calibration_details(self.current_calibration_id)
            if not calibration_details:
                messagebox.showwarning("Attenzione", "Dati della calibrazione non trovati.", parent=self)
                return

            # Popola i campi con i dati esistenti
            if calibration_details.ExpireOn:
                self.entry_new_expiry_date.set_date(calibration_details.ExpireOn)

            if calibration_details.SupplierId:
                supplier_name = self._get_supplier_name_by_id(calibration_details.SupplierId)
                if supplier_name:
                    self.combo_cert_body.set(supplier_name)

            # Gestione PDF esistente
            cert = getattr(calibration_details, 'NrCertificate', None)
            if cert:
                try:
                    self.selected_pdf_bytes = bytes(cert)
                except Exception:
                    self.selected_pdf_bytes = cert

                if self.selected_pdf_bytes:
                    self.lbl_cert_file.config(text="Certificato esistente caricato", foreground="green")
                    self.btn_save.state(["!disabled"])

            messagebox.showinfo("Modifica",
                                "Dati calibrazione caricati per la modifica. Modifica i campi necessari e salva.",
                                parent=self)

        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile caricare i dati per la modifica:\n{e}", parent=self)

    def _get_supplier_name_by_id(self, supplier_id):
        """Restituisce il nome del fornitore dato il suo ID"""
        for name, id_val in self.supplier_map.items():
            if id_val == supplier_id:
                return name
        return None

    def _choose_pdf_file(self):
        path = filedialog.askopenfilename(
            title=self.lang.get('select_pdf_title', "Seleziona file PDF"),
            filetypes=[("PDF", "*.pdf")]
        )
        if not path:
            self.btn_save.state(["disabled"])
            return
        try:
            with open(path, "rb") as f:
                data = f.read()
            if not data:
                raise ValueError("Empty file")
            self.selected_pdf_path = path
            self.selected_pdf_bytes = data
            filename = os.path.basename(path)
            self.lbl_cert_file.config(text=filename, foreground="black")
            self.btn_save.state(["!disabled"])  # abilita il pulsante Salva
        except Exception as e:
            self.btn_save.state(["disabled"])
            messagebox.showerror(self.lang.get('error', "Errore"),
                                 self.lang.get('pdf_load_error', f"Impossibile caricare il PDF: {e}"),
                                 parent=self)

    def _open_certificate(self):
        if not self.current_cert_bytes:
            messagebox.showinfo(self.lang.get('info', "Informazione"),
                                self.lang.get('no_certificate_to_open', "Nessun certificato da aprire."),
                                parent=self)
            return
        try:
            fd, temp_path = tempfile.mkstemp(prefix="calibration_", suffix=".pdf")
            os.close(fd)
            with open(temp_path, "wb") as f:
                f.write(self.current_cert_bytes)
            # Apri con app predefinita
            if hasattr(os, "startfile"):  # Windows
                os.startfile(temp_path)
            else:
                if sys.platform == "darwin":
                    subprocess.Popen(["open", temp_path])
                else:
                    subprocess.Popen(["xdg-open", temp_path])
        except Exception as e:
            messagebox.showerror(self.lang.get('error', "Errore"),
                                 self.lang.get('pdf_open_error', f"Impossibile aprire il PDF: {e}"),
                                 parent=self)

    def _save_calibration(self):
        selected_equipment_name = self.combo_equipment.get()
        equipment_id = self.equipment_map.get(selected_equipment_name)
        selected_supplier_name = self.combo_cert_body.get().strip()
        supplier_id = self.supplier_map.get(selected_supplier_name)
        new_expiry_date = self.entry_new_expiry_date.get_date().strftime('%Y-%m-%d')

        # Recupera il nome utente loggato dal parent
        username = self._get_logged_in_username()

        if not equipment_id:
            messagebox.showwarning(self.lang.get('missing_data', "Dati Mancanti"),
                                   "Selezionare un'attrezzatura valida.", parent=self)
            return
        if not supplier_id:
            messagebox.showwarning(self.lang.get('missing_data', "Dati Mancanti"),
                                   self.lang.get('supplier_not_valid',
                                                 "Selezionare un ente certificatore valido dalla lista."),
                                   parent=self)
            return
        if not self.selected_pdf_bytes:
            messagebox.showwarning(
                self.lang.get('missing_data', "Dati Mancanti"),
                self.lang.get('certificate_required', "Caricare un certificato PDF prima di salvare."),
                parent=self
            )
            return

        try:
            # Verifica se esiste già una calibrazione valida per questa attrezzatura
            existing_calibration = self.db.get_last_calibration(equipment_id)

            if existing_calibration and self.current_calibration_id:
                # MODIFICA: aggiorna la calibrazione esistente
                self.db.update_calibration(
                    self.current_calibration_id,
                    new_expiry_date,
                    supplier_id,
                    self.selected_pdf_bytes,
                    username  # Aggiunto username
                )
                messagebox.showinfo(self.lang.get('success', "Successo"),
                                    "Dati di calibrazione aggiornati correttamente.",
                                    parent=self)
            else:
                # NUOVA INSERZIONE: controlla se ci sono calibrazioni scadute da invalidare
                if existing_calibration:
                    # Imposta IsValid = 0 per le calibrazioni precedenti
                    self.db.invalidate_previous_calibrations(equipment_id)

                # Inserisce la nuova calibrazione
                self.db.add_new_calibration(equipment_id, new_expiry_date, supplier_id, self.selected_pdf_bytes,
                                            username)
                messagebox.showinfo(self.lang.get('success', "Successo"),
                                    "Nuova calibrazione inserita correttamente.",
                                    parent=self)

            # reset campo PDF selezionato
            self.selected_pdf_path = None
            self.selected_pdf_bytes = None
            self.lbl_cert_file.config(text=self.lang.get('no_file_selected', "Nessun file selezionato"),
                                      foreground="gray")
            self.btn_save.state(["disabled"])
            self.combo_cert_body.set('')
            # ricarica dati
            self._load_calibration_data(equipment_id)

        except Exception as e:
            messagebox.showerror(self.lang.get('error', "Errore di Salvataggio"),
                                 f"Impossibile salvare i dati:\n{e}", parent=self)

    def _get_logged_in_username(self):
        """Recupera il nome dell'utente loggato dalla finestra parent"""
        try:
            # Prova a recuperare l'utente dal parent (dove è stato salvato dal login)
            if hasattr(self.parent, 'current_user') and self.parent.current_user:
                return self.parent.current_user.name
            else:
                # Fallback: cerca di recuperare l'utente da qualsiasi metodo disponibile
                if hasattr(self.parent, 'get_current_username'):
                    return self.parent.get_current_username()
                else:
                    return 'Unknown'
        except Exception as e:
            logger.error(f"Errore nel recupero username: {e}")
            return 'Unknown'

    def destroy(self):
        """Override del metodo destroy per cleanup"""
        try:
            # Rilascia eventuali risorse
            self.grab_release()
            # Chiama il destroy della classe padre
            super().destroy()
        except Exception as e:
            logger.error(f"Errore durante il destroy: {e}")
            super().destroy()

    def _on_close(self):
        """Gestisce la chiusura della finestra"""
        try:
            self.grab_release()  # Rilascia il grab
            self.destroy()  # Distrugge la finestra
        except Exception as e:
            logger.error(f"Errore durante la chiusura della finestra: {e}")
            self.destroy()