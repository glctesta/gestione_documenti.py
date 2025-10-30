"""
FCT Transfer Module
Gestisce l'esecuzione schedulata di file batch con controllo multi-istanza
"""

import json
import logging
import os
import subprocess
import threading
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import pyodbc

logger = logging.getLogger("TraceabilityRS.FCTTransfer")


class FCTTransferConfig:
    """Gestisce la configurazione FCT Transfer salvata in JSON"""

    def __init__(self, config_path: str = None):
        if config_path is None:
            appdata = os.getenv("LOCALAPPDATA", ".")
            config_dir = Path(appdata) / "TraceabilityRS"
            config_dir.mkdir(parents=True, exist_ok=True)
            self.config_path = config_dir / "fct_transfer_config.json"
        else:
            self.config_path = Path(config_path)

        self.bat_file_path = ""
        self.timer_seconds = 30
        self._load()

    def _load(self):
        """Carica la configurazione dal file JSON"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.bat_file_path = data.get("bat_file_path", "")
                    self.timer_seconds = data.get("timer_seconds", 30)
                logger.info(f"Configurazione FCT caricata: {self.config_path}")
            except Exception as e:
                logger.error(f"Errore caricamento config FCT: {e}")

    def save(self):
        """Salva la configurazione nel file JSON"""
        try:
            data = {
                "bat_file_path": self.bat_file_path,
                "timer_seconds": self.timer_seconds
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, indent=4, fp=f)
            logger.info(f"Configurazione FCT salvata: {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Errore salvataggio config FCT: {e}")
            return False


class FCTTransferManager:
    """Gestisce l'esecuzione e il controllo del batch FCT"""

    def __init__(self, db_conn_str: str, config: FCTTransferConfig):
        self.db_conn_str = db_conn_str
        self.config = config
        self.is_running = False
        self.thread = None
        self._stop_event = threading.Event()

    def _get_connection(self):
        """Crea una nuova connessione al database"""
        return pyodbc.connect(self.db_conn_str, timeout=10)

    def check_bat_running_status(self) -> tuple[bool, list]:
        """
        Verifica se il batch è già in esecuzione su altre istanze
        Returns: (is_running, list_of_active_instances)
        """
        if not self.config.bat_file_path:
            return False, []

        query = """
                SELECT [DateStart], [DateStop], [BatProgram]
                FROM [Traceability_RS].[dbo].[TransferFCTStatus]
                WHERE [BatProgram] = ? AND [DateStop] IS NULL
                ORDER BY [DateStart] DESC \
                """

        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query, self.config.bat_file_path)
            rows = cursor.fetchall()
            conn.close()

            instances = []
            for row in rows:
                instances.append({
                    'DateStart': row.DateStart,
                    'BatProgram': row.BatProgram
                })

            return len(instances) > 0, instances

        except Exception as e:
            logger.error(f"Errore verifica stato batch: {e}")
            return False, []

    def start_bat_execution(self) -> bool:
        """Avvia l'esecuzione del batch e registra in DB"""
        if not self.config.bat_file_path or not Path(self.config.bat_file_path).exists():
            logger.error("File batch non trovato")
            return False

        # Verifica se già in esecuzione
        is_running, _ = self.check_bat_running_status()
        if is_running:
            logger.warning(f"Batch già in esecuzione: {self.config.bat_file_path}")
            return False

        # Registra avvio in DB
        query = """
                INSERT INTO [Traceability_RS].[dbo].[TransferFCTStatus]
                    ([DateStart], [DateStop], [BatProgram])
                VALUES (GETDATE(), NULL, ?) \
                """

        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query, self.config.bat_file_path)
            conn.commit()
            conn.close()

            logger.info(f"Avvio batch registrato: {self.config.bat_file_path}")

            # Avvia thread di esecuzione
            self.is_running = True
            self._stop_event.clear()
            self.thread = threading.Thread(target=self._execution_loop, daemon=True)
            self.thread.start()

            self._log_execution('avviato')
            return True

        except Exception as e:
            logger.error(f"Errore avvio batch: {e}")
            return False

    def stop_bat_execution(self, date_start: datetime = None):
        """
        Ferma l'esecuzione del batch e aggiorna DB
        Se date_start è None, ferma l'istanza più recente
        """
        if not self.is_running:
            logger.warning("Nessuna esecuzione batch attiva")
            return False

        # Ferma il thread
        self._stop_event.set()
        self.is_running = False

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)

        # Aggiorna DB
        if date_start:
            query = """
                    UPDATE [Traceability_RS].[dbo].[TransferFCTStatus]
                    SET [DateStop] = GETDATE()
                    WHERE [BatProgram] = ? AND [DateStart] = ? AND [DateStop] IS NULL \
                    """
            params = (self.config.bat_file_path, date_start)

        else:
            query = """
                    UPDATE [Traceability_RS].[dbo].[TransferFCTStatus]
                    SET [DateStop] = GETDATE()
                    WHERE [BatProgram] = ? AND [DateStop] IS NULL \
                    """
            params = (self.config.bat_file_path,)

        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query, *params)
            conn.commit()
            conn.close()

            self._log_execution('fermato')
            logger.info(f"Stop batch registrato: {self.config.bat_file_path}")
            return True

        except Exception as e:
            logger.error(f"Errore stop batch: {e}")
            return False

    def _execution_loop(self):
        """Loop di esecuzione del batch (eseguito in thread separato)"""
        logger.info(f"Avvio loop esecuzione batch: {self.config.bat_file_path}")

        while not self._stop_event.is_set():
            try:
                # Esegui batch
                self._run_bat_file()

                # # Log su DB
                # self._log_execution('fermato')

                # Attendi timer (con check periodici per stop)
                for _ in range(self.config.timer_seconds):
                    if self._stop_event.is_set():
                        break
                    time.sleep(1)

            except Exception as e:
                logger.error(f"Errore nel loop esecuzione: {e}")
                time.sleep(5)  # Pausa prima di riprovare

        logger.info("Loop esecuzione batch terminato")

    def _run_bat_file(self):
        """Esegue il file batch"""
        try:
            result = subprocess.run(
                [self.config.bat_file_path],
                capture_output=True,
                text=True,
                timeout=120,
                shell=True
            )

            if result.returncode == 0:
                logger.info(f"Batch eseguito con successo: {self.config.bat_file_path}")
            else:
                logger.warning(f"Batch terminato con errori (code {result.returncode}): {result.stderr}")

        except subprocess.TimeoutExpired:
            logger.error(f"Timeout esecuzione batch: {self.config.bat_file_path}")
        except Exception as e:
            logger.error(f"Errore esecuzione batch: {e}")

    def _log_execution(self, action='lanciato'):
        """
        Registra l'esecuzione nel log DB

        Args:
            action (str): 'lanciato' o 'fermato'
        """
        log_message = f"File Bat {self.config.bat_file_path} {action}"

        query = """
                INSERT INTO [Traceability_RS].[dbo].[TransferFctLog]
                    ([DateSys], [Texts])
                VALUES (GETDATE(), ?) \
                """

        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query, log_message)
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Errore log esecuzione: {e}")


