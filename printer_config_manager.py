"""
Modulo per la gestione delle configurazioni stampanti.
Gestisce:
- Configurazione stampanti (IP, Porta, Nome, Locazione)
- CRUD operations
- Test connessione stampante
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
import socket

logger = logging.getLogger("TraceabilityRS")


class PrinterConfigWindow(tk.Toplevel):
    """Finestra per la gestione delle configurazioni stampanti"""

    def __init__(self, parent, db_handler, lang_manager, user_id):
        logger.info(f"PrinterConfigWindow: Apertura finestra gestione configurazioni stampanti (user: {user_id})")
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager
        self.user_id = user_id

        self.title(self.lang.get('printer_config_title', 'Configurazione Stampanti'))
        self.geometry('1000x600')
        self.transient(parent)

        self._current_printer_id = None
        self._build_ui()
        self._load_printers()

    def _build_ui(self):
        """Costruisce l'interfaccia"""
        # Header con nome utente
        header = ttk.Frame(self)
        header.pack(fill='x', padx=10, pady=5)
        ttk.Label(header, text=f"{self.lang.get('logged_user', 'Utente')}: {self.user_id}",
                  font=('Arial', 10, 'bold')).pack(side='left')

        # Frame principale diviso in due colonne
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Colonna sinistra: Form inserimento
        left_frame = ttk.LabelFrame(main_frame, text=self.lang.get('printer_form', 'Dati Stampante'))
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        # Nome Stampante
        ttk.Label(left_frame, text=self.lang.get('printer_name', 'Nome Stampante') + ' *').grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.name_var, width=40).grid(
            row=0, column=1, padx=5, pady=5, sticky='ew')

        # IP Stampante
        ttk.Label(left_frame, text=self.lang.get('printer_ip', 'IP Stampante') + ' *').grid(
            row=1, column=0, sticky='w', padx=5, pady=5)
        self.ip_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.ip_var, width=40).grid(
            row=1, column=1, padx=5, pady=5, sticky='ew')

        # Porta Stampante
        ttk.Label(left_frame, text=self.lang.get('printer_port', 'Porta') + ' *').grid(
            row=2, column=0, sticky='w', padx=5, pady=5)
        self.port_var = tk.StringVar(value='9100')
        ttk.Entry(left_frame, textvariable=self.port_var, width=40).grid(
            row=2, column=1, padx=5, pady=5, sticky='ew')

        # Locazione Stampante
        ttk.Label(left_frame, text=self.lang.get('printer_location', 'Locazione')).grid(
            row=3, column=0, sticky='w', padx=5, pady=5)
        self.location_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.location_var, width=40).grid(
            row=3, column=1, padx=5, pady=5, sticky='ew')

        # Attiva
        self.is_active_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(left_frame, text=self.lang.get('is_active', 'Attiva'),
                       variable=self.is_active_var).grid(
            row=4, column=0, columnspan=2, sticky='w', padx=5, pady=5)

        # Pulsanti azione
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text=self.lang.get('btn_new', 'Nuovo'),
                  command=self._on_new).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_save', 'Salva'),
                  command=self._on_save).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_delete', 'Elimina'),
                  command=self._on_delete).pack(side='left', padx=2)
        ttk.Button(btn_frame, text=self.lang.get('btn_test', 'Test'),
                  command=self._on_test).pack(side='left', padx=2)

        left_frame.columnconfigure(1, weight=1)

        # Colonna destra: Lista stampanti configurate
        right_frame = ttk.LabelFrame(main_frame, text=self.lang.get('configured_printers', 'Stampanti Configurate'))
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        # Treeview
        columns = ('id', 'name', 'ip', 'port', 'location', 'active')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=20)
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text=self.lang.get('printer_name', 'Nome'))
        self.tree.heading('ip', text=self.lang.get('printer_ip', 'IP'))
        self.tree.heading('port', text=self.lang.get('printer_port', 'Porta'))
        self.tree.heading('location', text=self.lang.get('printer_location', 'Locazione'))
        self.tree.heading('active', text=self.lang.get('active', 'Attiva'))

        self.tree.column('id', width=50)
        self.tree.column('name', width=150)
        self.tree.column('ip', width=120)
        self.tree.column('port', width=60)
        self.tree.column('location', width=120)
        self.tree.column('active', width=60)

        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)

    def _load_printers(self):
        """Carica le stampanti configurate"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            query = """
                SELECT PrinterId, PrinterName, PrinterIP, PrinterPort, 
                       PrinterLocation, IsActive
                FROM [Traceability_RS].[pst].[PrinterConfigs]
                ORDER BY PrinterName
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            
            for row in cursor.fetchall():
                active_text = '✓' if row.IsActive else ''
                self.tree.insert('', 'end', values=(
                    row.PrinterId,
                    row.PrinterName,
                    row.PrinterIP,
                    row.PrinterPort,
                    row.PrinterLocation or '',
                    active_text
                ))
            
            cursor.close()
        except Exception as e:
            logger.error(f"Errore caricamento stampanti: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore caricamento stampanti: {str(e)}"
            )

    def _on_select(self, event):
        """Gestisce la selezione di una riga"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']

        self._current_printer_id = values[0]
        self.name_var.set(values[1])
        self.ip_var.set(values[2])
        self.port_var.set(str(values[3]))
        self.location_var.set(values[4])
        self.is_active_var.set(values[5] == '✓')

    def _on_new(self):
        """Pulisce il form per nuovo inserimento"""
        self._current_printer_id = None
        self.name_var.set('')
        self.ip_var.set('')
        self.port_var.set('9100')
        self.location_var.set('')
        self.is_active_var.set(True)

    def _validate_ip(self, ip):
        """Valida un indirizzo IP"""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False

    def _on_save(self):
        """Salva o aggiorna una stampante"""
        # Validazione
        if not self.name_var.get().strip():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('enter_printer_name', 'Inserire il nome della stampante')
            )
            return

        if not self.ip_var.get().strip():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('enter_printer_ip', 'Inserire l\'IP della stampante')
            )
            return

        if not self._validate_ip(self.ip_var.get().strip()):
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('invalid_ip', 'Indirizzo IP non valido')
            )
            return

        try:
            port = int(self.port_var.get().strip())
            if port <= 0 or port > 65535:
                raise ValueError()
        except ValueError:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('invalid_port', 'Porta non valida (1-65535)')
            )
            return

        name = self.name_var.get().strip()
        ip = self.ip_var.get().strip()
        location = self.location_var.get().strip() or None
        is_active = self.is_active_var.get()

        try:
            if self._current_printer_id:
                # Update
                query = """
                    UPDATE [Traceability_RS].[pst].[PrinterConfigs]
                    SET PrinterName = ?, PrinterIP = ?, PrinterPort = ?, 
                        PrinterLocation = ?, IsActive = ?
                    WHERE PrinterId = ?
                """
                cursor = self.db.conn.cursor()
                cursor.execute(query, (name, ip, port, location, is_active, self._current_printer_id))
                self.db.conn.commit()
                cursor.close()
                message = self.lang.get('printer_updated', 'Stampante aggiornata con successo')
            else:
                # Insert
                query = """
                    INSERT INTO [Traceability_RS].[pst].[PrinterConfigs]
                    (PrinterName, PrinterIP, PrinterPort, PrinterLocation, IsActive)
                    VALUES (?, ?, ?, ?, ?)
                """
                cursor = self.db.conn.cursor()
                cursor.execute(query, (name, ip, port, location, is_active))
                self.db.conn.commit()
                cursor.close()
                message = self.lang.get('printer_saved', 'Stampante salvata con successo')

            messagebox.showinfo(self.lang.get('success', 'Successo'), message)
            self._load_printers()
            self._on_new()

        except Exception as e:
            logger.error(f"Errore salvataggio stampante: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"Errore durante il salvataggio: {str(e)}"
            )

    def _on_delete(self):
        """Elimina una stampante"""
        if not self._current_printer_id:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('select_printer', 'Selezionare una stampante da eliminare')
            )
            return

        if messagebox.askyesno(
            self.lang.get('confirm', 'Conferma'),
            self.lang.get('confirm_delete_printer', 'Eliminare la stampante selezionata?')
        ):
            try:
                query = """
                    DELETE FROM [Traceability_RS].[pst].[PrinterConfigs]
                    WHERE PrinterId = ?
                """
                cursor = self.db.conn.cursor()
                cursor.execute(query, (self._current_printer_id,))
                self.db.conn.commit()
                cursor.close()

                messagebox.showinfo(
                    self.lang.get('success', 'Successo'),
                    self.lang.get('printer_deleted', 'Stampante eliminata con successo')
                )
                self._load_printers()
                self._on_new()

            except Exception as e:
                logger.error(f"Errore eliminazione stampante: {e}")
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    f"Errore durante l'eliminazione: {str(e)}"
                )

    def _on_test(self):
        """Testa la connessione alla stampante"""
        if not self.ip_var.get().strip():
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('enter_printer_ip', 'Inserire l\'IP della stampante')
            )
            return

        try:
            port = int(self.port_var.get().strip())
        except ValueError:
            messagebox.showwarning(
                self.lang.get('warning', 'Attenzione'),
                self.lang.get('invalid_port', 'Porta non valida')
            )
            return

        ip = self.ip_var.get().strip()

        try:
            # Test connessione
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # Timeout 5 secondi
            
            logger.info(f"Test connessione stampante {ip}:{port}")
            sock.connect((ip, port))
            sock.close()
            
            messagebox.showinfo(
                self.lang.get('success', 'Successo'),
                self.lang.get('printer_test_success', 'Connessione alla stampante riuscita!')
            )
            logger.info("Test connessione stampante riuscito")
            
        except socket.timeout:
            logger.error("Timeout test connessione stampante")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                self.lang.get('printer_timeout', 'Timeout connessione. Verificare che la stampante sia accesa e raggiungibile.')
            )
        except socket.error as e:
            logger.error(f"Errore test connessione stampante: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('printer_connection_error', 'Errore connessione stampante')}: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Errore test stampante: {e}")
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('test_error', 'Errore durante il test')}: {str(e)}"
            )


def open_printer_config(parent, db_handler, lang_manager, user_id):
    """Funzione helper per aprire la finestra di configurazione stampanti"""
    PrinterConfigWindow(parent, db_handler, lang_manager, user_id)
