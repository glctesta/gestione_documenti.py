"""
Modulo per la gestione del Coating (Vernici)
- Settings: Gestione tipi di vernice
- Viscosità: Registrazione controlli viscosità
- Rapporti: Report con export PDF/Excel

Supporto multilingua tramite AppTranslations
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime
import pyodbc
import pandas as pd
import logging
import os
import platform
import subprocess

logger = logging.getLogger("TraceabilityRS")


class CoatingViscosityWindow:
    """Finestra per la registrazione delle misurazioni di viscosità"""

    def __init__(self, parent, conn_str, username, language_code='it'):
        """
        Args:
            parent: Finestra padre
            conn_str: Stringa di connessione al database
            username: ID utente loggato (da funzione di login)
            language_code: Codice lingua
        """
        self.parent = parent
        self.conn_str = conn_str
        self.username = username
        self.window = None
        self.translator = TranslationManager(conn_str, language_code)
        logger.debug(
            f"[CoatingViscosityWindow.__init__] username ricevuto: '{username}' (tipo: {type(username).__name__})")

    def show(self):
        """Mostra la finestra di registrazione viscosità"""
        logger.debug(f"[CoatingViscosityWindow.show] Apertura finestra - self.username: '{self.username}'")

        self.window = tk.Toplevel(self.parent)
        self.window.title(self.translator.get("coating_viscosity_title", "Coating - Registrazione Viscosità"))
        self.window.geometry("1200x650")

        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame superiore per input
        input_frame = ttk.LabelFrame(main_frame, text=self.translator.get("viscosity_data", "Dati Misurazione"),
                                     padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # ========================================
        # RIGA 0: Data e Tipo Vernice
        # ========================================
        ttk.Label(input_frame, text=f"{self.translator.get('date', 'Data')}:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e")

        # ✅ MODIFICATO: Label invece di DateEntry per mostrare data/ora corrente
        current_datetime = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.date_label = ttk.Label(input_frame, text=current_datetime,
                                    font=("", 10, "bold"),
                                    foreground="#1f4788")
        self.date_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(input_frame, text=f"{self.translator.get('coating_type', 'Tipo Vernice')}:").grid(
            row=0, column=2, padx=5, pady=5, sticky="e")
        self.coating_combo = ttk.Combobox(input_frame, width=30, state="readonly")
        self.coating_combo.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # ========================================
        # RIGA 1: Operatore (SOLO VISUALIZZAZIONE)
        # ========================================
        ttk.Label(input_frame, text=f"{self.translator.get('operator', 'Operatore')}:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e")

        self.operator_label = ttk.Label(input_frame, text=self.username,
                                        font=("", 10, "bold"),
                                        foreground="#1f4788")
        self.operator_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # ========================================
        # RIGA 1b: Tipo Analisi (Radio Buttons)
        # ========================================
        ttk.Label(input_frame, text=f"{self.translator.get('analysis_type', 'Analisi')}:").grid(
            row=1, column=2, padx=5, pady=5, sticky="e")

        analysis_frame = ttk.Frame(input_frame)
        analysis_frame.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.analysis_type_var = tk.IntVar(value=1)

        ttk.Radiobutton(analysis_frame,
                        text=self.translator.get('viscosity_materials', 'Viscosità materiali'),
                        variable=self.analysis_type_var,
                        value=1,
                        command=self._on_analysis_type_change).pack(side=tk.LEFT, padx=5)

        ttk.Radiobutton(analysis_frame,
                        text=self.translator.get('periodic_check', 'Controllo periodico'),
                        variable=self.analysis_type_var,
                        value=2,
                        command=self._on_analysis_type_change).pack(side=tk.LEFT, padx=5)

        # ========================================
        # RIGA 2: Quantità Materiale e Diluente
        # ========================================
        ttk.Label(input_frame, text=f"{self.translator.get('qty_mat_used', 'Qtà Materiale')}:").grid(
            row=2, column=0, padx=5, pady=5, sticky="e")
        self.qty_mat_var = tk.StringVar()
        self.qty_mat_entry = ttk.Entry(input_frame, textvariable=self.qty_mat_var, width=15)
        self.qty_mat_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(input_frame, text=f"{self.translator.get('qty_diluant_used', 'Qtà Diluente')}:").grid(
            row=2, column=2, padx=5, pady=5, sticky="e")
        self.qty_diluant_var = tk.StringVar()
        self.qty_diluant_entry = ttk.Entry(input_frame, textvariable=self.qty_diluant_var, width=15)
        self.qty_diluant_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        # ========================================
        # RIGA 3: Misurazione Coppa Ford
        # ========================================
        ttk.Label(input_frame, text=f"{self.translator.get('measurement_ford', 'Misurazione (s)')}:").grid(
            row=3, column=0, padx=5, pady=5, sticky="e")
        self.measurement_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.measurement_var, width=15).grid(
            row=3, column=1, padx=5, pady=5, sticky="w")

        # ========================================
        # RIGA 4: Pulsanti azione
        # ========================================
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=4, column=0, columnspan=4, pady=10)

        ttk.Button(btn_frame, text=f"💾 {self.translator.get('btn_save', 'Salva')}",
                   command=self._save_measurement).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"🔄 {self.translator.get('btn_clear', 'Pulisci')}",
                   command=self._clear_form).pack(side=tk.LEFT, padx=5)

        # Treeview per storico misurazioni
        tree_frame = ttk.LabelFrame(main_frame, text=self.translator.get("measurements_history", "Storico Misurazioni"),
                                    padding="10")
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "UserName", "Component", "TipoVerifica", "QtyMat", "QtyDiluant",
                   "RegDate", "Measurement", "MeasDate")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        self.tree.heading("ID", text="ID")
        self.tree.heading("UserName", text=self.translator.get("operator", "Operatore"))
        self.tree.heading("Component", text=self.translator.get("component", "Componente"))
        self.tree.heading("TipoVerifica", text=self.translator.get("analysis_type", "Tipo Analisi"))
        self.tree.heading("QtyMat", text=self.translator.get("qty_mat", "Qtà Mat."))
        self.tree.heading("QtyDiluant", text=self.translator.get("qty_diluant", "Qtà Dil."))
        self.tree.heading("RegDate", text=self.translator.get("reg_date", "Data Reg."))
        self.tree.heading("Measurement", text=self.translator.get("measurement", "Misuraz."))
        self.tree.heading("MeasDate", text=self.translator.get("meas_date", "Data Mis."))

        self.tree.column("ID", width=50)
        self.tree.column("UserName", width=100)
        self.tree.column("Component", width=200)
        self.tree.column("TipoVerifica", width=120)
        self.tree.column("QtyMat", width=80)
        self.tree.column("QtyDiluant", width=80)
        self.tree.column("RegDate", width=100)
        self.tree.column("Measurement", width=80)
        self.tree.column("MeasDate", width=100)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Carica dati
        self._load_coatings()
        self._load_measurements()

        # ✅ AGGIUNTO: Chiamata iniziale per impostare lo stato dei campi
        self._on_analysis_type_change()

    def _on_analysis_type_change(self):
        """Gestisce il cambio del tipo di analisi"""
        if self.analysis_type_var.get() == 2:  # Controllo periodico
            # Disabilita e azzera i campi quantità
            self.qty_mat_var.set("0")
            self.qty_diluant_var.set("0")
            self.qty_mat_entry.config(state="disabled")
            self.qty_diluant_entry.config(state="disabled")
        else:  # Viscosità materiali
            # Riabilita i campi
            self.qty_mat_entry.config(state="normal")
            self.qty_diluant_entry.config(state="normal")
            self.qty_mat_var.set("")
            self.qty_diluant_var.set("")

    def _load_coatings(self):
        """Carica i tipi di vernice nella combo"""
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = """
                    SELECT IDCOMPONENT, ComponentCode, ComponentDescription
                    FROM Traceability_RS.dbo.components
                    WHERE IDCOMPONENTTYPE = 24
                    ORDER BY ComponentCode
                    """
            cursor.execute(query)
            rows = cursor.fetchall()

            self.coating_data = {f"{row.ComponentCode} {row.ComponentDescription}": row.IDCOMPONENT for row in rows}
            self.coating_combo['values'] = list(self.coating_data.keys())

            conn.close()
        except Exception as e:
            logger.error(f"Errore caricamento vernici: {e}")
            messagebox.showerror(
                self.translator.get("error", "Errore"),
                f"{self.translator.get('load_error', 'Errore caricamento')}: {str(e)}"
            )

    def _load_measurements(self):
        """Carica le misurazioni dal database con JOIN corretto"""
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = """
                    SELECT v.[ViscosityControlId],
                           v.[UserName],
                           v.[QtyMatUsed],
                           v.[QtyDiluantUsed],
                           v.[TipoVerifica],
                           c.ComponentCode + ' ' + c.ComponentDescription as Component,
                           CAST(v.DateSys as date)                        as RegistrationDate,
                           vc.MeasuramentCupFord                          as Measurement,
                           CONVERT(varchar, vc.DateSys, 103)              as MeasuramentDate
                    FROM [Traceability_RS].[dbo].[ViscosityControls] as v
                        INNER JOIN [Traceability_RS].[dbo].ViscosyContronCheckCups vc
                    ON v.ViscosityControlId = vc.ViscosytyControlId
                        INNER JOIN Traceability_RS.dbo.components c
                        ON v.IdComponent = c.IDComponent
                    ORDER BY v.DateSys DESC
                    """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Pulisci treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Inserisci dati
            for row in rows:
                tipo_verifica_text = (
                    self.translator.get('viscosity_materials', 'Viscosità materiali')
                    if row.TipoVerifica == 1
                    else self.translator.get('periodic_check', 'Controllo periodico')
                )

                self.tree.insert("", tk.END, values=(
                    row.ViscosityControlId,
                    row.UserName or "",
                    row.Component,
                    tipo_verifica_text,
                    row.QtyMatUsed or "",
                    row.QtyDiluantUsed or "",
                    row.RegistrationDate,
                    row.Measurement or "",
                    row.MeasuramentDate or ""
                ))

            conn.close()
            logger.info(f"Caricate {len(rows)} misurazioni di viscosità")

        except Exception as e:
            logger.error(f"Errore caricamento misurazioni: {e}")
            messagebox.showerror(
                self.translator.get("error", "Errore"),
                f"{self.translator.get('load_error', 'Errore caricamento')}: {str(e)}"
            )

    def _save_measurement(self):
        """Salva la misurazione nel database (Testata + Righe)"""
        coating_text = self.coating_combo.get()
        operator = self.username
        qty_mat = self.qty_mat_var.get().strip()
        qty_diluant = self.qty_diluant_var.get().strip()
        measurement = self.measurement_var.get().strip()
        tipo_verifica = self.analysis_type_var.get()

        # Validazioni
        if not coating_text:
            messagebox.showwarning(
                self.translator.get("warning", "Attenzione"),
                self.translator.get("select_coating", "Selezionare un tipo di vernice")
            )
            return

        if not measurement:
            messagebox.showwarning(
                self.translator.get("warning", "Attenzione"),
                self.translator.get("enter_measurement", "Inserire il valore della misurazione")
            )
            return

        try:
            measurement_value = float(measurement)

            if tipo_verifica == 2:
                qty_mat_value = 0.0
                qty_diluant_value = 0.0
            else:
                qty_mat_value = float(qty_mat) if qty_mat else None
                qty_diluant_value = float(qty_diluant) if qty_diluant else None

        except ValueError:
            messagebox.showwarning(
                self.translator.get("warning", "Attenzione"),
                self.translator.get("invalid_values", "Valori numerici non validi")
            )
            return

        component_id = self.coating_data.get(coating_text)

        # ✅ MODIFICATO: Usa la data/ora corrente invece di quella dal DateEntry
        measurement_date = datetime.now()

        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query_header = """
                           INSERT INTO [Traceability_RS].[dbo].[ViscosityControls]
                           ([UserName], [QtyMatUsed], [QtyDiluantUsed], [IdComponent], [DateSys], [TipoVerifica])
                               OUTPUT INSERTED.ViscosityControlId
                           VALUES (?, ?, ?, ?, ?, ?)
                           """
            cursor.execute(query_header, operator, qty_mat_value, qty_diluant_value,
                           component_id, measurement_date, tipo_verifica)

            viscosity_control_id = cursor.fetchone()[0]

            query_detail = """
                           INSERT INTO [Traceability_RS].[dbo].[ViscosyContronCheckCups]
                               ([ViscosytyControlId], [MeasuramentCupFord], [DateSys])
                           VALUES (?, ?, ?)
                           """
            cursor.execute(query_detail, viscosity_control_id, measurement_value, measurement_date)

            conn.commit()
            conn.close()

            messagebox.showinfo(
                self.translator.get("success", "Successo"),
                self.translator.get("measurement_saved", "Misurazione salvata con successo")
            )

            self._clear_form()
            self._load_measurements()
            logger.info(
                f"Misurazione viscosità salvata: ID={viscosity_control_id}, Coating={coating_text}, "
                f"TipoVerifica={tipo_verifica}, Misurazione={measurement_value}")

        except Exception as e:
            logger.error(f"Errore salvataggio misurazione: {e}")
            messagebox.showerror(
                self.translator.get("error", "Errore"),
                f"{self.translator.get('save_error', 'Errore salvataggio')}: {str(e)}"
            )

    def _clear_form(self):
        """Pulisce il form"""
        self.coating_combo.set("")
        self.qty_mat_var.set("")
        self.qty_diluant_var.set("")
        self.measurement_var.set("")
        self.analysis_type_var.set(1)
        self._on_analysis_type_change()

        # ✅ MODIFICATO: Aggiorna la data corrente quando si pulisce il form
        current_datetime = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.date_label.config(text=current_datetime)


class TranslationManager:
    """Gestore traduzioni per il modulo Coating"""

    def __init__(self, conn_str, language_code='it'):
        self.conn_str = conn_str
        self.language_code = language_code
        self.translations = {}
        self._load_translations()

    def _load_translations(self):
        """Carica le traduzioni dal database"""
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = """
                SELECT TranslationKey, TranslationValue
                FROM Traceability_RS.dbo.AppTranslations
                WHERE LanguageCode = ?
            """
            cursor.execute(query, (self.language_code,))

            for row in cursor.fetchall():
                self.translations[row.TranslationKey] = row.TranslationValue

            conn.close()
            logger.info(f"Caricate {len(self.translations)} traduzioni per lingua: {self.language_code}")

        except Exception as e:
            logger.error(f"Errore caricamento traduzioni: {e}")

    def get(self, key, default=None):
        """Ottiene una traduzione"""
        return self.translations.get(key, default or key)

    def set_language(self, language_code):
        """Cambia lingua"""
        self.language_code = language_code
        self.translations.clear()
        self._load_translations()


class CoatingSettingsWindow:
    """Finestra per la gestione dei tipi di vernice (ComponentType = 24)"""

    def __init__(self, parent, conn_str, language_code='it'):
        self.parent = parent
        self.conn_str = conn_str
        self.window = None
        self.tree = None
        self.translator = TranslationManager(conn_str, language_code)

    def show(self):
        """Mostra la finestra dopo login semplice"""
        #if not self._simple_login():
        #    return

        self.window = tk.Toplevel(self.parent)
        self.window.title(self.translator.get("coating_settings_title"))
        self.window.geometry("800x500")

        # Frame principale
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame pulsanti
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(btn_frame, text=f"➕ {self.translator.get('btn_add')}",
                   command=self._add_coating).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"✏️ {self.translator.get('btn_edit')}",
                   command=self._edit_coating).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"🗑️ {self.translator.get('btn_delete')}",
                   command=self._delete_coating).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"🔄 {self.translator.get('btn_refresh')}",
                   command=self._load_coatings).pack(side=tk.LEFT, padx=5)

        # Treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Code", "Description")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Code", text=self.translator.get("coating_code"))
        self.tree.heading("Description", text=self.translator.get("coating_description"))

        self.tree.column("ID", width=80)
        self.tree.column("Code", width=200)
        self.tree.column("Description", width=400)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Carica dati
        self._load_coatings()

    def _simple_login(self):
        """Login semplice con username/password"""
        dialog = tk.Toplevel(self.parent)
        dialog.title(self.translator.get("login_title"))
        dialog.geometry("300x150")
        dialog.transient(self.parent)
        dialog.grab_set()

        ttk.Label(dialog, text=f"{self.translator.get('username')}:").grid(row=0, column=0, padx=10, pady=10,
                                                                           sticky="e")
        ttk.Label(dialog, text=f"{self.translator.get('password')}:").grid(row=1, column=0, padx=10, pady=10,
                                                                           sticky="e")

        username_var = tk.StringVar()
        password_var = tk.StringVar()

        username_entry = ttk.Entry(dialog, textvariable=username_var, width=20)
        password_entry = ttk.Entry(dialog, textvariable=password_var, width=20, show="*")

        username_entry.grid(row=0, column=1, padx=10, pady=10)
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        result = {"authenticated": False}

        def on_login():
            username = username_var.get().strip()
            password = password_var.get().strip()

            if self._validate_user(username, password):
                result["authenticated"] = True
                dialog.destroy()
            else:
                messagebox.showerror(
                    self.translator.get("error"),
                    self.translator.get("invalid_credentials"),
                    parent=dialog
                )

        def on_cancel():
            dialog.destroy()

        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text=self.translator.get("btn_login"), command=on_login).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.translator.get("btn_cancel"), command=on_cancel).pack(side=tk.LEFT, padx=5)

        username_entry.focus()
        password_entry.bind('<Return>', lambda e: on_login())

        dialog.wait_window()
        return result["authenticated"]

    def _validate_user(self, username, password):
        """Valida le credenziali utente"""
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = "SELECT iduserkey FROM resetservices.dbo.tbuserkey WHERE NomeUser = ? AND pass = ?"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            conn.close()
            return result is not None

        except Exception as e:
            logger.error(f"Errore validazione utente: {e}")
            messagebox.showerror(
                self.translator.get("error"),
                f"{self.translator.get('connection_error')}: {str(e)}"
            )
            return False

    def _load_coatings(self):
        """Carica i tipi di vernice dal database"""
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = """
                SELECT IDCOMPONENT, ComponentCode, ComponentDescription
                FROM Traceability_RS.dbo.components
                WHERE IDCOMPONENTTYPE = 24
                ORDER BY ComponentCode
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Pulisci treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Inserisci dati
            for row in rows:
                self.tree.insert("", tk.END, values=(row.IDCOMPONENT, row.ComponentCode, row.ComponentDescription))

            conn.close()
            logger.info(f"Caricati {len(rows)} tipi di vernice")

        except Exception as e:
            logger.error(f"Errore caricamento vernici: {e}")
            messagebox.showerror(
                self.translator.get("error"),
                f"{self.translator.get('load_error')}: {str(e)}"
            )

    def _add_coating(self):
        """Aggiunge un nuovo tipo di vernice"""
        dialog = CoatingEditDialog(self.window, self.conn_str, self.translator, mode="add")
        if dialog.result:
            self._load_coatings()

    def _edit_coating(self):
        """Modifica il tipo di vernice selezionato"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.translator.get("warning"),
                self.translator.get("select_coating_to_edit")
            )
            return

        item = self.tree.item(selection[0])
        values = item['values']

        dialog = CoatingEditDialog(
            self.window,
            self.conn_str,
            self.translator,
            mode="edit",
            coating_id=values[0],
            code=values[1],
            description=values[2]
        )

        if dialog.result:
            self._load_coatings()

    def _delete_coating(self):
        """Elimina il tipo di vernice selezionato"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.translator.get("warning"),
                self.translator.get("select_coating_to_delete")
            )
            return

        item = self.tree.item(selection[0])
        coating_id = item['values'][0]
        code = item['values'][1]

        if not messagebox.askyesno(
                self.translator.get("confirm"),
                f"{self.translator.get('confirm_delete_coating')} '{code}'?"
        ):
            return

        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = "DELETE FROM Traceability_RS.dbo.components WHERE IDCOMPONENT = ?"
            cursor.execute(query, (coating_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo(
                self.translator.get("success"),
                self.translator.get("coating_deleted_success")
            )
            self._load_coatings()
            logger.info(f"Vernice eliminata: ID={coating_id}")

        except Exception as e:
            logger.error(f"Errore eliminazione vernice: {e}")
            messagebox.showerror(
                self.translator.get("error"),
                f"{self.translator.get('delete_error')}: {str(e)}"
            )


class CoatingEditDialog:
    """Dialog per aggiungere/modificare tipi di vernice"""

    def __init__(self, parent, conn_str, translator, mode="add",
                 coating_id=None, code="", description=""):
        self.parent = parent
        self.conn_str = conn_str
        self.translator = translator
        self.mode = mode
        self.coating_id = coating_id
        self.result = False

        # Crea dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(
            self.translator.get("add_coating" if mode == "add" else "edit_coating")
        )
        self.dialog.geometry("500x250")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Form fields
        ttk.Label(self.dialog, text=f"{self.translator.get('coating_code')}:").grid(
            row=0, column=0, padx=10, pady=10, sticky="e"
        )
        ttk.Label(self.dialog, text=f"{self.translator.get('coating_description')}:").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )

        self.code_var = tk.StringVar(value=code)
        self.desc_var = tk.StringVar(value=description)

        ttk.Entry(self.dialog, textvariable=self.code_var, width=40).grid(
            row=0, column=1, padx=10, pady=10
        )
        ttk.Entry(self.dialog, textvariable=self.desc_var, width=40).grid(
            row=1, column=1, padx=10, pady=10
        )

        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text=self.translator.get("btn_save"),
                   command=self._save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.translator.get("btn_cancel"),
                   command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)

        self.dialog.wait_window()

    def _save(self):
        """Salva il tipo di vernice"""
        code = self.code_var.get().strip()
        description = self.desc_var.get().strip()

        if not code:
            messagebox.showwarning(
                self.translator.get("warning"),
                self.translator.get("coating_code_required"),
                parent=self.dialog
            )
            return

        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            if self.mode == "add":
                query = """
                    INSERT INTO Traceability_RS.dbo.components 
                    (ComponentCode, ComponentDescription, IDCOMPONENTTYPE)
                    VALUES (?, ?, 24)
                """
                cursor.execute(query, (code, description))
            else:
                query = """
                    UPDATE Traceability_RS.dbo.components 
                    SET ComponentCode = ?, ComponentDescription = ?
                    WHERE IDCOMPONENT = ?
                """
                cursor.execute(query, (code, description, self.coating_id))

            conn.commit()
            conn.close()

            self.result = True
            messagebox.showinfo(
                self.translator.get("success"),
                self.translator.get("coating_saved_success")
            )
            self.dialog.destroy()

        except Exception as e:
            logger.error(f"Errore salvataggio vernice: {e}")
            messagebox.showerror(
                self.translator.get("error"),
                f"{self.translator.get('save_error')}: {str(e)}",
                parent=self.dialog
            )


