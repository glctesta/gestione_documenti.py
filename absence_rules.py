# -*- coding: utf-8 -*-
"""
Modulo per la gestione delle regole assenze.
Consente di configurare i giorni di anticipo richiesti per le richieste di assenza.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging

logger = logging.getLogger("TraceabilityRS")


class AbsenceRulesWindow(tk.Toplevel):
    """
    Finestra per la gestione delle regole di assenza.
    L'utente può:
    - Visualizzare le regole esistenti
    - Modificare il valore di DayNoZone
    - Cancellare regole esistenti
    - Aggiungere nuove regole
    """

    def __init__(self, parent, db_handler, lang_manager, authorized_user_id, authorized_user_name=None):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        self.authorized_user_id = authorized_user_id
        self.authorized_user_name = authorized_user_name

        self.title(self.lang.get('absence_rules_title', 'Regole Assenze'))
        self.geometry("800x600")
        self.resizable(True, True)

        # Variabili per la selezione
        self.selected_item = None
        self.request_types = []  # Lista dei tipi di richiesta disponibili

        self._create_widgets()
        self._load_request_types()
        self._load_absence_rules()

    def _create_widgets(self):
        """Crea i widget della finestra"""
        # Frame principale
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_label = ttk.Label(
            main_frame,
            text=self.lang.get('absence_rules_header', 'Configurazione Regole Assenze'),
            font=("Helvetica", 14, "bold")
        )
        header_label.pack(pady=(0, 10))

        # Frame per la combo di selezione tipo richiesta
        combo_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('select_request_type', 'Seleziona Tipo Richiesta'),
            padding="10"
        )
        combo_frame.pack(fill=tk.X, pady=(0, 10))

        self.request_type_combo = ttk.Combobox(
            combo_frame,
            state="readonly",
            width=50
        )
        self.request_type_combo.pack(fill=tk.X)

        # Bottone per aggiungere nuova regola
        add_button = ttk.Button(
            combo_frame,
            text=self.lang.get('add_rule', 'Aggiungi Regola'),
            command=self._add_rule
        )
        add_button.pack(pady=(10, 0))

        # Frame per le regole esistenti
        rules_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('existing_rules', 'Regole Esistenti'),
            padding="10"
        )
        rules_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Treeview per mostrare le regole
        columns = (
            'AbsenceRuleID',
            'IDRequestType',
            'RequestName',
            'DayNoZone'
        )
        
        self.tree = ttk.Treeview(
            rules_frame,
            columns=columns,
            show='headings',
            selectmode='browse'
        )

        # Configurazione colonne
        self.tree.heading('AbsenceRuleID', text='ID')
        self.tree.heading('IDRequestType', text=self.lang.get('col_request_type_id', 'ID Tipo'))
        self.tree.heading('RequestName', text=self.lang.get('col_request_name', 'Tipo Richiesta'))
        self.tree.heading('DayNoZone', text=self.lang.get('col_days_advance', 'Giorni di Anticipo'))

        self.tree.column('AbsenceRuleID', width=50, anchor='center')
        self.tree.column('IDRequestType', width=80, anchor='center')
        self.tree.column('RequestName', width=300, anchor='w')
        self.tree.column('DayNoZone', width=150, anchor='center')

        # Scrollbar
        scrollbar = ttk.Scrollbar(rules_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind per la selezione
        self.tree.bind('<<TreeviewSelect>>', self._on_rule_select)

        # Frame per i bottoni di azione
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 10))

        modify_button = ttk.Button(
            action_frame,
            text=self.lang.get('modify_days', 'Modifica Giorni'),
            command=self._modify_days
        )
        modify_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(
            action_frame,
            text=self.lang.get('delete_rule', 'Elimina Regola'),
            command=self._delete_rule
        )
        delete_button.pack(side=tk.LEFT, padx=5)

        refresh_button = ttk.Button(
            action_frame,
            text=self.lang.get('refresh', 'Aggiorna'),
            command=self._load_absence_rules
        )
        refresh_button.pack(side=tk.LEFT, padx=5)

        # Frame per la nota informativa
        note_frame = ttk.Frame(main_frame)
        note_frame.pack(fill=tk.X)

        note_text = self.lang.get(
            'absence_rules_note',
            'Queste regole influenzano la possibilità di richiedere giorni di assenza. '
            'La data di richiesta inizio assenza in relazione con la data inizio assenza desiderata, '
            'non potrà essere minore del valore di DayNoZone (Giorni di anticipo).'
        )

        note_label = ttk.Label(
            note_frame,
            text=note_text,
            wraplength=750,
            justify=tk.LEFT,
            foreground='red',
            font=("Helvetica", 9, "italic")
        )
        note_label.pack(pady=5)

    def _load_request_types(self):
        """Carica i tipi di richiesta dalla tabella RequestType"""
        try:
            query = """
                SELECT [IDRequestType], [RequestName], [Abbreviation]
                FROM [Timeclocking].[dbo].[RequestType]
                ORDER BY RequestName
            """
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()

            self.request_types = []
            combo_values = []

            for row in results:
                self.request_types.append({
                    'IDRequestType': row.IDRequestType,
                    'RequestName': row.RequestName,
                    'Abbreviation': row.Abbreviation
                })
                combo_values.append(f"{row.RequestName} ({row.Abbreviation})")

            self.request_type_combo['values'] = combo_values

            logger.info(f"Caricati {len(self.request_types)} tipi di richiesta")

        except Exception as e:
            logger.error(f"Errore nel caricamento dei tipi di richiesta: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('load_error', 'Errore nel caricamento')}: {e}"
            )

    def _load_absence_rules(self):
        """Carica le regole di assenza esistenti"""
        try:
            # Pulisce il Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            query = """
                SELECT 
                    [AbsenceRuleID],
                    r.[IDRequestType],
                    t.RequestName,
                    [DayNoZone]
                FROM [Employee].[dbo].[AbsenceRules] r
                RIGHT JOIN [Timeclocking].[dbo].[RequestType] t 
                    ON t.IDRequestType = r.[IDRequestType]
                WHERE t.IDRequestType IN (1,7,10,12) 
                    AND r.DateOut IS NULL
                ORDER BY t.RequestName
            """
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()

            for row in results:
                self.tree.insert('', tk.END, values=(
                    row.AbsenceRuleID if row.AbsenceRuleID else '',
                    row.IDRequestType,
                    row.RequestName,
                    row.DayNoZone if row.DayNoZone is not None else ''
                ))

            logger.info(f"Caricate {len(results)} regole di assenza")

        except Exception as e:
            logger.error(f"Errore nel caricamento delle regole: {e}", exc_info=True)
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('load_error', 'Errore nel caricamento')}: {e}"
            )

    def _on_rule_select(self, event):
        """Gestisce la selezione di una regola dalla lista"""
        selection = self.tree.selection()
        if selection:
            self.selected_item = self.tree.item(selection[0])['values']
            logger.debug(f"Regola selezionata: {self.selected_item}")

    def _add_rule(self):
        """Aggiunge una nuova regola di assenza"""
        if not self.request_type_combo.get():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_request_type_first', 'Selezionare prima un tipo di richiesta')
            )
            return

        # Ottieni l'ID del tipo richiesta selezionato
        selected_index = self.request_type_combo.current()
        if selected_index < 0:
            return

        selected_request_type = self.request_types[selected_index]
        id_request_type = selected_request_type['IDRequestType']

        # Chiedi i giorni di anticipo
        days_dialog = DaysInputDialog(
            self,
            self.lang,
            self.lang.get('add_rule', 'Aggiungi Regola')
        )
        self.wait_window(days_dialog)

        if hasattr(days_dialog, 'result') and days_dialog.result is not None:
            days_no_zone = days_dialog.result

            try:
                # Verifica se esiste già una regola attiva per questo tipo
                check_query = """
                    SELECT COUNT(*) as cnt
                    FROM [Employee].[dbo].[AbsenceRules]
                    WHERE [IDRequestType] = ? AND [DateOut] IS NULL
                """
                self.db.cursor.execute(check_query, id_request_type)
                count = self.db.cursor.fetchone().cnt

                if count > 0:
                    messagebox.showwarning(
                        self.lang.get('warning', 'Attenzione'),
                        self.lang.get('rule_already_exists', 'Esiste già una regola attiva per questo tipo di richiesta')
                    )
                    return

                # Inserisce la nuova regola
                insert_query = """
                    INSERT INTO [Employee].[dbo].[AbsenceRules]
                    ([IDRequestType], [DayNoZone], [DateOut])
                    VALUES (?, ?, NULL)
                """
                self.db.cursor.execute(insert_query, id_request_type, days_no_zone)
                self.db.conn.commit()

                messagebox.showinfo(
                    self.lang.get('success', 'Successo'),
                    self.lang.get('rule_added', 'Regola aggiunta con successo')
                )

                self._load_absence_rules()

            except Exception as e:
                self.db.conn.rollback()
                logger.error(f"Errore nell'inserimento della regola: {e}", exc_info=True)
                error_msg = self.lang.get('insert_error', 'Errore nell\'inserimento')
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    f"{error_msg}: {e}"
                )

    def _modify_days(self):
        """Modifica i giorni di anticipo per la regola selezionata"""
        if not self.selected_item or not self.selected_item[0]:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_rule_first', 'Selezionare prima una regola dalla lista')
            )
            return

        rule_id = self.selected_item[0]
        current_days = self.selected_item[3] if self.selected_item[3] else 0

        # Chiedi i nuovi giorni
        days_dialog = DaysInputDialog(
            self,
            self.lang,
            self.lang.get('modify_days', 'Modifica Giorni'),
            initial_value=current_days
        )
        self.wait_window(days_dialog)

        if hasattr(days_dialog, 'result') and days_dialog.result is not None:
            new_days = days_dialog.result

            try:
                update_query = """
                    UPDATE [Employee].[dbo].[AbsenceRules]
                    SET [DayNoZone] = ?
                    WHERE [AbsenceRuleID] = ?
                """
                self.db.cursor.execute(update_query, new_days, rule_id)
                self.db.conn.commit()

                messagebox.showinfo(
                    self.lang.get('success', 'Successo'),
                    self.lang.get('rule_updated', 'Regola aggiornata con successo')
                )

                self._load_absence_rules()

            except Exception as e:
                self.db.conn.rollback()
                logger.error(f"Errore nell'aggiornamento della regola: {e}", exc_info=True)
                error_msg = self.lang.get('update_error', 'Errore nell\'aggiornamento')
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    f"{error_msg}: {e}"
                )

    def _delete_rule(self):
        """Elimina (logicamente) la regola selezionata impostando DateOut"""
        if not self.selected_item or not self.selected_item[0]:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_rule_first', 'Selezionare prima una regola dalla lista')
            )
            return

        rule_id = self.selected_item[0]
        request_name = self.selected_item[2]

        # Conferma eliminazione
        confirm = messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_delete_rule', 'Confermare l\'eliminazione della regola per "{0}"?', request_name)
        )

        if not confirm:
            return

        try:
            # Imposta DateOut a GETDATE()
            update_query = """
                UPDATE [Employee].[dbo].[AbsenceRules]
                SET [DateOut] = GETDATE()
                WHERE [AbsenceRuleID] = ?
            """
            self.db.cursor.execute(update_query, rule_id)
            self.db.conn.commit()

            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('rule_deleted', 'Regola eliminata con successo')
            )

            self._load_absence_rules()

        except Exception as e:
            self.db.conn.rollback()
            logger.error(f"Errore nell'eliminazione della regola: {e}", exc_info=True)
            error_msg = self.lang.get('delete_error', 'Errore nell\'eliminazione')
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{error_msg}: {e}"
            )


class DaysInputDialog(tk.Toplevel):
    """Dialog per inserire il numero di giorni di anticipo"""

    def __init__(self, parent, lang_manager, title, initial_value=0):
        super().__init__(parent)
        self.lang = lang_manager
        self.result = None

        self.title(title)
        self.geometry("350x150")
        self.transient(parent)
        self.grab_set()

        self._create_widgets(initial_value)

    def _create_widgets(self, initial_value):
        """Crea i widget del dialog"""
        # Frame principale
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Label
        label = ttk.Label(
            main_frame,
            text=self.lang.get('enter_days_advance', 'Inserire i giorni di anticipo:')
        )
        label.pack(pady=(0, 10))

        # Spinbox per i giorni
        self.days_var = tk.IntVar(value=initial_value)
        spinbox = ttk.Spinbox(
            main_frame,
            from_=0,
            to=365,
            textvariable=self.days_var,
            width=10
        )
        spinbox.pack(pady=(0, 20))
        spinbox.focus()

        # Bottoni
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        ok_button = ttk.Button(
            button_frame,
            text=self.lang.get('ok', 'OK'),
            command=self._on_ok
        )
        ok_button.pack(side=tk.LEFT, padx=5)

        cancel_button = ttk.Button(
            button_frame,
            text=self.lang.get('cancel', 'Annulla'),
            command=self.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=5)

        # Bind Enter
        self.bind('<Return>', lambda e: self._on_ok())

    def _on_ok(self):
        """Gestisce il click su OK"""
        self.result = self.days_var.get()
        self.destroy()