class FCTTransferSettingsWindow(tk.Toplevel):
    """Finestra di configurazione FCT Transfer"""

    def __init__(self, master, db_handler, lang_manager, config: FCTTransferConfig):
        super().__init__(master)
        self.db = db_handler
        self.lang = lang_manager
        self.config = config

        self.title(self.lang.get('fct_settings_title', "FCT Transfer - Impostazioni"))
        self.geometry("600x250")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.bat_file_var = tk.StringVar(value=self.config.bat_file_path)
        self.timer_var = tk.IntVar(value=self.config.timer_seconds)

        self._build_ui()

    def _build_ui(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        # File BAT
        bat_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('fct_bat_file', "File Batch (.bat)"),
            padding=10
        )
        bat_frame.pack(fill="x", pady=(0, 15))

        entry_frame = ttk.Frame(bat_frame)
        entry_frame.pack(fill="x")

        self.bat_entry = ttk.Entry(entry_frame, textvariable=self.bat_file_var, state="readonly")
        self.bat_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ttk.Button(
            entry_frame,
            text=self.lang.get('fct_browse', "Sfoglia..."),
            command=self._browse_bat_file
        ).pack(side="left")

        # Timer
        timer_frame = ttk.LabelFrame(
            main_frame,
            text=self.lang.get('fct_timer', "Timer Esecuzione"),
            padding=10
        )
        timer_frame.pack(fill="x", pady=(0, 15))

        timer_inner = ttk.Frame(timer_frame)
        timer_inner.pack(fill="x")

        ttk.Label(
            timer_inner,
            text=self.lang.get('fct_timer_seconds', "Secondi tra esecuzioni:")
        ).pack(side="left", padx=(0, 10))

        self.timer_spinbox = ttk.Spinbox(
            timer_inner,
            from_=1,
            to=120,
            textvariable=self.timer_var,
            width=10
        )
        self.timer_spinbox.pack(side="left")

        ttk.Label(
            timer_inner,
            text=self.lang.get('fct_timer_range', "(1-120 secondi)")
        ).pack(side="left", padx=(10, 0))

        # Pulsanti
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(
            btn_frame,
            text=self.lang.get('button_save', "Salva"),
            command=self._save_settings
        ).pack(side="right", padx=(10, 0))

        ttk.Button(
            btn_frame,
            text=self.lang.get('button_cancel', "Annulla"),
            command=self.destroy
        ).pack(side="right")

    def _browse_bat_file(self):
        """Apre dialog per selezione file .bat"""
        filename = filedialog.askopenfilename(
            parent=self,
            title=self.lang.get('fct_select_bat', "Seleziona file batch"),
            filetypes=[
                (self.lang.get('fct_bat_files', "File Batch"), "*.bat"),
                (self.lang.get('all_files', "Tutti i file"), "*.*")
            ]
        )

        if filename:
            self.bat_file_var.set(filename)

    def _save_settings(self):
        """Salva le impostazioni"""
        bat_path = self.bat_file_var.get().strip()

        if not bat_path:
            messagebox.showwarning(
                self.lang.get('warning', "Attenzione"),
                self.lang.get('fct_no_bat_selected', "Selezionare un file batch"),
                parent=self
            )
            return

        if not Path(bat_path).exists():
            messagebox.showerror(
                self.lang.get('error', "Errore"),
                self.lang.get('fct_bat_not_found', "File batch non trovato"),
                parent=self
            )
            return

        timer_val = self.timer_var.get()
        if not (1 <= timer_val <= 120):
            messagebox.showwarning(
                self.lang.get('warning', "Attenzione"),
                self.lang.get('fct_invalid_timer', "Timer deve essere tra 1 e 120 secondi"),
                parent=self
            )
            return

        # Salva configurazione
        self.config.bat_file_path = bat_path
        self.config.timer_seconds = timer_val

        if self.config.save():
            messagebox.showinfo(
                self.lang.get('success', "Successo"),
                self.lang.get('fct_settings_saved', "Impostazioni salvate correttamente"),
                parent=self
            )
            self.destroy()
        else:
            messagebox.showerror(
                self.lang.get('error', "Errore"),
                self.lang.get('fct_save_error', "Errore durante il salvataggio"),
                parent=self
            )