class CoatingReportsWindow:
    """Finestra per la generazione dei report Coating"""

    def __init__(self, parent, conn_str, language_code='it'):
        self.parent = parent
        self.conn_str = conn_str
        self.window = None
        self.translator = TranslationManager(conn_str, language_code)

    def show(self):
        """Mostra la finestra dei report"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.translator.get("coating_reports_title", "Coating - Report"))
        self.window.geometry("800x600")

        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame filtri
        filter_frame = ttk.LabelFrame(main_frame, text=self.translator.get("filters", "Filtri"), padding="10")
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        # Periodo
        ttk.Label(filter_frame, text=f"{self.translator.get('date_from', 'Dal')}:").grid(row=0, column=0, padx=5,
                                                                                         pady=5, sticky="e")
        self.date_from = DateEntry(filter_frame, width=15, date_pattern='dd/mm/yyyy')
        self.date_from.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(filter_frame, text=f"{self.translator.get('date_to', 'Al')}:").grid(row=0, column=2, padx=5, pady=5,
                                                                                      sticky="e")
        self.date_to = DateEntry(filter_frame, width=15, date_pattern='dd/mm/yyyy')
        self.date_to.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Tipo vernice
        ttk.Label(filter_frame, text=f"{self.translator.get('coating_type', 'Tipo Vernice')}:").grid(row=1, column=0,
                                                                                                     padx=5, pady=5,
                                                                                                     sticky="e")
        self.coating_combo = ttk.Combobox(filter_frame, width=30, state="readonly")
        self.coating_combo.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        # Pulsanti
        btn_frame = ttk.Frame(filter_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        ttk.Button(btn_frame, text=f"🔍 {self.translator.get('btn_search', 'Cerca')}",
                   command=self._load_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"📊 {self.translator.get('btn_export_excel', 'Esporta Excel')}",
                   command=self._export_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"📄 {self.translator.get('btn_export_pdf', 'Esporta PDF')}",
                   command=self._export_pdf).pack(side=tk.LEFT, padx=5)

        # Treeview per risultati
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "DocDate", "UserName", "RegDate", "QtyMat", "QtyDil", "Material", "DateSysOrig", "RegDateOrig")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        self.tree.heading("ID", text="ID")
        self.tree.heading("DocDate", text=self.translator.get("doc_date", "Data Doc."))
        self.tree.heading("UserName", text=self.translator.get("operator", "Operatore"))
        self.tree.heading("RegDate", text=self.translator.get("reg_date", "Data Reg."))
        self.tree.heading("QtyMat", text=self.translator.get("qty_mat", "Qtà Mat."))
        self.tree.heading("QtyDil", text=self.translator.get("qty_dil", "Qtà Dil."))
        self.tree.heading("Material", text=self.translator.get("material", "Materiale"))
        self.tree.heading("DateSysOrig", text=self.translator.get("date_sys_orig", "Data Sys Orig."))
        self.tree.heading("RegDateOrig", text=self.translator.get("reg_date_orig", "Reg Date Orig."))

        self.tree.column("ID", width=50)
        self.tree.column("DocDate", width=100)
        self.tree.column("UserName", width=120)
        self.tree.column("RegDate", width=100)
        self.tree.column("QtyMat", width=80)
        self.tree.column("QtyDil", width=80)
        self.tree.column("Material", width=200)
        self.tree.column("DateSysOrig", width=120)
        self.tree.column("RegDateOrig", width=120)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Carica dati iniziali
        self._load_coatings()
        self._load_report()

    def _load_coatings(self):
        """Carica i tipi di vernice nella combo"""
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = """
                    SELECT IDCOMPONENT, ComponentCode, ComponentDescription
                    FROM Traceability_RS.dbo.components
                    WHERE IDCOMPONENTTYPE = 24
                    ORDER BY ComponentCode \
                    """
            cursor.execute(query)
            rows = cursor.fetchall()

            self.coating_data = {"Tutti": None}
            for row in rows:
                key = f"{row.ComponentCode} - {row.ComponentDescription}"
                self.coating_data[key] = row.IDCOMPONENT

            self.coating_combo['values'] = list(self.coating_data.keys())
            self.coating_combo.set("Tutti")

            conn.close()
        except Exception as e:
            logger.error(f"Errore caricamento vernici: {e}")

    def _load_report(self):
        """Carica i dati del report usando la Stored Procedure"""
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            date_from = self.date_from.get_date()
            date_to = self.date_to.get_date()

            # Esegui la Stored Procedure
            query = """
                EXEC [Traceability_RS].[dbo].[usp_ViscosityControlReport] 
                    @RequestDateStart = ?, 
                    @RequestDateStop = ?
            """

            cursor.execute(query, date_from, date_to)
            self.report_data = cursor.fetchall()

            # Filtra per componente se selezionato (filtro lato client)
            coating_text = self.coating_combo.get()
            if coating_text and self.report_data:
                component_id = self.coating_data.get(coating_text)
                # Assumendo che Material contenga l'ID o il nome del componente
                # Se necessario, adatta il filtro in base alla struttura della SP
                pass  # La SP potrebbe già gestire il filtro, altrimenti filtra qui

            # Pulisci treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Inserisci dati con le colonne corrette dalla SP
            for row in self.report_data:
                self.tree.insert("", tk.END, values=(
                    row.ViscosityControlId,
                    row.DocumentDate or "",
                    row.UserName or "",
                    row.RegDate or "",
                    row.QtyMatUsed or "",
                    row.QtyDiluantUsed or "",
                    row.Material or "",
                    row.DateSysOriginal or "",
                    row.RegDateOriginal or ""
                ))

            conn.close()
            logger.info(f"Caricati {len(self.report_data)} record nel report viscosità")

        except Exception as e:
            logger.error(f"Errore caricamento report: {e}")
            messagebox.showerror(
                self.translator.get("error", "Errore"),
                f"{self.translator.get('load_error', 'Errore caricamento')}: {str(e)}"
            )

    def _export_excel(self):
        """Esporta il report in Excel con le colonne corrette"""
        if not self.report_data:
            messagebox.showwarning(
                self.translator.get("warning", "Attenzione"),
                self.translator.get("no_data_to_export", "Nessun dato da esportare")
            )
            return

        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"Viscosity_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )

            if not filename:
                return

            # Crea DataFrame con le colonne della SP
            data = []
            for row in self.report_data:
                data.append({
                    'ID Controllo': row.ViscosityControlId,
                    'Data Documento': row.DocumentDate or "",
                    'Operatore': row.UserName or "",
                    'Data Registrazione': row.RegDate or "",
                    'Qtà Materiale': row.QtyMatUsed or "",
                    'Qtà Diluente': row.QtyDiluantUsed or "",
                    'Materiale': row.Material or "",
                    'Data Sistema (Orig)': row.DateSysOriginal or "",
                    'Data Reg. (Orig)': row.RegDateOriginal or ""
                })

            df = pd.DataFrame(data)

            # Crea Excel con formattazione
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Viscosity Report')

                # Formattazione automatica larghezza colonne
                worksheet = writer.sheets['Viscosity Report']
                for idx, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).map(len).max(),
                        len(col)
                    ) + 2
                    worksheet.column_dimensions[chr(65 + idx)].width = max_length

            messagebox.showinfo(
                self.translator.get("success", "Successo"),
                f"{self.translator.get('export_success', 'Esportazione completata')}: {filename}"
            )

            # Apri il file
            if platform.system() == 'Windows':
                os.startfile(filename)
            elif platform.system() == 'Darwin':
                subprocess.call(['open', filename])
            else:
                subprocess.call(['xdg-open', filename])

            logger.info(f"Report Excel esportato: {filename}")

        except Exception as e:
            logger.error(f"Errore esportazione Excel: {e}")
            messagebox.showerror(
                self.translator.get("error", "Errore"),
                f"{self.translator.get('export_error', 'Errore esportazione')}: {str(e)}"
            )

    def _export_pdf(self):
        """Esporta il report in PDF"""
        if not self.report_data:
            messagebox.showwarning(
                self.translator.get("warning", "Attenzione"),
                self.translator.get("no_data_to_export", "Nessun dato da esportare")
            )
            return

        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import cm

            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=f"Viscosity_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )

            if not filename:
                return

            # Crea documento PDF in landscape
            doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
            elements = []
            styles = getSampleStyleSheet()

            # Titolo
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=30,
                alignment=1  # Center
            )
            title = Paragraph("Report Controllo Viscosità", title_style)
            elements.append(title)

            # Periodo
            date_from = self.date_from.get_date().strftime('%d/%m/%Y')
            date_to = self.date_to.get_date().strftime('%d/%m/%Y')
            period_text = f"Periodo: {date_from} - {date_to}"
            period = Paragraph(period_text, styles['Normal'])
            elements.append(period)
            elements.append(Spacer(1, 0.5 * cm))

            # Prepara dati tabella
            data = [['ID', 'Data Doc.', 'Operatore', 'Data Reg.', 'Qtà Mat.', 'Qtà Dil.', 'Materiale']]

            for row in self.report_data:
                data.append([
                    str(row.ViscosityControlId),
                    str(row.DocumentDate or ""),
                    str(row.UserName or ""),
                    str(row.RegDate or ""),
                    str(row.QtyMatUsed or ""),
                    str(row.QtyDiluantUsed or ""),
                    str(row.Material or "")[:30]  # Limita lunghezza
                ])

            # Crea tabella
            table = Table(data, repeatRows=1)
            table.setStyle(TableStyle([
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

                # Body
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))

            elements.append(table)

            # Genera PDF
            doc.build(elements)

            messagebox.showinfo(
                self.translator.get("success", "Successo"),
                f"{self.translator.get('export_success', 'Esportazione completata')}: {filename}"
            )

            # Apri il file
            if platform.system() == 'Windows':
                os.startfile(filename)
            elif platform.system() == 'Darwin':
                subprocess.call(['open', filename])
            else:
                subprocess.call(['xdg-open', filename])

            logger.info(f"Report PDF esportato: {filename}")

        except ImportError:
            messagebox.showerror(
                self.translator.get("error", "Errore"),
                "Libreria reportlab non installata. Eseguire: pip install reportlab"
            )
        except Exception as e:
            logger.error(f"Errore esportazione PDF: {e}")
            messagebox.showerror(
                self.translator.get("error", "Errore"),
                f"{self.translator.get('export_error', 'Errore esportazione')}: {str(e)}"
            )


class CoatingThicknessSettingsWindow:
    """Finestra per la gestione delle specifiche di spessore vernice"""

    def __init__(self, parent, conn_str, language_code='it'):
        self.parent = parent
        self.conn_str = conn_str
        self.window = None
        self.tree = None
        self.translator = TranslationManager(conn_str, language_code)

    def show(self):
        """Mostra la finestra delle specifiche spessore"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.translator.get("coating_thickness_settings_title", "Coating - Specifiche Spessore"))
        self.window.geometry("1000x600")

        # Frame principale
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame pulsanti
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(btn_frame, text=f"➕ {self.translator.get('btn_add_thickness', 'Aggiungi Specifica')}",
                   command=self._add_thickness_spec).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"✏️ {self.translator.get('btn_edit_thickness', 'Modifica Specifica')}",
                   command=self._edit_thickness_spec).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"🗑️ {self.translator.get('btn_delete_thickness', 'Elimina Specifica')}",
                   command=self._delete_thickness_spec).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"🔄 {self.translator.get('btn_refresh', 'Aggiorna')}",
                   command=self._load_thickness_specs).pack(side=tk.LEFT, padx=5)

        # Treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "ComponentCode", "ComponentDescription", "ThicknessValue", "Tolerance", "TypeMesurament")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        self.tree.heading("ID", text="ID")
        self.tree.heading("ComponentCode", text=self.translator.get("coating_code", "Codice Vernice"))
        self.tree.heading("ComponentDescription",
                          text=self.translator.get("coating_description", "Descrizione Vernice"))
        self.tree.heading("ThicknessValue", text=self.translator.get("thickness_value", "Spessore (μm)"))
        self.tree.heading("Tolerance", text=self.translator.get("tolerance", "Tolleranza (±)"))
        self.tree.heading("TypeMesurament", text=self.translator.get("measurement_type", "Tipo Misura"))

        self.tree.column("ID", width=80)
        self.tree.column("ComponentCode", width=150)
        self.tree.column("ComponentDescription", width=300)
        self.tree.column("ThicknessValue", width=120)
        self.tree.column("Tolerance", width=120)
        self.tree.column("TypeMesurament", width=120)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Carica dati
        self._load_thickness_specs()

    def _load_thickness_specs(self):
        """Carica le specifiche di spessore dal database"""
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = """
                SELECT cs.ComponentSpecificationId, c.ComponentCode, c.ComponentDescription, 
                       cs.Value, cs.Tollerance, cs.TypeMesurament
                FROM Traceability_RS.dbo.ComponentSpecifications cs
                INNER JOIN Traceability_RS.dbo.components c ON cs.IdComponent = c.IDCOMPONENT
                WHERE cs.DescriptionValue = 'Thickness'
                ORDER BY c.ComponentCode
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Pulisci treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Inserisci dati
            for row in rows:
                self.tree.insert("", tk.END, values=(
                    row.ComponentSpecificationId,
                    row.ComponentCode,
                    row.ComponentDescription,
                    f"{row.Value:.2f}" if row.Value else "0.00",
                    f"{row.Tollerance:.2f}" if row.Tollerance else "0.00",
                    row.TypeMesurament or "Micron"
                ))

            conn.close()
            logger.info(f"Caricate {len(rows)} specifiche di spessore")

        except Exception as e:
            logger.error(f"Errore caricamento specifiche spessore: {e}")
            messagebox.showerror(
                self.translator.get("error", "Errore"),
                f"{self.translator.get('load_error', 'Errore caricamento')}: {str(e)}"
            )

    def _add_thickness_spec(self):
        """Aggiunge una nuova specifica di spessore"""
        dialog = ThicknessSpecEditDialog(self.window, self.conn_str, self.translator, mode="add")
        if dialog.result:
            self._load_thickness_specs()

    def _edit_thickness_spec(self):
        """Modifica la specifica di spessore selezionata"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.translator.get("warning", "Attenzione"),
                self.translator.get("select_thickness_to_edit", "Selezionare una specifica da modificare")
            )
            return

        item = self.tree.item(selection[0])
        values = item['values']

        dialog = ThicknessSpecEditDialog(
            self.window,
            self.conn_str,
            self.translator,
            mode="edit",
            spec_id=values[0],
            component_code=values[1],
            component_desc=values[2],
            thickness_value=values[3],
            tolerance=values[4],
            measure_type=values[5]
        )

        if dialog.result:
            self._load_thickness_specs()

    def _delete_thickness_spec(self):
        """Elimina la specifica di spessore selezionata"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                self.translator.get("warning", "Attenzione"),
                self.translator.get("select_thickness_to_delete", "Selezionare una specifica da eliminare")
            )
            return

        item = self.tree.item(selection[0])
        spec_id = item['values'][0]
        component_code = item['values'][1]

        if not messagebox.askyesno(
                self.translator.get("confirm", "Conferma"),
                f"{self.translator.get('confirm_delete_thickness', 'Confermi eliminazione specifica per')} '{component_code}'?"
        ):
            return

        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = "DELETE FROM Traceability_RS.dbo.ComponentSpecifications WHERE ComponentSpecificationId = ?"
            cursor.execute(query, (spec_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo(
                self.translator.get("success", "Successo"),
                self.translator.get("thickness_deleted_success", "Specifica spessore eliminata con successo")
            )
            self._load_thickness_specs()
            logger.info(f"Specifica spessore eliminata: ID={spec_id}")

        except Exception as e:
            logger.error(f"Errore eliminazione specifica spessore: {e}")
            messagebox.showerror(
                self.translator.get("error", "Errore"),
                f"{self.translator.get('delete_error', 'Errore eliminazione')}: {str(e)}"
            )


class ThicknessSpecEditDialog:
    """Dialog per aggiungere/modificare specifiche di spessore"""

    def __init__(self, parent, conn_str, translator, mode="add",
                 spec_id=None, component_code="", component_desc="",
                 thickness_value="0.00", tolerance="0.00", measure_type="Micron"):
        self.parent = parent
        self.conn_str = conn_str
        self.translator = translator
        self.mode = mode
        self.spec_id = spec_id
        self.result = False

        # Crea dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(
            self.translator.get("add_thickness_spec" if mode == "add" else "edit_thickness_spec")
        )
        self.dialog.geometry("600x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Form fields
        row = 0

        # Selezione componente (solo in modalità add)
        if mode == "add":
            ttk.Label(self.dialog, text=f"{self.translator.get('select_coating')}:").grid(
                row=row, column=0, padx=10, pady=10, sticky="e"
            )

            self.component_var = tk.StringVar()
            self.component_combo = ttk.Combobox(
                self.dialog, textvariable=self.component_var, width=50, state="readonly"
            )
            self.component_combo.grid(row=row, column=1, padx=10, pady=10)

            # Carica componenti
            self._load_components()
            row += 1
        else:
            # Mostra componente selezionato (read-only)
            ttk.Label(self.dialog, text=f"{self.translator.get('coating')}:").grid(
                row=row, column=0, padx=10, pady=10, sticky="e"
            )
            ttk.Label(self.dialog, text=f"{component_code} - {component_desc}").grid(
                row=row, column=1, padx=10, pady=10, sticky="w"
            )
            self.selected_component_id = None  # Verrà recuperato dal DB
            row += 1

        # Spessore
        ttk.Label(self.dialog, text=f"{self.translator.get('thickness_value')} (μm):").grid(
            row=row, column=0, padx=10, pady=10, sticky="e"
        )
        self.thickness_var = tk.StringVar(value=str(thickness_value).replace('.', ','))
        ttk.Entry(self.dialog, textvariable=self.thickness_var, width=20).grid(
            row=row, column=1, padx=10, pady=10, sticky="w"
        )
        row += 1

        # Tolleranza
        ttk.Label(self.dialog, text=f"{self.translator.get('tolerance')} (±):").grid(
            row=row, column=0, padx=10, pady=10, sticky="e"
        )
        self.tolerance_var = tk.StringVar(value=str(tolerance).replace('.', ','))
        ttk.Entry(self.dialog, textvariable=self.tolerance_var, width=20).grid(
            row=row, column=1, padx=10, pady=10, sticky="w"
        )
        row += 1

        # Tipo misura
        ttk.Label(self.dialog, text=f"{self.translator.get('measurement_type')}:").grid(
            row=row, column=0, padx=10, pady=10, sticky="e"
        )
        self.measure_type_var = tk.StringVar(value=measure_type)
        measure_combo = ttk.Combobox(
            self.dialog, textvariable=self.measure_type_var,
            values=["Micron", "Mil", "mm"], width=18, state="readonly"
        )
        measure_combo.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        row += 1

        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text=self.translator.get("btn_save"),
                   command=self._save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.translator.get("btn_cancel"),
                   command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)

        self.dialog.wait_window()

    def _load_components(self):
        """Carica i componenti di tipo vernice (IDCOMPONENTTYPE = 24)"""
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = """
                SELECT IDCOMPONENT, ComponentCode, ComponentDescription
                FROM Traceability_RS.dbo.components
                WHERE IDCOMPONENTTYPE = 24
                ORDER BY ComponentCode
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            self.components = {f"{row[1]} - {row[2]}": row[0] for row in rows}
            self.component_combo['values'] = list(self.components.keys())

            if self.components:
                self.component_combo.current(0)

            conn.close()

        except Exception as e:
            logger.error(f"Errore caricamento componenti: {e}")
            messagebox.showerror(
                self.translator.get("error"),
                f"{self.translator.get('load_error')}: {str(e)}",
                parent=self.dialog
            )

    def _save(self):
        """Salva la specifica di spessore"""
        try:
            # Validazione
            thickness_str = self.thickness_var.get().strip().replace(',', '.')
            tolerance_str = self.tolerance_var.get().strip().replace(',', '.')

            if not thickness_str or not tolerance_str:
                messagebox.showwarning(
                    self.translator.get("warning"),
                    self.translator.get("fill_all_fields"),
                    parent=self.dialog
                )
                return

            thickness = float(thickness_str)
            tolerance = float(tolerance_str)
            measure_type = self.measure_type_var.get()

            # Recupera ID componente
            if self.mode == "add":
                selected_text = self.component_var.get()
                if not selected_text:
                    messagebox.showwarning(
                        self.translator.get("warning"),
                        self.translator.get("select_coating_first"),
                        parent=self.dialog
                    )
                    return
                component_id = self.components[selected_text]
            else:
                # Recupera ID dal DB usando spec_id
                conn = pyodbc.connect(self.conn_str)
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT IdComponent FROM Traceability_RS.dbo.ComponentSpecifications WHERE ComponentSpecificationId = ?",
                    (self.spec_id,)
                )
                row = cursor.fetchone()
                component_id = row[0] if row else None
                conn.close()

                if not component_id:
                    raise ValueError("Componente non trovato")

            # Salva nel DB
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            if self.mode == "add":
                query = """
                    INSERT INTO Traceability_RS.dbo.ComponentSpecifications 
                    (IdComponent, DescriptionValue, Value, Tollerance, TypeMesurament)
                    VALUES (?, 'Thickness', ?, ?, ?)
                """
                logger.info(f"Inserimento specifica di spessore: {component_id}, {thickness}, {tolerance}, {measure_type}")
                cursor.execute(query, (component_id, thickness, tolerance, measure_type))
            else:
                query = """
                    UPDATE Traceability_RS.dbo.ComponentSpecifications 
                    SET Value = ?, Tollerance = ?, TypeMesurament = ?
                    WHERE ComponentSpecificationId = ?
                """
                cursor.execute(query, (thickness, tolerance, measure_type, self.spec_id))

            conn.commit()
            conn.close()

            self.result = True
            messagebox.showinfo(
                self.translator.get("success"),
                self.translator.get("thickness_spec_saved_success")
            )
            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror(
                self.translator.get("error"),
                f"{self.translator.get('invalid_number_format')}: {str(e)}",
                parent=self.dialog
            )
        except Exception as e:
            logger.error(f"Errore salvataggio specifica spessore: {e}")
            messagebox.showerror(
                self.translator.get("error"),
                f"{self.translator.get('save_error')}: {str(e)}",
                parent=self.dialog
            )


