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

    def __init__(self, parent, conn_str, language_code='it'):
        self.parent = parent
        self.conn_str = conn_str
        self.window = None
        self.translator = TranslationManager(conn_str, language_code)

    def show(self):
        """Mostra la finestra di registrazione viscosità"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.translator.get("coating_viscosity_title", "Coating - Registrazione Viscosità"))
        self.window.geometry("1200x600")

        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame superiore per input
        input_frame = ttk.LabelFrame(main_frame, text=self.translator.get("viscosity_data", "Dati Misurazione"),
                                     padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Data misurazione
        ttk.Label(input_frame, text=f"{self.translator.get('date', 'Data')}:").grid(row=0, column=0, padx=5, pady=5,
                                                                                    sticky="e")
        self.date_entry = DateEntry(input_frame, width=15, date_pattern='dd/mm/yyyy')
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Tipo vernice (Componente)
        ttk.Label(input_frame, text=f"{self.translator.get('coating_type', 'Tipo Vernice')}:").grid(row=0, column=2,
                                                                                                    padx=5, pady=5,
                                                                                                    sticky="e")
        self.coating_combo = ttk.Combobox(input_frame, width=30, state="readonly")
        self.coating_combo.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Operatore (UserName)
        ttk.Label(input_frame, text=f"{self.translator.get('operator', 'Operatore')}:").grid(row=1, column=0, padx=5,
                                                                                             pady=5, sticky="e")
        self.operator_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.operator_var, width=15).grid(row=1, column=1, padx=5, pady=5,
                                                                              sticky="w")

        # Qtà Materiale Usato
        ttk.Label(input_frame, text=f"{self.translator.get('qty_mat_used', 'Qtà Materiale')}:").grid(row=1, column=2,
                                                                                                     padx=5, pady=5,
                                                                                                     sticky="e")
        self.qty_mat_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.qty_mat_var, width=15).grid(row=1, column=3, padx=5, pady=5,
                                                                             sticky="w")

        # Qtà Diluente Usato
        ttk.Label(input_frame, text=f"{self.translator.get('qty_diluant_used', 'Qtà Diluente')}:").grid(row=2, column=0,
                                                                                                        padx=5, pady=5,
                                                                                                        sticky="e")
        self.qty_diluant_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.qty_diluant_var, width=15).grid(row=2, column=1, padx=5, pady=5,
                                                                                 sticky="w")

        # Misurazione Coppa Ford
        ttk.Label(input_frame, text=f"{self.translator.get('measurement_ford', 'Misurazione (s)')}:").grid(row=2,
                                                                                                           column=2,
                                                                                                           padx=5,
                                                                                                           pady=5,
                                                                                                           sticky="e")
        self.measurement_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.measurement_var, width=15).grid(row=2, column=3, padx=5, pady=5,
                                                                                 sticky="w")

        # Pulsanti azione
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(btn_frame, text=f"💾 {self.translator.get('btn_save', 'Salva')}",
                   command=self._save_measurement).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=f"🔄 {self.translator.get('btn_clear', 'Pulisci')}",
                   command=self._clear_form).pack(side=tk.LEFT, padx=5)

        # Treeview per storico misurazioni
        tree_frame = ttk.LabelFrame(main_frame, text=self.translator.get("measurements_history", "Storico Misurazioni"),
                                    padding="10")
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "UserName", "Component", "QtyMat", "QtyDiluant", "RegDate", "Measurement", "MeasDate")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        self.tree.heading("ID", text="ID")
        self.tree.heading("UserName", text=self.translator.get("operator", "Operatore"))
        self.tree.heading("Component", text=self.translator.get("component", "Componente"))
        self.tree.heading("QtyMat", text=self.translator.get("qty_mat", "Qtà Mat."))
        self.tree.heading("QtyDiluant", text=self.translator.get("qty_diluant", "Qtà Dil."))
        self.tree.heading("RegDate", text=self.translator.get("reg_date", "Data Reg."))
        self.tree.heading("Measurement", text=self.translator.get("measurement", "Misuraz."))
        self.tree.heading("MeasDate", text=self.translator.get("meas_date", "Data Mis."))

        self.tree.column("ID", width=50)
        self.tree.column("UserName", width=100)
        self.tree.column("Component", width=250)
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
                    SELECT v.[ViscosityControlId], \
                           v.[UserName], \
                           v.[QtyMatUsed], \
                           v.[QtyDiluantUsed], \
                           c.ComponentCode + ' ' + c.ComponentDescription as Component, \
                           CAST(v.DateSys as date)                        as RegistrationDate, \
                           vc.MeasuramentCupFord                          as Measurement, \
                           CONVERT(varchar, vc.DateSys, 103)              as MeasuramentDate
                    FROM [Traceability_RS].[dbo].[ViscosityControls] as v
                        INNER JOIN [Traceability_RS].[dbo].ViscosyContronCheckCups vc
                    ON v.ViscosityControlId = vc.ViscosytyControlId
                        INNER JOIN Traceability_RS.dbo.components c
                        ON v.IdComponent = c.IDComponent
                    ORDER BY v.DateSys DESC \
                    """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Pulisci treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Inserisci dati
            for row in rows:
                self.tree.insert("", tk.END, values=(
                    row.ViscosityControlId,
                    row.UserName or "",
                    row.Component,
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
        operator = self.operator_var.get().strip()
        qty_mat = self.qty_mat_var.get().strip()
        qty_diluant = self.qty_diluant_var.get().strip()
        measurement = self.measurement_var.get().strip()

        # Validazioni
        if not coating_text:
            messagebox.showwarning(
                self.translator.get("warning", "Attenzione"),
                self.translator.get("select_coating", "Selezionare un tipo di vernice")
            )
            return

        if not operator:
            messagebox.showwarning(
                self.translator.get("warning", "Attenzione"),
                self.translator.get("enter_operator", "Inserire il nome dell'operatore")
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
            qty_mat_value = float(qty_mat) if qty_mat else None
            qty_diluant_value = float(qty_diluant) if qty_diluant else None
        except ValueError:
            messagebox.showwarning(
                self.translator.get("warning", "Attenzione"),
                self.translator.get("invalid_values", "Valori numerici non validi")
            )
            return

        component_id = self.coating_data.get(coating_text)
        measurement_date = self.date_entry.get_date()

        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            # 1. Inserisci TESTATA in ViscosityControls
            query_header = """
                           INSERT INTO [Traceability_RS].[dbo].[ViscosityControls]
                           ([UserName], [QtyMatUsed], [QtyDiluantUsed], [IdComponent], [DateSys])
                               OUTPUT INSERTED.ViscosityControlId
                           VALUES (?, ?, ?, ?, ?) \
                           """
            cursor.execute(query_header, operator, qty_mat_value, qty_diluant_value, component_id, measurement_date)

            # Recupera l'ID appena inserito
            viscosity_control_id = cursor.fetchone()[0]

            # 2. Inserisci RIGA in ViscosyContronCheckCups
            query_detail = """
                           INSERT INTO [Traceability_RS].[dbo].[ViscosyContronCheckCups]
                               ([ViscosytyControlId], [MeasuramentCupFord], [DateSys])
                           VALUES (?, ?, ?) \
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
                f"Misurazione viscosità salvata: ID={viscosity_control_id}, Coating={coating_text}, Misurazione={measurement_value}")

        except Exception as e:
            logger.error(f"Errore salvataggio misurazione: {e}")
            messagebox.showerror(
                self.translator.get("error", "Errore"),
                f"{self.translator.get('save_error', 'Errore salvataggio')}: {str(e)}"
            )

    def _clear_form(self):
        """Pulisce il form"""
        self.coating_combo.set("")
        self.operator_var.set("")
        self.qty_mat_var.set("")
        self.qty_diluant_var.set("")
        self.measurement_var.set("")
        self.date_entry.set_date(datetime.now())


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
    """Dialog per aggiungere/modificare un tipo di vernice"""

    def __init__(self, parent, conn_str, translator, mode="add", coating_id=None, code="", description=""):
        self.parent = parent
        self.conn_str = conn_str
        self.translator = translator
        self.mode = mode
        self.coating_id = coating_id
        self.result = False

        self.dialog = tk.Toplevel(parent)
        title_key = "add_coating_title" if mode == "add" else "edit_coating_title"
        self.dialog.title(self.translator.get(title_key))
        self.dialog.geometry("400x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Campi
        ttk.Label(self.dialog, text=f"{self.translator.get('coating_code')}:").grid(row=0, column=0, padx=10, pady=10,
                                                                                    sticky="e")
        ttk.Label(self.dialog, text=f"{self.translator.get('coating_description')}:").grid(row=1, column=0, padx=10,
                                                                                           pady=10, sticky="e")

        self.code_var = tk.StringVar(value=code)
        self.desc_var = tk.StringVar(value=description)

        ttk.Entry(self.dialog, textvariable=self.code_var, width=30).grid(row=0, column=1, padx=10, pady=10)
        ttk.Entry(self.dialog, textvariable=self.desc_var, width=30).grid(row=1, column=1, padx=10, pady=10)

        # Pulsanti
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text=self.translator.get("btn_save"), command=self._save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self.translator.get("btn_cancel"), command=self.dialog.destroy).pack(side=tk.LEFT,
                                                                                                        padx=5)

        self.dialog.wait_window()

    def _save(self):
        """Salva il tipo di vernice"""
        code = self.code_var.get().strip()
        description = self.desc_var.get().strip()

        if not code:
            messagebox.showwarning(
                self.translator.get("warning"),
                self.translator.get("enter_coating_code"),
                parent=self.dialog
            )
            return

        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            if self.mode == "add":
                query = """
                    INSERT INTO Traceability_RS.dbo.components (IDCOMPONENTTYPE, ComponentCode, ComponentDescription)
                    VALUES (24, ?, ?)
                """
                cursor.execute(query, (code, description))
                logger.info(f"Vernice aggiunta: {code}")
            else:
                query = """
                    UPDATE Traceability_RS.dbo.components
                    SET ComponentCode = ?,
                        ComponentDescription = ?
                    WHERE IDCOMPONENT = ?
                """
                cursor.execute(query, (code, description, self.coating_id))
                logger.info(f"Vernice modificata: ID={self.coating_id}")

            conn.commit()
            conn.close()

            self.result = True
            messagebox.showinfo(
                self.translator.get("success"),
                self.translator.get("coating_saved_success"),
                parent=self.dialog
            )
            self.dialog.destroy()

        except Exception as e:
            logger.error(f"Errore salvataggio vernice: {e}")
            messagebox.showerror(
                self.translator.get("error"),
                f"{self.translator.get('save_error')}: {str(e)}",
                parent=self.dialog
            )


class ViscosityControlWindow:
    """Finestra per la registrazione dei controlli di viscosità"""

    def __init__(self, parent, conn_str, language_code='it'):
        self.parent = parent
        self.conn_str = conn_str
        self.window = None
        self.username = None
        self.current_control_id = None
        self.measurements_tree = None
        self.translator = TranslationManager(conn_str, language_code)

    def show(self):
        """Mostra la finestra dopo login speciale"""
        if not self._special_login():
            return

        self.window = tk.Toplevel(self.parent)
        title = f"{self.translator.get('viscosity_control_title')} - {self.translator.get('user')}: {self.username}"
        self.window.title(title)
        self.window.geometry("900x700")

        # Frame principale
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- SEZIONE TESTATA ---
        header_frame = ttk.LabelFrame(main_frame, text=self.translator.get("control_data"), padding="10")
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Riga 1: Utente e Data/Ora
        row1 = ttk.Frame(header_frame)
        row1.pack(fill=tk.X, pady=5)

        ttk.Label(row1, text=f"{self.translator.get('user')}:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(row1, text=self.username, font=("", 10, "bold")).pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(row1, text=f"{self.translator.get('datetime')}:").pack(side=tk.LEFT, padx=(0, 5))
        self.datetime_label = ttk.Label(row1, text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), font=("", 10, "bold"))
        self.datetime_label.pack(side=tk.LEFT)

        # Riga 2: Materiale (Coating)
        row2 = ttk.Frame(header_frame)
        row2.pack(fill=tk.X, pady=5)

        ttk.Label(row2, text=f"{self.translator.get('coating_material')}:").pack(side=tk.LEFT, padx=(0, 5))
        self.coating_combo = ttk.Combobox(row2, state="readonly", width=40)
        self.coating_combo.pack(side=tk.LEFT, padx=(0, 20))
        self._load_coatings()

        # Riga 3: Quantità materiale e diluente
        row3 = ttk.Frame(header_frame)
        row3.pack(fill=tk.X, pady=5)

        ttk.Label(row3, text=f"{self.translator.get('qty_material_used')} (g):").pack(side=tk.LEFT, padx=(0, 5))
        self.qty_material_var = tk.StringVar()
        ttk.Entry(row3, textvariable=self.qty_material_var, width=15).pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(row3, text=f"{self.translator.get('qty_diluent_used')} (g):").pack(side=tk.LEFT, padx=(0, 5))
        self.qty_diluent_var = tk.StringVar()
        ttk.Entry(row3, textvariable=self.qty_diluent_var, width=15).pack(side=tk.LEFT)

        # Pulsanti testata
        btn_header_frame = ttk.Frame(header_frame)
        btn_header_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_header_frame, text=f"💾 {self.translator.get('btn_save_header')}",
                   command=self._save_header).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_header_frame, text=f"🆕 {self.translator.get('btn_new_control')}",
                   command=self._new_control).pack(side=tk.LEFT, padx=5)

        # --- SEZIONE MISURAZIONI ---
        measurements_frame = ttk.LabelFrame(main_frame, text=self.translator.get("measurements"), padding="10")
        measurements_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Campo per nuova misurazione
        input_frame = ttk.Frame(measurements_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(input_frame, text=f"{self.translator.get('ford_cup_measurement')}:").pack(side=tk.LEFT, padx=(0, 5))
        self.measurement_var = tk.StringVar()
        measurement_entry = ttk.Entry(input_frame, textvariable=self.measurement_var, width=15)
        measurement_entry.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(input_frame, text=f"➕ {self.translator.get('btn_add_measurement')}",
                   command=self._add_measurement).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text=f"🗑️ {self.translator.get('btn_delete_measurement')}",
                   command=self._delete_measurement).pack(side=tk.LEFT, padx=5)

        measurement_entry.bind('<Return>', lambda e: self._add_measurement())

        # Treeview misurazioni
        tree_frame = ttk.Frame(measurements_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Measurement")
        self.measurements_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

        self.measurements_tree.heading("ID", text="ID")
        self.measurements_tree.heading("Measurement", text=self.translator.get("ford_cup_value"))

        self.measurements_tree.column("ID", width=100)
        self.measurements_tree.column("Measurement", width=200)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.measurements_tree.yview)
        self.measurements_tree.configure(yscrollcommand=scrollbar.set)

        self.measurements_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Statistiche
        stats_frame = ttk.Frame(measurements_frame)
        stats_frame.pack(fill=tk.X, pady=(10, 0))

        self.stats_label = ttk.Label(stats_frame, text="", font=("", 9))
        self.stats_label.pack(side=tk.LEFT)

        self._update_datetime()

    def _special_login(self):
        """Login speciale per controllo viscosità"""
        dialog = tk.Toplevel(self.parent)
        dialog.title(self.translator.get("login_viscosity_title"))
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

        result = {"authenticated": False, "username": None}

        def on_login():
            username = username_var.get().strip()
            password = password_var.get().strip()

            if self._validate_special_user(username, password):
                result["authenticated"] = True
                result["username"] = username
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

        if result["authenticated"]:
            self.username = result["username"]
            return True
        return False

    def _validate_special_user(self, username, password):
        """Valida le credenziali utente per controllo viscosità"""
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            # Verifica credenziali e permessi speciali
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

    def _update_datetime(self):
        """Aggiorna data/ora ogni secondo"""
        if self.window and self.window.winfo_exists():
            self.datetime_label.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.window.after(1000, self._update_datetime)

    def _load_coatings(self):
        """Carica i materiali coating nel combo"""
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = """
                SELECT IDCOMPONENT, ComponentCode, ComponentDescription
                FROM Traceability_RS.dbo.components
                WHERE IdComponentType = 24
                ORDER BY ComponentCode
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            self.coatings_data = {f"{row.ComponentCode} - {row.ComponentDescription}": row.IDCOMPONENT
                                  for row in rows}

            self.coating_combo['values'] = list(self.coatings_data.keys())
            if self.coating_combo['values']:
                self.coating_combo.current(0)

            conn.close()

        except Exception as e:
            logger.error(f"Errore caricamento coating: {e}")
            messagebox.showerror(
                self.translator.get("error"),
                f"{self.translator.get('load_error')}: {str(e)}"
            )

    def _save_header(self):
        """Salva la testata del controllo viscosità"""
        coating_selected = self.coating_combo.get()
        qty_material = self.qty_material_var.get().strip()
        qty_diluent = self.qty_diluent_var.get().strip()

        if not coating_selected:
            messagebox.showwarning(
                self.translator.get("warning"),
                self.translator.get("select_coating_material")
            )
            return

        if not qty_material or not qty_diluent:
            messagebox.showwarning(
                self.translator.get("warning"),
                self.translator.get("enter_quantities")
            )
            return

        try:
            qty_mat = float(qty_material)
            qty_dil = float(qty_diluent)

            if qty_mat <= 0 or qty_dil <= 0:
                raise ValueError()

        except ValueError:
            messagebox.showerror(
                self.translator.get("error"),
                self.translator.get("invalid_quantities")
            )
            return

        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            id_component = self.coatings_data[coating_selected]
            control_datetime = datetime.now()

            if self.current_control_id:
                # Aggiorna testata esistente
                query = """
                    UPDATE Traceability_RS.dbo.ViscosityControls
                    SET QtyMatUsed = ?,
                        QtyDiluantUsed = ?,
                        IdComponent = ?,
                        ControlDateTime = ?
                    WHERE ViscosityControlId = ?
                """
                cursor.execute(query, (qty_mat, qty_dil, id_component, control_datetime, self.current_control_id))
            else:
                # Nuova testata
                query = """
                    INSERT INTO Traceability_RS.dbo.ViscosityControls
                        (UserName, QtyMatUsed, QtyDiluantUsed, IdComponent, ControlDateTime)
                    VALUES (?, ?, ?, ?, ?)
                """
                cursor.execute(query, (self.username, qty_mat, qty_dil, id_component, control_datetime))

                # Recupera ID generato
                cursor.execute("SELECT @@IDENTITY AS ID")
                self.current_control_id = cursor.fetchone()[0]

            conn.commit()
            conn.close()

            messagebox.showinfo(
                self.translator.get("success"),
                self.translator.get("header_saved_success")
            )
            logger.info(f"Testata controllo salvata: ID={self.current_control_id}")

        except Exception as e:
            logger.error(f"Errore salvataggio testata: {e}")
            messagebox.showerror(
                self.translator.get("error"),
                f"{self.translator.get('save_error')}: {str(e)}"
            )

    def _add_measurement(self):
        """Aggiunge una misurazione"""
        if not self.current_control_id:
            messagebox.showwarning(
                self.translator.get("warning"),
                self.translator.get("save_header_first")
            )
            return

        measurement = self.measurement_var.get().strip()

        if not measurement:
            messagebox.showwarning(
                self.translator.get("warning"),
                self.translator.get("enter_measurement")
            )
            return

        try:
            meas_value = float(measurement)
            if meas_value <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror(
                self.translator.get("error"),
                self.translator.get("invalid_measurement")
            )
            return

        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = """
                INSERT INTO Traceability_RS.dbo.ViscosyContronCheckCups
                    (ViscosytyControlId, MeasuramentCupFord)
                VALUES (?, ?)
            """
            cursor.execute(query, (self.current_control_id, meas_value))
            conn.commit()

            # Recupera ID generato
            cursor.execute("SELECT @@IDENTITY AS ID")
            new_id = cursor.fetchone()[0]

            conn.close()

            # Aggiungi alla treeview
            self.measurements_tree.insert("", tk.END, values=(new_id, meas_value))
            self.measurement_var.set("")
            self._update_statistics()

            logger.info(f"Misurazione aggiunta: {meas_value}")

        except Exception as e:
            logger.error(f"Errore aggiunta misurazione: {e}")
            messagebox.showerror(
                self.translator.get("error"),
                f"{self.translator.get('save_error')}: {str(e)}"
            )

    def _delete_measurement(self):
        """Elimina la misurazione selezionata"""
        selection = self.measurements_tree.selection()
        if not selection:
            messagebox.showwarning(
                self.translator.get("warning"),
                self.translator.get("select_measurement_to_delete")
            )
            return

        item = self.measurements_tree.item(selection[0])
        measurement_id = item['values'][0]

        if not messagebox.askyesno(
                self.translator.get("confirm"),
                self.translator.get("confirm_delete_measurement")
        ):
            return

        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()

            query = "DELETE FROM Traceability_RS.dbo.ViscosyContronCheckCups WHERE ViscosytyControlId = ?"
            cursor.execute(query, (measurement_id,))
            conn.commit()
            conn.close()

            self.measurements_tree.delete(selection[0])
            self._update_statistics()

            logger.info(f"Misurazione eliminata: ID={measurement_id}")

        except Exception as e:
            logger.error(f"Errore eliminazione misurazione: {e}")
            messagebox.showerror(
                self.translator.get("error"),
                f"{self.translator.get('delete_error')}: {str(e)}"
            )

    def _update_statistics(self):
        """Aggiorna le statistiche delle misurazioni"""
        measurements = []
        for item in self.measurements_tree.get_children():
            values = self.measurements_tree.item(item)['values']
            measurements.append(float(values[1]))

        if measurements:
            count = len(measurements)
            avg = sum(measurements) / count
            min_val = min(measurements)
            max_val = max(measurements)

            count_text = self.translator.get('measurements_count')
            avg_text = self.translator.get('average')
            min_text = self.translator.get('min')
            max_text = self.translator.get('max')

            stats_text = f"{count_text}: {count} | {avg_text}: {avg:.2f} | {min_text}: {min_val:.2f} | {max_text}: {max_val:.2f}"
            self.stats_label.config(text=stats_text)
        else:
            self.stats_label.config(text="")

    def _new_control(self):
        """Inizia un nuovo controllo"""
        if messagebox.askyesno(
                self.translator.get("confirm"),
                self.translator.get("confirm_new_control")
        ):
            self.current_control_id = None
            self.qty_material_var.set("")
            self.qty_diluent_var.set("")
            self.measurement_var.set("")

            for item in self.measurements_tree.get_children():
                self.measurements_tree.delete(item)

            self._update_statistics()
            logger.info("Nuovo controllo iniziato")


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


# Funzioni di utilità per l'integrazione nel menu principale


def open_coating_settings(parent, conn_str, language_code='it'):
    """Apre la finestra Settings Coating"""
    window = CoatingSettingsWindow(parent, conn_str, language_code)
    window.show()


def open_viscosity_control(parent, conn_str, language_code='it'):
    """Apre la finestra Controllo Viscosità"""
    window = ViscosityControlWindow(parent, conn_str, language_code)
    window.show()


def open_coating_reports(parent, conn_str, language_code='it'):
    """Apre la finestra Rapporti Coating"""
    window = CoatingReportsWindow(parent, conn_str, language_code)
    window.show()