class FCTTransferStopDialog(tk.Toplevel):
    """Dialog per selezione istanze da fermare"""

    def __init__(self, master, lang_manager, instances: list):
        super().__init__(master)
        self.lang = lang_manager
        self.instances = instances
        self.selected_instances = []

        self.title(self.lang.get('fct_stop_title', "Ferma Istanze FCT"))
        self.geometry("500x350")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(
            main_frame,
            text=self.lang.get('fct_select_instances', "Seleziona le istanze da fermare:"),
            font=("", 10, "bold")
        ).pack(anchor="w", pady=(0, 10))

        # Lista istanze
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill="both", expand=True)

        cols = ("select", "date_start", "bat_program")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=8)

        self.tree.heading("select", text="")
        self.tree.column("select", width=30, anchor="center")
        self.tree.heading("date_start", text=self.lang.get('fct_date_start', "Data Avvio"))
        self.tree.column("date_start", width=150)
        self.tree.heading("bat_program", text=self.lang.get('fct_bat_program', "Programma"))
        self.tree.column("bat_program", width=280)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Popola lista
        for inst in self.instances:
            date_str = inst['DateStart'].strftime("%Y-%m-%d %H:%M:%S") if inst['DateStart'] else ""
            self.tree.insert("", "end", values=("☐", date_str, inst['BatProgram']), tags=("unchecked",))

        self.tree.bind("<Button-1>", self._on_click)

        # Checkbox "Seleziona tutto"
        self.select_all_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            main_frame,
            text=self.lang.get('fct_select_all', "Seleziona tutto"),
            variable=self.select_all_var,
            command=self._toggle_select_all
        ).pack(anchor="w", pady=(10, 0))

        # Pulsanti
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(15, 0))

        ttk.Button(
            btn_frame,
            text=self.lang.get('fct_stop_selected', "Ferma Selezionate"),
            command=self._confirm_stop
        ).pack(side="right", padx=(10, 0))

        ttk.Button(
            btn_frame,
            text=self.lang.get('button_cancel', "Annulla"),
            command=self.destroy
        ).pack(side="right")

    def _on_click(self, event):
        """Gestisce click su riga per toggle checkbox"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            if item:
                tags = self.tree.item(item, "tags")
                if "checked" in tags:
                    self.tree.item(item, values=("☐",) + self.tree.item(item, "values")[1:], tags=("unchecked",))
                else:
                    self.tree.item(item, values=("☑",) + self.tree.item(item, "values")[1:], tags=("checked",))

    def _toggle_select_all(self):
        """Seleziona/deseleziona tutte le istanze"""
        check_all = self.select_all_var.get()
        for item in self.tree.get_children():
            if check_all:
                self.tree.item(item, values=("☑",) + self.tree.item(item, "values")[1:], tags=("checked",))
            else:
                self.tree.item(item, values=("☐",) + self.tree.item(item, "values")[1:], tags=("unchecked",))

    def _confirm_stop(self):
        """Conferma e restituisce istanze selezionate"""
        self.selected_instances = []
        for i, item in enumerate(self.tree.get_children()):
            tags = self.tree.item(item, "tags")
            if "checked" in tags:
                self.selected_instances.append(self.instances[i])

        if not self.selected_instances:
            messagebox.showwarning(
                self.lang.get('warning', "Attenzione"),
                self.lang.get('fct_no_selection', "Selezionare almeno un'istanza"),
                parent=self
            )
            return

        self.destroy()