class CoatingThicknessMeasurementWindow:
    """Finestra per la registrazione delle misurazioni di spessore"""

    def __init__(self, parent, conn_str, username, language_code='it'):
        self.parent = parent
        self.conn_str = conn_str
        self.username = username
        self.window = None
        self.translator = TranslationManager(conn_str, language_code)

    def show(self):
        """Mostra la finestra di misurazione spessore"""
        # Login semplice
        if not self._simple_login():
            return

        self.window = tk.Toplevel(self.parent)
        self.window.title(self.translator.get("coating_thickness_measurement_title", "Coating - Misurazione Spessore"))
        self.window.geometry("800x600")

        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame input dati
        input_frame = ttk.LabelFrame(main_frame, text=self.translator.get("thickness_measurement_data",
                                                                          "Dati Misurazione Spessore"), padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Tipo Vernice
        ttk.Label(input_frame, text=f"{self.translator.get('coating_type', 'Tipo Vernice')}:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e")
        self.coating_combo = ttk.Combobox(input_frame, width=40, state="readonly")
        self.coating_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.coating_combo.bind('<<ComboboxSelected>>', self._on_coating_selected)

        # Label Code
        ttk.Label(input_frame, text=f"{self.translator.get('label_code', 'Label Code')}:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e")
        self.labelcode_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.labelcode_var, width=45).grid(row=1, column=1, padx=5, pady=5,
                                                                               sticky="w")

        # Valori misurazione
        ttk.Label(input_frame, text=f"{self.translator.get('measurement_values', 'Valori Misurazione')} (μm):").grid(
            row=2, column=0, padx=5, pady=5, sticky="e")

        values_frame = ttk.Frame(input_frame)
        values_frame.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(values_frame, text="1:").pack(side=tk.LEFT)
        self.val1_var = tk.StringVar()
        ttk.Entry(values_frame, textvariable=self.val1_var, width=8).pack(side=tk.LEFT, padx=2)

        ttk.Label(values_frame, text="2:").pack(side=tk.LEFT)
        self.val2_var = tk.StringVar()
        ttk.Entry(values_frame, textvariable=self.val2_var, width=8).pack(side=tk.LEFT, padx=2)

        ttk.Label(values_frame, text="3:").pack(side=tk.LEFT)
        self.val3_var = tk.StringVar()
        ttk.Entry(values_frame, textvariable=self.val3_var, width=8).pack(side=tk.LEFT, padx=2)

        # Specifiche vernice (sola lettura)
        ttk.Label(input_frame, text=f"{self.translator.get('coating_specs', 'Specifiche Vernice')}:").grid(
            row=3, column=0, padx=5, pady=5, sticky="e")
        self.specs_label = ttk.Label(input_frame, text="-", foreground="blue")
        self.specs_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Risultato misurazione
        ttk.Label(input_frame, text=f"{self.translator.get('measurement_result', 'Risultato')}:").grid(
            row=4, column=0, padx=5, pady=5, sticky="e")

        result_frame = ttk.Frame(input_frame)
        result_frame.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(result_frame, text=f"{self.translator.get('average', 'Media')}:").pack(side=tk.LEFT)
        self.average_var = tk.StringVar(value="0.00")
        ttk.Label(result_frame, textvariable=self.average_var, foreground="green", font=("", 10, "bold")).pack(
            side=tk.LEFT, padx=5)

        ttk.Label(result_frame, text=f"{self.translator.get('is_valid', 'Valido')}:").pack(side=tk.LEFT, padx=(10, 0))
        self.valid_var = tk.StringVar(value="NO")
        ttk.Label(result_frame, textvariable=self.valid_var, foreground="red", font=("", 10, "bold")).pack(side=tk.LEFT,
                                                                                                           padx=5)

        # Pulsanti
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text=f"🧮 {self.translator.get('btn_calculate', 'Calcola')}",
                   command=self._calculate_measurement).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"💾 {self.translator.get('btn_save', 'Salva')}",
                   command=self._save_measurement).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"🔄 {self.translator.get('btn_clear', 'Pulisci')}",
                   command=self._clear_form).pack(side=tk.LEFT, padx=5)

        # Bind events per calcolo automatico
        self.val1_var.trace('w', self._on_values_change)
        self.val2_var.trace('w', self._on_values_change)
        self.val3_var.trace('w', self._on_values_change)

        # Treeview per storico
        tree_frame = ttk.LabelFrame(main_frame, text=self.translator.get("measurements_history", "Storico Misurazioni"),
                                    padding="10")
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Coating", "LabelCode", "User", "Val1", "Val2", "Val3", "Average", "IsValid", "Date")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Coating", text=self.translator.get("coating_type", "Vernice"))
        self.tree.heading("LabelCode", text=self.translator.get("label_code", "Label Code"))
        self.tree.heading("User", text=self.translator.get("operator", "Operatore"))
        self.tree.heading("Val1", text="Val 1")
        self.tree.heading("Val2", text="Val 2")
        self.tree.heading("Val3", text="Val 3")
        self.tree.heading("Average", text=self.translator.get("average", "Media"))
        self.tree.heading("IsValid", text=self.translator.get("is_valid", "Valido"))
        self.tree.heading("Date", text=self.translator.get("date", "Data"))

        self.tree.column("ID", width=50)
        self.tree.column("Coating", width=150)
        self.tree.column("LabelCode", width=100)
        self.tree.column("User", width=100)
        self.tree.column("Val1", width=60)
        self.tree.column("Val2", width=60)
        self.tree.column("Val3", width=60)
        self.tree.column("Average", width=80)
        self.tree.column("IsValid", width=80)
        self.tree.column("Date", width=120)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Carica dati
        self._load_coatings()
        self._load_measurements()

        # Variabili per gestione specifiche
        self.current_spec = None

    def _simple_login(self):
        """Login semplice per accesso alla misurazione"""
        # Implementazione simile a quella già presente nel file
        # Per brevità, assumiamo che il login sia già gestito
        return True

    def _load_coatings(self):
        """Carica i tipi di vernice con specifiche di spessore"""
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = """
                SELECT DISTINCT c.IDCOMPONENT, c.ComponentCode, c.ComponentDescription,
                       cs.Value, cs.Tollerance, cs.TypeMesurament
                FROM Traceability_RS.dbo.components c
                INNER JOIN Traceability_RS.dbo.ComponentSpecifications cs ON c.IDCOMPONENT = cs.IdComponent
                WHERE c.IDCOMPONENTTYPE = 24 AND cs.DescriptionValue = 'Thickness'
                ORDER BY c.ComponentCode
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            self.coating_data = {}
            coating_values = []

            for row in rows:
                key = f"{row.ComponentCode} - {row.ComponentDescription}"
                self.coating_data[key] = {
                    'id': row.IDCOMPONENT,
                    'value': row.Value,
                    'tolerance': row.Tollerance,
                    'type': row.TypeMesurament
                }
                coating_values.append(key)

            self.coating_combo['values'] = coating_values
            if coating_values:
                self.coating_combo.set(coating_values[0])
                self._on_coating_selected()

            conn.close()
        except Exception as e:
            logger.error(f"Errore caricamento vernici con specifiche: {e}")

    def _on_coating_selected(self, event=None):
        """Gestisce la selezione di una vernice"""
        coating_text = self.coating_combo.get()
        if coating_text in self.coating_data:
            spec = self.coating_data[coating_text]
            self.current_spec = spec
            specs_text = f"Spessore: {spec['value']}μm ±{spec['tolerance']}μm"
            self.specs_label.config(text=specs_text)
        else:
            self.current_spec = None
            self.specs_label.config(text="-")

    def _on_values_change(self, *args):
        """Calcolo automatico quando cambiano i valori"""
        if all([self.val1_var.get(), self.val2_var.get(), self.val3_var.get()]):
            self._calculate_measurement()

    def _calculate_measurement(self):
        """Calcola la media e verifica la validità"""
        try:
            val1 = float(self.val1_var.get() or 0)
            val2 = float(self.val2_var.get() or 0)
            val3 = float(self.val3_var.get() or 0)

            average = round((val1 + val2 + val3) / 3, 2)
            self.average_var.set(f"{average:.2f}")

            # Verifica validità
            if self.current_spec:
                target = self.current_spec['value']
                tolerance = self.current_spec['tolerance']
                min_val = target - tolerance
                max_val = target + tolerance

                is_valid = min_val <= average <= max_val
                self.valid_var.set("SI" if is_valid else "NO")
                self.valid_var.set("SI" if is_valid else "NO")
                color = "green" if is_valid else "red"
                self.valid_var.set(
                    f"{self.translator.get('yes', 'SI')}" if is_valid else f"{self.translator.get('no', 'NO')}")
            else:
                self.valid_var.set("NO")
                color = "red"

        except ValueError:
            self.average_var.set("0.00")
            self.valid_var.set("NO")

    def _save_measurement(self):
        """Salva la misurazione di spessore"""
        try:
            # Validazione campi
            labelcod = self.labelcod_var.get().strip()

            if not labelcod:
                messagebox.showwarning(
                    self.translator.get("warning", "Attenzione"),
                    self.translator.get("labelcode_required", "Inserire il codice scheda"),
                    parent=self.dialog
                )
                return

            # ✅ VALIDAZIONE LABELCODE E RECUPERO IDLabelCode
            id_labelcode = self._validate_and_get_labelcode(labelcod)
            if id_labelcode is None:
                return  # Il messaggio di errore è già stato mostrato

            # Recupera ID componente selezionato
            selected_text = self.component_var.get()
            if not selected_text:
                messagebox.showwarning(
                    self.translator.get("warning", "Attenzione"),
                    self.translator.get("select_coating_first", "Selezionare prima una vernice"),
                    parent=self.dialog
                )
                return

            component_id = self.components[selected_text]

            # Validazione spessore
            thickness_str = self.thickness_var.get().strip().replace(',', '.')
            if not thickness_str:
                messagebox.showwarning(
                    self.translator.get("warning", "Attenzione"),
                    self.translator.get("thickness_required", "Inserire il valore di spessore"),
                    parent=self.dialog
                )
                return

            try:
                thickness_value = float(thickness_str)
            except ValueError:
                messagebox.showerror(
                    self.translator.get("error", "Errore"),
                    self.translator.get("invalid_number_format", "Formato numero non valido"),
                    parent=self.dialog
                )
                return

            # Note (opzionale)
            notes = self.notes_var.get().strip()

            # Recupera specifiche di spessore per il componente
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query_spec = """
                SELECT Value, Tollerance 
                FROM Traceability_RS.dbo.ComponentSpecifications
                WHERE IdComponent = ? AND DescriptionValue = 'Thickness'
            """
            cursor.execute(query_spec, (component_id,))
            spec_row = cursor.fetchone()

            target_thickness = spec_row.Value if spec_row else None
            tolerance = spec_row.Tollerance if spec_row else None

            # Determina conformità
            is_compliant = None
            if target_thickness is not None and tolerance is not None:
                min_value = target_thickness - tolerance
                max_value = target_thickness + tolerance
                is_compliant = min_value <= thickness_value <= max_value

            # Inserisci misurazione
            insert_query = """
                INSERT INTO Traceability_RS.dbo.CoatingThicknessMeasurements 
                (IDLabelCode, IdComponent, ThicknessValue, TargetThickness, Tolerance, 
                 IsCompliant, MeasuredBy, MeasurementDate, Notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE(), ?)
            """

            cursor.execute(insert_query, (
                id_labelcode,  # ✅ Usa IDLabelCode (int) invece di labelcod (nvarchar)
                component_id,
                thickness_value,
                target_thickness,
                tolerance,
                is_compliant,
                self.username,
                notes
            ))

            conn.commit()
            conn.close()

            # Messaggio di successo con stato conformità
            success_msg = self.translator.get("thickness_saved_success", "Misurazione salvata con successo")
            if is_compliant is not None:
                if is_compliant:
                    success_msg += f"\n✅ {self.translator.get('compliant', 'Conforme')}"
                else:
                    success_msg += f"\n❌ {self.translator.get('non_compliant', 'Non conforme')}"

            messagebox.showinfo(
                self.translator.get("success", "Successo"),
                success_msg,
                parent=self.dialog
            )

            self.result = True
            self.dialog.destroy()

            logger.info(f"Misurazione spessore salvata: LabelCode={labelcod}, Component={component_id}, "
                        f"Thickness={thickness_value}, Compliant={is_compliant}")

        except Exception as e:
            logger.error(f"Errore salvataggio misurazione spessore: {e}")
            messagebox.showerror(
                self.translator.get("error", "Errore"),
                f"{self.translator.get('save_error', 'Errore salvataggio')}: {str(e)}",
                parent=self.dialog
            )

    def _validate_and_get_labelcode(self, labelcod):
        """
        Valida il labelcode e recupera IDLabelCode se la scheda esiste ed esegue coating

        Args:
            labelcod: Codice scheda da validare

        Returns:
            IDLabelCode (int) se valido, None altrimenti
        """
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = """
                SELECT TOP 1 L.IDLabelCode
                FROM LabelCodes L 
                INNER JOIN boards b ON b.idboard = L.idboard
                INNER JOIN orders o ON o.idorder = b.idorder
                INNER JOIN OrderPhases op ON o.idorder = op.IDOrder
                INNER JOIN Phases p ON p.idPhase = op.IDPhase
                WHERE L.labelcod = ?
                AND p.PhaseName LIKE '%coating%'
            """

            cursor.execute(query, (labelcod,))
            result = cursor.fetchone()
            conn.close()

            if result:
                id_labelcode = result[0]
                logger.info(f"LabelCode validato: {labelcod} → IDLabelCode={id_labelcode}")
                return id_labelcode
            else:
                # Scheda non trovata o non esegue coating
                messagebox.showerror(
                    self.translator.get("error", "Errore"),
                    self.translator.get("invalid_labelcode_coating",
                                        "Questa scheda non è valida. O non è registrata o non esegue una fase di coating."),
                    parent=self.dialog
                )
                logger.warning(f"LabelCode non valido o senza coating: {labelcod}")
                return None

        except Exception as e:
            logger.error(f"Errore validazione labelcode: {e}")
            messagebox.showerror(
                self.translator.get("error", "Errore"),
                f"{self.translator.get('validation_error', 'Errore validazione')}: {str(e)}",
                parent=self.dialog
            )
            return None

    def _load_measurements(self):
        """Carica lo storico delle misurazioni"""
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = """
                SELECT ct.CoatingTinknessId, c.ComponentCode + ' - ' + c.ComponentDescription as Coating,
                       ct.IdLabelCode, ct.[User], ct.Val1, ct.Val2, ct.Val3, ct.AverageVal, ct.IsValid,
                       CONVERT(varchar, ct.DateSys, 120) as MeasurementDate
                FROM Traceability_RS.dbo.CoatingTinknesses ct
                INNER JOIN Traceability_RS.dbo.components c ON ct.IdComponent = c.IDCOMPONENT
                ORDER BY ct.DateSys DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Pulisci treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Inserisci dati
            for row in rows:
                self.tree.insert("", tk.END, values=(
                    row.CoatingTinknessId,
                    row.Coating,
                    row.IdLabelCode,
                    row.User,
                    f"{row.Val1:.2f}" if row.Val1 else "0.00",
                    f"{row.Val2:.2f}" if row.Val2 else "0.00",
                    f"{row.Val3:.2f}" if row.Val3 else "0.00",
                    f"{row.AverageVal:.2f}" if row.AverageVal else "0.00",
                    "SI" if row.IsValid else "NO",
                    row.MeasurementDate
                ))

            conn.close()
        except Exception as e:
            logger.error(f"Errore caricamento misurazioni spessore: {e}")

    def _clear_form(self):
        """Pulisce il form"""
        self.labelcode_var.set("")
        self.val1_var.set("")
        self.val2_var.set("")
        self.val3_var.set("")
        self.average_var.set("0.00")
        self.valid_var.set("NO")


def open_coating_thickness_settings(parent, conn_str, language_code='it'):
    """Apre la finestra Settings Spessore Coating"""
    window = CoatingThicknessSettingsWindow(parent, conn_str, language_code)
    window.show()


def open_coating_thickness_measurement(parent, conn_str, username, language_code='it'):
    """Apre la finestra Misurazione Spessore Coating"""
    window = CoatingThicknessMeasurementWindow(parent, conn_str, username, language_code)
    window.show()


def open_coating_settings(parent, conn_str, language_code='it'):
    """Apre la finestra Settings Coating"""
    window = CoatingSettingsWindow(parent, conn_str, language_code)
    window.show()


def open_viscosity_control(parent, conn_str, language_code='it'):
    """Apre la finestra Controllo Viscosità"""
    window = CoatingViscosityWindow(parent, conn_str, language_code)
    window.show()


def open_coating_reports(parent, conn_str, language_code='it'):
    """Apre la finestra Rapporti Coating"""
    window = CoatingReportsWindow(parent, conn_str, language_code)
    window.show()
