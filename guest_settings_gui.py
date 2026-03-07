# -*- coding: utf-8 -*-
"""
Modulo per le impostazioni ospiti: gestione Hotel, Shuttle e Compagnie Aeree.
Menu: Operazioni → Personale → Ospiti → Settings
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger("TraceabilityRS")


# ================================================================
# SUPPORTER SETTINGS (Hotel / Shuttle)
# ================================================================
class SupporterSettingsWindow(tk.Toplevel):
    """Finestra per gestire Hotel (type=1) o Shuttle (type=2) da VisitorSupportersData."""

    def __init__(self, parent, db, lang, user_name, supporter_type_id, title_label):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name
        self.supporter_type_id = supporter_type_id

        self.title(title_label)
        self.geometry('950x550')
        self.transient(parent)
        self.grab_set()

        self._towns = {}  # {display: TownId}
        self._selected_id = None

        self._build_ui()
        self._load_towns()
        self._load_data()

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _build_ui(self):
        """Costruisce l'interfaccia."""
        # TreeView
        tree_frame = ttk.Frame(self, padding=10)
        tree_frame.pack(fill='both', expand=True)

        columns = ('id', 'name', 'email', 'phone', 'city')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                  selectmode='browse', height=15)

        self.tree.heading('id', text='ID')
        self.tree.heading('name', text=self.lang.get('col_name', 'Nome'))
        self.tree.heading('email', text='Email')
        self.tree.heading('phone', text=self.lang.get('col_phone', 'Telefono'))
        self.tree.heading('city', text=self.lang.get('col_city', 'Città'))

        self.tree.column('id', width=50, anchor='center')
        self.tree.column('name', width=220)
        self.tree.column('email', width=250)
        self.tree.column('phone', width=150)
        self.tree.column('city', width=180)

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        # Form
        form = ttk.LabelFrame(self, text=self.lang.get('edit_details', 'Dettagli'), padding=10)
        form.pack(fill='x', padx=10, pady=(0, 5))

        ttk.Label(form, text=self.lang.get('col_name', 'Nome:')).grid(
            row=0, column=0, sticky='w', padx=5, pady=3)
        self.name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.name_var, width=30).grid(
            row=0, column=1, padx=5, pady=3, sticky='ew')

        ttk.Label(form, text='Email:').grid(
            row=0, column=2, sticky='w', padx=5, pady=3)
        self.email_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.email_var, width=30).grid(
            row=0, column=3, padx=5, pady=3, sticky='ew')

        ttk.Label(form, text=self.lang.get('col_phone', 'Telefono:')).grid(
            row=1, column=0, sticky='w', padx=5, pady=3)
        self.phone_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.phone_var, width=20).grid(
            row=1, column=1, padx=5, pady=3, sticky='w')

        ttk.Label(form, text=self.lang.get('col_city', 'Città:')).grid(
            row=1, column=2, sticky='w', padx=5, pady=3)
        self.city_var = tk.StringVar()
        self.city_combo = ttk.Combobox(form, textvariable=self.city_var, width=28, state='readonly')
        self.city_combo.grid(row=1, column=3, padx=5, pady=3, sticky='ew')

        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        # Pulsanti
        btn_frame = ttk.Frame(self, padding=5)
        btn_frame.pack(fill='x', padx=10, pady=(0, 10))

        ttk.Button(btn_frame, text=self.lang.get('btn_new', '➕ Nuovo'),
                   command=self._on_new).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_save', '💾 Salva'),
                   command=self._on_save).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_deactivate', '🚫 Disattiva'),
                   command=self._on_deactivate).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_close', 'Chiudi'),
                   command=self.destroy).pack(side='right', padx=5)

    def _load_towns(self):
        """Carica le città dal DB."""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT t.TownId, t.TownName, c.CountyName, n.NationName
                FROM Employee.Geo.Towns t
                INNER JOIN Employee.Geo.Counties c ON t.CountyId = c.CountyId
                INNER JOIN Employee.Geo.Nations n ON c.NationId = n.NationId
                ORDER BY n.NationName, t.TownName
            """)
            self._towns = {}
            towns_list = []
            for row in cursor.fetchall():
                display = f"{row.TownName} ({row.NationName})"
                self._towns[display] = row.TownId
                towns_list.append(display)
            self.city_combo['values'] = towns_list
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento città: {e}")

    def _load_data(self):
        """Carica i dati dalla tabella."""
        try:
            self.tree.delete(*self.tree.get_children())
            self._selected_id = None
            self._clear_form()

            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT vsd.SupporterDataId, vsd.Name, vsd.ReservationEmail,
                       vsd.Telephon, t.TownName, n.NationName
                FROM Employee.dbo.VisitorSupportersData vsd
                LEFT JOIN Employee.Geo.Towns t ON vsd.CityId = t.TownId
                LEFT JOIN Employee.Geo.Counties c ON t.CountyId = c.CountyId
                LEFT JOIN Employee.Geo.Nations n ON c.NationId = n.NationId
                WHERE vsd.SupporterTypeID = ?
                  AND vsd.DateOut IS NULL
                ORDER BY vsd.Name
            """, (self.supporter_type_id,))

            for row in cursor.fetchall():
                city_display = f"{row.TownName} ({row.NationName})" if row.TownName else ''
                self.tree.insert('', 'end', values=(
                    row.SupporterDataId,
                    row.Name or '',
                    row.ReservationEmail or '',
                    row.Telephon or '',
                    city_display
                ))
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento dati supporter: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")

    def _on_select(self, event=None):
        """Popola il form con il record selezionato."""
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], 'values')
        if not values:
            return

        self._selected_id = int(values[0])
        self.name_var.set(values[1])
        self.email_var.set(values[2])
        self.phone_var.set(values[3])
        self.city_var.set(values[4])

    def _clear_form(self):
        """Pulisce il form."""
        self._selected_id = None
        self.name_var.set('')
        self.email_var.set('')
        self.phone_var.set('')
        self.city_var.set('')

    def _on_new(self):
        """Prepara il form per un nuovo record."""
        self.tree.selection_remove(*self.tree.selection())
        self._clear_form()

    def _on_save(self):
        """Salva (INSERT o UPDATE) il record."""
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        city_display = self.city_var.get().strip()

        if not name:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('name_required', 'Il campo Nome è obbligatorio.'))
            return

        city_id = self._towns.get(city_display) if city_display else None

        try:
            cursor = self.db.conn.cursor()
            if self._selected_id:
                # UPDATE
                cursor.execute("""
                    UPDATE Employee.dbo.VisitorSupportersData
                    SET Name = ?, ReservationEmail = ?, Telephon = ?, CityId = ?
                    WHERE SupporterDataId = ?
                """, (name, email or None, phone or None, city_id, self._selected_id))
                logger.info(f"Aggiornato supporter ID={self._selected_id}")
            else:
                # INSERT
                cursor.execute("""
                    INSERT INTO Employee.dbo.VisitorSupportersData
                        (Name, ReservationEmail, CityId, SupporterTypeID, Telephon)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, email or None, city_id, self.supporter_type_id, phone or None))
                logger.info(f"Nuovo supporter creato: {name}")
            self.db.conn.commit()
            cursor.close()
            messagebox.showinfo(self.lang.get('success', 'Successo'),
                                self.lang.get('data_saved', 'Dati salvati con successo.'))
            self._load_data()
        except Exception as e:
            logger.error(f"Errore salvataggio supporter: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")

    def _on_deactivate(self):
        """Disattiva il record selezionato (DateOut = GETDATE())."""
        if not self._selected_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_record', 'Selezionare un record dalla lista.'))
            return

        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_deactivate', 'Disattivare questo record?')):
            return

        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                UPDATE Employee.dbo.VisitorSupportersData
                SET DateOut = GETDATE()
                WHERE SupporterDataId = ?
            """, (self._selected_id,))
            self.db.conn.commit()
            cursor.close()
            logger.info(f"Disattivato supporter ID={self._selected_id}")
            self._load_data()
        except Exception as e:
            logger.error(f"Errore disattivazione supporter: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")


