
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
        self.all_equipment_names = []  # Lista completa equipment per filtro
        self.current_equipment_id = None

        self.title(self.lang.get('calibrations_title', "Gestione Calibrazioni"))
        self.geometry("680x760")  # Aumentata altezza per sezione documenti multipli
        self.transient(parent)
        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._create_widgets()
        self._load_initial_data()

        self.selected_pdf_path = None  # nome del primo PDF scelto (retrocompatibilita')
        self.selected_pdf_bytes = None  # bytes del primo PDF scelto (retrocompatibilita')
        self.current_cert_bytes = None  # bytes del certificato legacy dell'ultima calibrazione caricata
        self.selected_docs = []  # lista di dict {'filename', 'bytes'} per upload multiplo
        self.current_docs = {}  # indice listbox -> (doc_id, filename) oppure ('legacy', filename)
        self.current_calibration_id = None

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # COMBOBOX MACCHINARI IN TESTA ALLA FORM
        select_frame = ttk.LabelFrame(main_frame, text=self.lang.get('select_equipment', "Seleziona Attrezzatura"),
                                      padding="10")
        select_frame.pack(fill=tk.X, expand=True, pady=(0, 10))

        # Intestazione con logo + istruzione per l'operatore
        header = ttk.Frame(select_frame)
        header.pack(fill=tk.X, pady=(0, 8))
        try:
            from PIL import Image, ImageTk
            img = Image.open("Logo.png")
            img.thumbnail((48, 48))
            self._logo_img = ImageTk.PhotoImage(img)
            ttk.Label(header, image=self._logo_img).pack(side="left", padx=(0, 10))
        except Exception:
            pass
        ttk.Label(header,
                  text=self.lang.get('calibration_search_hint',
                                     "Ricerca l'attrezzatura per aggiungere le informazioni di calibrazione."),
                  wraplength=480, font=('Segoe UI', 10, 'italic')).pack(side="left", fill=tk.X, expand=True)

        self.combo_equipment = ttk.Combobox(select_frame, state="normal", font=('Segoe UI', 10))
        self.combo_equipment.pack(fill=tk.X, expand=True)
        self.combo_equipment.bind("<<ComboboxSelected>>", self._on_equipment_select)
        self.combo_equipment.bind('<KeyRelease>', self._on_equipment_search)

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

        # Bottone Export Storico
        self.btn_export_history = ttk.Button(self.details_frame,
                                             text=self.lang.get('export_history', "Esporta Storico"),
                                             command=self._export_calibration_history,
                                             state="disabled")
        self.btn_export_history.grid(row=3, column=1, columnspan=2, sticky="e", pady=5, padx=5)

        # Elenco documenti dell'ultima calibrazione
        ttk.Label(self.details_frame, text=self.lang.get('calib_docs_label', "Documenti allegati:")).grid(
            row=4, column=0, sticky="w", pady=(10, 2), padx=5)
        self.details_frame.columnconfigure(0, weight=1)
        docs_row = ttk.Frame(self.details_frame)
        docs_row.grid(row=5, column=0, columnspan=3, sticky="ew", pady=2, padx=5)
        self.lb_docs = tk.Listbox(docs_row, height=4, font=('Segoe UI', 9))
        sb_docs = ttk.Scrollbar(docs_row, orient="vertical", command=self.lb_docs.yview)
        self.lb_docs.configure(yscrollcommand=sb_docs.set)
        self.lb_docs.pack(side="left", fill=tk.BOTH, expand=True)
        sb_docs.pack(side="left", fill="y")
        self.lb_docs.bind('<Double-Button-1>', lambda e: self._open_selected_document())
        self.btn_open_doc = ttk.Button(self.details_frame,
                                       text=self.lang.get('calib_open_document', "Apri documento"),
                                       command=self._open_selected_document, state="disabled")
        self.btn_open_doc.grid(row=6, column=2, sticky="e", pady=2, padx=5)

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

        # Upload multiplo PDF (relazione uno-a-molti con la calibrazione)
        ttk.Label(self.insert_frame, text=self.lang.get('certificate_pdf', "Certificato (PDF):")).grid(row=2,
                                                                                                       column=0,
                                                                                                       sticky="nw",
                                                                                                       pady=5, padx=5)
        docs_sel_row = ttk.Frame(self.insert_frame)
        docs_sel_row.grid(row=2, column=1, columnspan=2, sticky="ew", pady=5, padx=5)
        self.lb_selected_docs = tk.Listbox(docs_sel_row, height=4, font=('Segoe UI', 9))
        sb_sel = ttk.Scrollbar(docs_sel_row, orient="vertical", command=self.lb_selected_docs.yview)
        self.lb_selected_docs.configure(yscrollcommand=sb_sel.set)
        self.lb_selected_docs.pack(side="left", fill=tk.BOTH, expand=True)
        sb_sel.pack(side="left", fill="y")
        self.lbl_cert_file = ttk.Label(self.insert_frame,
                                       text=self.lang.get('no_file_selected', "Nessun file selezionato"),
                                       foreground="gray")
        self.lbl_cert_file.grid(row=3, column=1, sticky="w", pady=(0, 5), padx=5)

        btns_row = ttk.Frame(self.insert_frame)
        btns_row.grid(row=4, column=1, columnspan=2, sticky="e", pady=2, padx=5)
        self.btn_upload_pdf = ttk.Button(btns_row, text=self.lang.get('calib_add_pdf', "Aggiungi PDF"),
                                         command=self._choose_pdf_file)
        self.btn_upload_pdf.pack(side="left", padx=(0, 5))
        self.btn_remove_doc = ttk.Button(btns_row, text=self.lang.get('calib_remove_selected', "Rimuovi selezionato"),
                                         command=self._remove_selected_doc, state="disabled")
        self.btn_remove_doc.pack(side="left")

        self.btn_save = ttk.Button(self.insert_frame, text=self.lang.get('save_button', "Salva"),
                                   command=self._save_calibration)
        self.btn_save.grid(row=5, column=1, sticky="e", pady=10, padx=5)
        self.btn_save.state(["disabled"])  # Disabilitato finché non viene caricato almeno un PDF

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
            self.all_equipment_names = equipment_display_list  # Salva lista completa per filtro
            self.combo_equipment['values'] = equipment_display_list
        except Exception as e:
            messagebox.showerror(self.lang.get('error', "Errore"), f"Impossibile caricare la lista attrezzature:\n{e}",
                                 parent=self)

    def _on_equipment_search(self, event=None):
        """Filtra la lista equipment mentre l'utente digita"""
        value = self.combo_equipment.get().lower()
        if value == '':
            self.combo_equipment['values'] = self.all_equipment_names
        else:
            filtered_data = [name for name in self.all_equipment_names if value in name.lower()]
            self.combo_equipment['values'] = filtered_data

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
            # reset stato certificati e documenti
            self.current_cert_bytes = None
            self.selected_pdf_path = None
            self.selected_pdf_bytes = None
            self.selected_docs = []
            self.lb_selected_docs.delete(0, tk.END)
            self._refresh_selected_docs_label()
            self.current_docs = {}
            self.current_calibration_id = None
            self.lb_docs.delete(0, tk.END)
            self.btn_open_doc.configure(state="disabled")

            row = self.db.get_last_calibration(equipment_id)

            if row:
                self.lbl_last_date.config(text=str(row.CalibratedOn) if row.CalibratedOn else "N/D")
                self.lbl_expiry_date.config(text=str(row.ExpireOn) if row.ExpireOn else "NESSUNA")
                # certificato (colonna legacy)
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
                # Abilita export storico
                self.btn_export_history.configure(state="normal")
                # Documenti allegati (tabella uno-a-molti, fallback su legacy)
                self.current_calibration_id = getattr(row, 'CalibrationId', None)
                self._load_documents_list(cert)
            else:
                self.lbl_last_date.config(text="Nessuna calibrazione registrata")
                self.lbl_expiry_date.config(text="N/D")
                self.lbl_cert_status.config(text=self.lang.get('certificate_absent', "Assente"))
                self.btn_open_cert.configure(state="disabled")
                # Abilita export storico anche se non ci sono calibrazioni (per mostrare vuoto)
                self.btn_export_history.configure(state="normal")

            self.details_frame.pack(fill=tk.X, expand=True, pady=10)

            # Mostra sempre il frame di inserimento per nuove calibrazioni
            self.insert_frame.pack(fill=tk.X, expand=True, pady=10)

        except Exception as e:
            messagebox.showerror(self.lang.get('error', "Errore"), f"Impossibile caricare i dati di calibrazione:\n{e}",
                                 parent=self)

    def _load_documents_list(self, legacy_cert):
        """Popola la lista documenti dell'ultima calibrazione (fallback sulla colonna legacy)"""
        self.lb_docs.delete(0, tk.END)
        self.current_docs = {}
        docs = []
        if self.current_calibration_id:
            try:
                docs = self.db.get_calibration_documents(self.current_calibration_id) or []
            except Exception as e:
                logger.error(f"Errore caricamento documenti calibrazione {self.current_calibration_id}: {e}")
                docs = []
        idx = 0
        for d in docs:
            label = d.FileName
            if getattr(d, 'UploadedOn', None):
                label = f"{d.FileName}  ({d.UploadedOn})"
            self.lb_docs.insert(tk.END, label)
            self.current_docs[idx] = (d.Id, d.FileName)
            idx += 1
        if idx == 0 and legacy_cert:
            self.lb_docs.insert(tk.END, "certificato.pdf")
            self.current_docs[0] = ('legacy', 'certificato.pdf')
            idx += 1
        if idx == 0:
            self.lb_docs.insert(tk.END, self.lang.get('calib_no_documents', "Nessun documento allegato"))
        self.btn_open_doc.configure(state="normal" if idx else "disabled")

    def _refresh_selected_docs_label(self):
        """Aggiorna conteggio/label dei PDF selezionati e lo stato dei pulsanti"""
        n = len(self.selected_docs)
        self.selected_pdf_bytes = self.selected_docs[0]['bytes'] if n else None
        self.selected_pdf_path = self.selected_docs[0]['filename'] if n else None
        if n:
            self.lbl_cert_file.config(text=f"{n} PDF", foreground="black")
            self.btn_save.state(["!disabled"])
            self.btn_remove_doc.state(["!disabled"])
        else:
            self.lbl_cert_file.config(text=self.lang.get('no_file_selected', "Nessun file selezionato"),
                                      foreground="gray")
            self.btn_save.state(["disabled"])
            self.btn_remove_doc.state(["disabled"])

    def _remove_selected_doc(self):
        sel = self.lb_selected_docs.curselection()
        if not sel:
            return
        idx = sel[0]
        self.lb_selected_docs.delete(idx)
        if 0 <= idx < len(self.selected_docs):
            self.selected_docs.pop(idx)
        self._refresh_selected_docs_label()

    def _export_calibration_history(self):
        """Esporta lo storico calibrazioni dell'equipment selezionato in Excel"""
        if not self.current_equipment_id:
            messagebox.showwarning(
                self.lang.get('warning', "Attenzione"),
                "Selezionare un'attrezzatura prima di esportare lo storico.",
                parent=self
            )
            return

        try:
            # Recupera nome equipment per il filename
            selected_equipment_name = self.combo_equipment.get()
            equipment_safe_name = selected_equipment_name.replace('/', '_').replace('\\', '_').replace(':', '_')

            # Recupera tutte le calibrazioni per questo equipment (anche quelle non valide)
            calibrations = self.db.get_all_calibrations_history(self.current_equipment_id)

            if not calibrations:
                messagebox.showinfo(
                    self.lang.get('info', "Informazione"),
                    "Nessuna calibrazione trovata per questa attrezzatura.",
                    parent=self
                )
                return

            # Crea directory C:\Temp se non esiste
            import os
            temp_dir = r"C:\Temp"
            os.makedirs(temp_dir, exist_ok=True)

            # Nome file con timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Calibrazioni_{equipment_safe_name}_{timestamp}.xlsx"
            filepath = os.path.join(temp_dir, filename)

            # Crea Excel con openpyxl
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment

            wb = Workbook()
            ws = wb.active
            ws.title = "Storico Calibrazioni"

            # Header
            headers = [
                "ID Calibrazione",
                "Data Calibrazione",
                "Data Scadenza",
                "Ente Certificatore",
                "Valido"
            ]

            # Stile header
            header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF")

            for col_num, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col_num, value=header)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center")

            # Dati
            for row_num, cal in enumerate(calibrations, 2):
                ws.cell(row=row_num, column=1, value=cal.CalibrationID)
                ws.cell(row=row_num, column=2, value=str(cal.CalibratedOn) if cal.CalibratedOn else "N/D")
                ws.cell(row=row_num, column=3, value=str(cal.ExpireOn) if cal.ExpireOn else "N/D")

                # Recupera nome fornitore
                supplier_name = "N/D"
                if hasattr(cal, 'SupplierId') and cal.SupplierId:
                    for name, id_val in self.supplier_map.items():
                        if id_val == cal.SupplierId:
                            supplier_name = name
                            break
                ws.cell(row=row_num, column=4, value=supplier_name)

                ws.cell(row=row_num, column=5, value="Sì" if getattr(cal, 'IsValid', 1) == 1 else "No")

            # Auto-size columns
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width

            # Salva file
            wb.save(filepath)

            # Apri file automaticamente
            if hasattr(os, "startfile"):  # Windows
                os.startfile(filepath)
            else:
                if sys.platform == "darwin":
                    subprocess.Popen(["open", filepath])
                else:
                    subprocess.Popen(["xdg-open", filepath])

            messagebox.showinfo(
                self.lang.get('success', "Successo"),
                f"Storico esportato con successo:\n{filepath}",
                parent=self
            )

        except Exception as e:
            messagebox.showerror(
                self.lang.get('error', "Errore"),
                f"Errore durante l'esportazione:\n{e}",
                parent=self
            )
            logger.error(f"Errore export calibrazioni: {e}", exc_info=True)

    def _choose_pdf_file(self):
        """Permette di aggiungere uno o più PDF alla lista dei documenti da allegare"""
        paths = filedialog.askopenfilenames(
            title=self.lang.get('select_pdf_title', "Seleziona file PDF"),
            filetypes=[("PDF", "*.pdf")]
        )
        if not paths:
            return
        loaded = 0
        for path in paths:
            try:
                with open(path, "rb") as f:
                    data = f.read()
                if not data:
                    raise ValueError("Empty file")
                filename = os.path.basename(path)
                # Evita duplicati con lo stesso nome nella lista
                if any(d['filename'] == filename for d in self.selected_docs):
                    continue
                self.selected_docs.append({'filename': filename, 'bytes': data})
                self.lb_selected_docs.insert(tk.END, filename)
                loaded += 1
            except Exception as e:
                messagebox.showerror(self.lang.get('error', "Errore"),
                                     self.lang.get('pdf_load_error', f"Impossibile caricare il PDF: {e}"),
                                     parent=self)
        self._refresh_selected_docs_label()

    def _open_file_bytes(self, data, filename):
        """Scrive i dati binari su un file temporaneo e li apre con l'applicazione predefinita"""
        try:
            data = bytes(data)
        except Exception:
            pass  # pyodbc può restituire già bytes
        suffix = os.path.splitext(filename)[1] or ".pdf"
        fd, temp_path = tempfile.mkstemp(prefix="calibration_", suffix=suffix)
        os.close(fd)
        with open(temp_path, "wb") as f:
            f.write(data)
        # Apri con app predefinita
        if hasattr(os, "startfile"):  # Windows
            os.startfile(temp_path)
        else:
            if sys.platform == "darwin":
                subprocess.Popen(["open", temp_path])
            else:
                subprocess.Popen(["xdg-open", temp_path])

    def _open_certificate(self):
        if not self.current_cert_bytes:
            messagebox.showinfo(self.lang.get('info', "Informazione"),
                                self.lang.get('no_certificate_to_open', "Nessun certificato da aprire."),
                                parent=self)
            return
        try:
            self._open_file_bytes(self.current_cert_bytes, 'certificato.pdf')
        except Exception as e:
            messagebox.showerror(self.lang.get('error', "Errore"),
                                 self.lang.get('pdf_open_error', f"Impossibile aprire il PDF: {e}"),
                                 parent=self)

    def _open_selected_document(self):
        """Apre il documento selezionato nella lista dell'ultima calibrazione"""
        sel = self.lb_docs.curselection()
        if not sel:
            return
        entry = self.current_docs.get(sel[0])
        if not entry:
            return
        doc_id, filename = entry
        try:
            if doc_id == 'legacy':
                self._open_certificate()
                return
            row = self.db.get_calibration_document_data(doc_id)
            if not row or not row.DocumentData:
                messagebox.showinfo(self.lang.get('info', "Informazione"),
                                    self.lang.get('no_certificate_to_open', "Nessun certificato da aprire."),
                                    parent=self)
                return
            self._open_file_bytes(row.DocumentData, row.FileName or filename)
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
        if not self.selected_docs:
            messagebox.showwarning(
                self.lang.get('missing_data', "Dati Mancanti"),
                self.lang.get('certificate_required', "Caricare un certificato PDF prima di salvare."),
                parent=self
            )
            return

        try:
            # LOGICA SEMPLIFICATA: Sempre INSERT nuovo record
            # 1. Invalida tutte le calibrazioni precedenti per questo equipment (IsValid = 0)
            self.db.invalidate_previous_calibrations(equipment_id)

            # 2. Inserisce la nuova calibrazione (IsValid = 1 di default).
            #    Il primo PDF viene salvato anche nella colonna legacy NrCertificate
            #    per retrocompatibilità con i lettori esistenti.
            first_bytes = self.selected_docs[0]['bytes']
            new_cal_id = self.db.add_new_calibration(
                equipment_id,
                new_expiry_date,
                supplier_id,
                first_bytes,
                username
            )

            # 3. Inserisce tutti i documenti nella tabella uno-a-molti
            if new_cal_id:
                for doc in self.selected_docs:
                    self.db.add_calibration_document(new_cal_id, doc['filename'], doc['bytes'], username)
            else:
                logger.error("add_new_calibration non ha restituito un CalibrationId; documenti non salvati")

            messagebox.showinfo(
                self.lang.get('success', "Successo"),
                "Nuova calibrazione inserita correttamente.",
                parent=self
            )

            # Reset campi
            self.selected_docs = []
            self.lb_selected_docs.delete(0, tk.END)
            self._refresh_selected_docs_label()
            self.combo_cert_body.set('')

            # Ricarica dati per mostrare la nuova calibrazione
            self._load_calibration_data(equipment_id)

        except Exception as e:
            messagebox.showerror(
                self.lang.get('error', "Errore di Salvataggio"),
                f"Impossibile salvare i dati:\n{e}",
                parent=self
            )

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