# ================================================================
# AIRLINE SETTINGS (FlyghtCompanies)
# ================================================================
class AirlineSettingsWindow(tk.Toplevel):
    """Finestra per gestire le compagnie aeree (FlyghtCompanies)."""

    def __init__(self, parent, db, lang, user_name):
        super().__init__(parent)
        self.db = db
        self.lang = lang
        self.user_name = user_name

        self.title(self.lang.get('airline_settings_title', 'Gestione Compagnie Aeree'))
        self.geometry('700x500')
        self.transient(parent)
        self.grab_set()

        self._selected_id = None

        self._build_ui()
        self._load_data()

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _build_ui(self):
        """Costruisce l'interfaccia."""
        # TreeView
        tree_frame = ttk.Frame(self, padding=10)
        tree_frame.pack(fill='both', expand=True)

        columns = ('id', 'company_name', 'iata_code')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                  selectmode='browse', height=15)

        self.tree.heading('id', text='ID')
        self.tree.heading('company_name', text=self.lang.get('col_airline_name', 'Compagnia'))
        self.tree.heading('iata_code', text=self.lang.get('col_iata_code', 'Codice IATA'))

        self.tree.column('id', width=60, anchor='center')
        self.tree.column('company_name', width=350)
        self.tree.column('iata_code', width=150, anchor='center')

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        # Form
        form = ttk.LabelFrame(self, text=self.lang.get('edit_details', 'Dettagli'), padding=10)
        form.pack(fill='x', padx=10, pady=(0, 5))

        ttk.Label(form, text=self.lang.get('col_airline_name', 'Compagnia:')).grid(
            row=0, column=0, sticky='w', padx=5, pady=3)
        self.company_name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.company_name_var, width=40).grid(
            row=0, column=1, padx=5, pady=3, sticky='ew')

        ttk.Label(form, text=self.lang.get('col_iata_code', 'Codice IATA:')).grid(
            row=0, column=2, sticky='w', padx=5, pady=3)
        self.iata_code_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.iata_code_var, width=15).grid(
            row=0, column=3, padx=5, pady=3, sticky='w')

        form.columnconfigure(1, weight=1)

        # Pulsanti
        btn_frame = ttk.Frame(self, padding=5)
        btn_frame.pack(fill='x', padx=10, pady=(0, 10))

        ttk.Button(btn_frame, text=self.lang.get('btn_new', '➕ Nuovo'),
                   command=self._on_new).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_save', '💾 Salva'),
                   command=self._on_save).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete', '🗑 Elimina'),
                   command=self._on_delete).pack(side='left', padx=5)
        ttk.Button(btn_frame, text=self.lang.get('btn_close', 'Chiudi'),
                   command=self.destroy).pack(side='right', padx=5)

    def _load_data(self):
        """Carica le compagnie aeree."""
        try:
            self.tree.delete(*self.tree.get_children())
            self._selected_id = None
            self._clear_form()

            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT FlightCompanyId, CompanyName, FlightIdentifyCode
                FROM Employee.dbo.FlyghtCompanies
                ORDER BY CompanyName
            """)

            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=(
                    row.FlightCompanyId,
                    row.CompanyName or '',
                    row.FlightIdentifyCode or ''
                ))
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento compagnie aeree: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")

    def _on_select(self, event=None):
        """Popola il form."""
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], 'values')
        if not values:
            return

        self._selected_id = int(values[0])
        self.company_name_var.set(values[1])
        self.iata_code_var.set(values[2])

    def _clear_form(self):
        """Pulisce il form."""
        self._selected_id = None
        self.company_name_var.set('')
        self.iata_code_var.set('')

    def _on_new(self):
        """Prepara il form per un nuovo record."""
        self.tree.selection_remove(*self.tree.selection())
        self._clear_form()

    def _on_save(self):
        """Salva (INSERT o UPDATE)."""
        name = self.company_name_var.get().strip()
        code = self.iata_code_var.get().strip().upper()

        if not name:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('airline_name_required', 'Il nome della compagnia è obbligatorio.'))
            return

        try:
            cursor = self.db.conn.cursor()
            if self._selected_id:
                cursor.execute("""
                    UPDATE Employee.dbo.FlyghtCompanies
                    SET CompanyName = ?, FlightIdentifyCode = ?
                    WHERE FlightCompanyId = ?
                """, (name, code or None, self._selected_id))
                logger.info(f"Aggiornata compagnia ID={self._selected_id}")
            else:
                cursor.execute("""
                    INSERT INTO Employee.dbo.FlyghtCompanies (CompanyName, FlightIdentifyCode)
                    VALUES (?, ?)
                """, (name, code or None))
                logger.info(f"Nuova compagnia creata: {name}")
            self.db.conn.commit()
            cursor.close()
            messagebox.showinfo(self.lang.get('success', 'Successo'),
                                self.lang.get('data_saved', 'Dati salvati con successo.'))
            self._load_data()
        except Exception as e:
            logger.error(f"Errore salvataggio compagnia: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")

    def _on_delete(self):
        """Elimina la compagnia selezionata."""
        if not self._selected_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_record', 'Selezionare un record dalla lista.'))
            return

        if not messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_delete', 'Eliminare questo record?')):
            return

        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                DELETE FROM Employee.dbo.FlyghtCompanies
                WHERE FlightCompanyId = ?
            """, (self._selected_id,))
            self.db.conn.commit()
            cursor.close()
            logger.info(f"Eliminata compagnia ID={self._selected_id}")
            self._load_data()
        except Exception as e:
            logger.error(f"Errore eliminazione compagnia: {e}")
            messagebox.showerror(self.lang.get('error', 'Errore'), f"Errore: {e}")
