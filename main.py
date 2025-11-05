#import configparser
# --- StdIO safeguard + Faulthandler sicuro per exe windowed ---
import shutil
import sys, os, atexit
from pathlib import Path
import sys
import os

if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')
_STDOUT_FILE = None
_STDERR_FILE = None


try:
    base = Path(os.getenv("LOCALAPPDATA", ".")) / "TraceabilityRS" / "logs"
    base.mkdir(parents=True, exist_ok=True)

    if getattr(sys, "stdout", None) is None:
        _STDOUT_FILE = open(base / "stdout.log", "w", buffering=1, encoding="utf-8")
        sys.stdout = _STDOUT_FILE

    if getattr(sys, "stderr", None) is None:
        _STDERR_FILE = open(base / "stderr.log", "w", buffering=1, encoding="utf-8")
        sys.stderr = _STDERR_FILE
except Exception:
    pass

@atexit.register
def _close_stdio_files():
    for f in (_STDOUT_FILE, _STDERR_FILE):
        try:
            if f: f.close()
        except Exception:
            pass

# Faulthandler: opzionale e sicuro (usa un file dedicato)
try:
    import faulthandler
    if os.getenv("ENABLE_FAULTHANDLER", "0") == "1":
        _FH = open(base / "faulthandler.log", "w", buffering=1, encoding="utf-8")
        faulthandler.enable(file=_FH)
        t = int(os.getenv("FH_DUMP_TIMEOUT", "0"))
        if t > 0:
            faulthandler.dump_traceback_later(t, repeat=True, file=_FH)

        @atexit.register
        def _close_fh():
            try:
                _FH.close()
            except Exception:
                pass
except Exception:
    pass

# --- Logging robusto (file + console solo se esiste) ---
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(debug: bool = False,
                  log_dir: str | None = None,
                  logfile_name: str = "traceability_rs.log",
                  logger_name: str = "TraceabilityRS") -> str:
    root_logger = logging.getLogger()
    if root_logger.handlers:
        # già configurato
        for h in root_logger.handlers:
            if hasattr(h, "baseFilename"):
                return h.baseFilename
        return ""

    level = logging.DEBUG if debug or os.getenv("TRACE_RS_DEBUG") == "1" else logging.INFO
    root_logger.setLevel(level)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s", "%Y-%m-%d %H:%M:%S")

    if not log_dir:
        log_dir = os.path.join(os.getenv("LOCALAPPDATA", "."), "TraceabilityRS", "logs")
    os.makedirs(log_dir, exist_ok=True)
    file_path = os.path.join(log_dir, logfile_name)

    fh = RotatingFileHandler(file_path, maxBytes=5*1024*1024, backupCount=5, encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(fmt)
    root_logger.addHandler(fh)

    if getattr(sys, "stdout", None):
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(fmt)
        root_logger.addHandler(ch)

    app_logger = logging.getLogger(logger_name)
    app_logger.setLevel(level)
    app_logger.debug("Logging inizializzato. Livello=%s, file=%s", logging.getLevelName(level), file_path)
    return file_path

LOG_FILE_PATH = setup_logging(debug=False, logger_name="TraceabilityRS")
logger = logging.getLogger("TraceabilityRS")
logger.info("Logging avviato. File: %s", LOG_FILE_PATH)

import re
import subprocess
import atexit
import tkinter as tk
from collections import defaultdict
from datetime import datetime, timedelta
from tkinter import ttk, messagebox, filedialog
import random
import pyodbc
from PIL import ImageOps, ImageDraw, ImageFont
from packaging import version
from tkcalendar import DateEntry
import pandas as pd
import general_docs_gui
import maintenance_gui
import materials_gui
import operations_gui
import permissions_gui
import submissions_gui
import tools_gui
from traceability import TraceabilityManager
import logging.handlers
from calibration_gui import CalibrationsWindow
import fct_transfer
import collections.abc
import scarti_gui
import scrap_reports_gui
import coating_gui
import product_checks_gui
import tempfile
import assign_submissions_gui
import utils
import submissions_management_gui
import logging
import logging.config
from pathlib import Path
from logging.handlers import RotatingFileHandler
import json, socket
import threading
import time
import scrap_validation_gui

def _detect_log_file_path(logger_name: str) -> str:
    """
    Ritorna il percorso del primo FileHandler/RotatingFileHandler trovato
    sul logger specificato o, in fallback, sul root logger.
    """
    def _first_file_handler_path(lg: logging.Logger) -> str:
        for h in lg.handlers:
            if hasattr(h, "baseFilename"):
                try:
                    return str(Path(h.baseFilename).resolve())
                except Exception:
                    return str(h.baseFilename)
        return ""

    lg_app = logging.getLogger(logger_name)
    p = _first_file_handler_path(lg_app)
    if p:
        return p
    return _first_file_handler_path(logging.getLogger())


def setup_logging(debug: bool = False,
                  log_dir: str | None = None,
                  logfile_name: str = "traceability_rs.log",
                  logger_name: str = "TraceabilityRS") -> str:
    """
    Inizializza il logging:
    - File rotante in %LOCALAPPDATA%\\TraceabilityRS\\logs di default.
    - Console handler solo se sys.stdout esiste (in exe windowed è None).
    Evita duplicazioni se già configurato. Ritorna il path del file di log.
    """
    root_logger = logging.getLogger()

    # Se già configurato, non duplicare; prova a restituire il file esistente
    if root_logger.handlers:
        existing = _detect_log_file_path(logger_name)
        if existing:
            return existing
        # se non troviamo un file handler, proseguiamo a configurarne uno

    level = logging.DEBUG if debug or os.getenv("TRACE_RS_DEBUG") == "1" else logging.INFO
    root_logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler
    if not log_dir:
        log_dir = os.path.join(os.getenv("LOCALAPPDATA", "."), "TraceabilityRS", "logs")
    os.makedirs(log_dir, exist_ok=True)
    file_path = os.path.join(log_dir, logfile_name)

    fh = RotatingFileHandler(file_path, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(formatter)
    root_logger.addHandler(fh)

    # Console handler (solo se c’è stdout)
    stdout = getattr(sys, "stdout", None)
    if stdout:
        ch = logging.StreamHandler(stdout)
        ch.setLevel(level)
        ch.setFormatter(formatter)
        root_logger.addHandler(ch)

    # Imposta anche il logger applicativo al livello scelto
    app_logger = logging.getLogger(logger_name)
    app_logger.setLevel(level)
    app_logger.debug("Logging inizializzato. Livello=%s, file=%s",
                     logging.getLevelName(level), file_path)

    return str(Path(file_path).resolve())



# Esempio di utilizzo all’avvio (main.py):
LOG_FILE_PATH = setup_logging(debug=False, logger_name="TraceabilityRS")
logger = logging.getLogger("TraceabilityRS")
logger.info("Logging avviato. File: %s", LOG_FILE_PATH)

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# --- CONFIGURAZIONE APPLICAZIONE ---
APP_VERSION = "1.8.4"  # Versione aggiornata
APP_DEVELOPER = "Gianluca Testa"

# # --- CONFIGURAZIONE DATABASE ---
DB_DRIVER = '{SQL Server Native Client 11.0}'
DB_SERVER = 'roghipsql01.vandewiele.local\\emsreset'
DB_DATABASE = 'Traceability_rs'
DB_UID = 'emsreset'
DB_PWD = 'E6QhqKUxHFXTbkB7eA8c9ya'
DB_CONN_STR = (f'DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_DATABASE};'
               f'UID={DB_UID};PWD={DB_PWD};MARS_Connection=Yes;TrustServerCertificate=Yes')


def is_update_needed(current_ver_str, db_ver_str):
    """Confronta due stringhe di versione (es. '1.4.0') in modo sicuro."""
    try:
        return version.parse(db_ver_str) > version.parse(current_ver_str)
    except Exception:
        # Fallback a un confronto di stringhe semplice in caso di errore
        return db_ver_str > current_ver_str

def fetch_working_areas(self):
    """Recupera le Aree di Lavoro principali."""
    query = "SELECT [WorkingAreaID], [AreaName] FROM [ResetServices].[BreakDown].[WorkingAreas] ORDER BY AreaName;"
    try:
        self.cursor.execute(query)
        return self.cursor.fetchall()
    except pyodbc.Error as e:
        self.last_error_details = str(e); return []

def fetch_working_sub_areas(self, working_area_id):
    """Recupera le Sotto-Aree in base all'Area di Lavoro selezionata."""
    query = """
        SELECT [WorkingSubAreaID], [AreaSubName] 
        FROM [ResetServices].[BreakDown].[WorkingSubAreas]
        WHERE [WorkingAreaID] = ? ORDER BY AreaSubName;
    """
    try:
        self.cursor.execute(query, working_area_id)
        return self.cursor.fetchall()
    except pyodbc.Error as e:
        self.last_error_details = str(e); return []

def fetch_working_lines(self, working_area_id, sub_area_id):
    """Recupera le Linee in base all'Area e Sotto-Area selezionate."""
    query = """
        SELECT DISTINCT wl.WorkingLineID, WL.WorkingLineName 
        FROM [ResetServices].[BreakDown].[WorkingAreas] AS WA 
        INNER JOIN [ResetServices].[BreakDown].WorkingSubAreas WSA ON WA.WorkingAreaID = WSA.WorkingAreaID 
        INNER JOIN [ResetServices].[BreakDown].WorkingLines AS WL ON WSA.WorkingSubAreaID = WL.WorkingSubAreaID 
        WHERE WA.WorkingAreaID = ? AND WSA.workingsubareaid = ? 
        ORDER BY wl.WorkingLineName;
    """
    try:
        self.cursor.execute(query, working_area_id, sub_area_id)
        return self.cursor.fetchall()
    except pyodbc.Error as e:
        self.last_error_details = str(e); return []

def fetch_production_orders_for_breakdown(self):
    """Recupera gli ordini di produzione per la selezione."""
    query = """
        SELECT o.IdOrdine, o.po + ' [' + pf.epiccode +']' as OrderNumber
        FROM ResetServices.dbo.tbordini o 
        INNER JOIN Resetservices.dbo.tbsubordine so on o.IdOrdine=so.IdOrdine 
        INNER JOIN Resetservices.dbo.tbprodfin pf on so.idpf=pf.idpf 
        INNER JOIN resetservices.dbo.TbRegistro r on o.idregistro=r.contatore and r.idregistro in (21, 26)
        LEFT JOIN resetservices.dbo.TbFattStory fs on fs.IdPoSub=so.IdOrdStori
        LEFT JOIN resetservices.dbo.TbProdFinStuff Micro on micro.Idpf=so.idpf 
        WHERE year(o.dataord) >= 2025 and micro.idpf is null
        GROUP BY o.idordine, o.po + ' [' + pf.epiccode +']', so.QtaStory, o.dataord, so.DataDeliSubOrdine
        HAVING so.QtaStory > isnull(sum(fs.QtaFaturata) ,0)
        ORDER BY o.dataord DESC;
    """
    try:
        self.cursor.execute(query)
        return self.cursor.fetchall()
    except pyodbc.Error as e:
        self.last_error_details = str(e); return []

def fetch_issue_areas(self):
    """Recupera le aree problematiche (es. Meccanica, Elettrica)."""
    query = "SELECT [IssueAreaId], [IssueArea] FROM [ResetServices].[BreakDown].[IssuesAreas] ORDER BY [IssueArea];"
    try:
        self.cursor.execute(query)
        return self.cursor.fetchall()
    except pyodbc.Error as e:
        self.last_error_details = str(e); return []

class KanbanRulesManagementForm(tk.Toplevel):
    def __init__(self, master, db_handler, lang_manager):
        super().__init__(master)
        self.db = db_handler
        self.lang = lang_manager

        self.title(self.lang.get('rules_mgmt_title', "KanBan - Gestione regole"))
        self.geometry("640x460")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        # Stato form
        self._current_rule_id = None
        self.rule_type_var = tk.StringVar(value="percent")  # 'percent' | 'qty'
        self.rule_value_var = tk.StringVar()

        self._logo_imgtk = None

        self._build_ui()
        self._load_rules()

    def _build_ui(self):
        root = ttk.Frame(self, padding=12)
        root.pack(fill="both", expand=True)

        # Lista regole
        list_frame = ttk.Labelframe(root, text=self.lang.get('rules_list', "Regole"))
        list_frame.pack(fill="both", expand=True)

        cols = ("id", "type", "value", "status", "dateout")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=60, anchor="center")
        self.tree.heading("type", text=self.lang.get('rule_type', "Tipo"))
        self.tree.column("type", width=140)
        self.tree.heading("value", text=self.lang.get('rule_value', "Valore"))
        self.tree.column("value", width=100, anchor="e")
        self.tree.heading("status", text=self.lang.get('rule_status', "Stato"))
        self.tree.column("status", width=100)
        self.tree.heading("dateout", text="DateOut")
        self.tree.column("dateout", width=140)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # Editor regola
        edit = ttk.Labelframe(root, text=self.lang.get('rule_editor', "Editor regola"))
        edit.pack(fill="x", pady=(10, 0))

        r1 = ttk.Frame(edit); r1.pack(fill="x", padx=8, pady=6)
        ttk.Label(r1, text=self.lang.get('rule_type', "Tipo")).pack(side="left")

        ttk.Radiobutton(r1, text=self.lang.get('rule_percent', "Percentuale"), value="percent",
                        variable=self.rule_type_var).pack(side="left", padx=(8, 8))
        ttk.Radiobutton(r1, text=self.lang.get('rule_quantity', "Quantità"), value="qty",
                        variable=self.rule_type_var).pack(side="left", padx=(0, 8))

        r2 = ttk.Frame(edit); r2.pack(fill="x", padx=8, pady=6)
        ttk.Label(r2, text=self.lang.get('rule_value', "Valore")).pack(side="left")
        self.value_entry = ttk.Entry(r2, textvariable=self.rule_value_var, width=12)
        self.value_entry.pack(side="left", padx=(8, 8))
        ttk.Label(r2, text=self.lang.get('rule_value_hint', "(% intero 1..100 o quantità > 0)")).pack(side="left")

        # Pulsanti azione
        btns = ttk.Frame(root); btns.pack(fill="x", pady=(10, 0))
        ttk.Button(btns, text=self.lang.get('button_new', "Nuova"), command=self._on_new).pack(side="left")
        ttk.Button(btns, text=self.lang.get('button_save', "Salva"), command=self._on_save).pack(side="left", padx=(8,0))
        ttk.Button(btns, text=self.lang.get('button_delete', "Elimina"), command=self._on_delete).pack(side="left", padx=(8,0))
        ttk.Button(btns, text=self.lang.get('button_clear', "Pulisci"), command=self._on_clear).pack(side="left", padx=(8,0))

        # Logo in basso a destra
        bottom = ttk.Frame(root); bottom.pack(fill="both", expand=True)
        self.logo_lbl = ttk.Label(bottom)
        self.logo_lbl.pack(side="right", anchor="se", padx=4, pady=4)
        self._load_logo()

    def _load_logo(self):
        try:
            if os.path.exists("logo.png"):
                img = Image.open("logo.png")
                img.thumbnail((160, 80))
                self._logo_imgtk = ImageTk.PhotoImage(img)
                self.logo_lbl.configure(image=self._logo_imgtk)
        except Exception:
            pass

    def _load_rules(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        rows = self.db.fetch_all_kanban_rules()
        for r in rows:
            is_pct = getattr(r, "MinimumProcent", None) is not None
            value = int(getattr(r, "MinimumProcent", 0) if is_pct else getattr(r, "MinimumQty", 0))
            type_txt = self.lang.get('rule_percent', "Percentuale") if is_pct else self.lang.get('rule_quantity', "Quantità")
            status_txt = self.lang.get('rule_status_active', "Attiva") if getattr(r, "DateOut", None) is None else self.lang.get('rule_status_closed', "Chiusa")
            dateout_txt = "" if getattr(r, "DateOut", None) is None else str(getattr(r, "DateOut"))
            self.tree.insert("", "end", iid=str(r.KanBanRuleID),
                             values=(r.KanBanRuleID, type_txt, value, status_txt, dateout_txt))

    def _on_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        rid = int(sel[0])
        # recupera record dalla lista corrente
        rows = self.db.fetch_all_kanban_rules()
        the = next((x for x in rows if x.KanBanRuleID == rid), None)
        if not the:
            return
        self._current_rule_id = rid
        is_pct = getattr(the, "MinimumProcent", None) is not None
        self.rule_type_var.set("percent" if is_pct else "qty")
        val = int(getattr(the, "MinimumProcent", 0) if is_pct else getattr(the, "MinimumQty", 0))
        self.rule_value_var.set(str(val))

    def _validate(self):
        typ = self.rule_type_var.get()
        sval = self.rule_value_var.get().strip()
        if not sval.isdigit():
            return False, self.lang.get('rules_err_numeric', "Inserire un numero intero positivo.")
        n = int(sval)
        if typ == "percent":
            if n < 1 or n > 100:
                return False, self.lang.get('rules_err_percent_range', "La percentuale deve essere tra 1 e 100.")
            return True, ("percent", n)
        else:
            if n <= 0:
                return False, self.lang.get('rules_err_qty_positive', "La quantità deve essere > 0.")
            return True, ("qty", n)

    def _on_new(self):
        self._current_rule_id = None
        self.rule_type_var.set("percent")
        self.rule_value_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def _on_clear(self):
        self._on_new()

    def _on_save(self):
        ok, res = self._validate()
        if not ok:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"), res, parent=self)
            return
        typ, val = res
        min_pct = val if typ == "percent" else None
        min_qty = val if typ == "qty" else None

        if self._current_rule_id is None:
            ok, err = self.db.add_kanban_rule(min_pct, min_qty)
        else:
            ok, err = self.db.update_kanban_rule(self._current_rule_id, min_pct, min_qty)

        if ok:
            messagebox.showinfo(self.lang.get('info_title', "Informazione"), self.lang.get('rules_saved', "Regola salvata."), parent=self)
            self._load_rules()
            if self._current_rule_id is None:
                self._on_new()
        else:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('rules_save_err', f"Errore salvataggio: {err or self.db.last_error_details}"),
                                 parent=self)

    def _on_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"), self.lang.get('rules_select_row', "Seleziona una regola."), parent=self)
            return
        rid = int(sel[0])
        if not messagebox.askyesno(self.lang.get('confirm_title', "Conferma"),
                                   self.lang.get('confirm_delete_rule', "Eliminare (chiudere) la regola selezionata?"),
                                   parent=self):
            return
        ok, err = self.db.soft_delete_kanban_rule(rid)
        if ok:
            messagebox.showinfo(self.lang.get('info_title', "Informazione"), self.lang.get('rules_deleted', "Regola eliminata."), parent=self)
            self._load_rules()
            self._on_new()
        else:
            # già chiusa o altro errore
            msg = self.lang.get('rules_already_closed', "La regola è già chiusa o non esiste.") if err == "already_closed_or_not_found" else (err or self.db.last_error_details)
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('rules_delete_err', f"Errore eliminazione: {msg}"),
                                 parent=self)

class LanguageManager:
    """Gestisce le traduzioni e la lingua corrente dell'applicazione."""

    def __init__(self, db_handler):
        self.db = db_handler
        self.translations = defaultdict(dict)
        self.current_language = 'it'  # Lingua predefinita
        self.load_translations()

    def load_translations(self):
        """Carica le traduzioni dal database."""
        records = self.db.fetch_translations()
        if not records:
            # Usiamo print inizialmente, messagebox potrebbe non essere disponibile se la GUI principale fallisce
            print("Traduzioni Mancanti: Nessuna traduzione trovata nel database. Verrà usato il testo di default.")
            return
        for lang_code, key, value in records:
            self.translations[lang_code.lower()][key] = value

    def get(self, key, *args):
        """Restituisce la traduzione per una data chiave nella lingua corrente."""
        translated_text = self.translations[self.current_language].get(key, key)
        if args:
            try:
                return translated_text.format(*args)
            except (IndexError, KeyError):
                return translated_text
        return translated_text

    def get_raw(self, key):
        """Restituisce il template di traduzione senza formattazione."""
        return self.translations[self.current_language].get(key, key)

    def set_language(self, lang_code):
        """Imposta la lingua corrente."""
        self.current_language = lang_code.lower()

class Database:
    """Gestisce la connessione e le operazioni sul database."""

    def fetch_products_for_checks(self):
        """Recupera prodotti per combo gestione verifiche"""
        query = """
                SELECT p.IDProduct, ProductCode, ProductName
                FROM traceability_rs.dbo.products AS P
                         LEFT JOIN traceability_rs.dbo.PeriodicalProductChecks AS PC
                                   ON p.idproduct = pc.idproduct AND pc.datestop IS NULL
                WHERE CHARINDEX('MICR', ProductName, 1) = 0
                ORDER BY ProductCode; \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    #moduli di ricerca sql di scrap_validation_gui
    def fetch_scrap_declarations_pending(self):
        """Recupera le dichiarazioni di scrap in attesa di validazione"""
        query = """
                SELECT s.ScrapDeclarationId
                     , S.[User] as DECLAREDBY
                     , l.labelcod
                     , A.AreaName
                     , a.IDArea
                     , [Riferiments]
                     , d.IDDefect
                     , d.DefectNameRO as Defect
                     , [Picture]
                FROM [Traceability_RS].[dbo].ScarpDeclarations S
                    INNER JOIN Traceability_RS.dbo.LabelCodes L
                ON l.IDLabelCode=s.IdLabelCode
                    INNER JOIN [Traceability_RS].dbo.Areas A ON a.IDArea=s.IDParentPhase
                    INNER JOIN [Traceability_RS].dbo.defects D ON d.IDDefect=s.ScrapReasonId
                WHERE NOT s.ScrapDeclarationId IN (
                    SELECT sd.ScrapDeclarationId
                    FROM Scannings s
                    INNER JOIN Boards B ON b.idboard=s.IDBoard
                    INNER JOIN LabelCodes L ON l.IDBoard=b.IDBoard
                    INNER JOIN ScarpDeclarations sd ON sd.IdLabelCode=l.IDLabelCode
                    WHERE b.BoardState=4
                    )
                ORDER BY S.DateIn
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            logger.error(f"Errore fetch dichiarazioni scrap: {e}")
            return []

    def fetch_scrap_declaration_by_id(self, declaration_id):
        """Recupera una singola dichiarazione di scrap per ID"""
        query = """
                SELECT sd.ScrapDeclarationId, \
                       sd.DeclarationDate, \
                       sd.ProductionOrderId, \
                       po.OrderNumber, \
                       p.ProductCode, \
                       p.ProductName, \
                       sd.ScrapQuantity, \
                       sd.ScrapReasonId, \
                       sr.ReasonDescription, \
                       sd.Notes, \
                       sd.ValidationStatus, \
                       sd.ValidationDate, \
                       sd.ValidatorNotes, \
                       e.EmployeeName + ' ' + e.EmployeeSurname AS DeclaredBy
                FROM [Traceability_RS].[dbo].[ScarpDeclarations] sd
                    INNER JOIN [Traceability_RS].[dbo].[Orders] po
                ON sd.ProductionOrderId = po.ProductionOrderId
                    INNER JOIN [Traceability_RS].[dbo].[Products] p
                    ON po.ProductId = p.IDProduct
                    INNER JOIN [Traceability_RS].[dbo].[ScrapReasons] sr
                    ON sd.ScrapReasonId = sr.ScrapReasonId
                    INNER JOIN [Employee].[dbo].[EmployeeHireHistory] h
                    ON sd.EmployeeHireHistoryId = h.EmployeeHireHistoryId
                    INNER JOIN [Employee].[dbo].[Employees] e
                    ON h.EmployeeId = e.EmployeeId
                WHERE sd.ScrapDeclarationId = ?; \
                """
        try:
            self.cursor.execute(query, (declaration_id,))
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            logger.error(f"Errore fetch dichiarazione scrap {declaration_id}: {e}")
            return None

    def validate_scrap_declaration(self, declaration_id, validation_status, validator_notes, validator_name):
        """Valida o rifiuta una dichiarazione di scrap"""
        query = """
                UPDATE [Traceability_RS].[dbo].[ScarpDeclarations]
                SET ValidationStatus = ?, ValidationDate = GETDATE(), ValidatorNotes = ?, ValidatedBy = ?
                WHERE ScrapDeclarationId = ?; \
                """
        try:
            self.cursor.execute(query, (validation_status, validator_notes, validator_name, declaration_id))
            self.conn.commit()
            logger.info(f"Dichiarazione scrap {declaration_id} validata: {validation_status}")
            return True, None
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            logger.error(f"Errore validazione dichiarazione scrap {declaration_id}: {e}")
            return False, str(e)

    def fetch_scrap_reasons(self):
        """Recupera le causali di scarto"""
        query = """
                SELECT ScrapReasonId, ReasonCode, ReasonDescription
                FROM [Traceability_RS].[dbo].[ScrapReasons]
                WHERE DateStop IS NULL
                ORDER BY ReasonCode; \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            logger.error(f"Errore fetch causali scrap: {e}")
            return []


    def fetch_all_product_checks(self):
        """Recupera tutte le verifiche configurate"""
        query = """
                SELECT pc.PeriodicalProductCheckId, \
                       pc.IdProduct, \
                       pc.PeriodicityInQty,
                       p.ProductCode, \
                       p.ProductName
                FROM [Traceability_RS].[dbo].[PeriodicalProductChecks] pc
                    INNER JOIN dbo.products p \
                ON p.IDProduct = pc.IdProduct
                WHERE pc.datestop IS NULL
                ORDER BY p.ProductCode; \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def insert_product_check(self, product_id, periodicity):
        """Inserisce una nuova verifica prodotto"""
        query = """
                INSERT INTO [Traceability_RS].[dbo].[PeriodicalProductChecks]
                    (IdProduct, PeriodicityInQty)
                VALUES (?, ?); \
                """
        try:
            self.cursor.execute(query, product_id, periodicity)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False

    def update_product_check(self, check_id, product_id, periodicity):
        """Aggiorna una verifica prodotto"""
        query = """
                UPDATE [Traceability_RS].[dbo].[PeriodicalProductChecks]
                SET IdProduct = ?, PeriodicityInQty = ?
                WHERE PeriodicalProductCheckId = ?; \
                """
        try:
            self.cursor.execute(query, product_id, periodicity, check_id)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False

    def delete_product_check(self, check_id):
        """Elimina (soft delete) una verifica prodotto"""
        query = """
                UPDATE [Traceability_RS].[dbo].[PeriodicalProductChecks]
                SET datestop = GETDATE()
                WHERE PeriodicalProductCheckId = ?; \
                """
        try:
            self.cursor.execute(query, check_id)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False

    def fetch_products_with_checks(self):
        """Recupera prodotti con verifiche configurate"""
        query = """
                SELECT pc.PeriodicalProductCheckId, p.ProductCode, p.ProductName
                FROM [Traceability_RS].[dbo].[PeriodicalProductChecks] pc
                    INNER JOIN dbo.products p \
                ON p.IDProduct = pc.IdProduct
                WHERE pc.datestop IS NULL
                ORDER BY p.ProductCode; \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_all_check_tasks(self):
        """Recupera tutti i task di verifica"""
        query = """
                SELECT ppl.PriodicalProductCheckListId, \
                       ppl.ItemToCheck, \
                       ppl.IsGeneric,
                       ppl.UserType, \
                       ppl.Doc, \
                       ppl.DateIn,
                       p.ProductCode, \
                       p.ProductName
                FROM [Traceability_RS].[dbo].[PeriodicalProductCheckLists] ppl
                    LEFT JOIN [Traceability_RS].[dbo].[PeriodicProductCheckListSpecifics] ps
                ON ps.PriodicalProductCheckListId = ppl.PriodicalProductCheckListId
                    AND ps.dateout IS NULL
                    LEFT JOIN [Traceability_RS].[dbo].[PeriodicalProductChecks] pc
                    ON pc.PeriodicalProductCheckId = ps.PeriodicalProductCheckId
                    LEFT JOIN dbo.products p ON p.IDProduct = pc.IdProduct
                WHERE ppl.dateout IS NULL
                ORDER BY ppl.IsGeneric DESC, p.ProductCode, ppl.DateIn DESC; \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_check_task_by_id(self, task_id):
        """Recupera un task specifico per ID"""
        query = """
                SELECT ppl.PriodicalProductCheckListId, \
                       ppl.ItemToCheck, \
                       ppl.IsGeneric,
                       ppl.UserType, \
                       ppl.Doc, \
                       ppl.DateIn,
                       p.ProductCode, \
                       p.ProductName
                FROM [Traceability_RS].[dbo].[PeriodicalProductCheckLists] ppl
                    LEFT JOIN [Traceability_RS].[dbo].[PeriodicProductCheckListSpecifics] ps
                ON ps.PriodicalProductCheckListId = ppl.PriodicalProductCheckListId
                    LEFT JOIN [Traceability_RS].[dbo].[PeriodicalProductChecks] pc
                    ON pc.PeriodicalProductCheckId = ps.PeriodicalProductCheckId
                    LEFT JOIN dbo.products p ON p.IDProduct = pc.IdProduct
                WHERE ppl.PriodicalProductCheckListId = ?; \
                """
        try:
            self.cursor.execute(query, task_id)
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return None

    def insert_check_task(self, item_to_check, is_generic, user_type, doc_data, product_check_id=None):
        """Inserisce un nuovo task di verifica"""
        try:
            self.conn.autocommit = False

            # Inserisci in PeriodicalProductCheckLists
            query1 = """
                     SET NOCOUNT ON;
                     INSERT INTO [Traceability_RS].[dbo].[PeriodicalProductCheckLists]
                         (ItemToCheck, IsGeneric, UserType, Doc, DateIn)
                     VALUES (?, ?, ?, ?, GETDATE());
                     SELECT CAST(SCOPE_IDENTITY() AS INT) AS NewID;
                     """
            self.cursor.execute(query1, item_to_check, 1 if is_generic else 0, user_type, doc_data)
            result = self.cursor.fetchone()

            if not result:
                raise Exception("Impossibile recuperare l'ID del task inserito")

            task_id = result[0]

            # Se non è generico, inserisci anche in PeriodicProductCheckListSpecifics
            if not is_generic and product_check_id:
                query2 = """
                         INSERT INTO [Traceability_RS].[dbo].[PeriodicProductCheckListSpecifics]
                             (PeriodicalProductCheckId, PriodicalProductCheckListId)
                         VALUES (?, ?);
                         """
                self.cursor.execute(query2, product_check_id, task_id)

            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            print(f"❌ Errore insert_check_task: {e}")
            return False
        finally:
            self.conn.autocommit = True

    def delete_check_task(self, task_id):
        """Elimina (soft delete) un task di verifica"""
        try:
            self.conn.autocommit = False

            # Soft delete in PeriodicalProductCheckLists
            query1 = """
                     UPDATE [Traceability_RS].[dbo].[PeriodicalProductCheckLists]
                     SET dateout = GETDATE()
                     WHERE PriodicalProductCheckListId = ?; \
                     """
            self.cursor.execute(query1, task_id)

            # Soft delete anche in PeriodicProductCheckListSpecifics
            query2 = """
                     UPDATE [Traceability_RS].[dbo].[PeriodicProductCheckListSpecifics]
                     SET dateout = GETDATE()
                     WHERE PriodicalProductCheckListId = ? AND dateout IS NULL; \
                     """
            self.cursor.execute(query2, task_id)

            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False
        finally:
            self.conn.autocommit = True

    def check_label_code_exists(self, label_code, must_check_id):
        """Verifica se il label code esiste ed è relativo all'ordine selezionato e restituisce l'IDLabelCode"""
        try:
            query = """
                    SELECT l.IDLabelCode
                    FROM traceability_rs.dbo.orders O
                             INNER JOIN traceability_rs.dbo.boards b ON o.IDOrder = b.IDOrder
                             INNER JOIN traceability_rs.dbo.LabelCodes l ON l.IDBoard = b.IDBoard
                             INNER JOIN traceability_rs.dbo.PeriodicalProductCheckMustLists M ON m.idorder = o.IDOrder
                             INNER JOIN traceability_rs.dbo.products p ON p.idproduct = o.IDProduct
                    WHERE l.LabelCod = ?
                      AND m.PeriodicalProductCheckMustListId = ?; \
                    """

            self.cursor.execute(query, label_code, must_check_id)
            result = self.cursor.fetchone()

            if result:
                return result.IDLabelCode  # Restituisce l'IDLabelCode se trovato
            else:
                return None  # Restituisce None se non trovato
        except pyodbc.Error as e:
            logger.error(f"Error checking label code: {e}")
            return None

    def fetch_products_must_check(self):
        """Recupera prodotti che necessitano verifica"""
        query = """
                SELECT M.PeriodicalProductCheckMustListId, \
                       o.ordernumber, \
                       p.productcode, \
                       pa.PhaseName,
                       FORMAT([Date], 'd', 'it-it') AS [Date], [Ora]
                FROM [Traceability_RS].[dbo].[PeriodicalProductCheckMustLists] M
                    INNER JOIN [Traceability_RS].[dbo].Orders O \
                ON M.[IdOrder] = o.idorder
                    INNER JOIN [Traceability_RS].[dbo].products P ON p.idproduct = M.idproduct
                    INNER JOIN traceability_rs.dbo.Phases pa ON pa.IDPhase = m.idphase
                    LEFT JOIN [Traceability_RS].[dbo].PeriodicalProductChecks PP ON PP.IdProduct = M.idproduct
                    LEFT JOIN [Traceability_RS].[dbo].[PeriodicProductCheckListSpecifics] PS
                    ON PS.PeriodicalProductCheckId = pp.PeriodicalProductCheckId
                    LEFT JOIN [Traceability_RS].[dbo].PeriodicalProductCheckLogs L
                    ON l.PeriodicalProductCheckMustListId = m.PeriodicalProductCheckMustListId
                WHERE L.PeriodicalProductCheckMustListId IS NULL
                ORDER BY p.productcode, pa.PhaseName; \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_generic_check_tasks(self):
        """Recupera task generici"""
        query = """
                SELECT ppl.PriodicalProductCheckListId, ppl.ItemToCheck, ppl.Doc
                FROM [Traceability_RS].[dbo].[PeriodicalProductCheckLists] AS ppl
                WHERE isgeneric = 1 AND ppl.dateout IS NULL
                ORDER BY ppl.DateIn; \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_specific_check_tasks(self, must_check_id):
        """Recupera task specifici per un prodotto"""
        # Prima recupera il PeriodicalProductCheckId dal must_check_id
        query1 = """
                 SELECT pp.PeriodicalProductCheckId
                 FROM [Traceability_RS].[dbo].[PeriodicalProductCheckMustLists] M
                     INNER JOIN [Traceability_RS].[dbo].PeriodicalProductChecks PP \
                 ON PP.IdProduct = M.idproduct
                 WHERE M.PeriodicalProductCheckMustListId = ?; \
                 """
        try:
            self.cursor.execute(query1, must_check_id)
            row = self.cursor.fetchone()
            if not row:
                return []

            product_check_id = row.PeriodicalProductCheckId

            # Ora recupera i task specifici
            query2 = """
                     SELECT ppl.PriodicalProductCheckListId, ppl.ItemToCheck, ppl.Doc
                     FROM [Traceability_RS].[dbo].[PeriodicalProductCheckLists] AS ppl
                         INNER JOIN [Traceability_RS].[dbo].[PeriodicProductCheckListSpecifics] AS ps
                     ON ps.PriodicalProductCheckListId = ppl.PriodicalProductCheckListId
                     WHERE isgeneric = 0
                       AND ppl.dateout IS NULL
                       AND ps.dateout IS NULL
                       AND ps.PeriodicalProductCheckId = ?
                     ORDER BY ppl.DateIn; \
                     """
            self.cursor.execute(query2, product_check_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def save_product_verification(self, must_check_id, user_name, label_code_id, status, comments=None):
        """Salva una verifica prodotto completata usando l'IDLabelCode"""
        try:
            self.conn.autocommit = False

            # Inserisci in PeriodicalProductCheckLogs usando IDLabelCode
            query1 = """
                     INSERT INTO [Traceability_RS].[dbo].[PeriodicalProductCheckLogs]
                     (PeriodicalProductCheckMustListId, CheckTime, UserCheck, IDLabelCode, Status, Comments)
                     VALUES (?, GETDATE(), ?, ?, ?, ?);
                     """
            self.cursor.execute(query1, must_check_id, user_name, label_code_id, status, comments)

            # Aggiorna AllertActiveted in PeriodicalProductCheckMustLists
            query2 = """
                     UPDATE [dbo].[PeriodicalProductCheckMustLists]
                     SET AllertActiveted = 0
                     WHERE PeriodicalProductCheckMustListId = ?;
                     """
            self.cursor.execute(query2, must_check_id)

            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            logger.error(f"Error saving product verification: {e}")
            return False
        finally:
            self.conn.autocommit = True


    def execute_product_check_sp(self):
        """Esegue la stored procedure InsertProductToCheck"""
        try:
            self.cursor.execute("{CALL Traceability_rs.dbo.InsertProductToCheck}")
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            logger.error(f"Error executing InsertProductToCheck SP: {e}")
            return False

    def get_product_check_interval(self):
        """Recupera l'intervallo di controllo prodotti (in minuti)"""
        query = """
                SELECT [value]
                FROM traceability_rs.dbo.settings
                WHERE atribute = 'Sys_CheckTimeProduct'; \
                """
        try:
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row and row.value:
                return int(row.value)
            return 30  # Default: 30 minuti
        except (pyodbc.Error, ValueError) as e:
            self.last_error_details = str(e)
            logger.error(f"Error fetching check interval: {e}")
            return 30

    def fetch_assigned_submissions(self, employee_hire_history_id: int):
        """Carica segnalazioni assegnate all'utente"""
        sql = """
              SELECT s.SegnalazioneId, \
                     ts.NomeTipo, \
                     s.Titolo, \
                     s.Descrizione,
                     e.EmployeeName + ' ' + e.EmployeeSurname   as Segnalatore,
                     sst.TipoStato, \
                     e1.EmployeeName + ' ' + e1.EmployeeSurname as Assegnatario,
                     ass.NomeFile, \
                     ass.DatiFile
              FROM employee.dbo.Segnalazioni s
                       INNER JOIN employee.dbo.EmployeeHireHistory h ON s.IdDipendente = h.EmployeeHireHistoryId
                       INNER JOIN employee.dbo.employees e ON h.EmployeeId = e.EmployeeId
                       INNER JOIN employee.dbo.SegnalazioneStati ss ON s.SegnalazioneId = ss.SegnalazioneId
                       INNER JOIN employee.dbo.SegnalazioniTipoStati sst \
                                  ON sst.SegnalazioniTipoStatoId = ss.SegnalazioniTipoStatoId
                       INNER JOIN employee.dbo.TipiSegnalazione ts ON ts.TipoSegnalazioneId = s.TipoSegnalazioneId
                       LEFT JOIN employee.dbo.SegnalazioneAllegati ass ON ass.SegnalazioneId = s.SegnalazioneId
                       INNER JOIN employee.dbo.SegnalazioneAssegnazioni sa ON sa.SegnalazioneId = s.SegnalazioneId
                       INNER JOIN employee.dbo.employeehirehistory h1 \
                                  ON h1.EmployeeHireHistoryId = sa.EmployeeHireHistoryId
                       INNER JOIN employee.dbo.employees e1 ON e1.employeeid = h1.EmployeeId
              WHERE sa.EmployeeHireHistoryId = ?
                AND NOT EXISTS (SELECT 1 \
                                FROM [Employee].[dbo].[SegnalazioneStati] ss2 
            INNER JOIN employee.dbo.segnalazioniTipoStati sst2 
                ON sst2.SegnalazioniTipoStatoId = ss2.SegnalazioniTipoStatoId
            WHERE ss2.SegnalazioneId = s.SegnalazioneId AND sst2.statochiuso = 1)
                AND sst.SegnalazioniTipoStatoId IN (1, 2)
              ORDER BY s.SegnalazioneId, sa.DateSys; \
              """
        try:
            self.cursor.execute(sql, employee_hire_history_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            logger.error(f"Error fetching assigned submissions: {e}")
            return []

    def fetch_submission_activities(self, segnalazione_id: int):
        """Carica attività svolte per una segnalazione"""
        sql = """
              SELECT sv.[SegnalazioneSvolgimentoId], \
                     sa.Note, \
                     sv.[DescrizioneAttivita],
                     sv.[Documentazione], \
                     sv.DateSys as DataAzione
              FROM [Employee].[dbo].[SegnalazioneSvolgimenti] sv
                  INNER JOIN employee.dbo.SegnalazioneAssegnazioni sa
              ON sv.SegnalazioneAssegnazioneId=sa.SegnalazioniAssegnazioniID
                  INNER JOIN employee.dbo.Segnalazioni s ON s.SegnalazioneId=sa.SegnalazioneId
              WHERE s.SegnalazioneId=?
              ORDER BY sv.DateSys DESC; \
              """
        try:
            self.cursor.execute(sql, segnalazione_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            logger.error(f"Error fetching activities: {e}")
            return []

    def fetch_submission_status_types(self):
        """Carica tipi stato per combo"""
        sql = """
              SELECT [SegnalazioniTipoStatoId], [TipoStato], Statochiuso
              FROM [Employee].[dbo].[SegnalazioniTipoStati]
              WHERE SegnalazioniTipoStatoId IN (3, 2, 5, 4)
              ORDER BY [TipoStato]; \
              """
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def insert_submission_activity(self, assegnazione_id: int, descrizione: str):
        """Inserisce nuova attività"""
        sql = """
              INSERT INTO [Employee].[dbo].[SegnalazioneSvolgimenti]
                  ([SegnalazioneAssegnazioneId], [DescrizioneAttivita], [DateSys])
              VALUES (?, ?, GETDATE());
              SELECT SCOPE_IDENTITY(); \
              """
        try:
            self.conn.autocommit = False
            self.cursor.execute(sql, assegnazione_id, descrizione)
            svolgimento_id = int(self.cursor.fetchone()[0])
            self.conn.commit()
            return True, svolgimento_id
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            logger.error(f"Error inserting activity: {e}")
            return False, None
        finally:
            self.conn.autocommit = True

    def insert_activity_attachment(self, svolgimento_id: int, descrizione: str, file_data: bytes):
        """Inserisce allegato per attività"""
        sql = """
              INSERT INTO [Employee].[dbo].[SegnalazioniStatiAllegati]
              ([SegnalazioneSvolgimentoId], [DescrizioneDocumento], [Allegato], [DateIn])
              VALUES (?, ?, ?, GETDATE()); \
              """
        try:
            self.cursor.execute(sql, svolgimento_id, descrizione, file_data)
            self.conn.commit()
            return True, None
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False, str(e)

    def update_submission_status(self, segnalazione_id: int, tipo_stato_id: int,
                                 nota: str, operato_da: str):
        """Aggiorna stato segnalazione"""
        sql = """
              INSERT INTO [Employee].[dbo].[SegnalazioneStati]
              ([SegnalazioneId], [SegnalazioniTipoStatoId], [DataAttivita], [Nota], [OperatoDa])
              VALUES (?, ?, GETDATE(), ?, ?); \
              """
        try:
            self.conn.autocommit = False
            self.cursor.execute(sql, segnalazione_id, tipo_stato_id, nota, operato_da)
            self.conn.commit()
            return True, None
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False, str(e)
        finally:
            self.conn.autocommit = True

    def get_submission_assignment_id(self, segnalazione_id: int, employee_hire_history_id: int):
        """Recupera ID assegnazione per inserire attività"""
        sql = """
              SELECT SegnalazioniAssegnazioniID
              FROM employee.dbo.SegnalazioneAssegnazioni
              WHERE SegnalazioneId = ? \
                AND EmployeeHireHistoryId = ?; \
              """
        try:
            self.cursor.execute(sql, segnalazione_id, employee_hire_history_id)
            row = self.cursor.fetchone()
            return row.SegnalazioniAssegnazioniID if row else None
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return None


    # def fetch_kanban_current_stock_by_component(self) -> dict[int, int]:
    #     """
    #     Ritorna {IdComponent: StockTotale} (DateOut IS NULL).
    #     """
    #     sql = """
    #     SELECT IdComponent, COALESCE(SUM(Quantity),0) AS Stock
    #     FROM knb.KanBanRecords
    #     WHERE DateOut IS NULL
    #     GROUP BY IdComponent;
    #     """
    #     cur = None
    #     try:
    #         cur = self.conn.cursor()
    #         cur.execute(sql)
    #         rows = cur.fetchall()
    #         out = {int(r.IdComponent): int(r.Stock or 0) for r in rows}
    #         return out
    #         #cur.close()
    #     except pyodbc.Error as e:
    #         self.last_error_details = str(e)
    #         logger.error(f"Error in fetch_kanban_current_stock_by_component: {e}")
    #         return {}
    #     finally:
    #         # IMPORTANTE: Chiudi sempre il cursore
    #         if cur:
    #             try:
    #                 cur.close()
    #             except:
    #                 pass

    def fetch_kanban_current_stock_by_component(self) -> dict[int, int]:
        """
        Ritorna {IdComponent: StockTotale} per tutti i record dove DateOut IS NULL.
        """
        sql = """
              SELECT IdComponent, COALESCE(SUM(Quantity), 0) AS Stock
              FROM knb.KanBanRecords
              WHERE DateOut IS NULL
              GROUP BY IdComponent;
              """
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                # Usa indici numerici [0], [1] invece di .IdComponent, .Stock
                out = {int(row[0]): int(row[1]) for row in cur.fetchall()}

            return out

        except pyodbc.Error as e:
            self.last_error_details = str(e)
            logger.error(f"Error in fetch_kanban_current_stock_by_component: {e}")
            return {}


        
    def fetch_active_rules_by_component(self) -> dict[int, dict]:
        """
        Ritorna {IdComponent: {'rule_id':..., 'min_qty':..., 'min_pct':...}}
        per i link attivi (DateOut IS NULL) in knb.KanBanRecodRules.
        """
        sql = """
        SELECT rr.IdComponent, r.KanBanRuleID, r.MinimumQty, r.MinimumProcent
        FROM knb.KanBanRecodRules rr
        INNER JOIN knb.KanBanRules r ON r.KanBanRuleID = rr.KanBanRuleId
        WHERE rr.DateOut IS NULL;
        """
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            out = {}
            for r in rows:
                out[int(r.IdComponent)] = {
                    'rule_id': int(r.KanBanRuleID),
                    'min_qty': (int(r.MinimumQty) if getattr(r, 'MinimumQty', None) is not None else None),
                    'min_pct': (int(r.MinimumProcent) if getattr(r, 'MinimumProcent', None) is not None else None)
                }
            #cur.close()
            return out
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            logger.error(f"Error in fetch_active_rules_by_component: {e}")
            return {}
        finally:
            if cur:
                try:
                    cur.close()
                except:
                    pass

    def fetch_first_load_qty_by_component(self, comp_ids: list[int]) -> dict[int, int]:
        """
        Per i componenti richiesti, ritorna la 'prima quantità' caricata (earliest DateIn con Quantity>0).
        {IdComponent: first_qty}
        """
        if not comp_ids:
            return {}
        # Costruisco una tabella temporanea con i comp_ids per efficienza (in pyodbc uso IN con params)
        placeholders = ",".join("?" for _ in comp_ids)
        sql = f"""
        WITH ranked AS (
          SELECT IdComponent, Quantity,
                 ROW_NUMBER() OVER (PARTITION BY IdComponent ORDER BY DateIn ASC, KanBanRecordId ASC) AS rn
          FROM knb.KanBanRecords
          WHERE Quantity > 0 AND IdComponent IN ({placeholders})
        )
        SELECT IdComponent, Quantity FROM ranked WHERE rn = 1;
        """
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(sql, comp_ids)
            rows = cur.fetchall()
            out = {int(r.IdComponent): int(r.Quantity) for r in rows}
            #cur.close()
            return out
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            logger.error(f"Error in fetch_first_load_qty_by_component: {e}")
            return {}
        finally:
            if cur:
                try:
                    cur.close()
                except:
                    pass

    def fetch_max_single_load_by_component(self, comp_ids: list[int]) -> dict[int, dict]:
        """
        Per i componenti richiesti, ritorna la massima quantità di un singolo carico e la sua KanBanRecordId.
        {IdComponent: {'max_qty': int, 'record_id': int}}
        """
        if not comp_ids:
            return {}
        placeholders = ",".join("?" for _ in comp_ids)
        sql = f"""
        WITH ranked AS (
          SELECT IdComponent, Quantity, KanBanRecordId,
                 ROW_NUMBER() OVER (PARTITION BY IdComponent ORDER BY Quantity DESC, DateIn DESC, KanBanRecordId DESC) AS rn
          FROM knb.KanBanRecords
          WHERE Quantity > 0 AND IdComponent IN ({placeholders})
        )
        SELECT IdComponent, Quantity AS MaxQty, KanBanRecordId
        FROM ranked WHERE rn = 1;
        """
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(sql, comp_ids)
            rows = cur.fetchall()
            out = {int(r.IdComponent): {'max_qty': int(r.MaxQty), 'record_id': int(r.KanBanRecordId)} for r in
               rows}
            #cur.close()
            return out
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            logger.error(f"Error in fetch_max_single_load_by_component: {e}")
            return {}
        finally:
            if cur:
                try:
                    cur.close()
                except:
                    pass


    def fetch_components_master(self, comp_ids: list[int]) -> dict[int, dict]:
        """
        Ritorna {IdComponent: {'code':..., 'desc':...}}
        """
        if not comp_ids:
            return {}
        placeholders = ",".join("?" for _ in comp_ids)
        sql = f"SELECT IdComponent, ComponentCode, ComponentDescription FROM dbo.Components WHERE IdComponent IN ({placeholders});"
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(sql, comp_ids)
            rows = cur.fetchall()
            out = {
                int(r.IdComponent): {'code': r.ComponentCode, 'desc': getattr(r, 'ComponentDescription', '') or ''}
                for r in rows
            }
            return out
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            logger.error(f"Error in fetch_components_master: {e}")
            return {}
        finally:
            if cur:
                try:
                    cur.close()
                except:
                    pass

    def has_refill_request_today(self, kanban_record_id: int) -> bool:
        """
        True se esiste già una richiesta per la stessa KanBanRecordId oggi.
        """
        sql = """
        SELECT 1
        FROM knb.KanBanMaterialRequestes
        WHERE KanBanRecordId = ?
          AND CAST(RequestedOn AS date) = CAST(GETDATE() AS date);
        """
        cur = self.conn.cursor()
        cur.execute(sql, kanban_record_id)
        row = cur.fetchone()
        cur.close()
        return row is not None

    def insert_refill_request(self, kanban_record_id: int, qty_to_refill: int) -> bool:
        """
        Inserisce la richiesta di refill.
        """
        sql = """
        INSERT INTO knb.KanBanMaterialRequestes (KanBanRecordId, QtyToRefill, RequestedOn)
        VALUES (?, ?, GETDATE());
        """
        try:
            cur = self.conn.cursor()
            cur.execute(sql, kanban_record_id, qty_to_refill)
            self.conn.commit()
            cur.close()
            logger.info('Richiesta materiali KanBan, registrata in DB')
            return True
        except Exception as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False

    def get_total_stock_component(self, id_component: int) -> int:
        """
        Stock totale del componente su tutte le locazioni (DateOut IS NULL).
        """
        sql = """
        SELECT COALESCE(SUM(Quantity), 0) AS Qty
        FROM knb.KanBanRecords
        WHERE IdComponent = ? AND DateOut IS NULL;
        """
        self.cursor.execute(sql, id_component)
        row = self.cursor.fetchone()
        return int(row.Qty if row and row.Qty is not None else 0)

    def get_component_locations_with_stock(self, id_component: int) -> dict[int, int]:
        """
        Restituisce {LocationId: Qty} per le locazioni dove il componente ha stock > 0 (DateOut IS NULL).
        """
        sql = """
        SELECT LocationId, SUM(Quantity) AS Qty
        FROM knb.KanBanRecords
        WHERE IdComponent = ? AND DateOut IS NULL
        GROUP BY LocationId
        HAVING SUM(Quantity) > 0;
        """
        self.cursor.execute(sql, id_component)
        return {int(r.LocationId): int(r.Qty or 0) for r in self.cursor.fetchall()}

    def fetch_all_components_for_combo(self):
        """
        Elenco per combo: IdComponent, ComponentCode, ComponentDescription
        """
        sql = """
        SELECT IdComponent, ComponentCode, ComponentDescription
        FROM dbo.Components
        ORDER BY ComponentCode;
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def fetch_all_locations_for_combo(self):
        """
        Elenco per combo: LocationId, LocationCode, KanBanLocation (area)
        """
        sql = """
        SELECT l.LocationId, l.LocationCode, kbl.KanBanLocation
        FROM knb.Locations AS l
        LEFT JOIN knb.KanBanLocations AS kbl ON kbl.KanBanLocationId = l.KanBanLocationId
        ORDER BY kbl.KanBanLocation, l.LocationCode;
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_component_id_by_code(self, component_code: str):
        sql = "SELECT IdComponent FROM dbo.Components WHERE ComponentCode = ?;"
        self.cursor.execute(sql, component_code)
        row = self.cursor.fetchone()
        return row.IdComponent if row else None

    def get_location_id_by_code(self, location_code: str):
        sql = "SELECT LocationId FROM knb.Locations WHERE LocationCode = ?;"
        self.cursor.execute(sql, location_code)
        row = self.cursor.fetchone()
        return row.LocationId if row else None

    def get_current_stock(self, id_component: int, location_id: int) -> int:
        """
        Stock corrente = somma dei movimenti (Quantity) per componente+locazione con DateOut IS NULL.
        """
        sql = """
        SELECT COALESCE(SUM(Quantity), 0) AS Qty
        FROM knb.KanBanRecords
        WHERE IdComponent = ? AND LocationId = ? AND DateOut IS NULL;
        """
        self.cursor.execute(sql, id_component, location_id)
        row = self.cursor.fetchone()
        return int(row.Qty if row and row.Qty is not None else 0)

    def insert_kanban_movement(self, location_id: int, id_component: int, quantity: int, user_name: str | None = None):
        """
        Inserisce un movimento: quantity >0 carico, <0 prelievo.
        DateIn = GETDATE(), DateOut = NULL, [User] = utente che esegue l'operazione.
        """
        if not isinstance(quantity, int) or quantity == 0:
            return False, "invalid_quantity"
        try:
            self.conn.autocommit = False
            sql = """
            INSERT INTO knb.KanBanRecords (LocationId, IdComponent, Quantity, DateIn, DateOut, [User])
            VALUES (?, ?, ?, GETDATE(), NULL, ?);
            """
            self.cursor.execute(sql, location_id, id_component, quantity, user_name)
            self.conn.commit()
            return True, None
        except Exception as e:
            try:
                self.conn.rollback()
            except Exception:
                pass
            self.last_error_details = str(e)
            return False, str(e)
        finally:
            self.conn.autocommit = True

    def fetch_components_locations_report(self):
        """
        Elenca componenti attivi con la loro locazione e area (solo record aperti: DateOut IS NULL).
        Colonne: ComponentCode, ComponentDescription, LocationCode, KanBanLocation
        """
        sql = """
        SELECT c.ComponentCode,
               c.ComponentDescription,
               l.LocationCode,
               kbl.KanBanLocation
        FROM dbo.Components AS c
        INNER JOIN knb.KanBanRecords AS kr ON kr.IdComponent = c.IdComponent
        INNER JOIN knb.Locations     AS l  ON l.LocationId   = kr.LocationId
        INNER JOIN knb.KanBanLocations AS kbl ON kbl.KanBanLocationId = l.KanBanLocationId
        WHERE kr.DateOut IS NULL
        ORDER BY kbl.KanBanLocation, l.LocationCode, c.ComponentCode;
        """
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            self.last_error_details = str(e)
            return []

    def fetch_all_kanban_rules(self):
        """
        Ritorna tutte le regole (attive e chiuse).
        """
        sql = """
        SELECT KanBanRuleID, MinimumProcent, MinimumQty, DateOut
        FROM knb.KanBanRules
        ORDER BY CASE WHEN DateOut IS NULL THEN 0 ELSE 1 END,
                 CASE WHEN MinimumProcent IS NOT NULL THEN 0 ELSE 1 END,
                 MinimumProcent, MinimumQty, KanBanRuleID;
        """
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def add_kanban_rule(self, min_percent: int | None, min_qty: int | None):
        """
        Crea una nuova regola. Esattamente uno tra min_percent e min_qty deve essere valorizzato.
        """
        if (min_percent is None) == (min_qty is None):
            return False, "exactly_one_value_required"
        try:
            self.conn.autocommit = False
            self.cursor.execute(
                "INSERT INTO knb.KanBanRules (MinimumProcent, MinimumQty) VALUES (?, ?);",
                min_percent, min_qty
            )
            self.conn.commit()
            return True, None
        except pyodbc.Error as e:
            try:
                self.conn.rollback()
            except Exception:
                pass
            self.last_error_details = str(e)
            return False, str(e)
        finally:
            self.conn.autocommit = True

    def update_kanban_rule(self, rule_id: int, min_percent: int | None, min_qty: int | None):
        """
        Modifica una regola esistente. Esattamente uno tra min_percent e min_qty deve essere valorizzato.
        Non tocca DateOut.
        """
        if (min_percent is None) == (min_qty is None):
            return False, "exactly_one_value_required"
        try:
            self.conn.autocommit = False
            self.cursor.execute(
                "UPDATE knb.KanBanRules SET MinimumProcent = ?, MinimumQty = ? WHERE KanBanRuleID = ?;",
                min_percent, min_qty, rule_id
            )
            if self.cursor.rowcount == 0:
                self.conn.rollback()
                return False, "not_found"
            self.conn.commit()
            return True, None
        except pyodbc.Error as e:
            try:
                self.conn.rollback()
            except Exception:
                pass
            self.last_error_details = str(e)
            return False, str(e)
        finally:
            self.conn.autocommit = True

    def soft_delete_kanban_rule(self, rule_id: int):
        """
        Cancellazione logica: setta DateOut = GETDATE() se non è già valorizzata.
        """
        try:
            self.conn.autocommit = False
            self.cursor.execute(
                "UPDATE knb.KanBanRules SET DateOut = GETDATE() WHERE KanBanRuleID = ? AND DateOut IS NULL;",
                rule_id
            )
            if self.cursor.rowcount == 0:
                # già chiusa o non trovata
                self.conn.rollback()
                return False, "already_closed_or_not_found"
            self.conn.commit()
            return True, None
        except pyodbc.Error as e:
            try:
                self.conn.rollback()
            except Exception:
                pass
            self.last_error_details = str(e)
            return False, str(e)
        finally:
            self.conn.autocommit = True

    def fetch_component_types(self):
        """
        Select IdComponentType, ComponentTypeName from ComponentTypes order by ComponentTypeName;
        """
        sql = """
        SELECT IdComponentType, ComponentTypeName
        FROM dbo.ComponentTypes
        ORDER BY ComponentTypeName;
        """
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_components(self, component_type_id: int | None = None):
        """
        Carica i componenti (len(componentcode) > 5), opzionalmente filtrati per tipo.
        select idcomponent, c.ComponentCode, ComponentDescription, ct.ComponentTypeName
        from components c
        left join ComponentTypes ct on c.IDComponentType = ct.IDComponentType
        where len(c.componentcode) > 5
          [and c.IDComponentType = ?]
        order by c.componentcode;
        """
        base = """
        SELECT c.IdComponent, c.ComponentCode, c.ComponentDescription, ct.ComponentTypeName
        FROM dbo.Components c
        LEFT JOIN dbo.ComponentTypes ct ON c.IDComponentType = ct.IDComponentType
        WHERE LEN(c.ComponentCode) > 5
        """
        params = []
        if component_type_id:
            base += " AND c.IDComponentType = ?"
            params.append(component_type_id)
        base += " ORDER BY c.ComponentCode;"
        try:
            self.cursor.execute(base, params)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_kanban_rules(self):
        """
        SELECT KanBanRuleID, MinimumProcent, MinimumQty FROM knb.KanBanRules
        Ordina con percentuali prima, poi quantità.
        """
        sql = """
        SELECT KanBanRuleID, MinimumProcent, MinimumQty
        FROM knb.KanBanRules
        ORDER BY CASE WHEN MinimumProcent IS NOT NULL THEN 0 ELSE 1 END,
                 MinimumProcent, MinimumQty;
        """
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_active_rule_for_component(self, id_component: int):
        """
        Ritorna la regola attiva (DateOut IS NULL) per il componente, se presente.
        """
        sql = """
        SELECT TOP 1 KanBanRuleId
        FROM knb.KanBanRecodRules
        WHERE IdComponent = ? AND DateOut IS NULL
        ORDER BY DateIn DESC;
        """
        try:
            self.cursor.execute(sql, id_component)
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return None

    def assign_rule_to_component(self, id_component: int, kanban_rule_id: int | None):
        """
        Associa una regola a un componente:
        - Chiude eventuale regola attiva con DateOut = GETDATE()
        - Se kanban_rule_id è None: solo chiusura (rimozione regola)
        - Altrimenti inserisce un nuovo record con DateIn = GETDATE(), DateOut = NULL

        Usa transazione.
        """
        try:
            self.conn.autocommit = False

            # Chiudi eventuali regole attive
            self.cursor.execute(
                "UPDATE knb.KanBanRecodRules SET DateOut = GETDATE() WHERE IdComponent = ? AND DateOut IS NULL;",
                id_component
            )

            if kanban_rule_id is not None:
                self.cursor.execute(
                    "INSERT INTO knb.KanBanRecodRules (IdComponent, KanBanRuleId, DateIn) VALUES (?, ?, GETDATE());",
                    id_component, kanban_rule_id
                )

            self.conn.commit()
            return True, None
        except pyodbc.Error as e:
            try:
                self.conn.rollback()
            except Exception:
                pass
            self.last_error_details = str(e)
            return False, str(e)
        finally:
            self.conn.autocommit = True

    def _table_has_column(self, schema: str, table: str, column: str) -> bool:
        sql = """
        SELECT 1
        FROM sys.columns
        WHERE object_id = OBJECT_ID(?)
          AND name = ?;
        """
        try:
            self.cursor.execute(sql, f"{schema}.{table}", column)
            return self.cursor.fetchone() is not None
        except pyodbc.Error:
            return False

    def fetch_locations_for_combo(self):
        """
        Ritorna elenco locazioni per combo destinazione.
        Colonne: LocationId, KanBanLocationId, LocationCode, KanBanLocation
        """
        sql = """
        SELECT l.LocationId, k.KanBanLocationId, l.LocationCode, k.KanBanLocation
        FROM knb.Locations l
        INNER JOIN knb.KanBanLocations k ON k.KanBanLocationId = l.KanBanLocationId
        ORDER BY k.KanBanLocation, l.LocationCode;
        """
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def search_component_open_records(self, component_code: str):
        """
        Ricerca componenti attivi (DateOut IS NULL) per codice componente.
        Aggiungo KanBanRecordId per identificare il record da chiudere.
        """
        sql = """
        SELECT k.KanBanRecordId, c.IdComponent, l.LocationId,
               c.ComponentCode, c.ComponentDescription,
               l.LocationCode + ' (' +kl.KanBanLocation +')' as LocationCode, k.Quantity
        FROM dbo.Components AS c
        INNER JOIN knb.KanBanRecords AS k ON c.IdComponent = k.IdComponent
        INNER JOIN knb.Locations     AS l ON k.LocationId  = l.LocationId
        inner join knb.KanBanLocations as KL on l.KanBanLocationId=Kl.KanBanLocationId
        WHERE c.ComponentCode = ? AND k.DateOut IS NULL
        ORDER BY l.LocationCode;
        """
        try:
            self.cursor.execute(sql, component_code)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def move_record_to_location(self, record_id: int, to_location_id: int, to_kanban_location_id: int | None = None):
        """
        Sposta UN record (singolo componente in una specifica locazione) in un'altra locazione.
        - Chiude il record sorgente (DateOut = GETDATE()).
        - Inserisce nuovo record con stessa Quantity/IdComponent in locazione destinazione (DateIn = GETDATE()).
        Se la tabella ha la colonna KanBanLocationId, la valorizza.
        """
        has_kbl = self._table_has_column('knb', 'KanBanRecords', 'KanBanLocationId')
        try:
            self.conn.autocommit = False

            # Carico dati del record
            self.cursor.execute(
                "SELECT IdComponent, Quantity FROM knb.KanBanRecords WHERE KanBanRecordId = ?;", record_id
            )
            row = self.cursor.fetchone()
            if not row:
                self.conn.rollback()
                return False, "not_found"
            id_component, qty = row

            # Chiudi il record sorgente (solo se ancora aperto)
            self.cursor.execute(
                "UPDATE knb.KanBanRecords SET DateOut = GETDATE() WHERE KanBanRecordId = ? AND DateOut IS NULL;",
                record_id
            )
            if self.cursor.rowcount == 0:
                self.conn.rollback()
                return False, "already_closed"

            # Inserisci nuovo record in destinazione
            if has_kbl and to_kanban_location_id is not None:
                sql_ins = """
                INSERT INTO knb.KanBanRecords (LocationId, IdComponent, Quantity, DateIn, KanBanLocationId)
                VALUES (?, ?, ?, GETDATE(), ?);
                """
                self.cursor.execute(sql_ins, to_location_id, id_component, qty, to_kanban_location_id)
            else:
                sql_ins = """
                INSERT INTO knb.KanBanRecords (LocationId, IdComponent, Quantity, DateIn)
                VALUES (?, ?, ?, GETDATE());
                """
                self.cursor.execute(sql_ins, to_location_id, id_component, qty)

            self.conn.commit()
            return True, None
        except pyodbc.Error as e:
            try:
                self.conn.rollback()
            except Exception:
                pass
            self.last_error_details = str(e)
            return False, str(e)
        finally:
            self.conn.autocommit = True

    def move_all_from_location(self, from_location_id: int, to_location_id: int,
                               to_kanban_location_id: int | None = None):
        """
        Sposta TUTTI i record aperti (DateOut IS NULL) da una locazione a un'altra.
        Chiude i record sorgenti e inserisce nuovi record in blocco.
        """
        has_kbl = self._table_has_column('knb', 'KanBanRecords', 'KanBanLocationId')
        try:
            self.conn.autocommit = False

            # Conta quanti record aperti ci sono nella sorgente
            self.cursor.execute(
                "SELECT COUNT(*) FROM knb.KanBanRecords WHERE LocationId = ? AND DateOut IS NULL;",
                from_location_id
            )
            n = self.cursor.fetchone()[0]
            if n == 0:
                self.conn.rollback()
                return False, "nothing_to_move"

            # Chiudi i record sorgenti
            self.cursor.execute(
                "UPDATE knb.KanBanRecords SET DateOut = GETDATE() WHERE LocationId = ? AND DateOut IS NULL;",
                from_location_id
            )

            # Inserimento con INSERT ... SELECT
            if has_kbl and to_kanban_location_id is not None:
                sql_ins = """
                INSERT INTO knb.KanBanRecords (LocationId, IdComponent, Quantity, DateIn, KanBanLocationId)
                SELECT ?, IdComponent, Quantity, GETDATE(), ?
                FROM knb.KanBanRecords
                WHERE LocationId = ? AND DateOut = (SELECT MAX(DateOut) FROM knb.KanBanRecords kk WHERE kk.KanBanRecordId = knb.KanBanRecords.KanBanRecordId)
                   OR (LocationId = ? AND DateOut IS NULL) -- per sicurezza, ma dopo l'update sopra non ci saranno più NULL
                ;
                """
                # Notare: la riga sopra replica quantity e component dagli ultimi record; in pratica, dopo l'UPDATE, le righe appena chiuse vengono reinserite.
                # Passo due volte from_location_id per la OR.
                self.cursor.execute(sql_ins, to_location_id, to_kanban_location_id, from_location_id, from_location_id)
            else:
                sql_ins = """
                INSERT INTO knb.KanBanRecords (LocationId, IdComponent, Quantity, DateIn)
                SELECT ?, IdComponent, Quantity, GETDATE()
                FROM knb.KanBanRecords
                WHERE LocationId = ? AND DateOut = (SELECT MAX(DateOut) FROM knb.KanBanRecords kk WHERE kk.KanBanRecordId = knb.KanBanRecords.KanBanRecordId)
                   OR (LocationId = ? AND DateOut IS NULL);
                """
                self.cursor.execute(sql_ins, to_location_id, from_location_id, from_location_id)

            self.conn.commit()
            return True, None
        except pyodbc.Error as e:
            try:
                self.conn.rollback()
            except Exception:
                pass
            self.last_error_details = str(e)
            return False, str(e)
        finally:
            self.conn.autocommit = True

    def fetch_kanban_locations_all(self):
        """
        Restituisce tutte le locazioni KanBan (LocationCode) ordinate.
        """
        sql = """
            SELECT L.LocationCode, L.KanBanLocationId
            FROM knb.Locations AS L
            ORDER BY L.LocationCode;
        """
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()  # .LocationCode, .KanBanLocationId
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def count_kanban_locations(self) -> int | None:
        """
        Ritorna il numero totale di locazioni KanBan (knb.Locations).
        """
        try:
            return self.cursor.execute("SELECT COUNT(*) FROM knb.Locations;").fetchval()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return None

    def fetch_kanban_areas(self):
        """
        Restituisce le aree KanBan (IDParentPhase, ParentPhaseName) filtrate per CodCDC in (10,30,90).
        """
        query = """            
            select [KanBanLocationId] AS IDParentPhase,
            KanBanLocation AS ParentPhaseName
             FROM  KNB.KANBANLOCATIONS order by KanBanLocation;
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def insert_kanban_location(self, kanban_location_id: int, location_code: str):
        """
        Inserisce una nuova locazione KanBan.
        Ritorna (True, None) su successo, oppure (False, 'duplicate') se violazione chiave/unicità,
        oppure (False, 'messaggio_errore') per altri errori.
        """
        sql = """
            INSERT INTO knb.Locations (KanBanLocationId, LocationCode)
            VALUES (?, ?);
        """
        try:
            self.cursor.execute(sql, int(kanban_location_id), location_code)
            self.conn.commit()
            return True, None
        except pyodbc.IntegrityError as e:
            # SQL Server: 2627 (unique constraint), 2601 (duplicate key)
            msg = str(e)
            if any(code in msg for code in ("2627", "2601")) or "UNIQUE" in msg.upper() or "duplicate" in msg.lower():
                self.conn.rollback()
                return False, "duplicate"
            self.conn.rollback()
            return False, msg
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, str(e)

    def fetch_card_referiments(self, label_code):
        """
        Carica i riferimenti scheda per una label (LabelCod).
        Ritorna una lista di stringhe (Referiment).
        """
        query = """
        select 
            ProductRiferiments.CodRiferimento As Referiment
        from LabelCodes 
        inner join Boards on LabelCodes.IDBoard=Boards.IDBoard
        inner join Orders on Orders.IDOrder = Boards.IDOrder
        inner join Products on Products.IDProduct = Orders.IDProduct
        inner join ProductComponentsErp on Products.IDProduct = ProductComponentsErp.IDProduct
        inner join ProductRiferiments on ProductComponentsErp.IDProductCompErp = ProductRiferiments.IDProductCompErp
        inner join Components on Components.IDComponent = ProductComponentsErp.IDComponent
        inner join ParentPhases on ParentPhases.IDParentPhase = ProductRiferiments.IDParentPhase
        where LabelCodes.LabelCod = ?
        order by ParentPhases.ParentPhaseName,
                 ProductRiferiments.CodRiferimento + ' [' + ParentPhases.ParentPhaseName + ']';
        """
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(query, label_code)
            rows = cur.fetchall()
            return [getattr(r, 'Referiment', r[0]) for r in rows] if rows else []
        except Exception as e:
            self.last_error_details = str(e)
            return []
        finally:
            try:
                if cur: cur.close()
            except Exception:
                pass

    def fetch_calibration_warnings(self):
        """
        Elenco attrezzature con calibrazione mancante o in scadenza (<=7 giorni)
        e per cui NON è stato inviato un avviso nelle ultime 24 ore (tabella eqp.CalibrationWarnings).
        Considera solo l’ultima calibrazione per attrezzatura.
        """
        query = """
        SELECT 
            e.EquipmentId,
            e.InternalName + ' [Inventory: ' + ISNULL(e.InventoryNumber, '#N/DD') + ']' AS Equipment,
            CAST(c1.CalibratedOn AS date) AS LastCalibrationDate,
            s1.SiteName AS CalibratedBy,
            c1.NrCertificate,
            CAST(c1.ExpireOn AS date) AS ExpireOn,
            IIF(c1.CalibratedOn IS NULL, 'No calibration record!', '') AS [Note]
        FROM eqp.Equipments e
        OUTER APPLY (
            SELECT TOP 1 c.*
            FROM eqp.Calibrations c
            WHERE c.EquipmentID = e.EquipmentId
            ORDER BY c.CalibratedOn DESC
        ) c1
        LEFT JOIN dbo.Sites s1 ON s1.IDSite = c1.CalibrationSupplierId
        LEFT JOIN eqp.EquipmentBrands eb ON eb.EquipmentBrandId = e.BrandId
        INNER JOIN dbo.Sites s ON s.IDSite = eb.CompanyId
        OUTER APPLY (
            SELECT TOP 1 w.WarningSentOn AS LastWarn
            FROM eqp.CalibrationWarnings w
            WHERE w.EquipmentId = e.EquipmentId
            ORDER BY w.WarningSentOn DESC
        ) w1
        WHERE e.MustCalibrated = 1
          AND (
                c1.ExpireOn IS NULL
                OR DATEDIFF(day, GETDATE(), c1.ExpireOn) <= 7
              )
          AND (
                w1.LastWarn IS NULL
                OR DATEDIFF(day, w1.LastWarn, GETDATE()) >= 1
              )
        ORDER BY e.InternalName + ' [Inventory: ' + ISNULL(e.InventoryNumber,'#N/DD') + ']', c1.ExpireOn;
        """
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            return cur.fetchall()
        except Exception as e:
            self.last_error_details = str(e)
            return []
        finally:
            try:
                if cur: cur.close()
            except:
                pass

    def mark_calibration_warning_sent(self, equipment_ids):
        """
        Registra l'invio avviso per gli EquipmentId passati, inserendo una riga in eqp.CalibrationWarnings
        con WarningSentOn = GETDATE() per ciascun equipment.

        Ritorna True/False.
        """
        if not equipment_ids:
            return True

        sql = """INSERT INTO eqp.CalibrationWarnings (EquipmentId, WarningSentOn)
            SELECT ?, GETDATE()
            WHERE NOT EXISTS (
               SELECT 1 FROM eqp.CalibrationWarnings
               WHERE EquipmentId = ? AND CAST(WarningSentOn AS date) = CAST(GETDATE() AS date)
            );
            """
        cur = None
        try:
            cur = self.conn.cursor()
            # normalizza a int e crea tuples per executemany
            params = [(int(eid), int(eid)) for eid in equipment_ids]
            cur.executemany(sql, params)
            self.conn.commit()
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            self.last_error_details = str(e)
            return False
        finally:
            try:
                if cur: cur.close()
            except Exception:
                pass

    def fetch_unassigned_submissions(self):
        query = """
        SELECT
            CAST(se.SegnalazioneId AS int) AS SegID,
            CAST(se.DataSegnalazione AS date) AS DataSegnalazione,
            e.EmployeeName + ' ' + e.EmployeeSurname AS InputFrom,
            se.Titolo,
            se.Descrizione,
            IIF(sa.SegnalazioneStatoAllegatoID IS NULL, 'No attached doc', sa.DescrizioneDocumento) AS Documents,
            sts.TipoStato,
            IIF(sts.StatoChiuso = 0, 'OPEN', 'CLOSED') AS StatoType,
            eaFrom.WorkEmail AS Email,
            sa.
        FROM Employee.dbo.Segnalazioni se
        INNER JOIN Employee.dbo.SegnalazioneStati ss
            ON ss.SegnalazioneId = se.SegnalazioneId              -- join corretto sull'ID segnalazione
        INNER JOIN Employee.dbo.SegnalazioniTipoStati sts
            ON sts.SegnalazioniTipoStatoId = ss.SegnalazioniTipoStatoId
        LEFT JOIN Employee.dbo.EmployeeHireHistory h
            ON h.EmployeeHireHistoryId = se.IdDipendente
        LEFT JOIN Employee.dbo.Employees e
            ON e.EmployeeId = h.EmployeeId
        LEFT JOIN Employee.dbo.EmployeeAddress eaFrom
            ON eaFrom.EmployeeId = e.EmployeeId
           AND eaFrom.DateOut IS NULL
        LEFT JOIN Employee.dbo.SegnalazioniStatiAllegati sa
            ON sa.SegnalazioneStatoId = ss.SegnalazioneStatoId
        WHERE sts.StatoChiuso = 0
          AND NOT EXISTS (
              SELECT 1
              FROM Employee.dbo.SegnalazioneAssegnazioni sea
              WHERE sea.SegnalazioneId = se.SegnalazioneId
          )
        ORDER BY se.DataSegnalazione DESC;
        """
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            # ritorna lista di dict con chiavi: SegID, DataSegnalazione, InputFrom, Titolo, Descrizione, Documents, TipoStato, StatoType, Email
            return [dict(zip(cols, row)) for row in rows]
        except Exception as e:
            self.last_error_details = str(e)
            return []
        finally:
            try:
                if cur: cur.close()
            except:
                pass

    def fetch_assignable_employees(self):
        query = """
        SELECT h.EmployeeHireHistoryId,
               UPPER(e.EmployeeSurname + ' ' + e.EmployeeName) AS Employee,
               ea.WorkEmail
        FROM employee.dbo.employees e
        INNER JOIN employee.dbo.EmployeeHireHistory h ON e.EmployeeId = h.EmployeeId
        INNER JOIN employee.dbo.EmployeeCdcStories ec ON ec.EmployeeHireHistoryId = h.EmployeeHireHistoryId
                                                      AND ec.DateOut IS NULL
                                                      AND h.employeerid = 2
                                                      AND h.EndWorkDate IS NULL 
        INNER JOIN employee.dbo.Functions f ON ec.FunctionId = f.FunctionId
        INNER JOIN employee.dbo.EmployeeAddress ea ON ea.EmployeeId = e.EmployeeId
                                                 AND ea.DateOut IS NULL
        WHERE f.IsStructure = 1
        ORDER BY UPPER(e.EmployeeSurname + ' ' + e.EmployeeName);
        """
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            return cur.fetchall()
        except Exception as e:
            self.last_error_details = str(e)
            return []
        finally:
            try:
                if cur: cur.close()
            except:
                pass

    def assign_submission(self, segnalazione_id: int, employee_hire_history_id: int,
                          note: str = None):
        """
        Registra l'assegnazione:
          - Inserisce in SegnalazioneAssegnazioni (marca come assegnata)
          - Inserisce la nota in SegnalazioneSvolgimento
        """
        q_assign = """
            INSERT INTO Employee.dbo.SegnalazioneAssegnazioni
                (SegnalazioneId, EmployeeHireHistoryId, [Note])
            VALUES (?, ?, ?);
        """
        q_progress = """
            INSERT INTO Employee.dbo.SegnalazioneStati
                (SegnalazioneId, SegnalazioniTipoStatoId, DataAttivita,[Nota], [OperatoDa])
            VALUES (?, 1, GetDate(),'Assigned', 'System');
        """
        cur = None
        try:
            cur = self.conn.cursor()
            # Cast difensivo per evitare clash di tipi
            seg_id = int(segnalazione_id)
            ehh_id = int(employee_hire_history_id)

            cur.execute(q_assign, seg_id, ehh_id, note if note else None)
            cur.execute(q_progress, seg_id )# , ehh_id)

            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False
        finally:
            try:
                if cur: cur.close()
            except:
                pass

    def insert_scrap_reason(self, reason):
        query = "INSERT INTO Traceability_RS.dbo.ScrapResons ([Reason]) VALUES (?);"
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(query, reason.strip())
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False
        finally:
            try:
                if cur: cur.close()
            except:
                pass

    def update_scrap_reason(self, scrap_reason_id, reason):
        query = "UPDATE Traceability_RS.dbo.ScrapResons SET [Reason] = ? WHERE ScrapReasonId = ?;"
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(query, reason.strip(), scrap_reason_id)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False
        finally:
            try:
                if cur: cur.close()
            except:
                pass

    def delete_scrap_reason(self, scrap_reason_id):
        query = "DELETE FROM Traceability_RS.dbo.ScrapResons WHERE ScrapReasonId = ?;"
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute(query, scrap_reason_id)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False
        finally:
            try:
                if cur: cur.close()
            except:
                pass

    def get_scrap_label_info(self, label_code):
        """
        Verifica il codice etichetta (scheda scrap).
        Ritorna la riga con: IDLabelCode (se esiste), OrderNumber, OrderDate (formattata), OrderQuantity, ProductCode, IDBoard.
        """
        query = """
            SELECT 
                l.IDLabelCode,           -- se non esiste la colonna, verrà None nell'accesso attributo
                b.IDBoard,
                o.OrderNumber,
                FORMAT(o.OrderDate,'d','ro-ro') AS OrderDate,
                o.OrderQuantity,
                p.ProductCode
            FROM Traceability_RS.dbo.LabelCodes L
            INNER JOIN Traceability_RS.dbo.boards b ON b.idboard = l.IDBoard
            INNER JOIN Traceability_RS.dbo.orders o ON o.IDOrder = b.IDOrder
            INNER JOIN Traceability_RS.dbo.products p ON p.idproduct = o.idproduct
            WHERE l.labelcod = ?
        """
        try:
            cur = self.conn.cursor()
            cur.execute(query, label_code)
            return cur.fetchone()
        except Exception as e:
            self.last_error_details = str(e)
            return None
        finally:
            try:
                cur.close()
            except:
                pass

    def get_label_id_by_code(self, label_code):
        """
        Recupera l'ID della label se la colonna IDLabelCode esiste, altrimenti prova a dedurre dall'IDBoard.
        """
        try:
            cur = self.conn.cursor()
            # Primo tentativo: IDLabelCode
            cur.execute("SELECT IDLabelCode FROM Traceability_RS.dbo.LabelCodes WHERE LabelCod = ?", label_code)
            row = cur.fetchone()
            if row and hasattr(row, 'IDLabelCode') and row.IDLabelCode is not None:
                return row.IDLabelCode

            # Fallback (se non esiste IDLabelCode, NON lo forziamo a IDBoard: lasciamo None)
            return None
        except Exception as e:
            self.last_error_details = str(e)
            return None
        finally:
            try:
                cur.close()
            except:
                pass

    def fetch_origin_areas_for_scrap(self):
        """
        Carica la combo 'Area di provenienza' dalle ParentPhases (filtrate).
        """
        query = """
            SELECT idArea as idParentPhase, AreaName as ParentPhaseName
            FROM Traceability_RS.dbo.Areas           
            ORDER BY AreaName;
        """
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            return cur.fetchall()
        except Exception as e:
            self.last_error_details = str(e)
            return []
        finally:
            try:
                cur.close()
            except:
                pass

    def fetch_scrap_reasons(self):
        """
        Carica la combo 'Motivo' da dbo.ScrapResons (nome tabella fornito).
        """
        query = """
            SELECT ScrapReasonId, [Reason]
            FROM Traceability_RS.dbo.ScrapResons
            ORDER BY [Reason];
        """
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            return cur.fetchall()
        except Exception as e:
            self.last_error_details = str(e)
            return []
        finally:
            try:
                cur.close()
            except:
                pass

    def insert_scrap_declaration(self, user_name, id_label_code, id_parent_phase, scrap_reason_id,
                                 note, picture_bytes, riferiments=None):
        """
        Salva la dichiarazione nella tabella dbo.ScarpDeclarations.
        Tenta prima l'inserimento con la nuova colonna [Riferiments];
        se la colonna non esiste, fa fallback al vecchio INSERT.

        riferiments: stringa con riferimenti separati da ';' (può essere None o '')
        """
        if riferiments is None:
            riferiments = ""

        cur = None
        try:
            cur = self.conn.cursor()

            # Nuovo insert con Riferiments
            query_new = """
                INSERT INTO dbo.ScarpDeclarations
                    ([User], [IdLabelCode], [IDParentPhase], [ScrapReasonId], [Note], [Riferiments], [DateIn], [Picture])
                VALUES (?, ?, ?, ?, ?, ?, GETDATE(), ?);
            """
            cur.execute(query_new, user_name, id_label_code, id_parent_phase, scrap_reason_id,
                        note, riferiments, picture_bytes)
            self.conn.commit()
            return True

        except Exception as e:
            # Se la colonna non esiste, fallback al vecchio schema
            self.conn.rollback()
            msg = str(e).lower()
            if "invalid column" in msg and "riferiments" in msg:
                try:
                    cur = self.conn.cursor()
                    query_old = """
                        INSERT INTO dbo.ScarpDeclarations
                            ([User], [IdLabelCode], [IDParentPhase], [ScrapReasonId], [Note], [DateIn], [Picture])
                        VALUES (?, ?, ?, ?, ?, GETDATE(), ?);
                    """
                    cur.execute(query_old, user_name, id_label_code, id_parent_phase, scrap_reason_id,
                                note, picture_bytes)
                    self.conn.commit()
                    return True
                except Exception as e2:
                    self.conn.rollback()
                    self.last_error_details = str(e2)
                    return False
            else:
                self.last_error_details = str(e)
                return False
        finally:
            try:
                if cur: cur.close()
            except Exception:
                pass

    def authenticate_and_get_user(self, user_id, password):
        """
        Autentica un utente e, se ha successo, recupera i suoi dati e permessi.
        :return: Un oggetto User in caso di successo, altrimenti None.
        """
        # 1. Eseguiamo l'autenticazione esistente per verificare le credenziali
        employee_name = self.authenticate_user(user_id, password)
        logger.info("authenticate_user result for user_id=%r: %s", user_id,
                     "OK" if employee_name else "FAILED")

        if not employee_name:
            return None  # Login fallito

        # 2. Se l'autenticazione ha successo, carichiamo i permessi

        permissions_query = """
             SELECT p.PermissionKey , ep.[user]
            FROM dbo.EmployeePermissions ep
            inner JOIN dbo.Permissions p ON ep.PermissionId = p.PermissionId
           WHERE ep.[user] = ?            
        """
        permissions = set()
        cursor = None
        try:
            cursor = self.conn.cursor()
            logger.info("Executing permissions query with param user_id=%r", user_id)
            # Usiamo lo user_id numerico per la ricerca dei permessi
            cursor.execute(permissions_query, user_id)
            # Creiamo un set con tutte le chiavi di permesso trovate
            permissions = {row.PermissionKey for row in cursor.fetchall()}
        except Exception as e:
            print(f"ATTENZIONE: Impossibile caricare i permessi per l'utente {user_id}. Errore: {e}")
            # L'utente potrà accedere ma non avrà permessi speciali
        finally:
            if cursor:
                cursor.close()

        # 3. Creiamo e restituiamo l'oggetto User completo
        return User(name=employee_name, permissions=permissions)

    def get_calibratable_equipment(self):
        """
        Recupera dal database la lista di tutte le attrezzature che
        richiedono una calibrazione.
        :return: Una lista di righe (oggetti row) o None in caso di errore.
        """
        query = """
            SELECT e.EquipmentId, e.InternalName, e.InventoryNumber, eb.Brand, s.SiteName
            FROM eqp.equipments e 
            INNER JOIN eqp.EquipmentBrands eb ON e.BrandId = eb.EquipmentBrandId
            INNER JOIN dbo.Sites s ON eb.CompanyId = s.IDSite
            INNER JOIN eqp.EquipmentTypes et ON e.EquipmentTypeId = et.EquipmentTypeId
            WHERE e.MustCalibrated = 1
            ORDER BY e.InternalName
        """
        cursor = None
        try:
            # Assumo che la tua connessione si chiami self.conn
            cursor = self.conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()

    def get_last_calibration(self, equipment_id):
        """
        Recupera l'ultima registrazione di calibrazione per una specifica attrezzatura.
        :param equipment_id: L'ID dell'attrezzatura da cercare.
        :return: Una singola riga (oggetto row) o None se non trovata.
        """
        query = """
            SELECT TOP (1)
            c.CalibratedOn,
            c.ExpireOn,
            c.NrCertificate
            FROM eqp.Calibrations AS c
            WHERE c.EquipmentId = ?
        ORDER BY c.CalibratedOn DESC, c.CalibrationId DESC;
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, equipment_id)
            return cursor.fetchone()
        finally:
            if cursor:
                cursor.close()

    def get_suppliers(self):
        """
        NUOVO: Recupera la lista dei fornitori dal database.
        :return: Una lista di righe (oggetti row) con IDSite e SiteName.
        """
        query = "SELECT IDSite, SiteName FROM Sites WHERE IsSupplier = 1 ORDER BY SiteName;"
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()

    def add_new_calibration(self, equipment_id: int, expire_on: str, supplier_id: int, certificate_bytes):
        """
        Inserisce una calibrazione.
        NrCertificate: varbinary(MAX) -> passare bytes/bytearray o None.
        Se per retrocompatibilità arriva una str, viene codificata UTF-8.
        """
        sql = """
        INSERT INTO eqp.Calibrations (EquipmentId, CalibratedOn, ExpireOn, SupplierId, NrCertificate)
        VALUES (?, GETDATE(), ?, ?, ?);
        """

        # Normalizza il parametro binario
        if certificate_bytes is None:
            param_cert = None
        elif isinstance(certificate_bytes, (bytes, bytearray, memoryview)):
            # memoryview va bene, ma convertiamolo a bytes per sicurezza
            param_cert = bytes(certificate_bytes)
        elif isinstance(certificate_bytes, str):
            # solo se vuoi supportare ancora stringhe (verranno salvate come UTF-8)
            param_cert = certificate_bytes.encode('utf-8')
        else:
            # qualsiasi altro tipo (es. Path) -> prova a convertirlo in bytes
            param_cert = bytes(certificate_bytes)

        self.cursor.execute(sql, equipment_id, expire_on, supplier_id, param_cert)
        self.conn.commit()

    def get_equipment_info(self, equipment_id):
        """Recupera le informazioni del macchinario dal database."""
        try:
            query = """
            SELECT eb.Brand + ' ' + 
                [InternalName] + '(' + [SerialNumber] + ')' as InternalName,[InventoryNumber] as SerialNumber
                FROM [Traceability_RS].[eqp].[Equipments] e inner join [eqp].[EquipmentBrands] eb on e.BrandId=eb.EquipmentBrandId 
                where e.equipmentid= ?
            """
            with self.conn.cursor() as cursor:
                cursor.execute(query, (equipment_id,))
                row = cursor.fetchone()
                return row
        except Exception as e:
            self.last_error_details = str(e)
            return None

    def fetch_clients_for_verification(self):
        """Recupera i clienti per la verifica associazione."""
        query = """
        select distinct p.idclient, fc.FinalClientName
        from traceability_rs.dbo.FinalClients fc 
        inner join traceability_rs.dbo.products p on p.idfinalclient = fc.idfinalclient 
        inner join traceability_rs.dbo.Clients c on c.IDClient = p.idclient 
        order by fc.FinalClientName, p.idclient
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_orders_by_year_and_client(self, year, client_id=None):
        """Recupera gli ordini per anno e cliente."""
        query = """
        select o.idorder, o.OrderNumber, p.productcode, fc.FinalClientName
        from traceability_rs.dbo.products p 
        inner join traceability_rs.dbo.Clients c on c.IDClient = p.idclient 
        inner join traceability_rs.dbo.orders o on p.idproduct = o.IDProduct 
        inner join traceability_rs.dbo.FinalClients fc on fc.idfinalclient = p.idfinalclient
        where year(o.OrderDate) = ?
        """
        params = [year]

        if client_id:
            query += " AND p.idclient = ?"
            params.append(client_id)

        query += " order by o.ordernumber"

        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def verify_label_association(self, label_code):
        """Verifica l'associazione di un'etichetta."""
        query = """
        Select distinct o.OrderNumber, p.ProductCode, l.LabelCod, b.IDBoard
        from traceability_rs.dbo.orders as O 
        inner join traceability_rs.dbo.products as P on p.idproduct = o.idproduct 
        inner join traceability_rs.dbo.boards as B on b.IDOrder = o.idorder 
        inner join traceability_rs.dbo.LabelCodes as L on l.IDBoard = b.IDBoard
        where l.IDBoard in (select IDBoard from LabelCodes where LabelCod = ?)
        """
        try:
            self.cursor.execute(query, label_code)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_final_clients_for_linking(self):
        """Recupera i clienti finali per il filtro."""
        query = """
        SELECT fc.IDFinalClient, fc.FinalClientName, fc.AcronimForCode
        FROM 
         FinalClients fc 
        ORDER BY fc.FinalClientName
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_final_products_by_client(self, client_id):
        """Recupera i prodotti finali per un cliente specifico."""
        query = """
        SELECT idproduct, ProductCode, ProductName, ProductCodClienteFinal
        FROM traceability_rs.dbo.products
        WHERE idfinalclient = ? AND IsFinalProduct = 1
        ORDER BY ProductCode
        """
        try:
            self.cursor.execute(query, client_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_semi_products_by_client(self, client_id):
        """Recupera i semilavorati per un cliente specifico."""
        query = """
        SELECT idproduct, ProductCode, ProductName
        FROM traceability_rs.dbo.products
        WHERE (idfinalclient = ? ) 
        AND (IsFinalProduct = 0 OR IsFinalProduct IS NULL)
        AND CHARINDEX('cipr', productcode, 1) = 0
        ORDER BY ProductCode
        """
        try:
            self.cursor.execute(query, client_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_existing_links(self, final_product_id=None, client_id=None):
        """Recupera i collegamenti esistenti."""
        query = """
        SELECT pl.ProductLInkedTableId, pl.IdProductFinal, pl.IdProductSemi, pl.Dateout,
               pf.ProductCode as FinalCode, pf.ProductName as FinalName,
               ps.ProductCode as SemiCode, ps.ProductName as SemiName,
               fc.FinalClientName
        FROM traceability_rs.dbo.ProductsLinked pl
        INNER JOIN traceability_rs.dbo.products pf ON pl.IdProductFinal = pf.idproduct
        INNER JOIN traceability_rs.dbo.products ps ON pl.IdProductSemi = ps.idproduct
        INNER JOIN traceability_rs.dbo.FinalClients fc ON pf.idfinalclient = fc.IDFinalClient
        WHERE pl.Dateout IS NULL
        """
        params = []

        if final_product_id:
            query += " AND pl.IdProductFinal = ?"
            params.append(final_product_id)
        elif client_id:
            query += " AND pf.idfinalclient = ?"
            params.append(client_id)

        query += " ORDER BY fc.FinalClientName, pf.ProductCode, ps.ProductCode"

        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def add_product_link(self, final_product_id, semi_product_id):
        """Aggiunge un nuovo collegamento."""
        # Prima verifica se esiste già un collegamento attivo
        check_query = """
        SELECT COUNT(*) FROM traceability_rs.dbo.ProductsLinked 
        WHERE IdProductFinal = ? AND IdProductSemi = ? AND Dateout IS NULL
        """
        try:
            count = self.cursor.execute(check_query, final_product_id, semi_product_id).fetchval()
            if count > 0:
                return False, "Esiste già un collegamento attivo tra questi prodotti."

            insert_query = """
            INSERT INTO dbo.ProductsLinked (IdProductFinal, IdProductSemi)
            VALUES (?, ?)
            """
            self.cursor.execute(insert_query, final_product_id, semi_product_id)
            self.conn.commit()
            return True, "Collegamento aggiunto con successo."

        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def delete_product_link(self, link_id):
        """Esegue un soft delete del collegamento."""
        query = "UPDATE dbo.ProductsLinked SET Dateout = GETDATE() WHERE ProductLInkedTableId = ?"
        try:
            self.cursor.execute(query, link_id)
            self.conn.commit()
            return True, "Collegamento eliminato con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def fetch_final_products(self):
        """Recupera tutti i prodotti con informazioni sui clienti finali."""
        query = """
           select idproduct, upper(ProductCode) as ProductCode, ProductName, 
                  isnull(ProductCodClienteFinal,'#ND') as ProductCodClienteFinal, 
                  p.IsFinalProduct, fc.FinalClientName, AcronimForCode,
                  p.idfinalclient
           from dbo.products as P 
           left join FinalClients FC on fc.IDFinalClient = p.idfinalclient
           where charindex('cipr', p.productcode, 1) = 0
           order by p.ProductCode
           """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_final_clients_for_products(self):
        """Recupera i clienti finali per la selezione."""
        query = """
           SELECT [IDFinalClient], [FinalClientName], [AcronimForCode]
           FROM [Traceability_RS].[dbo].[FinalClients] 
           ORDER BY FinalClientName
           """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def update_product_final_info(self, product_id, is_final_product, final_client_id, customer_code):
        """Aggiorna le informazioni di prodotto finale."""
        query = """
           UPDATE dbo.products 
           SET IsFinalProduct = ?, idfinalclient = ?, ProductCodClienteFinal = ?
           WHERE idproduct = ?
           """
        try:
            # Converti i valori per il database
            is_final_int = 1 if is_final_product else 0
            final_client_id = final_client_id if final_client_id else None
            customer_code = customer_code if customer_code else None

            self.cursor.execute(query, is_final_int, final_client_id, customer_code, product_id)
            self.conn.commit()
            return True, "Prodotto aggiornato con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def fetch_final_customers(self):
        """Recupera tutti i clienti finali."""
        query = """
        SELECT [IDFinalClient], [FinalClientName], [FinalClientFullName], [AcronimForCode],
               [ClientAddress], [ClientCity], [ClientZIP], [ClientCountry], [VatCode]
        FROM [Traceability_RS].[dbo].[FinalClients] 
        ORDER BY [FinalClientName]
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def add_final_customer(self, name, full_name, acronim, address, city, zip_code, country, vat_code):
        """Aggiunge un nuovo cliente finale."""
        query = """
        INSERT INTO [Traceability_RS].[dbo].[FinalClients] 
        (FinalClientName, FinalClientFullName, AcronimForCode, ClientAddress, ClientCity, ClientZIP, ClientCountry, VatCode)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            self.cursor.execute(query, name, full_name, acronim, address, city, zip_code, country, vat_code)
            self.conn.commit()
            return True, "Cliente aggiunto con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def update_final_customer(self, customer_id, name, full_name, acronim, address, city, zip_code, country, vat_code):
        """Aggiorna un cliente finale esistente."""
        query = """
        UPDATE [Traceability_RS].[dbo].[FinalClients] 
        SET FinalClientName = ?, FinalClientFullName = ?, AcronimForCode = ?,
            ClientAddress = ?, ClientCity = ?, ClientZIP = ?, ClientCountry = ?, VatCode = ?
        WHERE IDFinalClient = ?
        """
        try:
            self.cursor.execute(query, name, full_name, acronim, address, city, zip_code, country, vat_code,
                                customer_id)
            self.conn.commit()
            return True, "Cliente aggiornato con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def delete_final_customer(self, customer_id):
        """Elimina un cliente finale."""
        query = "DELETE FROM [Traceability_RS].[dbo].[FinalClients] WHERE IDFinalClient = ?"
        try:
            self.cursor.execute(query, customer_id)
            self.conn.commit()
            return True, "Cliente eliminato con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def fetch_kce_products(self):
        query = "SELECT idProduct, ProductCode FROM dbo.PRODUCTS WHERE PRODUCTCODE LIKE '%KCE%' ORDER BY ProductCode;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e);
            return []

    def fetch_supplier_sites(self):
        """Recupera i fornitori/compagnie dalla tabella Sites."""
        query = "SELECT [IDSite], [SiteName] FROM [Traceability_RS].[dbo].[Sites] WHERE isSupplier = 1 ORDER BY SiteName;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_all_sites(self):
        """Recupera tutti i siti/compagnie per la gestione."""
        query = "SELECT IDSite, SiteName, SiteAddress, SiteVat, SiteCountry, Logo FROM dbo.Sites ORDER BY SiteName;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def add_new_site(self, name, address, vat, country, logo):
        """Aggiunge una nuova compagnia."""
        query = "INSERT INTO dbo.Sites (SiteName, SiteAddress, SiteVat, SiteCountry, Logo, IDLastPhase, IsSupplier, IsTempraryLeasingComp) VALUES (?, ?, ?, ?, ?, 139, 1, 0);"
        try:
            self.cursor.execute(query, name, address, vat, country, logo)
            self.conn.commit()
            return True, "Compagnia aggiunta con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            if 'UNIQUE' in str(e) or 'duplicate' in str(e):
                return False, "Errore: Esiste già una compagnia con questo nome o Partita IVA."
            return False, f"Errore database: {e}"

    def update_site(self, site_id, name, address, vat, country, logo):
        """Aggiorna una compagnia esistente."""
        query = "UPDATE dbo.Sites SET SiteName=?, SiteAddress=?, SiteVat=?, SiteCountry=?, Logo=? WHERE IDSite=?;"
        try:
            self.cursor.execute(query, name, address, vat, country, logo, site_id)
            self.conn.commit()
            return True, "Compagnia aggiornata con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def delete_site(self, site_id):
        """Cancella una compagnia (da usare con cautela)."""
        # Aggiungere un controllo per verificare se il sito è usato in altre tabelle prima di cancellare
        query = "DELETE FROM dbo.Sites WHERE IDSite = ?;"
        try:
            self.cursor.execute(query, site_id)
            self.conn.commit()
            return True, "Compagnia cancellata con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def check_if_brand_is_used(self, brand_id):
        """Controlla se un brand è utilizzato in almeno una macchina."""
        query = "SELECT COUNT(*) FROM eqp.Equipments WHERE BrandId = ?;"
        try:
            count = self.cursor.execute(query, brand_id).fetchval()
            return count > 0
        except pyodbc.Error:
            return True  # Per sicurezza, in caso di errore, si assume che sia usato

    def update_brand(self, brand_id, brand_name, company_id, logo_data):
        """Aggiorna un brand esistente."""
        query = "UPDATE eqp.EquipmentBrands SET Brand = ?, CompanyId = ?, BrandLogo = ? WHERE EquipmentBrandId = ?;"
        try:
            company_id_to_save = int(company_id) if company_id is not None else None
            self.cursor.execute(query, brand_name, company_id_to_save, logo_data, brand_id)
            self.conn.commit()
            return True, "Brand aggiornato con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def delete_brand(self, brand_id):
        """Cancella un brand."""
        query = "DELETE FROM eqp.EquipmentBrands WHERE EquipmentBrandId = ?;"
        try:
            self.cursor.execute(query, brand_id)
            self.conn.commit()
            return True, "Brand cancellato con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def execute_missing_action_report(self):
        """Esegue la stored procedure per il report delle manutenzioni mancanti."""
        try:
            # La sintassi per chiamare una stored procedure che restituisce risultati
            sql = "{CALL eqp.sp_CheckMaintenanceStatus}"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()

            # Recupera anche le intestazioni delle colonne per l'Excel
            headers = [column[0] for column in self.cursor.description]

            return results, headers, None
        except pyodbc.Error as e:
            error_message = f"Errore durante l'esecuzione della stored procedure: {e}"
            self.last_error_details = str(e)
            return None, None, error_message

    def fetch_shipping_plan_items(self, shipping_date):
        """Recupera le righe del piano di spedizione per una data specifica."""
        # --- CORREZIONE QUI: Aggiunta la clausola WHERE ---
        query = "SELECT * FROM dbo.ShippingPlanItems WHERE ShippingDate = ?;"
        try:
            self.cursor.execute(query, shipping_date)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def update_xls_sheet_name(self, file_type_id, sheet_name):
        """Aggiorna il nome del foglio di lavoro per un dato tipo di file."""
        query = "UPDATE dbo.XlsFileTypes SET SheetName = ? WHERE FileTypeId = ?;"
        try:
            self.cursor.execute(query, sheet_name, file_type_id)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False

    def fetch_xls_file_types(self):
        """Recupera i tipi di file configurabili per l'import."""
        query = "SELECT FileTypeId, FileTypeName, TranslationKey FROM dbo.XlsFileTypes ORDER BY FileTypeName;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e);
            return []

    def fetch_xls_mappings(self, file_type_id):
        """
        Recupera la mappatura delle colonne E il nome del foglio di lavoro
        per un dato tipo di file.
        """
        query = """
            SELECT 
                m.MappingId, m.FieldName, m.ColumnLetter, m.StartRow, t.SheetName
            FROM 
                dbo.XlsColumnMappings m
            INNER JOIN 
                dbo.XlsFileTypes t ON m.FileTypeId = t.FileTypeId
            WHERE 
                m.FileTypeId = ?;
        """
        try:
            results = self.cursor.execute(query, file_type_id).fetchall()
            if not results:
                return {}, None

            # Estrae il nome del foglio (sarà lo stesso per tutte le righe)
            sheet_name = results[0].SheetName

            # Costruisce il dizionario della mappatura
            mappings = {}
            for row in results:
                mappings[row.FieldName] = {'id': row.MappingId, 'col': row.ColumnLetter, 'row': row.StartRow}

            return mappings, sheet_name
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return {}, None

    def update_xls_mapping(self, mapping_id, column_letter, start_row):
        """Aggiorna una singola riga di mappatura."""
        query = "UPDATE dbo.XlsColumnMappings SET ColumnLetter = ?, StartRow = ? WHERE MappingId = ?;"
        try:
            self.cursor.execute(query, column_letter, start_row, mapping_id)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False

    def save_shipping_plan_items(self, plan_data_list):
        """Esegue un'operazione di UPSERT (Update/Insert) per i dati del piano."""
        if not plan_data_list: return True, "Nessun dato da salvare."
        try:
            # Prepara le query
            update_sql = """
                UPDATE dbo.ShippingPlanItems 
                SET OriginalQty = ?, ModifiedQty = ?, Note = ?, Status = ?, LastUpdated = GETDATE(), UpdatedBy = ?
                WHERE ItemId = ?;
            """
            insert_sql = """
                INSERT INTO dbo.ShippingPlanItems (ShippingDate, OrderNumber, ProductCode, OriginalQty, ModifiedQty, Note, Status, UpdatedBy)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """

            for item in plan_data_list:
                if item.get('id'):  # Se ha un ID, è un UPDATE
                    params = (item['original_qty'], item['modified_qty'], item['note'], item['status'], item['user'],
                              item['id'])
                    self.cursor.execute(update_sql, params)
                else:  # Altrimenti è un INSERT
                    params = (item['shipping_date'], item['order'], item['product'], item['original_qty'],
                              item['modified_qty'], item['note'], item['status'], item['user'])
                    self.cursor.execute(insert_sql, params)

            self.conn.commit()
            return True, "Piano di spedizione salvato con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False, f"Errore durante il salvataggio: {e}"

    def fetch_shipping_settings(self):
        """Recupera tutte le impostazioni di spedizione attive."""
        query = "SELECT [ShippingSettingId], [DayOfWeek], [ShippingType] FROM [Traceability_RS].[dbo].[ShippingSettings] WHERE dateend IS NULL ORDER BY dayofweek;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def save_backlog_report(self, user_name, general_note, excel_data, notes_list):
        """Salva il report di backlog, il file excel e le note in una transazione."""
        try:
            # 1. Inserisce il log principale e ottiene il nuovo ID
            insert_log_sql = "INSERT INTO dbo.BackLogs (UserLog, Note) OUTPUT INSERTED.BackLogId VALUES (?, ?);"
            new_log_id = self.cursor.execute(insert_log_sql, user_name, general_note).fetchval()
            if not new_log_id: raise Exception("Creazione BackLog fallita.")

            # 2. Inserisce i dati binari del file Excel
            insert_data_sql = "INSERT INTO dbo.BackLogData (BackLogId, ExcelDataFile) VALUES (?, ?);"
            self.cursor.execute(insert_data_sql, new_log_id, excel_data)

            # 3. Inserisce tutte le note specifiche per riga
            if notes_list:
                insert_notes_sql = "INSERT INTO dbo.BackLogNotes (BackLogId, ExcelRowNumber, Note) VALUES (?, ?, ?);"
                params = [(new_log_id, row_num, note) for row_num, note in notes_list]
                self.cursor.executemany(insert_notes_sql, params)

            self.conn.commit()
            return True, "Report di backlog salvato con successo nel database."
        except Exception as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False, f"Errore durante il salvataggio nel database: {e}"

    def add_shipping_setting(self, day_of_week, shipping_type):
        """Aggiunge una nuova impostazione di spedizione dopo aver controllato i duplicati."""
        # 1. Controlla se esiste già un'impostazione identica e attiva
        check_query = """
            SELECT COUNT(*) FROM [dbo].[ShippingSettings]
            WHERE DayOfWeek = ? AND ShippingType = ? AND DateEnd IS NULL;
        """
        insert_query = "INSERT INTO [dbo].[ShippingSettings] (DayOfWeek, ShippingType) VALUES (?, ?);"
        try:
            count = self.cursor.execute(check_query, day_of_week, shipping_type).fetchval()
            if count > 0:
                return False, "Errore: Esiste già un''impostazione identica per questo giorno e tipo di spedizione."

            # 2. Se non esiste, procedi con l'inserimento
            self.cursor.execute(insert_query, day_of_week, shipping_type)
            self.conn.commit()
            return True, "Impostazione aggiunta con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def delete_shipping_setting(self, setting_id):
        """Esegue un soft delete di un'impostazione di spedizione impostando DateEnd."""
        query = "UPDATE [dbo].[ShippingSettings] SET DateEnd = GETDATE() WHERE ShippingSettingId = ?;"
        try:
            self.cursor.execute(query, setting_id)
            self.conn.commit()
            return True, "Impostazione cancellata con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def fetch_all_active_employees_birthdays(self):
        """Recupera nome, cognome e data di nascita di tutti i dipendenti attivi."""
        query = """
                SELECT E.EmployeeName, E.EmployeeSurname, E.EmployeeBirthDate
                FROM employee.dbo.employees E
                         INNER JOIN employee.dbo.EmployeeHireHistory H ON E.EmployeeId = H.EmployeeId
                WHERE H.EMPLOYEERID = 2 \
                  AND H.EndWorkDate IS NULL \
                  AND E.EmployeeBirthDate IS NOT NULL; \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_equipments_for_timing(self):
        """Recupera i macchinari con il loro brand."""
        query = """
                SELECT e.EquipmentId, e.InternalName + ' [' + b.Brand + ']' AS EquipmentName
                FROM eqp.Equipments e
                         INNER JOIN eqp.EquipmentBrands b ON e.BrandId = b.EquipmentBrandId
                ORDER BY e.InternalName + ' [' + b.Brand + ']'; \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e);
            return []

    def fetch_tasks_for_timing(self, equipment_id, intervention_id):
        """Recupera i compiti di manutenzione con i relativi tempi."""
        # NOTA: Ho aggiunto cmt.CompitoManutenzioneTimingId alla SELECT perché è necessario per l'UPDATE.
        query = """
                SELECT am.CompitoId, \
                       am.NomeCompito, \
                       am.DescrizioneCompito, \
                       am.PdfRiferiment, \
                       cmt.TimingMinutes, \
                       cmt.CompitoManutenzioneTimingId
                FROM [Traceability_RS].[eqp].[CompitiManutenzione] am
                    INNER JOIN eqp.ProgrammedInterventions pr \
                ON pr.ProgrammedInterventionId = am.ProgrammedInterventionId
                    INNER JOIN eqp.Equipments e ON e.EquipmentId = am.EquipmentId
                    LEFT JOIN eqp.CompitiManutenzioneTiming cmt ON cmt.compitoid = am.CompitoId AND cmt.dateend IS NULL
                WHERE e.EquipmentId = ? AND pr.ProgrammedInterventionId = ?
                ORDER BY pr.Ordineprn, am.CompitoId; \
                """
        try:
            self.cursor.execute(query, equipment_id, intervention_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e);
            return []

    def update_task_pdf_reference(self, task_id, pdf_reference):
        """Aggiorna solo il campo PdfRiferiment per un dato compito."""
        query = "UPDATE [Traceability_RS].[eqp].[CompitiManutenzione] SET PdfRiferiment = ? WHERE compitoid = ?;"
        try:
            self.cursor.execute(query, pdf_reference, task_id)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False

    def update_task_timing(self, task_id, new_minutes, old_timing_id):
        """Aggiorna il tempo di manutenzione (chiude il vecchio record e inserisce il nuovo)."""
        try:
            # 1. Se esiste un vecchio record di timing, lo chiude impostando la DateEnd
            if old_timing_id:
                update_query = "UPDATE [Traceability_RS].[eqp].CompitiManutenzioneTiming SET Dateend = GETDATE() WHERE CompitoManutenzioneTimingId = ?;"
                self.cursor.execute(update_query, old_timing_id)

            # 2. Se è stato fornito un nuovo valore in minuti, lo inserisce
            if new_minutes is not None and new_minutes != '':
                insert_query = "INSERT INTO EQP.CompitiManutenzioneTiming (compitoid, TimingMinutes) VALUES (?, ?);"
                self.cursor.execute(insert_query, task_id, new_minutes)

            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False

    def fetch_working_areas(self):
        """Recupera le Aree di Lavoro principali."""
        query = "SELECT [WorkingAreaID], [AreaName] FROM [ResetServices].[BreakDown].[WorkingAreas] ORDER BY AreaName;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"ERRORE SQL in fetch_working_areas: {e}")
            self.last_error_details = str(e)
            return []

    def fetch_working_sub_areas(self, working_area_id):
        """Recupera le Sotto-Aree in base all'Area di Lavoro selezionata."""
        query = """
                SELECT [WorkingSubAreaID], [AreaSubName]
                FROM [ResetServices].[BreakDown].[WorkingSubAreas]
                WHERE [WorkingAreaID] = ? \
                ORDER BY AreaSubName; \
                """
        try:
            self.cursor.execute(query, working_area_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"ERRORE SQL in fetch_working_sub_areas: {e}")
            self.last_error_details = str(e)
            return []

    def fetch_working_lines(self, working_area_id, sub_area_id):
        """Recupera le Linee in base all'Area e Sotto-Area selezionate."""
        query = """
                SELECT DISTINCT wl.WorkingLineID, WL.WorkingLineName
                FROM [ResetServices].[BreakDown].[WorkingAreas] AS WA
                    INNER JOIN [ResetServices].[BreakDown].WorkingSubAreas WSA \
                ON WA.WorkingAreaID = WSA.WorkingAreaID
                    INNER JOIN [ResetServices].[BreakDown].WorkingLines AS WL ON WSA.WorkingSubAreaID = WL.WorkingSubAreaID
                WHERE WA.WorkingAreaID = ? AND WSA.workingsubareaid = ?
                ORDER BY wl.WorkingLineName; \
                """
        try:
            self.cursor.execute(query, working_area_id, sub_area_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"ERRORE SQL in fetch_working_lines: {e}")
            self.last_error_details = str(e)
            return []

    def fetch_production_orders_for_breakdown(self):
        """Recupera la lista degli ordini di produzione aperti."""
        query = """
                SELECT o.IdOrdine, o.po + ' [' + pf.epiccode + ']' as OrderNumber
                FROM ResetServices.dbo.tbordini o
                         INNER JOIN Resetservices.dbo.tbsubordine so on o.IdOrdine = so.IdOrdine
                         INNER JOIN Resetservices.dbo.tbprodfin pf on so.idpf = pf.idpf
                         INNER JOIN resetservices.dbo.TbRegistro r \
                                    on o.idregistro = r.contatore and r.idregistro in (21, 26)
                         LEFT JOIN resetservices.dbo.TbFattStory fs on fs.IdPoSub = so.IdOrdStori
                         LEFT JOIN resetservices.dbo.TbProdFinStuff Micro on micro.Idpf = so.idpf
                WHERE year (o.dataord) >= YEAR (GETDATE()) and micro.idpf is null
                GROUP BY o.idordine, o.po + ' [' + pf.epiccode +']', so.QtaStory, o.dataord, so.DataDeliSubOrdine
                HAVING so.QtaStory > isnull(sum (fs.QtaFaturata), 0)
                ORDER BY o.dataord DESC; \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            print(f"ERRORE SQL in fetch_production_orders_for_breakdown: {e}")
            return []

    def fetch_report_data(self, from_date, to_date, equipment_id=None, intervention_id=None):
        """Recupera i dati dei log di manutenzione per un dato periodo e filtri opzionali."""
        query = """
                SELECT eq.InternalName                             AS EquipmentName, \
                       pin.TimingDescriprion                       AS InterventionType, \
                       cm.NomeCompito                              AS TaskName, \
                       lm.UserName, \
                       lm.DateStart, \
                       lm.DateStop, \
                       DATEDIFF(MINUTE, lm.DateStart, lm.DateStop) AS DurationInMinutes
                FROM eqp.LogManutenzioni lm
                         JOIN eqp.CompitiManutenzione cm ON lm.CompitoId = cm.CompitoId
                         JOIN eqp.Equipments eq ON lm.EquipmentId = eq.EquipmentId
                         JOIN eqp.ProgrammedInterventions pin \
                              ON cm.ProgrammedInterventionId = pin.ProgrammedInterventionId
                WHERE lm.DateStart >= ? \
                  AND lm.DateStart < DATEADD(day, 1, ?) \
                """
        params = [from_date, to_date]

        if equipment_id:
            query += " AND eq.EquipmentId = ?"
            params.append(equipment_id)

        if intervention_id:
            query += " AND pin.ProgrammedInterventionId = ?"
            params.append(intervention_id)

        query += " ORDER BY lm.DateStart;"

        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_open_production_orders(self):
        """Recupera la lista degli ordini di produzione aperti."""
        query = """
                SELECT o.idordine, o.po + ' [' + pf.epiccode + ']' AS OrderNumber
                FROM ResetServices.dbo.tbordini o
                         INNER JOIN Resetservices.dbo.tbsubordine so ON o.IdOrdine = so.IdOrdine
                         INNER JOIN Resetservices.dbo.tbprodfin pf ON so.idpf = pf.idpf
                         INNER JOIN resetservices.dbo.TbRegistro r \
                                    ON o.idregistro = r.contatore AND r.idregistro IN (21, 26)
                         LEFT JOIN resetservices.dbo.TbFattStory fs ON fs.IdPoSub = so.IdOrdStori
                         LEFT JOIN resetservices.dbo.TbProdFinStuff Micro ON micro.Idpf = so.idpf
                WHERE YEAR (o.dataord) >= 2025 AND micro.idpf IS NULL
                GROUP BY o.idordine, o.po + ' [' + pf.epiccode +']', so.QtaStory, o.dataord, so.DataDeliSubOrdine
                HAVING so.QtaStory > ISNULL(SUM (fs.QtaFaturata), 0)
                ORDER BY o.dataord; \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            print(f"Errore nel recupero degli ordini di produzione: {e}")
            return []

    def fetch_issue_problems_by_subarea(self, sub_area_id):
        """Recupera i problemi/eventi specifici per una Sotto-Area."""
        # CORREZIONE 1: Nome tabella da '...PerLines' a '...PerLine'
        # CORREZIONE 2: Nome colonna da 'bdl.IusseProblemId' a 'bdl.IssueProblemId'
        query = """
                SELECT ip.IssueProblemId, ip.DescriptionEN
                FROM ResetServices.BreakDown.IssueProblemsPerLines AS BDL
                         INNER JOIN ResetServices.BreakDown.IssueProblems AS ip ON ip.IssueProblemId = bdl.IusseProblemId
                WHERE BDL.WorkingSubAreaId = ?
                GROUP BY ip.IssueProblemId, ip.DescriptionEN; \
                """
        try:
            print(
                f"DEBUG: La query per 'Evento/Problema' viene eseguita con il parametro WorkingSubAreaId = {sub_area_id}")
            self.cursor.execute(query, sub_area_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"ERRORE SQL in fetch_issue_problems_by_subarea: {e}")
            self.last_error_details = str(e)
            return []

    def fetch_issue_areas(self):
        """Recupera le aree problematiche (es. Meccanica, Elettrica)."""
        query = "SELECT [IssueAreaId], [IssueArea] FROM [ResetServices].[BreakDown].[IssuesAreas] ORDER BY [IssueArea];"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"ERRORE SQL in fetch_issue_areas: {e}")
            self.last_error_details = str(e)
            return []

    def fetch_issue_problems(self, working_area_id, issue_area_id, sub_area_id):
        """
        Recupera i problemi/eventi seguendo ESATTAMENTE la logica VBA fornita.
        """
        # Query per contare i problemi specifici per la linea/sotto-area
        # Ho corretto i typo 'IusseProblemId' in 'IssueProblemId' e 'PerLines' in 'PerLine'
        count_query = """
                      SELECT COUNT(BDL.IssueProblemsPerLineId)
                      FROM ResetServices.BreakDown.IssueProblemsPerLines AS BDL
                      WHERE BDL.WorkingSubAreaId = ?; \
                      """
        try:
            count = self.cursor.execute(count_query, sub_area_id).fetchval()
            print(f"DEBUG: Conteggio problemi specifici per SubAreaID {sub_area_id}: {count}")

            if count == 0:
                # NESSUN problema specifico -> Esegui la query GENERICA
                print("DEBUG: Eseguo la query GENERICA.")
                final_query = """
                              SELECT IP.IssueProblemId, \
                                     '[' + IP.Code + '] ' + IP.DescriptionEN AS IssueDescription, \
                                     IP.MandatoryExplication
                              FROM ResetServices.BreakDown.IssueProblems AS IP
                                       INNER JOIN ResetServices.BreakDown.IssuesAreas AS IA ON IA.IssueAreaId = IP.IssueAreaId
                                       INNER JOIN ResetServices.BreakDown.WorkingAreas AS WA ON IP.WorkingAreaID = WA.WorkingAreaID
                              WHERE (WA.WorkingAreaID = ?) \
                                AND (IP.IssueAreaId = ?) \
                                AND (IP.DateOut IS NULL); \
                              """
                params = (working_area_id, issue_area_id)
            else:
                # TROVATI problemi specifici -> Esegui la query SPECIFICA
                print("DEBUG: Eseguo la query SPECIFICA.")
                final_query = """
                              SELECT IP.IssueProblemId, \
                                     '[' + IP.Code + '] ' + IP.DescriptionEN AS IssueDescription, \
                                     IP.MandatoryExplication
                              FROM ResetServices.BreakDown.IssueProblems AS IP
                                       INNER JOIN ResetServices.BreakDown.IssuesAreas AS IA ON IA.IssueAreaId = IP.IssueAreaId
                                       INNER JOIN ResetServices.BreakDown.WorkingAreas AS WA ON IP.WorkingAreaID = WA.WorkingAreaID
                                       INNER JOIN ResetServices.BreakDown.IssueProblemsPerLines AS BDL \
                                                  on ip.IssueProblemId = bdl.IusseProblemId
                              WHERE (WA.WorkingAreaID = ?) \
                                AND (IP.IssueAreaId = ?) \
                                AND (IP.DateOut IS NULL); \
                              """
                params = (working_area_id, issue_area_id)

            self.cursor.execute(final_query, params)
            return self.cursor.fetchall()

        except pyodbc.Error as e:
            print(f"ERRORE SQL in fetch_issue_problems: {e}")
            self.last_error_details = str(e)
            return []

    def add_production_interruption(self, params):
        """Salva un nuovo record di interruzione produzione in ReportIssueLogs."""
        query = """
                INSERT INTO ResetServices.[BreakDown].[ReportIssueLogs] ([DateReport], [HourReport], [UserName], [IssueAreaId], \
                                                            [WorkingAreaID],
                    [WorkingLineID], [WorkingSubAreaID], [IssueProblemId], [FromHour], [ToHour],
                    [Lost_OR_Gain], [Hours], [PoNumber], [ProductCode], [Note], [ActionPlan]) \
                VALUES (?, GETDATE(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); \
                """
        try:
            self.cursor.execute(query,
                                params['report_date'], params['user_name'], params['issue_area_id'],
                                params['working_area_id'],
                                params['line_id'], params['sub_area_id'], params['problem_id'], params['from_hour'],
                                params['to_hour'],
                                params['lost_gain'], params['hours'], params['po_number'], params['product_code'],
                                params['note'], params['action_plan']
                                )
            self.conn.commit()
            return True, "Interruzione di produzione registrata con successo."
        except Exception as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False, f"Errore durante il salvataggio: {e}"

    def check_if_material_exists(self, part_number):
        """Controlla se un materiale con un dato Codice Articolo esiste già. Restituisce True se esiste, altrimenti False."""
        query = "SELECT COUNT(*) FROM eqp.SparePartMaterials WHERE MaterialPartNumber = ?;"
        try:
            count = self.cursor.execute(query, part_number).fetchval()
            return count > 0
        except pyodbc.Error as e:
            print(f"Errore nel controllo esistenza materiale: {e}")
            return False  # Per sicurezza, non blocchiamo l'utente in caso di errore

    def fetch_material_document(self, material_id):
        """Recupera i dati binari del documento per un singolo materiale."""
        query = "SELECT CatalogDetail FROM eqp.SparePartMaterials WHERE SparePartMaterialId = ?;"
        try:
            self.cursor.execute(query, material_id)
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return None

    def search_materials(self, code_filter, desc_filter):
        """Cerca i materiali in base a filtri per codice/nome e descrizione."""
        query = """
                SELECT SparePartMaterialId, MaterialPartNumber, MaterialCode, MaterialDescription
                FROM eqp.SparePartMaterials
                WHERE (MaterialPartNumber LIKE ? OR MaterialCode LIKE ?)
                  AND MaterialDescription LIKE ?
                ORDER BY MaterialCode; \
                """
        try:
            # I parametri % per il LIKE vengono aggiunti qui
            code_param = f"%{code_filter}%"
            desc_param = f"%{desc_filter}%"

            self.cursor.execute(query, code_param, code_param, desc_param)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_single_material(self, material_id):
        """Recupera tutti i dati di un singolo materiale."""
        query = "SELECT * FROM eqp.SparePartMaterials WHERE SparePartMaterialId = ?;"
        try:
            self.cursor.execute(query, material_id)
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            self.last_error_details = str(e);
            return None

    def add_material(self, part_number, code, description, catalog_data, doc_name, user_name):
        """Aggiunge un nuovo materiale, includendo l'utente che ha eseguito l'operazione."""
        query = """
                INSERT INTO eqp.SparePartMaterials
                (MaterialPartNumber, MaterialCode, MaterialDescription, CatalogDetail, CatalogFileName, [User])
                    OUTPUT INSERTED.SparePartMaterialId
                VALUES (?, ?, ?, ?, ?, ?); \
                """
        try:
            new_id = self.cursor.execute(query, part_number, code, description, catalog_data, doc_name,
                                         user_name).fetchval()
            self.conn.commit()
            return True, new_id
        except pyodbc.IntegrityError as e:
            self.conn.rollback()
            if 'UQ_SparePartMaterials_MaterialPartNumber' in str(e):
                return False, "error_duplicate_material"
            else:
                self.last_error_details = str(e)
                return False, str(e)
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False, str(e)

    def update_material(self, material_id, part_number, code, description, catalog_data, doc_name, user_name):
        """Aggiorna un materiale esistente, includendo l'utente che ha eseguito l'operazione."""
        query = """
                UPDATE eqp.SparePartMaterials
                SET MaterialPartNumber  = ?, \
                    MaterialCode        = ?, \
                    MaterialDescription = ?,
                    CatalogDetail       = ?, \
                    CatalogFileName     = ?, [User] = ?
                WHERE SparePartMaterialId = ?; \
                """
        try:
            self.cursor.execute(query, part_number, code, description, catalog_data, doc_name, user_name, material_id)
            self.conn.commit()
            return True, "Aggiornato."
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False, str(e)

    def delete_material(self, material_id):
        """Cancella un materiale. La cancellazione a cascata (ON DELETE CASCADE) rimuoverà i link."""
        query = "DELETE FROM eqp.SparePartMaterials WHERE SparePartMaterialId = ?;"
        try:
            self.cursor.execute(query, material_id)
            self.conn.commit()
            return True, "Cancellato."
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False, str(e)

    def fetch_linked_equipment(self, material_id):
        """Recupera gli ID delle macchine collegate a un materiale."""
        query = "SELECT EquipmentId FROM eqp.SparePartParents WHERE SparePartMaterialId = ?;"
        try:
            self.cursor.execute(query, material_id)
            return [row.EquipmentId for row in self.cursor.fetchall()]
        except pyodbc.Error as e:
            self.last_error_details = str(e);
            return []

    def update_material_links(self, material_id, equipment_ids, user_name):
        """Sincronizza i collegamenti tra un materiale e le macchine, includendo l'utente."""
        try:
            self.cursor.execute("DELETE FROM eqp.SparePartParents WHERE SparePartId = ?", material_id)

            if equipment_ids:
                insert_query = "INSERT INTO eqp.SparePartParents (SparePartId, EquipmentId, [User]) VALUES (?, ?, ?);"
                # Aggiunge l'utente a ogni tupla di parametri
                params = [(material_id, eq_id, user_name) for eq_id in equipment_ids]
                self.cursor.executemany(insert_query, params)

            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            print(f"Errore durante l'aggiornamento dei link materiali: {e}")
            return False

    def fetch_materials_for_equipment(self, equipment_id):
        """Recupera tutti i materiali collegati a una specifica macchina."""
        query = """
                SELECT m.MaterialPartNumber, m.MaterialCode, m.MaterialDescription
                FROM eqp.SparePartMaterials m
                         INNER JOIN eqp.SparePartParents l ON m.SparePartMaterialId = l.SparePartMaterialId
                WHERE l.EquipmentId = ?
                ORDER BY m.MaterialCode; \
                """
        try:
            self.cursor.execute(query, equipment_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e);
            return []

    def fetch_user_permissions(self, employee_hire_history_id):
        """Recupera i permessi attivi per un dato dipendente."""
        query = """
                SELECT a.AuthorizedUsedId, ap.TranslationValue + ' [' + ap.MenuValue + ']' AS MenuKey
                FROM Employee.dbo.employees e
                         INNER JOIN employee.dbo.EmployeeHireHistory h ON h.EmployeeId = e.EmployeeId
                         LEFT JOIN Traceability_rs.dbo.AutorizedUsers a \
                                   ON h.EmployeeHireHistoryId = a.EmployeeHireHistoryId
                         LEFT JOIN traceability_rs.dbo.AppTranslations ap ON ap.TranslationKey = a.TranslationKey
                WHERE h.EmployeeHireHistoryId = ? \
                  AND a.DateOut IS NULL
                  ORDER BY ap.TranslationValue + ' [' + ap.LanguageCode + ']'; \
                """
        try:
            self.cursor.execute(query, employee_hire_history_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_available_permissions(self, employee_hire_history_id):
        """Recupera i menu a cui un utente NON è ancora abilitato."""
        query = """
        SELECT DISTINCT
               a.TranslationKey AS Translationkey,
               CAST(a.MenuValue AS nvarchar(255)) AS translationvalue
        FROM AppTranslations AS a
        WHERE a.MenuValue IS NOT NULL
          AND NOT EXISTS (
              SELECT 1
              FROM AutorizedUsers AS au
              WHERE au.TranslationKey = a.TranslationKey
                AND au.EmployeeHireHistoryId = ?
                AND au.DateOut IS NULL
          )
        ORDER BY translationvalue, Translationkey;
                """
        try:
            self.cursor.execute(query, employee_hire_history_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def grant_permission(self, employee_hire_history_id, translation_key):
        """Assegna un permesso a un utente."""
        query = "INSERT INTO AutorizedUsers (EmployeeHireHistoryId ,TranslationKey) VALUES (?, ?);"
        query2 = "INSERT INTO [Traceability_RS].[dbo].[EmployeePermissions] ("
        try:
            logger.info(f"HistoryHireId:{employee_hire_history_id} per argomento  {translation_key}")
            self.cursor.execute(query, employee_hire_history_id, translation_key)
            self.conn.commit()
            return True
        except pyodbc.Error:
            self.conn.rollback()
            return False

    def revoke_permission(self, authorized_user_id):
        """Revoca un permesso (soft delete)."""
        query = "UPDATE AutorizedUsers SET DateOut = GETDATE() WHERE AuthorizedUsedId = ?;"
        try:
            self.cursor.execute(query, authorized_user_id)
            self.conn.commit()
            return True
        except pyodbc.Error:
            self.conn.rollback()
            return False

    def check_if_doc_type_is_used(self, category_id):
        """Controlla se una categoria di documenti è usata in almeno un documento."""
        query = "SELECT COUNT(DocumentoId) FROM dbo.DocumentiGenerali WHERE CategoriaId = ?;"
        try:
            count = self.cursor.execute(query, category_id).fetchval()
            return count > 0
        except pyodbc.Error as e:
            print(f"Errore nel controllo uso categoria: {e}")
            return True  # Per sicurezza, in caso di errore, si assume che sia usata

    def add_new_doc_type(self, name, key):
        """Aggiunge una nuova categoria di documenti."""
        query = "INSERT INTO dbo.DocCategorie (NomeCategoria, TranslationKey) VALUES (?, ?);"
        try:
            self.cursor.execute(query, name, key)
            self.conn.commit()
            return True, "Tipo documento aggiunto con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            # Gestisce l'errore di chiave duplicata
            if 'UNIQUE KEY' in str(e):
                return False, "Errore: Esiste già un tipo con questo nome o chiave di traduzione."
            return False, f"Errore database: {e}"

    def update_doc_type(self, category_id, name, key):
        """Aggiorna una categoria di documenti esistente."""
        query = "UPDATE dbo.DocCategorie SET NomeCategoria = ?, TranslationKey = ? WHERE CategoriaId = ?;"
        try:
            self.cursor.execute(query, name, key, category_id)
            self.conn.commit()
            return True, "Tipo documento aggiornato con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            if 'UNIQUE KEY' in str(e):
                return False, "Errore: Esiste già un tipo con questo nome o chiave di traduzione."
            return False, f"Errore database: {e}"

    def delete_doc_type(self, category_id):
        """Cancella una categoria di documenti."""
        query = "DELETE FROM dbo.DocCategorie WHERE CategoriaId = ?;"
        try:
            self.cursor.execute(query, category_id)
            self.conn.commit()
            return True, "Tipo documento cancellato con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def fetch_doc_categories(self):
        """Recupera tutte le categorie di documenti generali per il menu."""
        query = "SELECT CategoriaId, NomeCategoria, TranslationKey FROM dbo.DocCategorie ORDER BY CategoriaId;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore recupero categorie documenti: {e}")
            return []

    def fetch_general_documents(self, category_id):
        """Recupera i metadati dei documenti per una data categoria."""
        query = "SELECT DocumentoId, Titolo, Versione, DataCaricamento, CaricatoDa FROM dbo.DocumentiGenerali WHERE CategoriaId = ? ORDER BY Titolo;"
        try:
            self.cursor.execute(query, category_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def fetch_single_general_document(self, document_id):
        """Recupera tutti i dati di un singolo documento, inclusi i dati binari."""
        query = "SELECT * FROM dbo.DocumentiGenerali WHERE DocumentoId = ?;"
        try:
            self.cursor.execute(query, document_id)
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return None

    def add_general_document(self, category_id, title, desc, version, file_name, data, user):
        """Aggiunge un nuovo documento generale."""
        query = """
                INSERT INTO dbo.DocumentiGenerali (CategoriaId, Titolo, Descrizione, Versione, NomeFile, DatiFile, \
                                                   CaricatoDa)
                VALUES (?, ?, ?, ?, ?, ?, ?); \
                """
        try:
            self.cursor.execute(query, category_id, title, desc, version, file_name, data, user)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False

    def update_general_document(self, doc_id, title, desc, version, file_name, data, user):
        """Aggiorna un documento generale esistente."""
        query = """
                UPDATE dbo.DocumentiGenerali
                SET Titolo          = ?, \
                    Descrizione     = ?, \
                    Versione        = ?, \
                    NomeFile        = ?, \
                    DatiFile        = ?, \
                    CaricatoDa      = ?, \
                    DataCaricamento = GETDATE()
                WHERE DocumentoId = ?; \
                """
        try:
            self.cursor.execute(query, title, desc, version, file_name, data, user, doc_id)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False

    def delete_general_document(self, doc_id):
        """Cancella un documento generale."""
        query = "DELETE FROM dbo.DocumentiGenerali WHERE DocumentoId = ?;"
        try:
            self.cursor.execute(query, doc_id)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False

    def authenticate_and_authorize(self, user_id, password, menu_translation_key):
        """
        Esegue l'autenticazione e controlla l'autorizzazione per una specifica funzione.
        Restituisce l'intera riga del DB se l'utente e la password sono corretti, altrimenti None.
        La riga conterrà AuthorizedUsedId (che può essere NULL se non autorizzato).
        """
        query = """
                SELECT u.NomeUser, \
                       ISNULL(e.EmployeeName + ' ' + e.EmployeeSurname, '#ND') as EmployeeName, \
                       u.pass, \
                       a.AuthorizedUsedId
                FROM resetservices.dbo.tbuserkey as U
                         INNER JOIN employee.dbo.employees as e ON e.EmployeeId = u.idanga
                         INNER JOIN employee.dbo.EmployeeHireHistory as h ON e.EmployeeId = h.EmployeeId
                         LEFT JOIN dbo.AutorizedUsers as a \
                                   ON a.Employeehirehistoryid = h.EmployeeHireHistoryId AND a.TranslationKey = ?
                WHERE h.EndWorkDate IS NULL \
                  AND h.employeerid = 2 \
                  AND u.Nomeuser = ? \
                  AND u.Pass = ? \
                  AND a.DateOut IS NULL; \
                """
        try:
            # L'ordine dei parametri è fondamentale: TranslationKey, Nomeuser, Pass
            logger.info(f"Chiave per accesso speciale:{menu_translation_key} per user:{user_id}")

            self.cursor.execute(query, menu_translation_key, user_id, password)
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            print(f"Error during authentication/authorization: {e}")
            self.last_error_details = str(e)
            return None

    def fetch_maintenance_cycles(self):
        """Recupera tutti i cicli di manutenzione programmati."""
        query = "SELECT ProgrammedInterventionId, TimingDescriprion, TimingValue FROM eqp.ProgrammedInterventions ORDER BY TimingDescriprion;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero dei cicli di manutenzione: {e}")
            return []

    def check_if_cycle_is_used(self, intervention_id):
        """Controlla se un ciclo di manutenzione è usato in almeno un log."""
        # Un ciclo è usato se esiste un compito associato ad esso che è stato registrato in LogManutenzioni
        query = """
                SELECT COUNT(lm.LogId)
                FROM eqp.LogManutenzioni lm
                         INNER JOIN eqp.CompitiManutenzione cm ON lm.CompitoId = cm.CompitoId
                WHERE cm.ProgrammedInterventionId = ?; \
                """
        try:
            count = self.cursor.execute(query, intervention_id).fetchval()
            return count > 0
        except pyodbc.Error as e:
            print(f"Errore nel controllo uso ciclo: {e}")
            return True  # Per sicurezza, in caso di errore, si assume che sia usato

    def add_new_maintenance_cycle(self, description, value):
        """Aggiunge un nuovo ciclo di manutenzione."""
        query = "INSERT INTO eqp.ProgrammedInterventions (TimingDescriprion, TimingValue) VALUES (?, ?);"
        try:
            self.cursor.execute(query, description, value)
            self.conn.commit()
            return True, "Ciclo aggiunto con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def update_maintenance_cycle(self, intervention_id, description, value):
        """Aggiorna un ciclo di manutenzione esistente."""
        query = "UPDATE eqp.ProgrammedInterventions SET TimingDescriprion = ?, TimingValue = ? WHERE ProgrammedInterventionId = ?;"
        try:
            self.cursor.execute(query, description, value, intervention_id)
            self.conn.commit()
            return True, "Ciclo aggiornato con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def delete_maintenance_cycle(self, intervention_id):
        """Cancella un ciclo di manutenzione."""
        query = "DELETE FROM eqp.ProgrammedInterventions WHERE ProgrammedInterventionId = ?;"
        try:
            self.cursor.execute(query, intervention_id)
            self.conn.commit()
            return True, "Ciclo cancellato con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def fetch_authorized_employees(self):
        """Recupera la lista dei dipendenti autorizzati a fare segnalazioni."""
        query = """
                SELECT eh.EmployeeHireHistoryId, UPPER(e.EmployeeSurname + ' ' + e.EmployeeName) AS Employ
                FROM employee.dbo.employees e
                         INNER JOIN employee.dbo.EmployeeHireHistory eh \
                                    ON e.EmployeeId = eh.EmployeeId AND eh.EndWorkDate IS NULL
                         INNER JOIN employee.dbo.employeers er \
                                    ON eh.EmployeerId = er.EmployeerId AND er.EmployeerFiscalCode = 'RO35713341'
                ORDER BY UPPER(e.EmployeeSurname + ' ' + e.EmployeeName); \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore recupero dipendenti autorizzati: {e}")
            return []

    def fetch_submission_types(self, lang_code):
        """Recupera i tipi di segnalazione tradotti in base alla lingua selezionata."""
        # La tabella TipiSegnalazione deve essere quella corretta, es. dbo.TipiSegnalazione
        # Assicurati che i nomi delle tabelle e delle colonne siano corretti.
        query = """
                SELECT t.TipoSegnalazioneId, t.NomeTipo
                FROM employee.dbo.TipiSegnalazione AS t
                         INNER JOIN employee.dbo.Languages L ON t.LanguageID = l.LanguageID
                WHERE l.LanguageAcronim = ?
                ORDER BY t.NomeTipo; \
                """
        try:
            print(f"DEBUG: Sto cercando tipi di segnalazione con il codice lingua: '{lang_code}'")
            self.cursor.execute(query, lang_code)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore recupero tipi di segnalazione per lingua '{lang_code}': {e}")
            self.last_error_details = str(e)
            return []

    def add_new_submission(self, type_id, title, desc, location, employee_id, attachments):
        """Salva una nuova segnalazione e i suoi allegati in una transazione."""
        try:
            # 1. Inserisce la segnalazione principale e ottiene il suo ID
            insert_submission_sql = """
                                    INSERT INTO Employee.dbo.Segnalazioni (TipoSegnalazioneId, Titolo, Descrizione, Luogo, IdDipendente)
                                        OUTPUT INSERTED.SegnalazioneId
                                    VALUES (?, ?, ?, ?, ?); \
                                    """
            new_submission_id = self.cursor.execute(
                insert_submission_sql, type_id, title, desc, location, employee_id
            ).fetchval()

            if not new_submission_id:
                raise Exception("Creazione segnalazione fallita, ID non restituito.")

            # 2. Inserisce il record nella tabella delle verifiche con stato 5 - da analizzare
            insert_status_sql = """
                            INSERT INTO Employee.dbo.SegnalazioneStati
                                (SegnalazioneId, SegnalazioniTipoStatoId, Nota, OperatoDa)
                            VALUES (?, 5, 'Trigger after insert', 'System'); \
                             """
            self.cursor.execute(insert_status_sql, new_submission_id)

            # 3. Se ci sono allegati, li inserisce uno per uno
            if attachments:
                insert_attachment_sql = """
                                        INSERT INTO Employee.dbo.SegnalazioneAllegati (SegnalazioneId, NomeFile, DatiFile)
                                        VALUES (?, ?, ?); \
                                        """
                for attachment in attachments:
                    self.cursor.execute(insert_attachment_sql, new_submission_id, attachment['name'],
                                        attachment['data'])

            # 3. Se tutto è andato bene, conferma la transazione
            self.conn.commit()
            return True, "Segnalazione registrata con successo."

        except Exception as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False, f"Errore durante il salvataggio: {e}"

    def fetch_brands_with_company_name(self):
        """Recupera tutti i brand con il nome del produttore associato."""
        query = """
                SELECT b.EquipmentBrandId, \
                       b.Brand, \
                       b.BrandLogo, \
                       s.acronimo AS CompanyName, \
                       s.idsoc    AS CompanyId
                FROM eqp.EquipmentBrands b \
                         INNER JOIN \
                     resetservices.dbo.tbsocieta s ON b.CompanyId = s.idsoc
                ORDER BY b.Brand; \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero dei brand: {e}")
            return []

    def add_new_brand(self, brand_name, company_id, logo_data):
        """Aggiunge un nuovo brand."""
        query = "INSERT INTO eqp.EquipmentBrands (Brand, CompanyId, BrandLogo) VALUES (?, ?, ?);"
        try:
            # Assicura che company_id sia None se non è un numero valido
            company_id_to_save = int(company_id) if company_id is not None else None
            self.cursor.execute(query, brand_name, company_id_to_save, logo_data)
            self.conn.commit()
            return True, "Brand aggiunto con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            if 'UNIQUE' in str(e) or 'duplicate' in str(e):
                return False, "Errore: Esiste già un brand con questo nome."
            return False, f"Errore database: {e}"

    def update_brand(self, brand_id, brand_name, company_id, logo_data):
        """Aggiorna un brand esistente."""
        query = "UPDATE eqp.EquipmentBrands SET Brand = ?, CompanyId = ?, BrandLogo = ? WHERE EquipmentBrandId = ?;"
        try:
            company_id_to_save = int(company_id) if company_id is not None else None
            self.cursor.execute(query, brand_name, company_id_to_save, logo_data, brand_id)
            self.conn.commit()
            return True, "Brand aggiornato con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def fetch_suppliers(self):
        """Recupera la lista dei fornitori."""
        query = "SELECT idsoc, acronimo, nazione FROM resetservices.dbo.tbsocieta WHERE acronimo IS NOT NULL ORDER BY acronimo;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero fornitori: {e}")
            return []

    def fetch_currencies(self):
        """Recupera la lista delle valute attive."""
        query = "SELECT IdValuta, [desc] FROM resetservices.dbo.TbValute WHERE loadexchange = 1 ORDER BY [desc];"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero valute: {e}")
            return []

    def add_new_supplier(self, denom_soc, nazione, cui, id_valuta):
        """Aggiunge un nuovo fornitore dopo aver controllato che la P.IVA non esista già."""
        # 1. Controlla se la Partita IVA (cui) esiste già
        check_query = "SELECT COUNT(*) FROM resetservices.dbo.tbsocieta WHERE cui = ?;"
        insert_query = """
                       INSERT INTO resetservices.dbo.tbsocieta (DenomSoc, Nazione, cui, IdValuta, Appruved)
                       VALUES (?, ?, ?, ?, 1); \
                       """
        try:
            count = self.cursor.execute(check_query, cui).fetchval()
            if count > 0:
                return False, "Errore: Partita IVA già presente nel database."

            # 2. Se non esiste, procedi con l'inserimento
            self.cursor.execute(insert_query, denom_soc, nazione, cui, id_valuta)
            self.conn.commit()
            return True, "Fornitore aggiunto con successo."

        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False, f"Errore database: {e}"

    def fetch_tasks_for_editing(self, intervention_id, equipment_id):
        """Recupera i compiti per un intervento e una macchina specifici."""
        query = """
                SELECT CompitoId, NomeCompito, Categoria, DescrizioneCompito, LinkedDocument
                FROM eqp.CompitiManutenzione
                WHERE ProgrammedInterventionId = ? \
                  AND EquipmentId = ?
                ORDER BY Ordine, CompitoId; \
                """
        try:
            self.cursor.execute(query, intervention_id, equipment_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero dei task per la modifica: {e}")
            self.last_error_details = str(e)
            return []

    def update_maintenance_task(self, task_id, equipment_id, category, task_name, description, document_data):
        """Aggiorna un compito di manutenzione esistente, incluso l'EquipmentId."""
        query = """
                UPDATE eqp.CompitiManutenzione
                SET EquipmentId        = ?, \
                    Categoria          = ?, \
                    NomeCompito        = ?, \
                    DescrizioneCompito = ?, \
                    LinkedDocument     = ?
                WHERE CompitoId = ?; \
                """
        try:
            self.cursor.execute(query, equipment_id, category, task_name, description, document_data, task_id)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False

    def delete_maintenance_tasks(self, task_ids_to_delete):
        """Cancella una lista di compiti dal database."""
        if not task_ids_to_delete:
            return True  # Nessuna operazione da eseguire

        # Crea i segnaposto '?' per la clausola IN
        placeholders = ', '.join('?' for _ in task_ids_to_delete)
        query = f"DELETE FROM eqp.CompitiManutenzione WHERE CompitoId IN ({placeholders});"

        try:
            self.cursor.execute(query, task_ids_to_delete)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False

    def fetch_maintenance_interventions(self):
        """Recupera i tipi di intervento di manutenzione per la selezione."""
        query = """
                SELECT [ProgrammedInterventionId], [TimingDescriprion]
                FROM [Traceability_RS].[eqp].[ProgrammedInterventions]
                ORDER BY TimingDescriprion; \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero dei tipi di intervento: {e}")
            return []

    def insert_new_maintenance_task(self, intervention_id, equipment_id, category, task_name, description, order,
                                    document_data=None):
        """Inserisce un singolo nuovo compito, ora direttamente collegato a una macchina."""
        query = """
                INSERT INTO eqp.CompitiManutenzione
                (ProgrammedInterventionId, EquipmentId, Categoria, NomeCompito, DescrizioneCompito, Ordine, \
                 LinkedDocument)
                VALUES (?, ?, ?, ?, ?, ?, ?); \
                """
        try:
            self.cursor.execute(query, intervention_id, equipment_id, category, task_name, description, order,
                                document_data)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            print(f"Errore nell'inserimento del nuovo task: {e}")
            self.last_error_details = str(e)
            return False
    def fetch_report_maintainers(self):
        """Recupera la lista dei manutentori che hanno eseguito almeno una manutenzione."""
        query = """
                SELECT DISTINCT UPPER(e.EmployeeName + ' ' + e.EmployeeSurname) AS Manutentore
                FROM resetservices.dbo.tbuserkey AS U
                         INNER JOIN employee.dbo.employees AS e ON e.EmployeeId = u.idanga AND U.DataOut IS NULL
                         INNER JOIN employee.dbo.EmployeeHireHistory AS h \
                                    ON e.EmployeeId = h.EmployeeId AND h.EndWorkDate IS NULL AND h.employeerid = 2
                         INNER JOIN Traceability_rs.EQP.LogManutenzioni LM ON lm.UserName COLLATE DATABASE_DEFAULT = \
                                                                              UPPER(e.EmployeeName + ' ' + e.EmployeeSurname)
                ORDER BY UPPER(e.EmployeeName + ' ' + e.EmployeeSurname); \
                """
        try:
            self.cursor.execute(query)
            # Restituiamo una lista semplice di nomi
            return [row.Manutentore for row in self.cursor.fetchall()]
        except pyodbc.Error as e:
            print(f"Errore nel recupero dei manutentori per report: {e}")
            return []

    def fetch_report_dates(self):
        """Recupera le date uniche in cui sono state fatte manutenzioni."""
        query = """
                SELECT DISTINCT CAST(lm.datestart AS DATE) AS DateMaintenance
                FROM Traceability_rs.EQP.LogManutenzioni lm
                ORDER BY CAST(lm.datestart AS DATE) DESC; \
                """
        try:
            self.cursor.execute(query)
            # Restituiamo una lista di oggetti data
            return [row.DateMaintenance for row in self.cursor.fetchall()]
        except pyodbc.Error as e:
            print(f"Errore nel recupero delle date per report: {e}")
            return []

    def search_maintenance_report(self, equipment_id=None, maintenance_date=None, maintainer_name=None):
        """Esegue la ricerca per il report di manutenzione con filtri opzionali."""
        # Query di base
        base_query = """
                     SELECT ROW_NUMBER() OVER (ORDER BY cm.ordine, UPPER(ISNULL(e.EmployeeName + ' ' + e.EmployeeSurname, '#ND'))) AS [Row],
                UPPER(ISNULL(e.EmployeeName + ' ' + e.EmployeeSurname, '#ND')) AS EmployeeName,
                cm.NomeCompito,
                eq.InternalName AS EquipmentName,
                cm.DescrizioneCompito,
                FORMAT(lm.datestart, 'd', 'ro-ro') AS DataIntervento,
                CONVERT(VARCHAR(8), lm.datestart, 108) AS InizioOraIntervento,
                CONVERT(VARCHAR(8), lm.datestop, 108) AS FineIntervento,
                DATEDIFF(MINUTE, lm.DateStart, lm.DateStop) AS [DurataInterventoInMin]
                     FROM Traceability_rs.EQP.LogManutenzioni LM
                         INNER JOIN employee.dbo.employees AS e \
                     ON lm.UserName COLLATE DATABASE_DEFAULT = UPPER (e.EmployeeName + ' ' + e.EmployeeSurname)
                         INNER JOIN resetservices.dbo.tbuserkey AS U ON e.EmployeeId = u.idanga AND U.DataOut IS NULL
                         INNER JOIN employee.dbo.EmployeeHireHistory AS h ON e.EmployeeId = h.EmployeeId AND h.EndWorkDate IS NULL AND h.employeerid = 2
                         INNER JOIN traceability_rs.eqp.CompitiManutenzione cm ON lm.CompitoId = cm.CompitoId
                         INNER JOIN traceability_rs.eqp.Equipments eq ON eq.EquipmentID = lm.EquipmentID \
                     """

        # Costruzione dinamica della clausola WHERE
        where_clauses = []
        params = []

        if equipment_id:
            where_clauses.append("eq.EquipmentId = ?")
            params.append(equipment_id)

        if maintenance_date:
            where_clauses.append("CAST(lm.dateStart AS DATE) = ?")
            params.append(maintenance_date)

        if maintainer_name:
            where_clauses.append("UPPER(e.EmployeeName + ' ' + e.EmployeeSurname) = ?")
            params.append(maintainer_name.upper())

        # Combina la query finale
        final_query = base_query
        if where_clauses:
            final_query += " WHERE " + " AND ".join(where_clauses)

        final_query += " ORDER BY lm.datestart, EmployeeName, cm.ordine;"

        try:
            self.cursor.execute(final_query, params)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nella ricerca del report di manutenzione: {e}")
            self.last_error_details = str(e)
            return []

    def add_new_spare_part(self, material_part_number, material_code, material_description):
        """
        Inserisce una nuova parte di ricambio in eqp.SparePartMaterials,
        imposta toberevizited a 1 e restituisce il nuovo ID.
        """
        query = """
                INSERT INTO eqp.SparePartMaterials (MaterialPartNumber, MaterialCode, MaterialDescription, toberevizited)
                    OUTPUT INSERTED.SparePartMaterialId
                VALUES (?, ?, ?, 1);
                """
        try:
            # Usiamo fetchval() che è perfetto per recuperare un singolo valore
            # da una query che restituisce una riga e una colonna, come il nostro OUTPUT.
            new_id = self.cursor.execute(query, material_part_number, material_code, material_description).fetchval()

            if new_id:
                self.conn.commit()
                return new_id
            else:
                # Questo caso è improbabile con OUTPUT, ma è una buona pratica gestirlo
                self.conn.rollback()
                self.last_error_details = "Inserimento nel DB riuscito ma impossibile recuperare il nuovo ID."
                return None

        except pyodbc.Error as e:
            self.conn.rollback()
            print(f"Errore nell'aggiunta di una nuova parte di ricambio: {e}")
            self.last_error_details = str(e)
            return None

    def fetch_setting(self, attribute_name):
        """Recupera un valore dalla tabella Settings."""
        query = "select [value] from traceability_rs.dbo.Settings where atribute = ?;"
        try:
            self.cursor.execute(query, attribute_name)
            row = self.cursor.fetchone()
            return row.value if row else None
        except pyodbc.Error as e:
            print(f"Errore nel recupero impostazione '{attribute_name}': {e}")
            return None
        # NUOVO METODO: Aggiunge una nuova parte di ricambio al catalogo

    # def add_new_spare_part(self, material_part_number, material_code=None, material_description=None,
    #                        to_be_revizited=1):
    #     """Inserisce una nuova parte in eqp.SparePartMaterials e restituisce il nuovo ID."""
    #     # Assumiamo che la tabella abbia un IDENTITY ID (SparePartMaterialId)
    #     query = """
    #             INSERT INTO eqp.SparePartMaterials (MaterialPartNumber, MaterialCode, MaterialDescription,toberevizited)
    #             OUTPUT INSERTED.SparePartMaterialId
    #             VALUES (?, ?, ?, 1);
    #             """
    #     try:
    #         # Esegui l'INSERT
    #         self.cursor.execute(query, material_part_number, material_code, material_description)
    #
    #         # Poiché abbiamo usato OUTPUT, l'INSERT ora restituisce un risultato che possiamo leggere con fetchval().
    #         new_id = self.cursor.fetchval()
    #
    #         if new_id:
    #             self.conn.commit()
    #             return new_id
    #         else:
    #             self.conn.rollback()
    #             self.last_error_details = "Inserimento riuscito ma impossibile recuperare il nuovo ID."
    #             return None

        except pyodbc.Error as e:
            self.conn.rollback()
            print(f"Errore nell'aggiunta nuova parte di ricambio: {e}")
            self.last_error_details = str(e)
            return None

    def insert_spare_part_request(self, equipment_id, spare_part_id, quantity, notes, requested_by):
        """Inserisce una nuova richiesta di parti di ricambio o intervento."""
        query = """
                INSERT INTO eqp.RequestSpareParts
                (EquipmentId, SparePartMaterialId, Quantity, Note, RequestedBy, DateRequest, Solved)
                VALUES (?, ?, ?, ?, ?, GETDATE(), 0)
                """
        try:
            self.cursor.execute(query, equipment_id, spare_part_id, quantity, notes, requested_by)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            print(f"Errore nell'inserimento richiesta: {e}")
            self.last_error_details = str(e)
            return False

    def fetch_and_open_document_by_task_id(self, task_id):
        """Recupera e apre il documento associato a un CompitoId."""

        self.last_error_details = ""

        # Query fornita dall'utente. Aggiungiamo FileName e FileType necessari per l'apertura.
        # Aggiungiamo ORDER BY per assicurarci di prendere il documento più recente se la JOIN ne producesse più di uno.
        query = """
                select emd.DocumentSource, emd.FileName, emd.FileType
                from Traceability_rs.eqp.EquipmentMantainanceDocs emd
                         left join Traceability_rs.eqp.CompitiManutenzione CM \
                                   on cm.ProgrammedInterventionId = emd.ProgrammedInterventionId
                where cm.compitoid = ?
                -- Potresti voler aggiungere AND emd.DateOut IS NULL se vuoi mostrare solo documenti attivi
                ORDER BY emd.DateSys DESC
                """
        try:
            self.cursor.execute(query, task_id)
            # Usiamo fetchone() per prendere solo il primo risultato (il più recente)
            row = self.cursor.fetchone()

            if row and row.DocumentSource:
                binary_data = row.DocumentSource

                # --- Logica Gestione File Temporaneo (Robusta) ---

                # 1. Determina estensione e prefisso
                file_extension = row.FileType if row.FileType else os.path.splitext(row.FileName)[1]
                if not file_extension:
                    print(f"Attenzione: Estensione mancante per task ID {task_id}. Usando default .pdf")
                    file_extension = '.pdf'  # Default ragionevole

                if not file_extension.startswith('.'):
                    file_extension = '.' + file_extension

                temp_prefix = "task_doc_"
                if row.FileName:
                    # Pulisce il nome del file (rimuove caratteri non sicuri) per usarlo come prefisso
                    safe_name = re.sub(r'[^\w\-]', '_', os.path.splitext(row.FileName)[0])
                    temp_prefix = safe_name[:50] + "_"

                # 2. Crea e scrivi file temporaneo
                # delete=False è necessario affinché il programma esterno possa aprirlo
                temp_file = tempfile.NamedTemporaryFile(prefix=temp_prefix, delete=False, suffix=file_extension)
                temp_file.write(binary_data)
                temp_file.close()  # Chiudi handle Python per permettere apertura esterna

                print(f"Apertura documento per compito ID {task_id}: {temp_file.name}")

                # 3. Apertura File (Cross-platform)
                try:
                    if sys.platform == "win32":
                        # Metodo per Windows (es. apre con Adobe Reader o Word/Excel predefinito)
                        os.startfile(temp_file.name)
                    else:
                        # Fallback per macOS e Linux
                        opener = "open" if sys.platform == "darwin" else "xdg-open"
                        subprocess.call([opener, temp_file.name])
                except Exception as open_e:
                    self.last_error_details = f"Errore OS nell'apertura del file: {open_e}"
                    return False

                return True
            else:
                # Caso in cui la query non restituisce risultati (nessun documento collegato)
                self.last_error_details = f"Nessun documento trovato associato al compito ID {task_id}."
                return False

        except pyodbc.Error as e:
            print(f"Errore durante il recupero del documento dal DB per task ID {task_id}: {e}")
            self.last_error_details = f"Errore Database: {e}"
            return False
        except Exception as e:
            # Gestione errori (es. permessi scrittura file temporaneo)
            print(f"Errore imprevisto durante la gestione del file temporaneo: {e}")
            self.last_error_details = f"Errore Applicazione (File System): {e}"
            return False

    def fetch_spare_parts(self):
        """Recupera la lista di parti di ricambio e servizi disponibili."""
        # ATTENZIONE: Assicurati che i nomi delle colonne corrispondano alla tua tabella eqp.SparePartMaterials.
        query = """
                SELECT SparePartMaterialId, MaterialPartNumber, MaterialCode, MaterialDescription
                FROM eqp.SparePartMaterials
                ORDER BY MaterialCode \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero parti di ricambio: {e}")
            self.last_error_details = str(e)
            return []

    def __init__(self, conn_str):
        self.conn_str = conn_str
        self.conn = None
        self.cursor = None
        self.last_error_details = ""

    def connect(self):
        try:
            # Usiamo autocommit=False per gestire le transazioni manualmente (commit/rollback)
            self.conn = pyodbc.connect(self.conn_str, autocommit=False)
            self.cursor = self.conn.cursor()
            return True
        except pyodbc.Error as ex:
            # L'errore specifico verrà gestito dalla classe App che chiama questo metodo
            self.last_error_details = str(ex)
            print(f"Database Connection Error: {ex}")
            return False

    def disconnect(self):
        """Closes the cursor and connection safely, preventing errors if called multiple times."""
        if self.cursor:
            self.cursor.close()
            self.cursor = None  # Set to None after closing
        if self.conn:
            self.conn.close()
            self.conn = None  # Set to None after closing

        # NUOVO METODO: Cerca documenti esistenti attivi che corrispondono ai parametri

    def fetch_and_open_maintenance_document(self, document_id):
        """Recupera i dati binari di un documento di manutenzione dal DB, lo salva temporaneamente e lo apre."""

        self.last_error_details = ""  # Resetta l'errore

        try:
            # Seleziona i dati binari (DocumentSource) e i metadati (FileType, FileName)
            sql_select = """
                         SELECT DocumentSource, FileName, FileType
                         FROM eqp.EquipmentMantainanceDocs
                         WHERE EquipmentDocumentationId = ? \
                         """
            self.cursor.execute(sql_select, document_id)
            row = self.cursor.fetchone()

            if row and row.DocumentSource:
                binary_data = row.DocumentSource

                # --- 1. Gestione Robusta dell'Estensione e del Nome File Temporaneo ---

                # Determina l'estensione: Priorità a FileType, fallback su FileName, default a .pdf
                file_extension = row.FileType if row.FileType else os.path.splitext(row.FileName)[1]
                if not file_extension:
                    print(f"Attenzione: Estensione mancante per doc ID {document_id}. Usando default .pdf")
                    file_extension = '.pdf'  # Default ragionevole

                # Assicurarsi che l'estensione inizi con '.'
                if not file_extension.startswith('.'):
                    file_extension = '.' + file_extension

                # Usa una versione pulita del nome file originale come prefisso per facilitare l'identificazione
                temp_prefix = "doc_"
                if row.FileName:
                    # Pulisce il nome del file (rimuove caratteri non sicuri)
                    safe_name = re.sub(r'[^\w\-]', '_', os.path.splitext(row.FileName)[0])
                    temp_prefix = safe_name[:50] + "_"  # Limita la lunghezza e aggiunge separatore

                # --- 2. Creazione File Temporaneo ---

                # delete=False è necessario affinché il programma esterno possa aprirlo prima che Python lo elimini
                temp_file = tempfile.NamedTemporaryFile(prefix=temp_prefix, delete=False, suffix=file_extension)
                temp_file.write(binary_data)
                # Chiudi il file handle in Python affinché il sistema operativo possa aprirlo
                temp_file.close()

                print(f"Apertura del file temporaneo: {temp_file.name}")

                # --- 3. Apertura File (Cross-platform) ---
                try:
                    if sys.platform == "win32":
                        # Metodo specifico per Windows
                        os.startfile(temp_file.name)
                    else:
                        # Fallback per macOS e Linux
                        opener = "open" if sys.platform == "darwin" else "xdg-open"
                        subprocess.call([opener, temp_file.name])
                except Exception as open_e:
                    self.last_error_details = f"Errore OS nell'apertura del file: {open_e}"
                    return False

                return True
            else:
                self.last_error_details = f"Documento ID {document_id} non trovato o dati binari assenti nel database."
                return False

        except pyodbc.Error as e:
            print(f"Errore durante il recupero del documento dal DB: {e}")
            self.last_error_details = f"Errore Database: {e}"
            return False
        except Exception as e:
            # Gestione errori generici (es. permessi scrittura file temporaneo)
            print(f"Errore imprevisto durante la gestione del file temporaneo: {e}")
            self.last_error_details = f"Errore Applicazione (File System): {e}"
            return False

    def fetch_programmed_interventions(self):
        """Recupera tutti gli interventi programmati (Tipi di manutenzione)."""
        query = """
                SELECT [ProgrammedInterventionId]
                      ,[TimingDescriprion]
                      ,[TimingValue]
                FROM [Traceability_RS].[eqp].[ProgrammedInterventions]
                ORDER BY [TimingValue] -- Ordinamento per facilitare la lettura
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero degli interventi programmati: {e}")
            return []

        # Assicuriamoci che DateOut sia NULL per il nuovo documento.
        insert_query = """
                       INSERT INTO eqp.EquipmentMantainanceDocs
                       (EquipmentId, ProgrammedInterventionId, EquipmentMaintenanceDocTypeId, DocDescription, FileName, \
                        FileType, DocumentSource, UploadedBy, DateSys, DateOut)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), NULL) \
                       """
        try:
            # --- INIZIO TRANSAZIONE ATOMICA ---
            # (Poiché pyodbc è stato connesso con autocommit=False, siamo già in una transazione)

            # 1. Se richiesto, invalida i vecchi documenti (UPDATE)
            if invalidate_ids:
                if not self._invalidate_maintenance_docs(invalidate_ids):
                    # Se l'UPDATE fallisce, annulla tutto (ROLLBACK) e restituisci False
                    self.conn.rollback()
                    return False

            # 2. Inserisci il nuovo documento (INSERT)
            self.cursor.execute(insert_query, equipment_id, intervention_id, doc_type_id, description, file_name,
                                file_type, binary_data, user_name)

            # 3. Conferma la transazione (COMMIT)
            self.conn.commit()
            return True

            # --- FINE TRANSAZIONE ATOMICA ---

        except pyodbc.Error as e:
            self.conn.rollback()  # Annulla tutto in caso di errore nell'INSERT
            self.last_error_details = str(e)
            print(f"Errore SQL nella transazione replace_maintenance_document: {e}")
            return False

    def search_equipments(self, filters):
        """
        Esegue una ricerca dinamica delle macchine basata su un dizionario di filtri.
        """
        query = """
                SELECT eq.EquipmentId, eq.InternalName, eq.SerialNumber, b.Brand, et.EquipmentType, pp.ParentPhaseName
                FROM eqp.Equipments eq
                         LEFT JOIN eqp.EquipmentBrands b ON eq.BrandId = b.EquipmentBrandId
                         LEFT JOIN eqp.EquipmentTypes et ON eq.EquipmentTypeId = et.EquipmentTypeId
                         LEFT JOIN dbo.ParentPhases pp ON eq.ParentPhaseId = pp.IDParentPhase
                """
        where_clauses = []
        params = []

        if filters.get('brand_id'):
            where_clauses.append("eq.BrandId = ?")
            params.append(filters['brand_id'])

        if filters.get('type_id'):
            where_clauses.append("eq.EquipmentTypeId = ?")
            params.append(filters['type_id'])

        if filters.get('phase_id'):
            where_clauses.append("eq.ParentPhaseId = ?")
            params.append(filters['phase_id'])

        if filters.get('search_text'):
            # Cerca il testo nel nome, seriale o inventario
            where_clauses.append("(eq.InternalName LIKE ? OR eq.SerialNumber LIKE ? OR eq.InventoryNumber LIKE ?)")
            search_param = f"%{filters['search_text']}%"
            params.extend([search_param, search_param, search_param])

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        query += " ORDER BY eq.InternalName;"

        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nella ricerca macchine: {e}")
            return []

    def fetch_full_equipment_details(self, equipment_id):
        """
        Recupera tutte le informazioni correlate a una singola macchina.
        """
        details = {}
        try:
            # 1. Dati anagrafici
            master_query = """
                           SELECT eq.*, b.Brand, et.EquipmentType, pp.ParentPhaseName
                           FROM eqp.Equipments eq
                                    LEFT JOIN eqp.EquipmentBrands b ON eq.BrandId = b.EquipmentBrandId
                                    LEFT JOIN eqp.EquipmentTypes et ON eq.EquipmentTypeId = et.EquipmentTypeId
                                    LEFT JOIN dbo.ParentPhases pp ON eq.ParentPhaseId = pp.IDParentPhase
                           WHERE eq.EquipmentId = ?
                           """
            details['master'] = self.cursor.execute(master_query, equipment_id).fetchone()

            # 2. Log delle modifiche
            changes_query = "SELECT Changed, WhoChange, DateChange FROM eqp.EquipmentChanges WHERE EquipmentId = ? ORDER BY DateChange DESC"
            details['changes'] = self.cursor.execute(changes_query, equipment_id).fetchall()

            # 3. Documenti di manutenzione
            # NOTA: Selezioniamo FileName invece di DocumentSource (che è binario e pesante) per l'elenco
            docs_query = "SELECT FileName, UploadedBy, DateSys FROM eqp.EquipmentMantainanceDocs WHERE EquipmentId = ? ORDER BY DateSys DESC"
            details['docs'] = self.cursor.execute(docs_query, equipment_id).fetchall()

            # 4. Schede di manutenzione compilate
            logs_query = "SELECT DataEsecuzione, IdManutentore, NoteGenerali FROM dbo.LogManutenzioni WHERE EquipmentId = ? ORDER BY DataEsecuzione DESC"
            details['logs'] = self.cursor.execute(logs_query, equipment_id).fetchall()

            return details
        except pyodbc.Error as e:
            print(f"Errore nel recupero dettagli completi macchina: {e}")
            return None

    def fetch_all_equipments(self):
        """Recupera ID, Nome Interno e Seriale di tutte le macchine per la selezione."""
        #query = "SELECT EquipmentId, InternalName, SerialNumber FROM eqp.Equipments ORDER BY InternalName, SerialNumber;"
        query = "SELECT  distinct e.EquipmentId, InternalName +  + iif(cm.CompitoId is null, '',' (*) ') As InternalName, SerialNumber FROM eqp.Equipments E left join [eqp].[CompitiManutenzione] CM on e.EquipmentId=cm.EquipmentId ORDER BY InternalName, SerialNumber;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero delle macchine: {e}")
            return []

    def fetch_equipment_details(self, equipment_id):
        """Recupera i dettagli di una singola macchina per la modifica."""
        query = "SELECT ParentPhaseId, InternalName, SerialNumber FROM eqp.Equipments WHERE EquipmentId = ?;"
        try:
            self.cursor.execute(query, equipment_id)
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            print(f"Errore nel recupero dei dettagli macchina: {e}")
            return None

    def update_and_log_equipment_changes(self, equipment_id, new_phase_id, new_internal_name, new_serial,
                                         change_log_string, user_name):
        """Aggiorna la macchina e registra la modifica in una transazione."""
        try:
            # 1. Aggiorna la tabella principale
            update_query = """
                           UPDATE eqp.Equipments
                           SET ParentPhaseId = ?,
                               InternalName  = ?,
                               SerialNumber  = ?
                           WHERE EquipmentId = ?;
                           """
            self.cursor.execute(update_query, new_phase_id, new_internal_name, new_serial, equipment_id)

            # 2. Inserisce il log delle modifiche
            log_query = """
                        INSERT INTO eqp.EquipmentChanges (EquipmentId, Changed, WhoChange, DateChange)
                        VALUES (?, ?, ?, GETDATE());
                        """
            self.cursor.execute(log_query, equipment_id, change_log_string, user_name)

            # 3. Se entrambe le operazioni vanno a buon fine, conferma la transazione
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            # Se una delle due query fallisce, annulla tutto
            self.conn.rollback()
            self.last_error_details = str(e)
            print(f"Errore durante l'aggiornamento della macchina: {e}")
            return False

    def fetch_brands(self):
        """Recupera tutti i brand delle macchine."""
        query = "SELECT EquipmentBrandId, Brand FROM eqp.EquipmentBrands ORDER BY Brand;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero dei brand: {e}")
            return []

    def fetch_equipment_types(self):
        """Recupera tutti i tipi di macchine."""
        query = "SELECT EquipmentTypeId, EquipmentType FROM eqp.EquipmentTypes ORDER BY EquipmentType;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero dei tipi di macchine: {e}")
            return []

    def fetch_parent_phases_for_maintenance(self):
        """Recupera tutte le fasi di produzione."""
        query = "SELECT IDParentPhase, ParentPhaseName FROM dbo.ParentPhases ORDER BY ParentPhaseName;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero delle fasi di produzione: {e}")
            return []

    def add_new_equipment(self, brand_id, type_id, phase_id, serial_number, internal_name, prod_year, inv_number, must_calibrated):
        """Salva una nuova macchina nel database."""
        query = """
                INSERT INTO eqp.Equipments
                (BrandId, EquipmentTypeId, ParentPhaseId, SerialNumber, InternalName, ProductionYear, InventoryNumber,
                 DateSys, MustCalibrated)
                VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE(), ?)
                """
        try:
            self.cursor.execute(query, brand_id, type_id, phase_id, serial_number, internal_name, prod_year, inv_number, must_calibrated)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            print(f"Errore durante l'inserimento della macchina: {e}")
            return False

    def fetch_translations(self):
        query = "SELECT LanguageCode, TranslationKey, TranslationValue FROM Traceability_rs.dbo.AppTranslations;"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Error fetching translations: {e}")
            return []

    def authenticate_user(self, user_id, password):
        query = """
                SELECT u.NomeUser, ISNULL(e.EmployeeName + ' ' + e.EmployeeSurname, '#ND') as EmployeeName, u.pass
                FROM resetservices.dbo.tbuserkey as U
                INNER JOIN employee.dbo.employees as e ON e.EmployeeId = u.idanga
                INNER JOIN employee.dbo.EmployeeHireHistory as h ON e.EmployeeId = h.EmployeeId
                WHERE h.EndWorkDate IS NULL AND h.employeerid = 2 AND u.Nomeuser = ? AND Pass = ?;
                """
        try:

            self.cursor.execute(query, user_id, password)
            row = self.cursor.fetchone()
            return row.EmployeeName if row else None

        except pyodbc.Error as e:
            print(f"Error during authentication: {e}")
            return None

    def fetch_products(self):
        query = """
                SELECT DISTINCT p.IDProduct, p.ProductCode + ' ['+ SUBSTRING(p.productcode, 3, 2) + ']' AS ProductCode
                FROM Traceability_RS.dbo.Products AS P
                INNER JOIN [Traceability_RS].[dbo].[ProductParentPhases] AS PP ON pp.IDProduct = p.IDProduct
                INNER JOIN Traceability_RS.dbo.ParentPhases AS PF ON pf.IDParentPhase = pp.IDParentPhase
                ORDER BY p.ProductCode + ' ['+ SUBSTRING(p.productcode, 3, 2) + ']';
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error:
            return []

    def fetch_products_with_documents(self):
        query = """
                SELECT p.IDProduct,
                       p.ProductCode + ' [' + CAST(doc_counts.DocCount AS NVARCHAR(10)) + ' docs]' AS ProductCode
                FROM Traceability_RS.dbo.Products AS p
                         INNER JOIN (SELECT ProductId, COUNT(*) AS DocCount
                                     FROM Traceability_RS.dbo.ProductDocuments
                                     WHERE DateOutOfValidation IS NULL
                                     GROUP BY ProductId) AS doc_counts ON p.IDProduct = doc_counts.ProductId
                ORDER BY ProductCode;
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error:
            return []

    def fetch_phases_with_documents_for_product(self, product_id):
        """
        Recupera solo le fasi di produzione che contengono almeno un documento
        per un dato ID prodotto.
        """
        # Query ottimizzata per restituire una lista pulita di fasi
        query = """
                SELECT DISTINCT pp.IDParentPhase, pp.ParentPhaseName
                FROM dbo.ProductDocuments p
                         INNER JOIN dbo.ParentPhases pp ON p.ParentPhaseId = pp.IDParentPhase
                WHERE p.ProductId = ?
                ORDER BY pp.ParentPhaseName; \
                """
        try:
            self.cursor.execute(query, product_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero delle fasi con documenti: {e}")
            self.last_error_details = str(e)
            return []

    def fetch_parent_phases(self, id_product):
        query = """
                SELECT distinct pf.IDParentPhase, pf.ParentPhaseName + IIF(pp.IDProduct IS NULL, '*', '') AS Phase
                FROM Traceability_RS.dbo.ParentPhases AS pf
                LEFT JOIN Traceability_RS.dbo.ProductParentPhases AS pp ON pf.IDParentPhase = pp.IDParentPhase AND pp.IDProduct = ?
                ORDER BY Phase;
                """
        try:
            self.cursor.execute(query, id_product)
            return self.cursor.fetchall()
        except pyodbc.Error:
            return []

    def fetch_existing_documents(self, product_id, parent_phase_id):
        """
        Recupera i metadati dei documenti per una data fase.
        """
        query = """
                SELECT DocumentProductionID, documentName, DocumentRevisionNumber, CONVERT(bit, Validated) as IsValid
                FROM Traceability_RS.dbo.ProductDocuments
                WHERE Productid = ?
                  AND ParentPhaseId = ?
                  AND DateOutOfValidation IS NULL;
                """
        try:
            self.cursor.execute(query, product_id, parent_phase_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore critico in fetch_existing_documents: {e}")
            self.last_error_details = str(e)
            return []

    def fetch_and_open_document(self, document_id):
        """Recupera i dati binari di un PDF dal DB, li salva in un file temporaneo e lo apre."""
        try:
            sql_select = "SELECT DocumentData FROM Traceability_RS.dbo.ProductDocuments WHERE DocumentProductionID = ?"
            self.cursor.execute(sql_select, document_id)
            row = self.cursor.fetchone()

            if row and row.DocumentData:
                pdf_binary_data = row.DocumentData

                # Crea un file temporaneo sicuro
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
                temp_file.write(pdf_binary_data)
                temp_file.close()

                print(f"Apertura del file temporaneo: {temp_file.name}")
                # Metodo cross-platform per aprire il file con l'applicazione predefinita
                os.startfile(temp_file.name)
                return True
            else:
                print("Nessun dato binario trovato per questo ID documento.")
                return False

        except pyodbc.Error as e:
            print(f"Errore durante il recupero del documento dal DB: {e}")
            return False
        except Exception as e:
            print(f"Errore durante l'apertura del file temporaneo: {e}")
            return False

    def save_document_to_db(self, product_id, parent_phase_id, doc_name, local_file_path, revision, user_name,
                            validated_int):
        """Legge un file e lo salva nel database, includendo il percorso del file originale."""
        try:
            # 1. Leggi i dati binari del file
            with open(local_file_path, 'rb') as f:
                binary_data = f.read()

            # 2. Prepara la NUOVA query di INSERT, come da te specificato
            # I nomi delle colonne 'InsertedBy' e 'InsertionDate' sono stati corretti
            # in 'UserName' e 'Datein' per corrispondere alla tua nuova query.
            sql_insert = """
                         INSERT INTO Traceability_RS.dbo.ProductDocuments
                         (ProductId, ParentPhaseId, documentName, DocumentRevisionNumber, DocumentData, UserName,
                          Datein, Validated, DocumentPath)
                         VALUES (?, ?, ?, ?, ?, ?, GETDATE(), ?, ?);
                         """

            # 3. Esegui la query passando anche il nuovo parametro 'local_file_path'
            self.cursor.execute(sql_insert,
                                product_id,
                                parent_phase_id,
                                doc_name,
                                revision,
                                binary_data,  # Dati del file
                                user_name,
                                validated_int,
                                local_file_path)  # <-- NUOVO PARAMETRO AGGIUNTO
            self.conn.commit()
            return True

        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            print(f"Errore durante il salvataggio del documento nel DB: {e}")
            return False
        except FileNotFoundError:
            self.last_error_details = f"File non trovato al percorso: {local_file_path}"
            print(self.last_error_details)
            return False

    def fetch_latest_version_info(self, software_name):
        """
        Recupera la versione più recente e il percorso di aggiornamento per un dato software.
        """
        query = "SELECT Version, MainPath FROM traceability_rs.dbo.SwVersions WHERE NameProgram = ? AND dateout IS NULL"
        try:
            self.cursor.execute(query, software_name)
            return self.cursor.fetchone()  # Restituisce l'intera riga (o None)
        except pyodbc.Error as e:
            print(f"Errore durante il recupero della versione del software: {e}")
            return None

    def fetch_available_maintenance_plans(self, equipment_id):
        """Recupera i piani di manutenzione disponibili per una macchina, basandosi sui compiti assegnati."""
        # La logica per determinare se un piano è "scaduto" è complessa e la manteniamo,
        # ma la struttura della query è più semplice senza join inutili.
        query = """
                WITH LatestLogs AS (SELECT CompitoId, MAX(DateStop) AS LastCompletionDate \
                                    FROM eqp.LogManutenzioni \
                                    WHERE EquipmentId = ? \
                                    GROUP BY CompitoId)
                SELECT DISTINCT pi.ProgrammedInterventionId, pi.TimingDescriprion
                FROM eqp.CompitiManutenzione cm
                         INNER JOIN eqp.ProgrammedInterventions pi \
                                    ON cm.ProgrammedInterventionId = pi.ProgrammedInterventionId
                         LEFT JOIN LatestLogs ll ON cm.CompitoId = ll.CompitoId
                WHERE cm.EquipmentId = ? \
                  AND (
                    ll.LastCompletionDate IS NULL OR
                    (CASE
                         WHEN pi.TimingValue < 1 THEN IIF(DATEDIFF(HOUR, ll.LastCompletionDate, GETDATE()) > 8, 1, 0)
                         WHEN pi.TimingValue >= 1 THEN IIF( \
                                 DATEDIFF(DAY, ll.LastCompletionDate, GETDATE()) >= pi.TimingValue, 1, 0)
                         ELSE 1
                        END) = 1
                    )
                ORDER BY pi.TimingDescriprion; \
                """
        try:
            self.cursor.execute(query, equipment_id, equipment_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero piani manutenzione: {e}")
            self.last_error_details = str(e)
            return []

    def fetch_maintenance_tasks(self, programmed_intervention_id, equipment_id):
        query = """
                WITH LatestLogs AS (SELECT CompitoId, MAX(DateStop) AS LastCompletionDate \
                                    FROM eqp.LogManutenzioni \
                                    WHERE EquipmentId = ? \
                                    GROUP BY CompitoId)
                SELECT cm.CompitoId, cm.NomeCompito, cm.Categoria, cm.DescrizioneCompito
                FROM eqp.CompitiManutenzione AS cm
                         INNER JOIN eqp.ProgrammedInterventions AS pin \
                                    ON cm.ProgrammedInterventionId = pin.ProgrammedInterventionId
                         LEFT JOIN LatestLogs AS ll ON cm.CompitoId = ll.CompitoId
                WHERE cm.ProgrammedInterventionId = ?
                  AND cm.EquipmentId = ?
                  AND (
                    ll.LastCompletionDate IS NULL OR
                    (CASE
                         WHEN pin.TimingValue = 0 THEN 1
                         WHEN pin.TimingValue < 1 THEN IIF(DATEDIFF(HOUR, ll.LastCompletionDate, GETDATE()) > 8, 1, 0)
                         WHEN pin.TimingValue >= 1 THEN IIF( \
                                 DATEDIFF(DAY, ll.LastCompletionDate, GETDATE()) >= pin.TimingValue, 1, 0)
                         ELSE 0
                        END) = 1
                    )
                ORDER BY cm.Ordine, cm.CompitoId; \
                """
        try:
            # I parametri sono: equipment_id (per WITH), intervention_id (per WHERE), equipment_id (per WHERE)
            self.cursor.execute(query, equipment_id, programmed_intervention_id, equipment_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero dei task da eseguire: {e}")
            self.last_error_details = str(e)
            return []

    def log_completed_tasks(self, equipment_id, user_name, completed_task_ids, start_time, notes=""):
        """Inserisce record in LogManutenzioni per i compiti completati in una transazione batch."""
        if not completed_task_ids:
            return True
        query = """
                INSERT INTO Traceability_rs.eqp.LogManutenzioni
                (CompitoId, EquipmentId, UserName, DateStop, DateStart, NoteGenerali)
                VALUES (?, ?, ?, GETDATE(), ?, ?)
                """
        try:
            # Prepariamo i dati per l'inserimento batch
            batch_data = []
            for task_id in completed_task_ids:
                # Ordine parametri: (CompitoId, EquipmentId, IdManutentore, StartTime, NoteGenerali)
                batch_data.append((task_id, equipment_id, user_name, start_time, notes))

            # Esegui l'inserimento batch (efficiente)
            self.cursor.executemany(query, batch_data)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            print(f"Errore nel logging dei compiti completati: {e}")
            self.last_error_details = str(e)
            return False

    def fetch_and_open_document_by_task_id(self, task_id):
        """
        Recupera e apre il documento specifico per un compito, leggendo
        i dati binari dalla colonna [LinkedDocument] della tabella CompitiManutenzione.
        """
        self.last_error_details = ""

        # --- QUERY MODIFICATA ---
        # Seleziona direttamente il documento binario dalla riga del compito specifico.
        query = """
                SELECT LinkedDocument
                FROM eqp.CompitiManutenzione
                WHERE CompitoId = ?; \
                """
        try:
            self.cursor.execute(query, task_id)
            row = self.cursor.fetchone()

            # Controlla che la riga esista e che il campo LinkedDocument non sia vuoto
            if row and row.LinkedDocument:
                binary_data = row.LinkedDocument

                # --- Logica per il file temporaneo (con nome generico) ---
                # Poiché non abbiamo il nome/tipo file, usiamo un default.
                file_extension = '.pdf'  # Assumiamo PDF come default
                temp_prefix = f"task_{task_id}_documento_"

                temp_file = tempfile.NamedTemporaryFile(prefix=temp_prefix, delete=False, suffix=file_extension)
                temp_file.write(binary_data)
                temp_file.close()

                print(f"Apertura documento specifico per compito ID {task_id}: {temp_file.name}")

                # Apertura del file cross-platform
                try:
                    if sys.platform == "win32":
                        os.startfile(temp_file.name)
                    else:
                        opener = "open" if sys.platform == "darwin" else "xdg-open"
                        subprocess.call([opener, temp_file.name])
                    return True
                except Exception as open_e:
                    self.last_error_details = f"Errore del sistema operativo nell'apertura del file: {open_e}"
                    return False
            else:
                self.last_error_details = f"Nessun documento specifico trovato per il compito ID {task_id}."
                return False

        except pyodbc.Error as e:
            print(f"Errore DB durante il recupero del documento specifico per il task ID {task_id}: {e}")
            self.last_error_details = f"Errore Database: {e}"
            return False
        except Exception as e:
            print(f"Errore imprevisto durante la gestione del file temporaneo: {e}")
            self.last_error_details = f"Errore Applicazione (File System): {e}"
            return False

class LoginWindow(tk.Toplevel):
    """Finestra per raccogliere le credenziali dell'utente."""

    def __init__(self, master, db_handler, lang_manager):
        super().__init__(master)
        self.db = db_handler  # Manteniamo db e lang per i testi tradotti
        self.lang = lang_manager

        # Attributi per restituire i risultati
        self.user_id = None
        self.password = None
        self.clicked_login = False

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.transient(master)
        self.grab_set()

        self._create_widgets()
        self.update_texts()
        self.bind('<Return>', self._attempt_login_event)

    def _create_widgets(self):
        # ... questo metodo rimane ESATTAMENTE invariato ...
        self.geometry("350x200")
        frame = ttk.Frame(self, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        self.user_id_label = ttk.Label(frame)
        self.user_id_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.user_id_entry = ttk.Entry(frame, width=30)
        self.user_id_entry.grid(row=0, column=1, padx=5, pady=10)
        self.password_label = ttk.Label(frame)
        self.password_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.password_entry = ttk.Entry(frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=5, pady=10)
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(15, 0))
        self.login_button = ttk.Button(button_frame, command=self._attempt_login)
        self.login_button.pack(side=tk.LEFT, padx=10)
        self.cancel_button = ttk.Button(button_frame, command=self._on_cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=10)
        self.user_id_entry.focus_set()

    def update_texts(self):
        # ... questo metodo rimane ESATTAMENTE invariato ...
        self.title(self.lang.get('login_title'))
        self.user_id_label.config(text=self.lang.get('login_user_id'))
        self.password_label.config(text=self.lang.get('login_password'))
        self.login_button.config(text=self.lang.get('login_button'))
        self.cancel_button.config(text=self.lang.get('login_cancel_button'))

    def _attempt_login_event(self, event=None):
        self._attempt_login()

    def _attempt_login(self):
        # --- LOGICA MODIFICATA ---
        # Ora la finestra si limita a raccogliere i dati
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()
        if not user_id or not password:
            messagebox.showerror(self.lang.get('login_title'), self.lang.get('login_error_credentials'), parent=self)
            return

        self.user_id = user_id
        self.password = password
        self.clicked_login = True
        self.destroy()  # Chiude la finestra

    def _on_cancel(self):
        # L'utente ha chiuso la finestra senza premere login
        self.clicked_login = False
        self.destroy()

class InsertDocumentForm(tk.Toplevel):
    """Finestra di inserimento documenti (di Produzione)."""

    def __init__(self, master, db_handler, user_name, lang_manager):
        super().__init__(master)
        self.db = db_handler
        self.user_name = user_name
        self.lang = lang_manager

        self.products_data = {}
        self.all_product_names = []
        self.parent_phases_data = {}

        self.product_var = tk.StringVar()
        self.parent_phase_var = tk.StringVar()
        self.file_name_var = tk.StringVar()
        self.revision_var = tk.StringVar()
        self.validated_var = tk.BooleanVar()

        self._create_widgets()
        self.update_texts()
        self._load_products()

    def _create_widgets(self):
        self.geometry("650x650")
        frame = ttk.Frame(self, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        self.product_label = ttk.Label(frame, font=("Helvetica", 10, "bold"))
        self.product_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        self.product_combo = ttk.Combobox(frame, textvariable=self.product_var)
        self.product_combo.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))
        self.product_combo.bind("<<ComboboxSelected>>", self._on_product_select)
        self.product_combo.bind("<KeyRelease>", self._on_product_keyrelease)

        self.phase_label = ttk.Label(frame, font=("Helvetica", 10, "bold"))
        self.phase_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        self.parent_phase_combo = ttk.Combobox(frame, textvariable=self.parent_phase_var, state="disabled")
        self.parent_phase_combo.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))
        self.parent_phase_combo.bind("<<ComboboxSelected>>", self._on_phase_select)

        self.details_frame = ttk.LabelFrame(frame, padding="10")
        self.details_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))
        self.details_frame.columnconfigure(1, weight=1)

        self.file_name_label = ttk.Label(self.details_frame)
        self.file_name_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.file_entry = ttk.Entry(self.details_frame, textvariable=self.file_name_var, state="disabled")
        self.file_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        self.browse_button = ttk.Button(self.details_frame, command=self._browse_file, state="disabled")
        self.browse_button.grid(row=0, column=2, padx=(0, 5), pady=5)

        self.revision_label = ttk.Label(self.details_frame)
        self.revision_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.revision_entry = ttk.Entry(self.details_frame, textvariable=self.revision_var, state="disabled")
        self.revision_entry.grid(row=1, column=1, columnspan=2, sticky=tk.EW, padx=5, pady=5)

        self.validated_check = ttk.Checkbutton(self.details_frame, variable=self.validated_var, state="disabled")
        self.validated_check.grid(row=2, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)

        self.docs_frame = ttk.LabelFrame(frame, padding="10")
        self.docs_frame.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=(0, 15))
        self.docs_listbox = tk.Listbox(self.docs_frame, height=6, selectbackground="#a6a6a6")
        self.docs_listbox.pack(fill=tk.BOTH, expand=True)

        self.save_button = ttk.Button(frame, command=self._save_document, state="disabled")
        self.save_button.grid(row=6, column=1, sticky=tk.E, pady=10)

    def update_texts(self):
        """Aggiorna i testi della UI."""
        self.title(self.lang.get('insert_doc_title'))
        self.product_label.config(text=self.lang.get('label_select_product'))
        self.phase_label.config(text=self.lang.get('label_select_phase'))
        self.details_frame.config(text=self.lang.get('frame_new_doc_details'))
        self.file_name_label.config(text=self.lang.get('label_file_name'))
        self.browse_button.config(text=self.lang.get('button_browse'))
        self.revision_label.config(text=self.lang.get('label_revision'))
        self.validated_check.config(text=self.lang.get('check_validated'))
        self.docs_frame.config(text=self.lang.get('frame_active_docs'))
        self.save_button.config(text=self.lang.get('button_save'))
        self._refresh_document_list()

    def _load_products(self):
        products = self.db.fetch_products()
        if products:
            self.products_data = {p.ProductCode: p.IDProduct for p in products}
            self.all_product_names = list(self.products_data.keys())
            self.product_combo['values'] = self.all_product_names
        else:
            messagebox.showwarning(self.lang.get('app_title'), self.lang.get('warn_no_products_found'))

    def _on_product_keyrelease(self, event):
        typed_text = self.product_var.get()
        if not typed_text:
            self.product_combo['values'] = self.all_product_names
        else:
            filtered_list = [name for name in self.all_product_names if typed_text.lower() in name.lower()]
            self.product_combo['values'] = filtered_list

    def _on_product_select(self, event=None):
        self._reset_phase_section()
        self._reset_details_section()
        product_id = self.products_data.get(self.product_var.get())

        if product_id:
            parent_phases = self.db.fetch_parent_phases(product_id)
            if parent_phases:
                self.parent_phases_data = {p.Phase: p.IDParentPhase for p in parent_phases}
                self.parent_phase_combo['values'] = list(self.parent_phases_data.keys())
                self.parent_phase_combo.config(state="readonly")
            else:
                messagebox.showerror(self.lang.get('app_title'), self.lang.get('error_no_phases_found'))
                self.product_combo.focus()

    def _on_phase_select(self, event=None):
        self._reset_details_section()
        self.file_entry.config(state="readonly")
        self.browse_button.config(state="normal")
        self.revision_entry.config(state="normal")
        self.validated_check.config(state="normal")
        self.save_button.config(state="normal")
        self._refresh_document_list()

    def _browse_file(self, event=None):
        file_path = filedialog.askopenfilename(title=self.lang.get('insert_doc_title'),
                                               filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if file_path:
            self.file_name_var.set(file_path)

    def _save_document(self):
        # Validazione input
        if not all([self.product_var.get(), self.parent_phase_var.get(), self.file_name_var.get(),
                    self.revision_var.get()]):
            messagebox.showerror(self.lang.get('app_title'), self.lang.get('error_input_all_fields'))
            return

        # ... altre validazioni
        revision = self.revision_var.get()
        if len(revision) > 10:
            # Gestione sicura del messaggio di errore se il template usa .replace()
            msg_template = self.lang.get_raw('error_input_revision_length')
            msg = msg_template.replace('{revision}', revision).replace('{length}', str(len(revision)))
            messagebox.showerror(self.lang.get('app_title'), msg)
            return

        # Recupero dati per il salvataggio
        product_id = self.products_data.get(self.product_var.get())
        parent_phase_id = self.parent_phases_data.get(self.parent_phase_var.get())
        local_file_path = self.file_name_var.get()
        doc_name = os.path.basename(local_file_path)
        is_validated_bool = self.validated_var.get()
        validated_as_int = 1 if is_validated_bool else 0

        success = self.db.save_document_to_db(
            product_id,
            parent_phase_id,
            doc_name,
            local_file_path,
            revision,
            self.user_name,
            validated_as_int
        )

        if success:
            messagebox.showinfo(self.lang.get('app_title'), self.lang.get('info_save_success'))
            self._reset_input_fields()
            self._refresh_document_list()
        else:
            # Gestione sicura del messaggio di errore se il template usa .replace()
            msg_template = self.lang.get_raw('error_save_failed')
            msg = msg_template.replace('{e}', self.db.last_error_details)
            messagebox.showerror(self.lang.get('app_title'), msg)

    def _refresh_document_list(self):
        self.docs_listbox.delete(0, tk.END)
        product_id = self.products_data.get(self.product_var.get())
        parent_phase_id = self.parent_phases_data.get(self.parent_phase_var.get())

        if not (product_id and parent_phase_id):
            return

        existing_docs = self.db.fetch_existing_documents(product_id, parent_phase_id)
        yes_text = self.lang.get('text_yes')
        no_text = self.lang.get('text_no')
        for i, doc in enumerate(existing_docs):
            # Accesso alle proprietà dell'oggetto Row di pyodbc
            is_valid_text = yes_text if doc.IsValid else no_text
            display_text = f"File: {doc.documentName} | Rev: {doc.DocumentRevisionNumber} | Validato: {is_valid_text}"
            self.docs_listbox.insert(tk.END, display_text)
            if doc.IsValid:
                self.docs_listbox.itemconfig(i, {'bg': '#c8e6c9'})  # Verde chiaro per validati

    def _reset_phase_section(self):
        self.parent_phase_var.set("")
        self.parent_phase_combo.config(state="disabled", values=[])

    def _reset_details_section(self):
        self._reset_input_fields()
        self.file_entry.config(state="disabled")
        self.browse_button.config(state="disabled")
        self.revision_entry.config(state="disabled")
        self.validated_check.config(state="disabled")
        self.save_button.config(state="disabled")
        self.docs_listbox.delete(0, tk.END)

    def _reset_input_fields(self):
        self.file_name_var.set("")
        self.revision_var.set("")
        self.validated_var.set(False)
        self.file_entry.config(state="readonly")

class KanbanLocationCreateForm(tk.Toplevel):
    """
    Crea una locazione KanBan:
    - Combo aree (da dbo.ParentPhases, CodCDC in 10,30,90)
    - Campo locazione (max 8 char)
    - Bottone salva
    - Logo bottom-right
    """
    def __init__(self, master, db_handler, lang_manager):
        super().__init__(master)
        self.db = db_handler
        self.lang = lang_manager

        self.title(self.lang.get('kanban_locations_title', "Crea locazione KanBan"))
        self.geometry("500x260")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        # State
        self.area_map = {}  # {display_name: id}
        self.area_var = tk.StringVar()
        self.location_var = tk.StringVar()

        self._build_ui()
        self._load_areas()
        self._update_save_state()

    def _build_ui(self):
        container = ttk.Frame(self, padding=16)
        container.pack(fill=tk.BOTH, expand=True)

        # Area label + combo
        ttk.Label(container, text=self.lang.get('kanban_area_label', "Area KanBan"),
                  font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w")
        self.area_combo = ttk.Combobox(container, textvariable=self.area_var, state="readonly", width=44)
        self.area_combo.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(2, 12))
        self.area_combo.bind("<<ComboboxSelected>>", lambda e: self._update_save_state())

        # Location label + entry
        ttk.Label(container, text=self.lang.get('kanban_location_label', "Locazione"),
                  font=("Helvetica", 10, "bold")).grid(row=2, column=0, sticky="w")
        self.location_entry = ttk.Entry(container, textvariable=self.location_var, width=30)
        self.location_entry.grid(row=3, column=0, sticky="w", pady=(2, 12))
        self.location_entry.bind("<KeyRelease>", self._on_location_change)

        # Buttons (Save + Close)
        btns = ttk.Frame(container)
        btns.grid(row=4, column=0, columnspan=2, sticky="e", pady=(10, 0))

        self.save_btn = ttk.Button(btns, text=self.lang.get('button_save', "Salva"), command=self._on_save)
        self.save_btn.pack(side="right", padx=(6, 0))

        close_btn = ttk.Button(btns, text=self.lang.get('button_close', "Chiudi"), command=self.destroy)
        close_btn.pack(side="right")

        # Bottom bar: left -> total locations, right -> logo
        bottom = ttk.Frame(container)
        bottom.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        bottom.columnconfigure(0, weight=1)  # sinistra si espande

        # Totale locazioni (sinistra)
        self.total_locations_label = ttk.Label(bottom, text="")
        self.total_locations_label.grid(row=0, column=0, sticky="w")

        # Logo (destra)
        if PIL_AVAILABLE:
            try:
                from PIL import Image, ImageTk
                img = Image.open("logo.png")
                img.thumbnail((100, 100))
                self._logo_img = ImageTk.PhotoImage(img)
                ttk.Label(bottom, image=self._logo_img).grid(row=0, column=1, sticky="e")
            except Exception as e:
                print(f"Errore caricamento logo: {e}")

        # Grid weights
        container.columnconfigure(0, weight=1)

        # Carica il totale
        self._load_locations_count()

    def _load_locations_count(self):
        n = self.db.count_kanban_locations()
        n_str = str(n) if n is not None else "#N/A"
        # usa template traducibile con {n}
        template = self.lang.get('kanban_locations_total', "Totale locazioni: {n}")
        self.total_locations_label.config(text=template.replace("{n}", n_str))

    def _load_areas(self):
        rows = self.db.fetch_kanban_areas()
        if not rows:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('kanban_areas_load_error', "Impossibile caricare le aree KanBan."),
                                 parent=self)
            self.area_combo.config(state="disabled")
            self.save_btn.config(state="disabled")
            return

        # Mappa display -> id
        self.area_map = {row.ParentPhaseName: row.IDParentPhase for row in rows}
        self.area_combo['values'] = list(self.area_map.keys())
        if self.area_combo['values']:
            self.area_combo.current(0)

    def _on_location_change(self, event=None):
        # Uppercase e max 8 caratteri
        val = self.location_var.get().upper()
        if len(val) > 8:
            val = val[:8]
        if val != self.location_var.get():
            self.location_var.set(val)
            # riposiziona il cursore alla fine
            self.location_entry.icursor(tk.END)
        self._update_save_state()

    def _update_save_state(self):
        has_area = bool(self.area_var.get())
        loc = self.location_var.get().strip()
        enable = has_area and 1 <= len(loc) <= 8
        self.save_btn.config(state=("normal" if enable else "disabled"))

    def _on_save(self):
        # Validazioni
        area_name = self.area_var.get()
        if not area_name:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"),
                                   self.lang.get('kanban_area_required', "Selezionare un'area."), parent=self)
            return
        area_id = self.area_map.get(area_name)
        print(area_id)
        loc = self.location_var.get().strip().upper()

        if not loc:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"),
                                   self.lang.get('kanban_location_required', "Inserire una locazione."), parent=self)
            self.location_entry.focus_set()
            return
        if len(loc) > 8:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"),
                                   self.lang.get('kanban_location_len', "La locazione può avere al massimo 8 caratteri."),
                                   parent=self)
            self.location_entry.focus_set()
            return

        ok, err = self.db.insert_kanban_location(area_id, loc)
        if ok:
            messagebox.showinfo(self.lang.get('info_title', "Informazione"),
                                self.lang.get('kanban_location_saved', "Locazione creata con successo."),
                                parent=self)
            self.location_var.set("")
            self.location_entry.focus_set()
            self._update_save_state()
            self._load_locations_count()  # <-- aggiorna conteggio
            return

        if err == "duplicate":
            self.location_var.set("")
            self.location_entry.focus_set()
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"),
                                   self.lang.get('kanban_location_exists',
                                                 "La locazione esiste già per l'area selezionata. Inserire un valore diverso."),
                                   parent=self)
            return

        messagebox.showerror(self.lang.get('error_title', "Errore"),
                             self.lang.get('kanban_location_save_error',
                                           f"Errore durante il salvataggio della locazione: {err}"),
                             parent=self)

class KanbanLocationLabelsForm(tk.Toplevel):
    def __init__(self, master, db_handler, lang_manager):
        super().__init__(master)
        self.db = db_handler
        self.lang = lang_manager
        self.title(self.lang.get('kanban_labels_title', "Stampa etichette locazioni"))
        self.geometry("520x260")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.cfg = load_printer_config()
        if not self.cfg:
            # chiedi subito la configurazione
            dlg = PrinterSetupDialog(self, self.lang)
            self.wait_window(dlg)
            if not getattr(dlg, "result", None):
                messagebox.showwarning(self.lang.get('warn_title', "Attenzione"),
                                       self.lang.get('printer_not_configured', "Stampante non configurata."), parent=self)
                self.destroy()
                return
            self.cfg = dlg.result

        self.location_var = tk.StringVar()
        self.copies_var = tk.StringVar(value="1")

        self._build_ui()
        self._load_locations()

    def _build_ui(self):
        frm = ttk.Frame(self, padding=16)
        frm.pack(fill="both", expand=True)

        # Riga configurazione stampante + bottone setup
        top = ttk.Frame(frm)
        top.grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(top, text=self.lang.get('printer_current', "Stampante:")).pack(side="left")
        self.prn_label = ttk.Label(top, text=self._printer_summary(), foreground="#006400")
        self.prn_label.pack(side="left", padx=(6, 0))
        ttk.Button(top, text=self.lang.get('printer_setup_btn', "Imposta..."), command=self._setup_printer).pack(side="right")

        # Selezione locazione
        ttk.Label(frm, text=self.lang.get('kanban_location_label', "Locazione"), font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky="w", pady=(12,2))
        self.location_combo = ttk.Combobox(frm, textvariable=self.location_var, state="readonly", width=40)
        self.location_combo.grid(row=2, column=0, sticky="w")

        # Copie
        ttk.Label(frm, text=self.lang.get('copies_label', "Copie")).grid(row=1, column=1, sticky="w", pady=(12,2))
        self.copies_entry = ttk.Spinbox(frm, from_=1, to=99, textvariable=self.copies_var, width=5)
        self.copies_entry.grid(row=2, column=1, sticky="w")

        # Pulsanti
        btns = ttk.Frame(frm)
        btns.grid(row=10, column=0, columnspan=2, sticky="e", pady=(16,0))
        ttk.Button(btns, text=self.lang.get('button_close', "Chiudi"), command=self.destroy).pack(side="right")
        self.print_btn = ttk.Button(btns, text=self.lang.get('button_print', "Stampa"), command=self._on_print)
        self.print_btn.pack(side="right", padx=(0,8))

        frm.columnconfigure(0, weight=1)

    def _printer_summary(self) -> str:
        c = self.cfg or {}
        return f"{c.get('name','?')} ({c.get('ip','?')}:{c.get('port','?')}, {c.get('dpi','203')} dpi)"

    def _setup_printer(self):
        dlg = PrinterSetupDialog(self, self.lang)
        self.wait_window(dlg)
        if getattr(dlg, "result", None):
            self.cfg = dlg.result
            self.prn_label.config(text=self._printer_summary())

    def _load_locations(self):
        rows = self.db.fetch_kanban_locations_all()
        if not rows:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('kanban_locations_load_error', "Impossibile caricare le locazioni."),
                                 parent=self)
            self.print_btn.config(state="disabled")
            return
        values = [r.LocationCode for r in rows]
        self.location_combo['values'] = values
        if values:
            self.location_combo.current(0)

    def _on_print(self):
        loc = self.location_var.get().strip().upper()
        if not loc:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"),
                                   self.lang.get('kanban_location_required', "Inserire una locazione."), parent=self)
            return

        # Conformità al limite 8 char se desideri mantenerlo anche in stampa
        if len(loc) > 8:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"),
                                   self.lang.get('kanban_location_len', "La locazione può avere al massimo 8 caratteri."),
                                   parent=self)
            return

        try:
            copies = int(self.copies_var.get())
        except ValueError:
            copies = 1

        zpl = build_zpl_label(loc, copies, self.cfg)
        ok, err = send_raw_to_printer(self.cfg["ip"], int(self.cfg["port"]), zpl.encode("utf-8"))
        if ok:
            messagebox.showinfo(self.lang.get('info_title', "Informazione"),
                                self.lang.get('print_ok', "Stampa inviata alla stampante."), parent=self)
        else:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('print_error', f"Errore di stampa: {err}"), parent=self)

def get_printer_config_dir() -> Path:
    base = Path(os.getenv("LOCALAPPDATA", ".")) / "TraceabilityRS"
    base.mkdir(parents=True, exist_ok=True)
    return base

def get_printer_config_path() -> Path:
    return get_printer_config_dir() / "printer_config.json"

def migrate_printer_config(cfg: dict) -> dict:
    # Versioning e default
    cfg = dict(cfg or {})
    cfg.setdefault("version", 1)
    cfg.setdefault("name", "")
    cfg.setdefault("ip", "")
    cfg.setdefault("port", 9100)
    cfg.setdefault("dpi", 203)
    cfg.setdefault("label_cm", [5, 5])   # [Larghezza, Altezza] in cm
    cfg.setdefault("text_pt", 12)
    cfg.setdefault("language", "ZPL")
    # NUOVO: scheduling refill Kanban
    cfg.setdefault("kanban_refill_enabled", True)
    cfg.setdefault("kanban_refill_check_minutes", 60)
    return cfg

def load_printer_config() -> dict | None:
    path = get_printer_config_path()
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return migrate_printer_config(raw)
    except Exception:
        # JSON corrotto o non leggibile
        return None

def save_printer_config(cfg: dict) -> tuple[bool, str | None]:
    """
    Scrive il JSON con backup e sostituzione atomica.
    Ritorna (True, None) se ok, (False, err) se errore.
    """
    try:
        cfg = migrate_printer_config(cfg)
        path = get_printer_config_path()
        dir_ = path.parent
        dir_.mkdir(parents=True, exist_ok=True)

        # Backup del file esistente
        if path.exists():
            bak = dir_ / f"printer_config.bak"
            shutil.copy2(path, bak)

        # Scrittura atomica: tmp -> replace
        with tempfile.NamedTemporaryFile("w", delete=False, dir=str(dir_), encoding="utf-8") as tf:
            json.dump(cfg, tf, ensure_ascii=False, indent=2)
            tmp_name = tf.name
        os.replace(tmp_name, path)
        return True, None
    except Exception as e:
        return False, str(e)

def validate_ip(ip: str) -> bool:
    try:
        socket.inet_aton(ip)
        return True
    except OSError:
        return False

def open_config_folder():
    # Apre la cartella del file JSON nel file manager
    path = get_printer_config_dir()
    try:
        os.startfile(str(path))  # Windows
    except AttributeError:
        import subprocess, sys
        if sys.platform.startswith("darwin"):
            subprocess.call(["open", str(path)])
        else:
            subprocess.call(["xdg-open", str(path)])

def pt_to_dots(pt: int, dpi: int) -> int:
    # 1 pt = 1/72 inch
    return max(10, round(dpi * (pt / 72.0)))

def cm_to_dots(cm: float, dpi: int) -> int:
    return round(dpi * (cm / 2.54))

def build_zpl_label(location_code: str, copies: int, cfg: dict) -> str:
    """
    Costruisce ZPL per etichetta 5x5 cm:
    - QR centrato
    - Testo sotto, corpo 12pt
    """
    dpi = int(cfg.get("dpi", 203))
    w_cm, h_cm = cfg.get("label_cm", [5, 5])
    width = cm_to_dots(w_cm, dpi)
    height = cm_to_dots(h_cm, dpi)
    text_h = pt_to_dots(int(cfg.get("text_pt", 12)), dpi)
    text_w = text_h  # quadrato

    margin = max(12, round(0.1 * dpi))  # ~2.5mm a 203dpi -> ~20 dot
    available_h = height - text_h - margin * 3
    if available_h < 50:
        available_h = max(50, height - text_h - margin)

    # Magnification QR (1..10). Considero QR v1 21x21 moduli.
    modules = 21
    max_qr_dots = min(width - 2 * margin, available_h)
    mag = max(1, min(10, max_qr_dots // modules))
    qr_size = modules * mag
    qr_x = (width - qr_size) // 2
    qr_y = margin

    text_y = qr_y + qr_size + margin

    # ZPL
    data = location_code.upper()
    zpl = []
    zpl.append("^XA")
    zpl.append("^CI28")                           # UTF-8 (anche se non serve per A-Z0-9)
    zpl.append(f"^PW{width}")                    # print width
    zpl.append(f"^LL{height}")                   # label length
    zpl.append("^LH0,0")

    # QR code centrato
    zpl.append(f"^FO{qr_x},{qr_y}")
    zpl.append(f"^BQN,2,{mag}")
    zpl.append(f"^FDLA,{data}^FS")

    # Testo centrato
    # Uso ^FB per centrare rispetto alla larghezza disponibile
    zpl.append(f"^FO0,{text_y}")
    zpl.append(f"^A0N,{text_h},{text_w}")
    zpl.append(f"^FB{width},1,0,C,0")
    zpl.append(f"^FD{data}^FS")

    # Numero copie
    copies = max(1, int(copies))
    zpl.append(f"^PQ{copies},0,1,Y")

    zpl.append("^XZ")
    return "".join(zpl)

def send_raw_to_printer(ip: str, port: int, payload: bytes, timeout: float = 5.0) -> tuple[bool, str | None]:
    try:
        with socket.create_connection((ip, port), timeout=timeout) as s:
            s.sendall(payload)
        return True, None
    except Exception as e:
        return False, str(e)

class KanbanLocationModifyForm(tk.Toplevel):
    def __init__(self, master, db_handler, lang_manager):
        super().__init__(master)
        self.db = db_handler
        self.lang = lang_manager
        self.title(self.lang.get('kanban_modify_title', "Modifica locazioni"))
        self.geometry("720x420")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.component_var = tk.StringVar()
        self.dest_loc_var = tk.StringVar()
        self.src_loc_var = tk.StringVar()
        self.dest_loc_var2 = tk.StringVar()

        self._locations_cache = []  # rows for combo

        self._build_ui()
        self._load_locations()

    def _build_ui(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=12, pady=12)

        # Tab 1: Sposta componente
        tab1 = ttk.Frame(nb)
        nb.add(tab1, text=self.lang.get('tab_move_component', "Sposta componente"))

        frm1 = ttk.Frame(tab1, padding=12)
        frm1.pack(fill="both", expand=True)

        # Ricerca componente
        row = ttk.Frame(frm1)
        row.pack(fill="x")
        ttk.Label(row, text=self.lang.get('component_code', "Codice componente")).pack(side="left")
        ent = ttk.Entry(row, textvariable=self.component_var, width=30)
        ent.pack(side="left", padx=(8,8))
        ttk.Button(row, text=self.lang.get('button_search', "Cerca"), command=self._on_search_component).pack(side="left")

        # Risultati
        ttk.Label(frm1, text=self.lang.get('results_label', "Risultati")).pack(anchor="w", pady=(12,4))
        cols = ("record_id", "loc_code", "qty", "desc")
        self.tree = ttk.Treeview(frm1, columns=cols, show="headings", height=8)
        self.tree.heading("record_id", text="ID")
        self.tree.column("record_id", width=60, anchor="center")
        self.tree.heading("loc_code", text=self.lang.get('location', "Locazione"))
        self.tree.column("loc_code", width=140)
        self.tree.heading("qty", text=self.lang.get('quantity', "Q.tà"))
        self.tree.column("qty", width=80, anchor="e")
        self.tree.heading("desc", text=self.lang.get('description', "Descrizione"))
        self.tree.column("desc", width=360)
        self.tree.pack(fill="both", expand=True)

        # Destinazione
        dest_row = ttk.Frame(frm1)
        dest_row.pack(fill="x", pady=(12,0))
        ttk.Label(dest_row, text=self.lang.get('destination', "Destinazione")).pack(side="left")
        self.dest_combo = ttk.Combobox(dest_row, textvariable=self.dest_loc_var, state="readonly", width=48)
        self.dest_combo.pack(side="left", padx=(8,8))

        ttk.Button(frm1, text=self.lang.get('button_move', "Sposta"), command=self._on_move_single).pack(anchor="e", pady=(10,0))

        # Tab 2: Sposta intera locazione
        tab2 = ttk.Frame(nb)
        nb.add(tab2, text=self.lang.get('tab_move_location', "Sposta locazione"))

        frm2 = ttk.Frame(tab2, padding=12)
        frm2.pack(fill="both", expand=True)

        r2a = ttk.Frame(frm2); r2a.pack(fill="x")
        ttk.Label(r2a, text=self.lang.get('source_location', "Sorgente")).pack(side="left")
        self.src_combo = ttk.Combobox(r2a, textvariable=self.src_loc_var, state="readonly", width=40)
        self.src_combo.pack(side="left", padx=(8,16))
        ttk.Label(r2a, text=self.lang.get('destination', "Destinazione")).pack(side="left")
        self.dest_combo2 = ttk.Combobox(r2a, textvariable=self.dest_loc_var2, state="readonly", width=40)
        self.dest_combo2.pack(side="left", padx=(8,0))

        ttk.Button(frm2, text=self.lang.get('button_move_all', "Sposta tutto"), command=self._on_move_all).pack(anchor="e", pady=(12,0))

    def _load_locations(self):
        rows = self.db.fetch_locations_for_combo()
        self._locations_cache = rows
        values = [f"{r.KanBanLocation} • {r.LocationCode}" for r in rows]
        self.dest_combo['values'] = values
        self.src_combo['values'] = values
        self.dest_combo2['values'] = values
        if values:
            self.dest_combo.current(0)
            self.src_combo.current(0)
            if len(values) > 1:
                self.dest_combo2.current(1)
            else:
                self.dest_combo2.current(0)

    def _on_search_component(self):
        code = self.component_var.get().strip()
        if not code:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"), self.lang.get('component_required', "Inserire un codice componente."), parent=self)
            return
        rows = self.db.search_component_open_records(code)
        # pulisci
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in rows:
            self.tree.insert("", "end", iid=str(r.KanBanRecordId),
                             values=(r.KanBanRecordId, r.LocationCode, r.Quantity, r.ComponentDescription or ""))

    def _pick_combo_ids(self, combo_value: str):
        """
        Estrae LocationId e KanBanLocationId dal valore scelto in combo (usando cache).
        """
        try:
            idx = list(self.dest_combo['values']).index(combo_value)
        except ValueError:
            # prova con altre combo
            vals = list(self.src_combo['values'])
            idx = vals.index(combo_value) if combo_value in vals else -1
        if idx < 0:
            return None, None
        row = self._locations_cache[idx]
        return row.LocationId, row.KanBanLocationId

    def _on_move_single(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"), self.lang.get('select_row', "Seleziona una riga dai risultati."), parent=self)
            return
        record_id = int(sel[0])
        dest_val = self.dest_loc_var.get()
        to_loc_id, to_kbl_id = self._pick_combo_ids(dest_val)
        if not to_loc_id:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"), self.lang.get('destination_required', "Seleziona la destinazione."), parent=self)
            return

        # Evita movimento verso la stessa locazione (se deducibile)
        # Recupero LocationId della riga selezionata leggendo i dati dal DB (più sicuro)
        rows = self.db.search_component_open_records(self.component_var.get().strip())
        src_loc_id = None
        for r in rows:
            if r.KanBanRecordId == record_id:
                src_loc_id = r.LocationId
                break
        if src_loc_id == to_loc_id:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"), self.lang.get('same_location', "Sorgente e destinazione coincidono."), parent=self)
            return

        ok, err = self.db.move_record_to_location(record_id, to_loc_id, to_kbl_id)
        if ok:
            messagebox.showinfo(self.lang.get('info_title', "Informazione"), self.lang.get('move_ok', "Spostamento completato."), parent=self)
            self._on_search_component()  # refresh risultati
        else:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('move_err', f"Errore durante lo spostamento: {err or self.db.last_error_details}"),
                                 parent=self)

    def _on_move_all(self):
        src_val = self.src_loc_var.get()
        dest_val = self.dest_loc_var2.get()
        if not src_val or not dest_val:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"), self.lang.get('source_dest_required', "Seleziona sorgente e destinazione."), parent=self)
            return
        src_loc_id, _ = self._pick_combo_ids(src_val)
        to_loc_id, to_kbl_id = self._pick_combo_ids(dest_val)
        if not src_loc_id or not to_loc_id:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"), self.lang.get('source_dest_required', "Seleziona sorgente e destinazione."), parent=self)
            return
        if src_loc_id == to_loc_id:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"), self.lang.get('same_location', "Sorgente e destinazione coincidono."), parent=self)
            return

        ok, err = self.db.move_all_from_location(src_loc_id, to_loc_id, to_kbl_id)
        if ok:
            messagebox.showinfo(self.lang.get('info_title', "Informazione"), self.lang.get('move_ok', "Spostamento completato."), parent=self)
        else:
            msg = self.lang.get('nothing_to_move', "Nessun record da spostare.") if err == "nothing_to_move" else (err or self.db.last_error_details)
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('move_err', f"Errore durante lo spostamento: {msg}"),
                                 parent=self)

class KanbanMaterialsManagementForm(tk.Toplevel):
    def __init__(self, master, db_handler, lang_manager):
        super().__init__(master)
        self.db = db_handler
        self.lang = lang_manager

        self.title(self.lang.get('materials_mgmt_title', "KanBan - Materiali: Gestione"))
        self.geometry("760x420")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        # State
        self.type_var = tk.StringVar()
        self.comp_var = tk.StringVar()
        self.rule_var = tk.StringVar()

        self._types = []       # cache tipi
        self._components = []  # cache componenti
        self._rules = []       # cache regole
        self._comp_index_by_display = {}  # mappa display->row
        self._rule_index_by_display = {}  # mappa display->row

        self._logo_imgtk = None

        self._build_ui()
        self._load_types()
        self._load_rules()
        self._load_components(None)  # all

    def _build_ui(self):
        root = ttk.Frame(self, padding=12)
        root.pack(fill="both", expand=True)

        # Filtri riga 1: Tipo componente
        fr1 = ttk.Frame(root)
        fr1.pack(fill="x")
        ttk.Label(fr1, text=self.lang.get('material_type', "Tipo componente")).pack(side="left")
        self.type_combo = ttk.Combobox(fr1, textvariable=self.type_var, width=40, state="readonly")
        self.type_combo.pack(side="left", padx=(8, 0))
        self.type_combo.bind("<<ComboboxSelected>>", self._on_type_changed)

        # Filtri riga 2: Componente
        fr2 = ttk.Frame(root)
        fr2.pack(fill="x", pady=(8, 0))
        ttk.Label(fr2, text=self.lang.get('component', "Componente")).pack(side="left")
        self.comp_combo = ttk.Combobox(fr2, textvariable=self.comp_var, width=60, state="readonly")
        self.comp_combo.pack(side="left", padx=(8, 8))
        self.comp_combo.bind("<<ComboboxSelected>>", self._on_component_changed)

        # Stato/regola corrente
        state = ttk.Labelframe(root, text=self.lang.get('current_rule_group', "Regola attiva"))
        state.pack(fill="x", pady=(12, 0))
        self.current_rule_label = ttk.Label(state, text=self.lang.get('no_rule', "Nessuna regola associata"))
        self.current_rule_label.pack(anchor="w", padx=8, pady=6)

        # Assegnazione regola
        assign = ttk.Labelframe(root, text=self.lang.get('assign_rule_group', "Associa regola"))
        assign.pack(fill="x", pady=(12, 0))
        row = ttk.Frame(assign)
        row.pack(fill="x", padx=8, pady=6)
        ttk.Label(row, text=self.lang.get('select_rule', "Regola")).pack(side="left")
        self.rule_combo = ttk.Combobox(row, textvariable=self.rule_var, state="readonly", width=50)
        self.rule_combo.pack(side="left", padx=(8, 8))
        ttk.Button(row, text=self.lang.get('button_assign', "Associa"), command=self._on_assign).pack(side="left")
        ttk.Button(row, text=self.lang.get('button_remove', "Rimuovi"), command=self._on_remove).pack(side="left", padx=(8,0))

        # Logo in basso a destra
        bottom = ttk.Frame(root)
        bottom.pack(fill="both", expand=True)
        self.logo_lbl = ttk.Label(bottom)
        self.logo_lbl.pack(side="right", anchor="se", padx=4, pady=4)
        self._load_logo()

    def _load_logo(self):
        try:
            if os.path.exists("logo.png"):
                img = Image.open("logo.png")
                # Ridimensiona per adattare
                img.thumbnail((160, 80))
                self._logo_imgtk = ImageTk.PhotoImage(img)
                self.logo_lbl.configure(image=self._logo_imgtk)
        except Exception:
            # Fallback: nessun logo
            pass

    def _load_types(self):
        rows = self.db.fetch_component_types()
        self._types = rows
        values = [self.lang.get('all_types', "Tutti i tipi")] + [r.ComponentTypeName for r in rows]
        self.type_combo['values'] = values
        if values:
            self.type_combo.current(0)

    def _load_components(self, type_id: int | None):
        rows = self.db.fetch_components(type_id)
        self._components = rows
        values = []
        self._comp_index_by_display.clear()
        for r in rows:
            disp = f"{r.ComponentCode} • {r.ComponentDescription or ''}"
            values.append(disp)
            self._comp_index_by_display[disp] = r
        self.comp_combo['values'] = values
        if values:
            self.comp_combo.current(0)
            # Aggiorna stato per il primo elemento
            self._on_component_changed()

    def _load_rules(self):
        rows = self.db.fetch_kanban_rules()
        self._rules = rows
        values = []
        self._rule_index_by_display.clear()
        for r in rows:
            if getattr(r, "MinimumProcent", None) is not None:
                disp = f"Percentuale {int(r.MinimumProcent)}%"
            elif getattr(r, "MinimumQty", None) is not None:
                disp = f"Quantità {int(r.MinimumQty)}"
            else:
                disp = f"Regola {r.KanBanRuleID}"
            values.append(disp)
            self._rule_index_by_display[disp] = r
        self.rule_combo['values'] = values
        if values:
            self.rule_combo.current(0)

    def _on_type_changed(self, event=None):
        sel = self.type_var.get()
        if not sel or sel == self.lang.get('all_types', "Tutti i tipi"):
            self._load_components(None)
            return
        # Trova type_id selezionato
        type_id = None
        for t in self._types:
            if t.ComponentTypeName == sel:
                type_id = t.IdComponentType
                break
        self._load_components(type_id)

    def _get_selected_component_row(self):
        disp = self.comp_var.get()
        return self._comp_index_by_display.get(disp)

    def _on_component_changed(self, event=None):
        row = self._get_selected_component_row()
        if not row:
            self.current_rule_label.configure(text=self.lang.get('no_rule', "Nessuna regola associata"))
            return
        active = self.db.fetch_active_rule_for_component(row.IdComponent)
        if active and getattr(active, "KanBanRuleId", None) is not None:
            # Trova dettaglio regola per visualizzare percentuale/qty
            rule = None
            for r in self._rules:
                if r.KanBanRuleID == active.KanBanRuleId:
                    rule = r
                    break
            if rule:
                if getattr(rule, "MinimumProcent", None) is not None:
                    text = self.lang.get('current_rule_fmt_pct', "Regola attiva: {v}%").format(v=int(rule.MinimumProcent))
                elif getattr(rule, "MinimumQty", None) is not None:
                    text = self.lang.get('current_rule_fmt_qty', "Regola attiva: Q.tà {v}").format(v=int(rule.MinimumQty))
                else:
                    text = self.lang.get('current_rule_fmt_id', "Regola attiva ID {id}").format(id=rule.KanBanRuleID)
                self.current_rule_label.configure(text=text)
                # Pre-seleziona la regola nel combo se matcha
                for disp, rr in self._rule_index_by_display.items():
                    if rr.KanBanRuleID == rule.KanBanRuleID:
                        self.rule_var.set(disp)
                        break
            else:
                self.current_rule_label.configure(text=self.lang.get('current_rule_unknown', "Regola attiva non trovata"))
        else:
            self.current_rule_label.configure(text=self.lang.get('no_rule', "Nessuna regola associata"))

    def _on_assign(self):
        comp = self._get_selected_component_row()
        if not comp:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"), self.lang.get('component_required', "Seleziona un componente."), parent=self)
            return
        disp = self.rule_var.get()
        rule = self._rule_index_by_display.get(disp)
        if not rule:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"), self.lang.get('rule_required', "Seleziona una regola."), parent=self)
            return
        ok, err = self.db.assign_rule_to_component(comp.IdComponent, rule.KanBanRuleID)
        if ok:
            messagebox.showinfo(self.lang.get('info_title', "Informazione"), self.lang.get('rule_assigned', "Regola associata."), parent=self)
            self._on_component_changed()
        else:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('rule_assign_err', f"Errore associazione: {err or self.db.last_error_details}"),
                                 parent=self)

    def _on_remove(self):
        comp = self._get_selected_component_row()
        if not comp:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"), self.lang.get('component_required', "Seleziona un componente."), parent=self)
            return
        if not messagebox.askyesno(self.lang.get('confirm_title', "Conferma"), self.lang.get('confirm_remove_rule', "Rimuovere la regola attiva?"), parent=self):
            return
        ok, err = self.db.assign_rule_to_component(comp.IdComponent, None)  # solo chiusura
        if ok:
            messagebox.showinfo(self.lang.get('info_title', "Informazione"), self.lang.get('rule_removed', "Regola rimossa."), parent=self)
            self._on_component_changed()
        else:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('rule_remove_err', f"Errore rimozione: {err or self.db.last_error_details}"),
                                 parent=self)

class KanbanMoveForm(tk.Toplevel):
    def __init__(self, master, db_handler, lang_manager):
        super().__init__(master)
        self.db = db_handler
        self.lang = lang_manager

        self.title(self.lang.get('kanban_move_title', 'KanBan - Movimenta'))
        self.geometry("720x420")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        # Stato
        self.op_var = tk.StringVar(value="unload")  # default: Withdrawal
        self._session_user = self._get_app_username()  # utente loggato alla maschera (se esiste)
        self._load_user = None  # utente che fa login quando passa a Load
        self.qty_var = tk.StringVar()
        self.component_var = tk.StringVar()
        self.location_var = tk.StringVar()

        # Cache liste per filtro
        self._components = []   # list of (IdComponent, code, descr)
        self._locations = []    # list of (LocationId, code, area)
        self._in_use_location_ids = set()  # locazioni dove il componente ha stock > 0
        self._build_ui()
        self._load_lists()

    def _build_ui(self):
        root = ttk.Frame(self, padding=12)
        root.pack(fill="both", expand=True)

        # Operazione
        opf = ttk.Labelframe(root, text=self.lang.get('move_operation', 'Operazione'))
        opf.pack(fill="x")
        ttk.Radiobutton(opf, text=self.lang.get('move_load', 'Carico'),
                        variable=self.op_var, value="load", command=self._on_op_changed).pack(side="left", padx=(10, 10), pady=6)
        ttk.Radiobutton(opf, text=self.lang.get('move_unload', 'Prelievo'),
                        variable=self.op_var, value="unload", command=self._on_op_changed).pack(side="left", padx=(0, 10), pady=6)

        # Selezioni
        sf = ttk.Labelframe(root, text=self.lang.get('move_selection', 'Selezione'))
        sf.pack(fill="x", pady=(10, 0))

        r1 = ttk.Frame(sf); r1.pack(fill="x", padx=6, pady=6)
        ttk.Label(r1, text=self.lang.get('component', 'Componente'), width=16).pack(side="left")
        self.cb_component = ttk.Combobox(r1, textvariable=self.component_var, width=50)
        self.cb_component.pack(side="left", fill="x", expand=True)
        self.cb_component.bind("<KeyRelease>", self._on_component_typed)

        # Location row (già presente)
        r2 = ttk.Frame(sf)
        r2.pack(fill="x", padx=6, pady=6)
        ttk.Label(r2, text=self.lang.get('location', 'Locazione'), width=16).pack(side="left")
        self.cb_location = ttk.Combobox(r2, textvariable=self.location_var, width=50)
        self.cb_location.pack(side="left", fill="x", expand=True)
        self.cb_location.bind("<KeyRelease>", self._on_location_typed)

        # HINT: *** in uso per questo componente
        self.lbl_loc_hint = ttk.Label(
            r2,
            text=self.lang.get('loc_in_use_hint', '*** = locazione in uso per questo componente'),
            foreground="gray"
        )
        self.lbl_loc_hint.pack(side="left", padx=(8, 0))

        # Quantity row (già presente)
        r3 = ttk.Frame(sf);
        r3.pack(fill="x", padx=6, pady=6)
        ttk.Label(r3, text=self.lang.get('quantity', 'Quantità'), width=16).pack(side="left")
        ttk.Entry(r3, textvariable=self.qty_var, width=12).pack(side="left")

        # Etichette saldo: qui e altrove
        self.lbl_here_balance = ttk.Label(r3, text=self.lang.get('balance_here', 'Saldo qui: {qty}').format(qty='-'))
        self.lbl_here_balance.pack(side="left", padx=(16, 8))
        self.lbl_other_balance = ttk.Label(r3, text=self.lang.get('balance_other', 'Altrove: {qty}').format(qty='-'))
        self.lbl_other_balance.pack(side="left")

        # Pulsanti
        bf = ttk.Frame(root); bf.pack(fill="x", pady=(12, 0))
        ttk.Button(bf, text=self.lang.get('button_execute', 'Esegui'),
                   command=self._on_execute).pack(side="left")
        ttk.Button(bf, text=self.lang.get('button_import_excel', 'Importa da Excel'),
                   command=self._on_import_excel).pack(side="left", padx=(8,0))
        ttk.Button(bf, text=self.lang.get('button_close', 'Chiudi'),
                   command=self.destroy).pack(side="right")

        # Log/risultati
        self.log = tk.Text(root, height=10, state="disabled")
        self.log.pack(fill="both", expand=True, pady=(12, 0))

        # Component combobox bindings
        self.cb_component.bind("<<ComboboxSelected>>", self._on_component_selected)
        self.cb_component.bind("<FocusOut>", self._on_component_focus_out)

        # Location combobox bindings
        self.cb_location.bind("<<ComboboxSelected>>", self._on_location_selected)
        self.cb_location.bind("<FocusOut>", lambda e: self._update_balances())

    def _on_op_changed(self):
        if self.op_var.get() == "load":
            if not self._ensure_load_login():
                # login annullato/negato: torna a Withdrawal
                self.op_var.set("unload")
                messagebox.showwarning(
                    self.lang.get('warn_title', 'Attenzione'),
                    self.lang.get('load_requires_login', 'Per eseguire un carico è necessario effettuare il login.'),
                    parent=self
                )

    def _load_lists(self):
        # Componenti
        self._components = []
        for r in self.db.fetch_all_components_for_combo():
            self._components.append((r.IdComponent, r.ComponentCode, r.ComponentDescription or ""))
        # Stringhe combo: "CODE - Description"
        comp_items = [f"{c[1]} - {c[2]}" if c[2] else c[1] for c in self._components]
        self.cb_component["values"] = comp_items

        # Locazioni
        self._locations = []
        for r in self.db.fetch_all_locations_for_combo():
            self._locations.append((r.LocationId, r.LocationCode, r.KanBanLocation or ""))
        loc_items = [f"{x[1]} - {x[2]}" if x[2] else x[1] for x in self._locations]
        self.cb_location["values"] = loc_items

    def _on_component_typed(self, event):
        text = self.component_var.get().lower().strip()
        items = []
        for (_id, code, descr) in self._components:
            s = f"{code} - {descr}" if descr else code
            if text in code.lower() or text in (descr or "").lower():
                items.append(s)
        self.cb_component["values"] = items

    def _on_location_typed(self, event):
        text = self.location_var.get().lower().strip()
        items = []
        for (lid, code, area) in self._locations:
            if text in code.lower() or text in (area or "").lower():
                star = " (***)" if lid in getattr(self, "_in_use_location_ids", set()) else ""
                s = f"{code}{star} - {area}" if area else f"{code}{star}"
                items.append(s)
        self.cb_location["values"] = items
        # non aggiorniamo i saldi finché non c'è una locazione valida; ci pensa <<ComboboxSelected>> o FocusOut

    def _resolve_component(self, text: str):
        if not text:
            return None, None, None
        code = text.split(" - ", 1)[0].strip()
        # Prova match veloce dal cache
        for (cid, ccode, cdescr) in self._components:
            if ccode == code:
                return cid, ccode, cdescr
        # Fallback DB
        cid = self.db.get_component_id_by_code(code)
        return (cid, code, None) if cid else (None, None, None)

    def _resolve_location(self, text: str):
        if not text:
            return None, None, None
        code = text.split(" - ", 1)[0].strip()
        code = code.replace(" (***)", "")  # rimuove marcatura
        for (lid, lcode, area) in self._locations:
            if lcode == code:
                return lid, lcode, area
        lid = self.db.get_location_id_by_code(code)
        return (lid, code, None) if lid else (None, None, None)

    def _append_log(self, msg: str):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.configure(state="disabled")
        self.log.see("end")

    def _parse_qty(self):
        s = self.qty_var.get().strip()
        if not s.isdigit():
            return None
        n = int(s)
        return n if n > 0 else None

    def _on_execute(self):
        # Validazioni
        comp_id, comp_code, _ = self._resolve_component(self.component_var.get())
        if not comp_id:
            messagebox.showwarning(self.lang.get('warn_title', 'Attenzione'),
                                   self.lang.get('move_err_select_component', 'Seleziona un componente valido.'),
                                   parent=self)
            return
        loc_id, loc_code, _ = self._resolve_location(self.location_var.get())
        if not loc_id:
            messagebox.showwarning(self.lang.get('warn_title', 'Attenzione'),
                                   self.lang.get('move_err_select_location', 'Seleziona una locazione valida.'),
                                   parent=self)
            return
        qty = self._parse_qty()
        if qty is None:
            messagebox.showwarning(self.lang.get('warn_title', 'Attenzione'),
                                   self.lang.get('move_err_qty_positive', 'La quantità deve essere un intero > 0.'),
                                   parent=self)
            return

        op = self.op_var.get()
        delta = qty if op == "load" else -qty

        # Se prelievo, verifica disponibilità
        if delta < 0:
            avail = self.db.get_current_stock(comp_id, loc_id)
            if avail + delta < 0:
                message = self.lang.get('move_err_stock_insufficient',
                                        'Quantità non disponibile. Disponibile: {avail}').format(avail=avail)
                messagebox.showerror(self.lang.get('error_title', 'Errore'), message, parent=self)
                return

        # Determina l'utente da salvare
        if delta < 0:
            user_to_save = self._session_user or self._get_app_username()
        else:
            if not self._ensure_load_login():
                messagebox.showwarning(
                    self.lang.get('warn_title', 'Attenzione'),
                    self.lang.get('load_requires_login', 'Per eseguire un carico è necessario effettuare il login.'),
                    parent=self
                )
                return
            user_to_save = self._load_user

        ok, err = self.db.insert_kanban_movement(loc_id, comp_id, int(delta), user_to_save)

        if ok:
            msg = self.lang.get('move_ok_load', 'Carico registrato.') if delta > 0 else \
                  self.lang.get('move_ok_unload', 'Prelievo registrato.')
            messagebox.showinfo(self.lang.get('info_title', 'Informazione'), msg, parent=self)
            self._append_log(f"{'+' if delta>0 else ''}{delta} {comp_code} @ {self.location_var.get()} - OK")
            self.qty_var.set("")
            self._refresh_component_dependent_ui()  # riflette il nuovo stock
        else:
            messagebox.showerror(self.lang.get('error_title', 'Errore'),
                                 err or self.db.last_error_details, parent=self)

    def _on_import_excel(self):
        """
        Importa movimenti da file CSV o XLSX con colonne:
          - Component (o codici simili: ComponentCode, Codice, Code)
          - Location (o LocationCode, Locazione, Loc)
          - Quantity (o Qty, Quantita, Qta)
        Regole utente:
          - Prelievo (qty < 0): salva l'utente di sessione (login alla maschera).
          - Carico (qty > 0): al primo carico richiede login; usa quell'utente per tutti i carichi dell'import.
        """
        import os, csv
        from tkinter import filedialog, messagebox

        # Selezione file
        file_path = filedialog.askopenfilename(
            title=self.lang.get('import_select_file', 'Seleziona file movimenti'),
            filetypes=[('Excel/CSV', '*.xlsx *.csv'), ('Excel', '*.xlsx'), ('CSV', '*.csv'), ('Tutti i file', '*.*')]
        )
        if not file_path:
            return

        ext = os.path.splitext(file_path)[1].lower()

        # Lettura righe dal file in una lista di dict con chiavi canoniche: Component, Location, Quantity
        rows = []

        def _canon(key: str) -> str:
            k = (key or '').strip().lower().replace(' ', '').replace('_', '')
            if k in ('component', 'componentcode', 'code', 'codice', 'idcomponent', 'idcomp', 'comp'):
                return 'Component'
            if k in ('location', 'locationcode', 'loc', 'locazione', 'codicelocazione'):
                return 'Location'
            if k in ('quantity', 'qty', 'quantita', 'qta', 'quantità'):
                return 'Quantity'
            return key

        try:
            if ext == '.csv':
                with open(file_path, 'r', encoding='utf-8-sig', newline='') as f:
                    reader = csv.DictReader(f)
                    # Mappa header a canonici
                    field_map = {h: _canon(h) for h in reader.fieldnames or []}
                    for r in reader:
                        row = {field_map.get(k, k): (v if v is not None else '') for k, v in r.items()}
                        rows.append(row)
            elif ext == '.xlsx':
                try:
                    from openpyxl import load_workbook
                except Exception:
                    messagebox.showerror(
                        self.lang.get('error_title', 'Errore'),
                        self.lang.get('openpyxl_missing', 'Per importare file .xlsx è necessario openpyxl.'),
                        parent=self
                    )
                    return
                wb = load_workbook(file_path, data_only=True)
                ws = wb.active
                headers = []
                for j, cell in enumerate(ws[1], start=1):
                    headers.append(_canon(str(cell.value) if cell.value is not None else f'Col{j}'))
                for i, xrow in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                    r = {}
                    for j, val in enumerate(xrow):
                        key = headers[j] if j < len(headers) else f'Col{j + 1}'
                        r[key] = '' if val is None else str(val)
                    rows.append(r)
            else:
                messagebox.showerror(
                    self.lang.get('error_title', 'Errore'),
                    self.lang.get('unsupported_file', 'Formato file non supportato. Usa .csv o .xlsx.'),
                    parent=self
                )
                return
        except Exception as e:
            messagebox.showerror(
                self.lang.get('error_title', 'Errore'),
                self.lang.get('import_read_error', f'Errore lettura file: {e}'),
                parent=self
            )
            return

        if not rows:
            messagebox.showinfo(
                self.lang.get('info_title', 'Informazione'),
                self.lang.get('import_no_rows', 'Nessuna riga da importare.'),
                parent=self
            )
            return

        # Stato utenti per salvataggio
        load_login_done = False
        session_user = self._session_user or self._get_app_username()

        ok_count = 0
        err_count = 0
        first_error_msg = None

        for idx, r in enumerate(rows, start=1):
            comp_text = str(r.get('Component', '') or '').strip()
            loc_text = str(r.get('Location', '') or '').strip()
            qty_text = str(r.get('Quantity', '') or '').strip()

            # Validazioni base
            if not comp_text or not loc_text or not qty_text:
                err_count += 1
                if first_error_msg is None:
                    first_error_msg = self.lang.get('import_err_missing_fields',
                                                    f'Riga {idx}: campi mancanti (Component/Location/Quantity).')
                continue

            # Parse quantità
            try:
                qty = int(float(qty_text))  # accetta "10.0" -> 10
            except Exception:
                err_count += 1
                if first_error_msg is None:
                    first_error_msg = self.lang.get('import_err_qty', f'Riga {idx}: Quantità non valida: {qty_text}')
                continue
            if qty == 0:
                err_count += 1
                if first_error_msg is None:
                    first_error_msg = self.lang.get('import_err_qty_zero', f'Riga {idx}: Quantità zero non valida.')
                continue

            # Risolvi component e location
            comp_id, comp_code, _ = self._resolve_component(comp_text)
            if not comp_id:
                err_count += 1
                if first_error_msg is None:
                    first_error_msg = self.lang.get('import_err_comp',
                                                    f'Riga {idx}: Componente non trovato: {comp_text}')
                continue

            loc_id, loc_code, _ = self._resolve_location(loc_text)
            if not loc_id:
                err_count += 1
                if first_error_msg is None:
                    first_error_msg = self.lang.get('import_err_loc', f'Riga {idx}: Locazione non trovata: {loc_text}')
                continue

            # Determina l'utente da salvare, in base al segno della quantità
            if qty < 0:
                # Prelievo: richiede utente di sessione (maschera)
                if not session_user:
                    # L'app richiede che nei prelievi ci sia un utente loggato alla maschera
                    messagebox.showwarning(
                        self.lang.get('warn_title', 'Attenzione'),
                        self.lang.get('withdraw_requires_session_login',
                                      'Prelievo rilevato nell\'import: è necessario essere loggati alla maschera.'),
                        parent=self
                    )
                    return  # interrompe l'import intero
                user_to_save = session_user
            else:
                # Carico: richiede login on-demand (una sola volta)
                if not load_login_done:
                    if not self._ensure_load_login():
                        messagebox.showwarning(
                            self.lang.get('warn_title', 'Attenzione'),
                            self.lang.get('import_load_requires_login',
                                          'Import annullato: login necessario per i carichi.'),
                            parent=self
                        )
                        return  # interrompe l'import intero
                    load_login_done = True
                user_to_save = self._load_user

            # Controllo disponibilità per prelievo (opzionale, ma utile)
            if qty < 0:
                try:
                    avail = self.db.get_current_stock(comp_id, loc_id)
                except Exception:
                    avail = None
                if avail is not None and avail + qty < 0:
                    err_count += 1
                    if first_error_msg is None:
                        first_error_msg = self.lang.get(
                            'import_err_insufficient',
                            f'Riga {idx}: Quantità non disponibile. Disponibile: {avail}'
                        )
                    continue

            # Inserimento movimento
            ok, err = self.db.insert_kanban_movement(loc_id, comp_id, qty, user_to_save)
            if ok:
                ok_count += 1
                if hasattr(self, '_append_log'):
                    sign = '+' if qty > 0 else ''
                    self._append_log(f"{sign}{qty} {comp_code} @ {loc_code} - {user_to_save} - OK")
            else:
                err_count += 1
                if first_error_msg is None:
                    first_error_msg = self.lang.get('import_err_db', f'Riga {idx}: Errore DB: {err}')
                if hasattr(self, '_append_log'):
                    self._append_log(f"{qty} {comp_code} @ {loc_code} - {user_to_save} - ERR: {err}")

        # Riepilogo
        if err_count == 0:
            messagebox.showinfo(
                self.lang.get('success_title', 'Successo'),
                self.lang.get('import_ok', f'Import completato: {ok_count} movimenti importati.'),
                parent=self
            )
        else:
            msg = self.lang.get('import_summary',
                                f'Import terminato: OK={ok_count}, Errori={err_count}.\n{first_error_msg or ""}')
            messagebox.showwarning(self.lang.get('warn_title', 'Attenzione'), msg, parent=self)

        # Refresh UI/saldi dopo import
        if hasattr(self, '_refresh_component_dependent_ui'):
            try:
                self._refresh_component_dependent_ui()
            except Exception:
                pass

    def _on_component_selected(self, event=None):
        self._refresh_component_dependent_ui()

    def _on_component_focus_out(self, event=None):
        # Se il testo corrisponde a un componente valido, aggiorna UI
        comp_id, _, _ = self._resolve_component(self.component_var.get())
        if comp_id:
            self._refresh_component_dependent_ui()

    def _on_location_selected(self, event=None):
        self._update_balances()

    def _refresh_component_dependent_ui(self):
        """
        Dopo la scelta del componente: marca le locazioni in uso (***), aggiorna i saldi.
        """
        comp_id, _, _ = self._resolve_component(self.component_var.get())
        if not comp_id:
            # reset marcature e saldi
            self._in_use_location_ids = set()
            # ricostruisci la lista locazioni senza marcature
            items = []
            for (lid, code, area) in self._locations:
                s = f"{code} - {area}" if area else code
                items.append(s)
            self.cb_location["values"] = items
            self._update_balances()
            return

        # Ottieni locazioni in uso per il componente
        loc_map = self.db.get_component_locations_with_stock(comp_id)  # {LocationId: Qty}
        self._in_use_location_ids = set(loc_map.keys())

        # Ricostruisci la lista locazioni con (***) dove presente stock
        items = []
        for (lid, code, area) in self._locations:
            star = " (***)" if lid in self._in_use_location_ids else ""
            label = f"{code}{star} - {area}" if area else f"{code}{star}"
            items.append(label)
        self.cb_location["values"] = items

        self._update_balances()

    def _update_balances(self):
        """
        Aggiorna le etichette 'Saldo qui' e 'Altrove' in base a componente/locazione selezionati.
        """
        comp_id, _, _ = self._resolve_component(self.component_var.get())
        if not comp_id:
            self.lbl_here_balance.config(text=self.lang.get('balance_here', 'Saldo qui: {qty}').format(qty='-'))
            self.lbl_other_balance.config(text=self.lang.get('balance_other', 'Altrove: {qty}').format(qty='-'))
            return

        loc_id, _, _ = self._resolve_location(self.location_var.get())
        total = self.db.get_total_stock_component(comp_id)
        here = self.db.get_current_stock(comp_id, loc_id) if loc_id else 0
        other = max(total - here, 0)

        self.lbl_here_balance.config(text=self.lang.get('balance_here', 'Saldo qui: {qty}').format(qty=here))
        self.lbl_other_balance.config(text=self.lang.get('balance_other', 'Altrove: {qty}').format(qty=other))

    def _get_app_username(self):
        app = self.master
        for attr in ('last_authenticated_user_name', 'current_user', 'logged_user',
                     'current_username', 'username', 'user_name', 'session_user'):
            if hasattr(app, attr):
                val = getattr(app, attr)
                if isinstance(val, dict):
                    if 'username' in val and val['username']:
                        return str(val['username'])
                    if 'name' in val and val['name']:
                        return str(val['name'])
                elif val:
                    return str(val)
        return None

    def _ensure_load_login(self) -> bool:
        """
        Richiede il login quando si seleziona 'Load'. Se ok, memorizza _load_user.
        Ritorna True se login effettuato (o già presente), False se annullato/negato.
        """
        if self._load_user:
            return True

        app = self.master
        did_login = {'ok': False}

        def _after_login():
            # Preferisci il nome impostato da _execute_authorized_action; fallback a _get_app_username
            user = getattr(app, 'last_authenticated_user_name', None) or self._get_app_username()
            if user:
                self._load_user = user
                did_login['ok'] = True

        # NB: non affidarti al valore di ritorno (None); usa il flag did_login
        app._execute_authorized_action(menu_translation_key='kanban_load', action_callback=_after_login)
        return did_login['ok']

        def _after_login():
            # Preferisci il nome impostato da _execute_authorized_action; fallback a _get_app_username
            user = getattr(app, 'last_authenticated_user_name', None) or self._get_app_username()
            if user:
                self._load_user = user
                did_login['ok'] = True

        # NB: non affidarti al valore di ritorno (None); usa il flag did_login
        app._execute_authorized_action(menu_translation_key='kanban_load', action_callback=_after_login)
        return did_login['ok']
        def _after_login():
            # Preferisci il nome impostato da _execute_authorized_action; fallback a _get_app_username
            user = getattr(app, 'last_authenticated_user_name', None) or self._get_app_username()
            if user:
                self._load_user = user
                did_login['ok'] = True

        # NB: non affidarti al valore di ritorno (None); usa il flag did_login
        app._execute_authorized_action(menu_translation_key='kanban_load', action_callback=_after_login)
        return did_login['ok']

class PrinterSetupDialog(tk.Toplevel):
    def __init__(self, master, lang):
        super().__init__(master)
        self.lang = lang
        self.title(self.lang.get('printer_setup_title', "Configurazione stampante"))
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.name_var = tk.StringVar()
        self.ip_var = tk.StringVar()
        self.port_var = tk.StringVar(value="9100")
        self.dpi_var = tk.StringVar(value="203")
        self.textpt_var = tk.StringVar(value="12")

        frm = ttk.Frame(self, padding=16)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text=self.lang.get('printer_name', "Nome stampante")).grid(row=0, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.name_var, width=36).grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(frm, text="IP").grid(row=1, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.ip_var, width=36).grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(frm, text=self.lang.get('printer_port', "Porta")).grid(row=2, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.port_var, width=10).grid(row=2, column=1, sticky="w", pady=4)

        ttk.Label(frm, text=self.lang.get('printer_dpi', "DPI")).grid(row=3, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.dpi_var, width=10).grid(row=3, column=1, sticky="w", pady=4)

        ttk.Label(frm, text=self.lang.get('printer_textpt', "Corpo testo")).grid(row=4, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.textpt_var, width=10).grid(row=4, column=1, sticky="w", pady=4)

        # Bottoni azione
        btns = ttk.Frame(frm)
        btns.grid(row=10, column=0, columnspan=2, sticky="e", pady=(10,0))

        # Extra: Apri cartella config
        ttk.Button(btns, text=self.lang.get('printer_open_folder', "Apri cartella"),
                   command=open_config_folder).pack(side="left")

        # Extra: Test stampa veloce
        ttk.Button(btns, text=self.lang.get('printer_test', "Test stampa"),
                   command=self._test_print).pack(side="left", padx=(8, 0))

        ttk.Button(btns, text=self.lang.get('button_cancel', "Annulla"),
                   command=self._cancel).pack(side="right")
        ttk.Button(btns, text=self.lang.get('button_save', "Salva"),
                   command=self._save).pack(side="right", padx=(0,6))

        frm.columnconfigure(1, weight=1)

        # Precarica config
        cur = load_printer_config()
        if cur:
            self.name_var.set(cur.get("name",""))
            self.ip_var.set(cur.get("ip",""))
            self.port_var.set(str(cur.get("port","9100")))
            self.dpi_var.set(str(cur.get("dpi","203")))
            self.textpt_var.set(str(cur.get("text_pt","12")))

    def _cancel(self):
        self.result = None
        self.destroy()

    def _save(self):
        name = self.name_var.get().strip()
        ip = self.ip_var.get().strip()
        port = self.port_var.get().strip()
        dpi = self.dpi_var.get().strip()
        textpt = self.textpt_var.get().strip()

        if not name or not ip or not port:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"),
                                   self.lang.get('printer_required', "Compila nome, IP e porta."), parent=self)
            return
        if not validate_ip(ip):
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"),
                                   self.lang.get('printer_ip_invalid', "IP non valido."), parent=self)
            return
        try:
            port_i = int(port)
            dpi_i = int(dpi)
            textpt_i = int(textpt)
        except ValueError:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"),
                                   self.lang.get('printer_numeric_required', "Porta, DPI e corpo testo devono essere numerici."), parent=self)
            return

        cfg = {
            "name": name,
            "ip": ip,
            "port": port_i,
            "dpi": dpi_i,
            "label_cm": [5, 5],
            "text_pt": textpt_i,
            "language": "ZPL",
            "version": 1
        }
        ok, err = save_printer_config(cfg)
        if not ok:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('printer_save_error', f"Impossibile salvare la configurazione. {err}"),
                                 parent=self)
            return

        self.result = cfg
        self.destroy()

    def _test_print(self):
        # Costruisce e invia una piccola etichetta di test
        try:
            ip = self.ip_var.get().strip()
            port = int(self.port_var.get().strip())
            dpi = int(self.dpi_var.get().strip() or "203")
        except ValueError:
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"),
                                   self.lang.get('printer_numeric_required', "Porta, DPI e corpo testo devono essere numerici."), parent=self)
            return
        if not validate_ip(ip):
            messagebox.showwarning(self.lang.get('warn_title', "Attenzione"),
                                   self.lang.get('printer_ip_invalid', "IP non valido."), parent=self)
            return
        zpl = "^XA^CI28^PW400^LL400^FO20,20^A0N,40,40^FDTest stampa^FS^FO20,80^GB350,1,1^FS^XZ"
        ok, err = send_raw_to_printer(ip, port, zpl.encode("utf-8"))
        if ok:
            messagebox.showinfo(self.lang.get('info_title', "Informazione"),
                                self.lang.get('print_ok', "Stampa inviata alla stampante."), parent=self)
        else:
            messagebox.showerror(self.lang.get('error_title', "Errore"),
                                 self.lang.get('print_error', f"Errore di stampa: {err}"), parent=self)

class ViewDocumentForm(tk.Toplevel):
    """Finestra per visualizzare un documento (di Produzione)."""

    def __init__(self, master, db_handler, lang_manager):
        super().__init__(master)
        self.db = db_handler
        self.lang = lang_manager

        self.transient(master)
        self.grab_set()

        self.products_data = {}
        self.all_product_names = []
        self.parent_phases_data = {}
        self.documents_in_phase = []

        self.product_var = tk.StringVar()
        self.parent_phase_var = tk.StringVar()

        self._create_widgets()
        self.update_texts()
        self._load_products()

    def _create_widgets(self):
        self.geometry("600x350")
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(0, weight=1)

        self.product_label = ttk.Label(frame, font=("Helvetica", 10, "bold"))
        self.product_label.pack(fill=tk.X, pady=(0, 5))
        self.product_combo = ttk.Combobox(frame, textvariable=self.product_var, width=50)
        self.product_combo.pack(fill=tk.X, pady=(0, 15))
        self.product_combo.bind("<<ComboboxSelected>>", self._on_product_select)
        self.product_combo.bind("<KeyRelease>", self._on_product_keyrelease)

        self.phase_label = ttk.Label(frame, font=("Helvetica", 10, "bold"))
        self.phase_label.pack(fill=tk.X, pady=(0, 5))
        self.parent_phase_combo = ttk.Combobox(frame, textvariable=self.parent_phase_var, state="disabled", width=50)
        self.parent_phase_combo.pack(fill=tk.X, pady=(0, 15))
        self.parent_phase_combo.bind("<<ComboboxSelected>>", self._on_phase_select)

        self.docs_listbox = tk.Listbox(frame, height=5)
        self.docs_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        self.docs_listbox.bind("<Double-1>", self._on_doc_double_click)  # Evento doppio click

        self.close_button = ttk.Button(frame, command=self.destroy)
        self.close_button.pack(side="bottom", pady=10)

    def update_texts(self):
        """Aggiorna i testi della UI."""
        self.title(self.lang.get('view_doc_title'))
        self.product_label.config(text=self.lang.get('label_select_product'))
        self.phase_label.config(text=self.lang.get('label_select_phase'))
        self.close_button.config(text=self.lang.get('button_close'))

    def _load_products(self):
        products = self.db.fetch_products_with_documents()
        if products:
            self.products_data = {p.ProductCode: p.IDProduct for p in products}
            self.all_product_names = list(self.products_data.keys())
            self.product_combo['values'] = self.all_product_names
        else:
            messagebox.showwarning(self.lang.get('app_title'), self.lang.get('warn_no_products_found'), parent=self)

    def _on_product_keyrelease(self, event):
        typed_text = self.product_var.get()
        if not typed_text:
            self.product_combo['values'] = self.all_product_names
        else:
            filtered_list = [name for name in self.all_product_names if typed_text.lower() in name.lower()]
            self.product_combo['values'] = filtered_list

    def _on_product_select(self, event=None):
        self.parent_phase_var.set("")
        self.parent_phase_combo.config(state="disabled", values=[])
        self.docs_listbox.delete(0, tk.END)
        self.documents_in_phase = []

        product_id = self.products_data.get(self.product_var.get())
        if product_id:
            # --- RIGA MODIFICATA ---
            # Ora chiama il nuovo metodo per ottenere solo le fasi con documenti
            parent_phases = self.db.fetch_phases_with_documents_for_product(product_id)
            # --- FINE MODIFICA ---

            if parent_phases:
                # La logica per popolare il combobox rimane la stessa
                self.parent_phases_data = {p.ParentPhaseName: p.IDParentPhase for p in parent_phases}
                self.parent_phase_combo.config(state="readonly", values=list(self.parent_phases_data.keys()))
            else:
                # Questo messaggio ora significa che non ci sono documenti per questo prodotto
                messagebox.showwarning(self.lang.get('app_title'), self.lang.get('warn_no_document_found_for_product',
                                                                                 "Nessun documento trovato per il prodotto selezionato."),
                                       parent=self)

    def _on_phase_select(self, event=None):
        """Popola la lista dei documenti."""
        self.docs_listbox.delete(0, tk.END)
        self.documents_in_phase = []

        product_id = self.products_data.get(self.product_var.get())
        parent_phase_id = self.parent_phases_data.get(self.parent_phase_var.get())

        if not (product_id and parent_phase_id):
            return

        # 1. Recupera la lista di tutti i documenti per la fase scelta
        self.documents_in_phase = self.db.fetch_existing_documents(product_id, parent_phase_id)

        if not self.documents_in_phase:
            messagebox.showwarning(self.lang.get('app_title'), self.lang.get('warn_no_document_found'), parent=self)
        else:
            # 2. Popola la Listbox con i nomi dei documenti trovati
            for doc in self.documents_in_phase:
                self.docs_listbox.insert(tk.END, f"{doc.documentName} (Rev: {doc.DocumentRevisionNumber})")

    def _on_doc_double_click(self, event=None):
        """Gestisce il doppio click su un documento nella lista."""
        selected_indices = self.docs_listbox.curselection()
        if not selected_indices:
            return

        selected_index = selected_indices[0]
        # Recupera il documento corrispondente dalla lista che abbiamo salvato
        selected_doc = self.documents_in_phase[selected_index]

        # Chiama il metodo corretto per recuperare e aprire il file binario usando il suo ID
        print(f"Richiesta apertura documento con ID: {selected_doc.DocumentProductionID}")
        success = self.db.fetch_and_open_document(selected_doc.DocumentProductionID)
        if not success:
            messagebox.showerror(self.lang.get('error_title', "Errore"), "Impossibile aprire il documento.",
                                 parent=self)

class LineStoppageReportForm(tk.Toplevel):
    def __init__(self, parent, db_handler, lang_manager):
        super().__init__(parent)
        self.db = db_handler
        self.lang = lang_manager

        self.title(self.lang.get('line_stoppage_report_title', "Report Fermi Linea"))
        self.geometry("400x300")

        # Crea il frame principale
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Date selectors
        date_frame = ttk.LabelFrame(main_frame, text=self.lang.get('date_range_label', "Intervallo Date"),
                                    padding="10")
        date_frame.pack(fill=tk.X, pady=(0, 20))

        # From Date
        ttk.Label(date_frame, text=self.lang.get('from_date_label', "Da:")).grid(row=0, column=0, padx=5, pady=5)
        self.from_date = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.from_date.grid(row=0, column=1, padx=5, pady=5)

        # To Date
        ttk.Label(date_frame, text=self.lang.get('to_date_label', "A:")).grid(row=1, column=0, padx=5, pady=5)
        self.to_date = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.to_date.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)

        ttk.Button(button_frame, text=self.lang.get('generate_report_button', "Genera Report"),
                   command=self._generate_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.lang.get('close_button', "Chiudi"),
                   command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def _generate_report(self):
        """Genera il report Excel dei fermi linea."""
        try:
            # Esegue la query
            query = """
                SELECT [BreakDownProblemLogId] AS ID,
                       cast([DateReport] as DATE) AS ReportIussedOn,
                       [HourReport] as TimeIussed,
                       [FromHour] as FromTime,
                       [ToHour] as ToTime,
                       [UserName] AS IussedBy,
                       wa.AreaName As WorkingArea,
                       ia.IssueArea As Thema,
                       WS.AreaSubName As SubWorkingArea,
                       WL.WorkingLineName As Line,
                       [Lost_OR_Gain] AS BreakDownType,
                       [Hours] AS NrMinutesBreakDown,
                       [PoNumber],
                       [ProductCode],
                       [ip].DescriptionEN As BreakDownReason,
                       cast([Note] as text) as [Note],
                       CAST([DateSys] as datetime) As RealDataEntry 
                FROM [ResetServices].[BreakDown].[ReportIssueLogs] AS RI 
                inner join [ResetServices].[BreakDown].IssuesAreas AS IA on Ri.IssueAreaId=IA.IssueAreaId 
                inner join [ResetServices].[BreakDown].WorkingAreas as WA on Wa.WorkingAreaID=RI.WorkingAreaID 
                inner join [ResetServices].[BreakDown].WorkingLines AS WL on WL.WorkingLineID=RI.WorkingLineID 
                inner join [ResetServices].[BreakDown].WorkingSubAreas AS WS on WS.WorkingSubAreaID=Ri.WorkingSubAreaID 
                inner join [ResetServices].[BreakDown].IssueProblems AS [IP] on [IP].IssueProblemId=ri.IssueProblemId 
                Where Datereport between ? AND ?
                """

            # Esegue la query con i parametri delle date
            self.db.cursor.execute(query, (self.from_date.get_date(), self.to_date.get_date()))
            results = self.db.cursor.fetchall()

            if not results:
                messagebox.showinfo(self.lang.get('info_title', "Informazione"),
                                    self.lang.get('no_data_found',
                                                  "Nessun dato trovato per il periodo selezionato."),
                                    parent=self)
                return

            # Crea la cartella C:\temp se non esiste
            temp_dir = r"C:\temp"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # Genera il nome del file con timestamp
            timestamp = datetime.now().strftime("%y%m%d%H%M%S")
            file_name = f"ReportBreakDown{timestamp}.xlsx"
            file_path = os.path.join(temp_dir, file_name)

            # Usa pandas per creare un Excel formattato
            df = pd.DataFrame.from_records(results, columns=[x[0] for x in self.db.cursor.description])

            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Report Fermi Linea', index=False)

                # Ottiene il foglio di lavoro
                worksheet = writer.sheets['Report Fermi Linea']

                # Formatta le intestazioni
                header_format = writer.book.add_format({
                    'bold': True,
                    'fg_color': '#D7E4BC',
                    'border': 1,
                    'align': 'center'
                })

                # Formatta le date
                date_format = writer.book.add_format({'num_format': 'dd/mm/yyyy'})
                time_format = writer.book.add_format({'num_format': 'hh:mm'})

                # Applica la formattazione alle intestazioni e imposta le larghezze delle colonne
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)

                    # Imposta larghezze colonne specifiche
                    if 'Date' in value or 'Data' in value:
                        worksheet.set_column(col_num, col_num, 12)
                        # Applica formato data alle celle della colonna
                        worksheet.set_column(col_num, col_num, 12, date_format)
                    elif 'Time' in value or 'Hour' in value:
                        worksheet.set_column(col_num, col_num, 10)
                        # Applica formato ora alle celle della colonna
                        worksheet.set_column(col_num, col_num, 10, time_format)
                    elif value in ['Note', 'BreakDownReason']:
                        worksheet.set_column(col_num, col_num, 40)
                    else:
                        worksheet.set_column(col_num, col_num, 15)

                # Imposta filtri automatici
                worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)

                # Congela la prima riga
                worksheet.freeze_panes(1, 0)

            # Apre il file Excel direttamente
            os.startfile(file_path)

            # Chiude la finestra del form
            self.destroy()

        except Exception as e:
            messagebox.showerror(
                self.lang.get('error_title', "Errore"),
                self.lang.get('error_generating_report', f"Errore durante la generazione del report: {str(e)}"),
                parent=self
            )

def connect_to_database():
    """Stabilisce la connessione al database usando la configurazione sicura"""
    try:
        # Ottieni la stringa di connessione sicura
        from database_config import db_config
        conn_str = db_config.get_connection_string()

        # DEBUG: Controlla il tipo e il valore
        logger.info(f"Tipo conn_str: {type(conn_str)}")
        if not isinstance(conn_str, str):
            error_msg = f"ERRORE: conn_str non è una stringa! Tipo: {type(conn_str)}, Valore: {conn_str}"
            logger.error(error_msg)
            raise TypeError(error_msg)

        logger.info("Tentativo di connessione al database...")

        # Connessione con timeout
        timeout = db_config.get_connection_params().get('timeout', 30)
        conn = pyodbc.connect(conn_str, timeout=timeout)

        logger.info("Connessione al database stabilita con successo")
        return conn

    except pyodbc.Error as e:
        logger.error(f"Errore di connessione al database: {e}")
        raise
    except Exception as e:
        logger.error(f"Errore imprevisto nella connessione: {e}")
        raise

class User:
    """Una semplice classe per contenere i dati dell'utente loggato."""
    def __init__(self, name, permissions=None):
        self.name = name
        # Usiamo un 'set' per ricerche di permessi super veloci
        self.permissions = set(permissions) if permissions else set()

    def has_permission(self, permission_key):
        """Verifica se l'utente ha un permesso specifico."""
        return permission_key in self.permissions

class App(tk.Tk):
    """Classe principale dell'applicazione."""

    def __init__(self):
        super().__init__()
        logger.debug("INIT: start __init__")
        self.should_exit = False  # Flag to control shutdown
        self.geometry("1024x768")

        # Variabili per lo slideshow
        self.slideshow_label = None
        self.slideshow_photo = None  # Riferimento per evitare garbage collection
        self.image_files = []
        self.current_image_index = 0
        self.slideshow_interval_ms = 60000  # Default a 1 minuto
        self.slideshow_job_id = None

        # --- NUOVE VARIABILI PER IL FLASHING ---
        self.birthday_flash_job_id = None
        self.birthday_stop_job_id = None
        self.periodic_check_job_id = None
        # --- NUOVE VARIABILI PER LA SCRITTA SCORREVOLE ---
        self.scrolling_job_id = None
        self.scrolling_text = ""
        self.scrolling_position = 0
        # Lista di colori vivaci per l'effetto
        self.flash_colors = ["#FFD700", "#FF4500", "#1E90FF", "#32CD32", "#FF69B4", "#9400D3"]
        # --- FINE ---

        # Inizializza il database
        self.db = Database(DB_CONN_STR)
        logger.info("Connessione al database stabilita con successo")
        if not self.db.connect():
            logger.debug("INIT: DB connect OK")
            messagebox.showerror("Database Error",
                                 f"Impossibile connettersi al database.\n\nDetails: {self.db.last_error_details}")
            self.destroy()
            self.should_exit = True
            return

        # Carica la lingua salvata
        initial_lang = self._load_language_setting()
        logger.debug("INIT: language setting loaded -> %s", initial_lang)
        self.lang = LanguageManager(self.db)
        logger.debug("INIT: LanguageManager loaded")
        self.lang.set_language(initial_lang)
        self.doc_categories = self.db.fetch_doc_categories()

        # Controlla la versione (e se l'app deve chiudersi)
        if self.check_version() is False:
            # check_version already handles shutdown, we just need to stop __init__
            return
        logger.debug("INIT: after check_version")

        self.traceability_manager = TraceabilityManager(self, self.db, self.lang)
        logger.debug("INIT: traceability manager OK")

        self.logo_label = None
        self.authenticated_user_for_maintenance = None
        self._create_widgets()
        logger.debug("INIT: widgets created")
        self._create_menu()
        self.update_idletasks()
        self.deiconify()
        self.lift()
        self.focus_force()

        self.attributes('-topmost', True)
        self.after(500, lambda: self.attributes('-topmost', False))

        #self.after(1000, lambda: messagebox.showinfo("Test", "UI pronta e reattiva.", parent=self))

        logger.debug("INIT: menu created")
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.update_texts()
        logger.debug("INIT: texts updated")
        self._update_clock()  # Avvia l'orologio

        self.after(100, self._post_startup_tasks)
        logger.debug("INIT: scheduled post_startup_tasks")

        # Aggiungi questi attributi per FCT Transfer
        self.fct_config = fct_transfer.FCTTransferConfig()
        self.fct_manager = fct_transfer.FCTTransferManager(DB_CONN_STR, self.fct_config)
        self.fct_run_menu_index = None  # Per tenere traccia del menu item

        # Inizializza il thread per il controllo periodico prodotti
        self._product_check_thread = None
        self._product_check_stop_event = threading.Event()

        # Avvia la routine di controllo prodotti
        self._start_product_check_routine()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._start_product_check_background_task()

    def open_scrap_validation_with_login(self):
        """Apre la finestra di validazione scarti dopo login."""

        def action():
            user_name = getattr(self, 'last_authenticated_user_name', 'Unknown')
            scrap_validation_gui.open_scrap_validation(self, self.db, self.lang, user_name)

        self._execute_authorized_action('validate_scrap', action)

    def _start_product_check_background_task(self):
        """Avvia il thread per il controllo periodico dei prodotti"""
        if self._product_check_thread is None or not self._product_check_thread.is_alive():
            self._product_check_stop_event.clear()
            self._product_check_thread = threading.Thread(
                target=self._product_check_worker,
                daemon=True,  # Il thread termina quando l'app si chiude
                name="ProductCheckWorker"
            )
            self._product_check_thread.start()
            logger.info("Background task per controllo prodotti avviato")

    def _product_check_worker(self):
        """Worker thread che esegue periodicamente la SP InsertProductToCheck"""
        while not self._product_check_stop_event.is_set():
            try:
                # 1. Leggi l'intervallo in minuti dal database
                interval_minutes = self.db.get_product_check_interval()

                if interval_minutes <= 0:
                    logger.warning("Intervallo controllo prodotti non valido, uso default 30 min")
                    interval_minutes = 30

                logger.info(f"Prossimo controllo prodotti tra {interval_minutes} minuti")

                # 2. Attendi per l'intervallo specificato (con controllo stop ogni 10 secondi)
                wait_seconds = interval_minutes * 60
                elapsed = 0
                while elapsed < wait_seconds and not self._product_check_stop_event.is_set():
                    time.sleep(10)  # Check ogni 10 secondi per permettere stop rapido
                    elapsed += 10

                if self._product_check_stop_event.is_set():
                    break

                # 3. Esegui la stored procedure
                logger.info("Esecuzione SP InsertProductToCheck...")
                success = self.db.execute_product_check_sp()

                if success:
                    logger.info("✓ SP InsertProductToCheck eseguita con successo")

                    # 4. (Opzionale) Verifica se ci sono nuovi prodotti da controllare
                    # e mostra una notifica all'utente
                    self._check_and_notify_pending_verifications()
                else:
                    logger.error(f"✗ Errore esecuzione SP: {self.db.last_error_details}")

            except Exception as e:
                logger.error(f"Errore nel worker controllo prodotti: {e}", exc_info=True)
                # In caso di errore, attendi 5 minuti prima di riprovare
                time.sleep(300)

        logger.info("Background task controllo prodotti terminato")

    def _show_verification_notification(self, count):
        """Mostra una notifica all'utente (eseguito nel thread principale)"""
        msg = f"⚠️ Ci sono {count} prodotti che necessitano verifica!"
        logger.info(msg)

        # Opzione 1: Messagebox (invasivo)
        # messagebox.showinfo(self.lang.get('app_title'), msg)

        # Opzione 2: Label temporanea nella status bar (meno invasivo)
        if hasattr(self, 'status_label'):
            original_text = self.status_label.cget('text')
            self.status_label.config(text=f"⚠️ {msg}", foreground='orange')
            # Ripristina dopo 10 secondi
            self.after(10000, lambda: self.status_label.config(
                text=original_text, foreground='black'))

    def _stop_product_check_background_task(self):
        """Ferma il thread di controllo prodotti (chiamato alla chiusura app)"""
        if self._product_check_thread and self._product_check_thread.is_alive():
            logger.info("Arresto background task controllo prodotti...")
            self._product_check_stop_event.set()
            self._product_check_thread.join(timeout=5)

    def _check_and_notify_pending_verifications(self):
        """Controlla se ci sono verifiche pendenti e notifica l'utente"""
        try:
            pending = self.db.fetch_products_must_check()

            if pending:
                count = len(pending)
                # Mostra notifica nella UI (thread-safe)
                self.after(0, lambda: self._show_verification_notification(count))
        except Exception as e:
            logger.error(f"Errore controllo verifiche pendenti: {e}")

    def _open_product_checks_management(self):
        """Apre la finestra di gestione periodicità verifiche prodotti"""
        import product_checks_gui
        product_checks_gui.ProductChecksManagementWindow(
            self, self.db, self.lang, self._temp_authorized_user_id
        )

    def _open_check_tasks_management(self):
        """Apre la finestra di gestione task di verifica"""
        import product_checks_gui
        product_checks_gui.CheckTasksManagementWindow(
            self, self.db, self.lang, self._temp_authorized_user_id
        )

    def _open_product_verification(self):
        """Apre la finestra di esecuzione verifiche prodotti"""
        import product_checks_gui
        product_checks_gui.ProductVerificationWindow(
            self, self.db, self.lang, self._temp_authorized_user_id
        )

    def _start_product_check_routine(self):
        """Avvia la routine periodica di controllo prodotti"""

    def open_coating_reports_direct(self):
        """Apre i report coating SENZA login"""
        try:
            from coating_gui import show_coating_reports_direct
            show_coating_reports_direct()
        except Exception as e:
            messagebox.showerror(
                self.lang.get('error', 'Errore'),
                f"{self.lang.get('error_opening_coating_reports', 'Errore apertura report coating')}: {str(e)}"
            )

    def _schedule_kanban_refill_check(self, manual=False):
        """
        Pianifica il controllo refill Kanban su base configurabile (JSON stampante).
        """
        try:
            cfg = load_printer_config() or {}
            enabled = bool(cfg.get("kanban_refill_enabled", True))
            minutes = int(cfg.get("kanban_refill_check_minutes", 60))
        except Exception:
            enabled = True
            minutes = 60

        if not enabled or minutes <= 0:
            return

        self._kanban_refill_check_async(manual=manual)

        # Esegui subito la prima volta in background
        self._kanban_refill_check_async()

        # Pianifica ripetizione
        interval_ms = max(60_000, minutes * 60 * 1000)
        # Salva l'id per eventuale cancel
        self.kanban_refill_job_id = self.after(interval_ms, self._schedule_kanban_refill_check)

    def _kanban_refill_check_async(self, manual=False):
        """
        Avvia il controllo in un thread per non bloccare la UI.
        """
        import threading
        threading.Thread(
            target=self._kanban_refill_check_worker,
            kwargs={'manual': manual},
            name="KanbanRefillCheck",
            daemon=True).start()

    def _kanban_refill_check_worker(self, manual=False):
        """
        Logica di controllo:
        - calcola stock correnti per componente
        - calcola soglia (assoluta o % su prima quantità) per i componenti con regola
        - per i componenti senza regola, soglia=0
        - se stock <= soglia -> prepara richiesta: Qty = max singolo carico; dedup su KanBanRecordId/day
        - genera Excel, invia mail, salva righe in knb.KanBanMaterialRequestes
        """
        log = logging.getLogger("TraceabilityRS")
        try:
            # 1. Stock corrente per componente
            stock_map = self.db.fetch_kanban_current_stock_by_component()  # {comp: stock}

            if not stock_map:
                if manual:
                    self.after(0, lambda: messagebox.showinfo(
                        self.lang.get('info_title', 'Informazione'),
                        self.lang.get('kanban_refill_none', 'Nessun componente da richiedere.')
                    ))
                return

            comp_ids = list(stock_map.keys())

            # 2. Regole attive per componente
            rules_map = self.db.fetch_active_rules_by_component()  # {comp: {'min_qty':..., 'min_pct':...}}

            # 3. Prima quantità (per chi ha regola percentuale)
            pct_comp_ids = [cid for cid, r in rules_map.items() if r.get('min_pct') is not None]
            first_qty_map = self.db.fetch_first_load_qty_by_component(pct_comp_ids) if pct_comp_ids else {}

            # 4. Max singolo carico + record id
            max_load_map = self.db.fetch_max_single_load_by_component(comp_ids)  # {comp: {'max_qty','record_id'}}

            # 5. Master component
            master_map = self.db.fetch_components_master(comp_ids)  # {comp: {'code','desc'}}

            # 6. Valuta richieste
            requests = []  # elementi: dict con info per Excel e per insert
            for cid, cur_stock in stock_map.items():
                rule = rules_map.get(cid)
                if rule:
                    if rule.get('min_qty') is not None:
                        threshold = int(rule['min_qty'])
                        rule_type = "ABS"
                        rule_value = threshold
                    else:
                        # percentuale: calcolo su prima quantità
                        base = int(first_qty_map.get(cid, 0))
                        pct = int(rule.get('min_pct') or 0)
                        # floor per non anticipare troppo
                        threshold = int((base * pct) / 100) if base > 0 and pct > 0 else 0
                        rule_type = "PCT"
                        rule_value = pct
                else:
                    threshold = 0
                    rule_type = "NA"
                    rule_value = None

                if cur_stock <= threshold:
                    ml = max_load_map.get(cid)
                    if not ml:
                        continue
                    qty_to_refill = int(ml['max_qty'])
                    krec_id = int(ml['record_id'])
                    # dedup: se già presente oggi per questa KanBanRecordId, salta
                    if self.db.has_refill_request_today(krec_id):
                        continue
                    # prepara riga
                    meta = master_map.get(cid, {'code': f"#{cid}", 'desc': ''})
                    requests.append({
                        'component_id': cid,
                        'component_code': meta['code'],
                        'component_desc': meta['desc'],
                        'current_stock': int(cur_stock),
                        'threshold': int(threshold),
                        'rule_type': rule_type,
                        'rule_value': rule_value,
                        'max_single_load': qty_to_refill,
                        'qty_to_refill': qty_to_refill,
                        'kanban_record_id': krec_id
                    })

            if not requests:
                if manual:
                    self.after(0, lambda: messagebox.showinfo(
                        self.lang.get('info_title', 'Informazione'),
                        self.lang.get('kanban_refill_none', 'Nessun componente da richiedere.')
                    ))
                return

            # 7. Genera Excel in memoria
            excel_bytes = self._build_kanban_refill_excel(requests)

            # 8. Destinatari mail
            try:
                recipients = utils.get_email_recipients(self.db.conn, attribute='Sys_email_KanBanRefill')
            except Exception as e:
                log.error("KanbanRefill: error reading recipients: %s", e)
                recipients = []

            if not recipients:
                log.warning("KanbanRefill: no recipients for Sys_email_KanBanRefill; skipping email.")
                return

            # 9. Invia email (con allegato Excel)
            subject = "[Kanban] Refill request - Repair Kanban"
            body = (
                "Dear Colleagues,\n\n"
                "Please find attached the refill request for dedicated materials of the repairers' KANBAN.\n"
                "The list includes all components whose current stock is at or below the configured reorder point.\n\n"
                "Regards,\nTraceability System"
            )

            # Nota: adegua utils.send_email se non gestisce attach; qui assumiamo supports attachments=[(filename, bytes)]
            try:
                utils.send_email(
                    recipients=recipients,
                    subject=subject,
                    body=body,
                    attachments=[("KanbanRefill.xlsx", excel_bytes)]
                )
                log.info("KanbanRefill: email sent to %d recipients.", len(recipients))
            except Exception as e:
                log.error("KanbanRefill: email send failed: %s", e)
                return

            # 10. Registra richieste su DB
            for req in requests:
                ok = self.db.insert_refill_request(req['kanban_record_id'], req['qty_to_refill'])
                if not ok:
                    log.warning("KanbanRefill: insert failed for KanBanRecordId=%s: %s",
                                req['kanban_record_id'], self.db.last_error_details)

        except Exception as e:
            logging.getLogger("TraceabilityRS").exception("KanbanRefill job failed: %s", e)

    def _build_kanban_refill_excel(self, rows: list[dict]) -> bytes:
        """
        Crea un Excel ben formattato in memoria e ritorna i bytes.
        Colonne: Component, Description, Current stock, Threshold, Rule type, Rule value, Max single load, Qty requested.
        """
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
        import io

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Kanban Refill"

        headers = ["Component", "Description", "Current stock", "Threshold",
                   "Rule type", "Rule value", "Max single load", "Qty requested"]
        ws.append(headers)

        # Header style
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(fill_type="solid", start_color="4F81BD", end_color="4F81BD")
        center = Alignment(horizontal="center", vertical="center")
        thin = Side(style='thin', color='B7CCE1')
        header_border = Border(left=thin, right=thin, top=thin, bottom=thin)

        for c in range(1, len(headers) + 1):
            cell = ws.cell(row=1, column=c)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center
            cell.border = header_border

        # Rows with zebra stripes and borders
        alt_fill = PatternFill(fill_type="solid", start_color="EEF3F7", end_color="EEF3F7")
        data_border = Border(left=thin, right=thin, top=thin, bottom=thin)

        for i, r in enumerate(rows, start=2):
            values = [
                r['component_code'],
                r['component_desc'],
                r['current_stock'],
                r['threshold'],
                r['rule_type'],
                r['rule_value'] if r['rule_type'] == 'PCT' else (r['rule_value'] if r['rule_type'] == 'ABS' else ""),
                r['max_single_load'],
                r['qty_to_refill']
            ]
            ws.append(values)
            if i % 2 == 0:
                for c in range(1, len(headers) + 1):
                    ws.cell(row=i, column=c).fill = alt_fill
            for c in range(1, len(headers) + 1):
                ws.cell(row=i, column=c).border = data_border

        # Autofit columns
        for col_idx in range(1, len(headers) + 1):
            col_letter = get_column_letter(col_idx)
            max_len = len(headers[col_idx - 1])
            for r in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=col_idx, max_col=col_idx):
                v = r[0].value
                if v is not None:
                    max_len = max(max_len, len(str(v)))
            ws.column_dimensions[col_letter].width = min(max_len + 3, 60)

        # Filters, freeze
        ws.auto_filter.ref = f"A1:H{ws.max_row}"
        ws.freeze_panes = "A2"

        buf = io.BytesIO()
        wb.save(buf)
        logger.info('File xls per richiesta materiali di kanban creato')
        return buf.getvalue()

    def open_kanban_move(self):
        ok = self._execute_authorized_action(
            menu_translation_key='kanban_move',
            action_callback=lambda: KanbanMoveForm(self, self.db, self.lang)
        )
        if not ok:
            return

    def open_kanban_materials_report(self):
        import os
        from datetime import datetime
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
        from tkinter import messagebox

        rows = self.db.fetch_components_locations_report()
        if not rows:
            messagebox.showinfo(self.lang.get('info_title', 'Informazione'),
                                self.lang.get('materials_report_no_data', 'Nessun dato da esportare.'))
            return

        # Workbook e foglio
        wb = Workbook()
        ws = wb.active
        ws.title = self.lang.get('materials_report_title', 'Materiali - Report')

        # Intestazioni con filtro e colore azzurro tenue
        headers = [
            self.lang.get('col_component_code', 'Codice componente'),
            self.lang.get('col_description', 'Descrizione'),
            self.lang.get('col_location', 'Locazione'),
            self.lang.get('col_area', 'Area')
        ]
        ws.append(headers)

        header_fill = PatternFill(fill_type='solid', start_color='DDEBF7', end_color='DDEBF7')  # azzurro tenue
        header_font = Font(bold=True)
        header_alignment = Alignment(horizontal='center', vertical='center')
        thin = Side(style='thin', color='B7CCE1')
        header_border = Border(left=thin, right=thin, top=thin, bottom=thin)

        for col_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_alignment
            cell.border = header_border

        # Dati
        for r in rows:
            ws.append([
                getattr(r, 'ComponentCode', ''),
                getattr(r, 'ComponentDescription', '') or '',
                getattr(r, 'LocationCode', ''),
                getattr(r, 'KanBanLocation', '')
            ])

        # Auto filtro e freeze pane
        ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}1"
        ws.freeze_panes = "A2"

        # Zebra stripes leggere e bordi sottili
        alt_fill = PatternFill(fill_type='solid', start_color='F7FBFF', end_color='F7FBFF')
        data_border = Border(left=Side(style='thin', color='D9D9D9'),
                             right=Side(style='thin', color='D9D9D9'),
                             top=Side(style='thin', color='D9D9D9'),
                             bottom=Side(style='thin', color='D9D9D9'))
        for r in range(2, ws.max_row + 1):
            if r % 2 == 0:
                for c in range(1, len(headers) + 1):
                    ws.cell(row=r, column=c).fill = alt_fill
            for c in range(1, len(headers) + 1):
                ws.cell(row=r, column=c).border = data_border

        # Larghezza colonne auto-fit semplice
        for col_idx in range(1, len(headers) + 1):
            col_letter = get_column_letter(col_idx)
            max_len = len(str(headers[col_idx - 1]))
            for r in range(2, ws.max_row + 1):
                val = ws.cell(row=r, column=col_idx).value
                if val is None:
                    continue
                max_len = max(max_len, len(str(val)))
            ws.column_dimensions[col_letter].width = min(max_len + 2, 60)

            # Salva in C:\Temp e chiedi se aprire il file
            try:
                target_dir = r"C:\Temp"
                os.makedirs(target_dir, exist_ok=True)
                filename = f"KanBan_Materiali_Report_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
                fullpath = os.path.join(target_dir, filename)
                wb.save(fullpath)

                prompt = self.lang.get('materials_report_saved_open',
                                       'Report salvato in: {path}\nAprirlo ora?').format(path=fullpath)
                if messagebox.askyesno(self.lang.get('info_title', 'Informazione'), prompt):
                    try:
                        if hasattr(os, 'startfile'):  # Windows
                            os.startfile(fullpath)
                        else:
                            import subprocess, sys
                            if sys.platform == 'darwin':  # macOS
                                subprocess.Popen(['open', fullpath])
                            else:  # Linux
                                subprocess.Popen(['xdg-open', fullpath])
                    except Exception as e:
                        messagebox.showerror(self.lang.get('error_title', 'Errore'),
                                             self.lang.get('materials_report_open_error',
                                                           f'Impossibile aprire il file: {e}'))
            except Exception as e:
                messagebox.showerror(self.lang.get('error_title', 'Errore'),
                                     self.lang.get('materials_report_error',
                                                   f'Errore durante la creazione del report: {e}'))

    def open_kanban_rules_management(self):
        KanbanRulesManagementForm(self, self.db, self.lang)

    def open_printer_setup(self):
        # Apre la finestra di configurazione stampante.
        # Richiede che PrinterSetupDialog sia importata/definita.
        dlg = PrinterSetupDialog(self, self.lang)
        self.wait_window(dlg)
        if getattr(dlg, "result", None):
            # Se vuoi tenere un cache della config
            self.printer_cfg = dlg.result
            # TODO: notifica eventuali form aperte che usano la stampante
            # es. if hasattr(self, "labels_form") and self.labels_form.winfo_exists(): ...
            pass

    def _check_calibration_warnings_startup_async(self):
        #return
        import threading, logging

        logging.getLogger("TraceabilityRS").debug("Startup: launch calibration warning check in background thread")

        try:
            threading.Thread(
                target=self._check_calibration_warnings_startup,
                name="CalibWarnStartup",
                daemon=True
            ).start()
            logging.info("Startup: controllo calibrazioni completato.")
        except Exception as e:
            logging.exception("Errore controllo calibrazioni in avvio: %s", e)

    def _check_calibration_warnings_startup(self):
        """
        Controlla le calibrazioni in scadenza/mancanti e invia un avviso email una volta al giorno.
        Non blocca l’avvio: eventuali errori vengono loggati.
        """
        #return
        log = logging.getLogger("TraceabilityRS")
        log.info("Startup: avvio controllo calibrazioni...")

        try:
            rows = self.db.fetch_calibration_warnings() or []
            log.info("Startup: controllo calibrazioni -> %d righe da notificare", len(rows))
            if not rows:
                return

            # Destinatari da settings (passa l'attributo dinamicamente)
            try:
                recipients = utils.get_email_recipients(self.db.conn, attribute='Sys_Email_Calibration')
            except Exception as e:
                log.error("Errore lettura destinatari calibrazioni: %s", e)
                recipients = []

            if not recipients:
                log.warning("Nessun destinatario per Sys_Email_Calibration: avviso non inviato.")
                return

            # Prepara email HTML
            import html as html_mod
            from datetime import date as dtdate, datetime as dtdt

            def nz(v):
                return "#N/A" if v in (None, "", "None") else str(v)

            def fmt_date(d):
                try:
                    if isinstance(d, (dtdt, dtdate)):
                        return d.strftime("%d.%m.%Y")
                    return nz(d)
                except Exception:
                    return nz(d)

            def hesc(s):
                return html_mod.escape(nz(s))

            rows_html = []
            cal_ids_to_mark = []
            equip_ids_to_mark = []
            today = dtdate.today()

            for r in rows:
                # Estrai campi con fallback sicuro
                equip_id = getattr(r, 'EquipmentId', None)
                equip = getattr(r, 'Equipment', None) or (r[1] if isinstance(r, (tuple, list)) and len(r) > 1 else None)
                last_cal = getattr(r, 'LastCalibrationDate', None)
                by = getattr(r, 'CalibratedBy', None)
                cert = getattr(r, 'NrCertificate', None)
                exp = getattr(r, 'ExpireOn', None)
                note = getattr(r, 'Note', None)
                cal_id = getattr(r, 'CalibrationId', None)
                equip_id = getattr(r, 'EquipmentId', None)
                if equip_id is None and isinstance(r, (tuple, list)) and len(r) > 0:
                    equip_id = r[0]
                if equip_id is not None:
                    equip_ids_to_mark.append(int(equip_id))

                # Calcolo stato e colore
                if exp is None:
                    status = "MISSING calibration"
                    status_color = "#cc0000"
                else:
                    try:
                        days = (exp - today).days if isinstance(exp, dtdate) else None
                    except Exception:
                        days = None
                    if days is None:
                        status = "#N/A"
                        status_color = "#999999"
                    elif days < 0:
                        status = f"EXPIRED {-days} day(s) ago"
                        status_color = "#cc0000"
                    elif days <= 7:
                        status = f"Expires in {days} day(s)"
                        status_color = "#d17f00"  # arancione
                    else:
                        status = f"Expires in {days} day(s)"
                        status_color = "#006600"  # verde (in pratica non dovrebbe capitare col filtro SQL)

                rows_html.append(f"""
                  <tr>
                    <td>{hesc(equip)}</td>
                    <td>{hesc(fmt_date(last_cal))}</td>
                    <td>{hesc(by)}</td>
                    <td>{hesc(cert)}</td>
                    <td>{hesc(fmt_date(exp))}</td>
                    <td style="color:{status_color}; font-weight:600;">{hesc(status)}</td>
                    <td>{hesc(note)}</td>
                  </tr>
                """)

                if cal_id is not None:
                    cal_ids_to_mark.append(cal_id)

            subject = f"[Calibration] Warning report - {len(rows_html)} item(s)"
            body = f"""
            <html>
              <body style="font-family:Segoe UI, Arial, sans-serif; font-size:12px; color:#222; line-height:1.35;">
                <p>Dear Colleagues,</p>
                <p>
                  Below is a list of equipment with missing or expiring calibrations.
                  Unavailable values are indicated by  <strong>#N/A</strong>.
                </p>
                <table cellpadding="6" cellspacing="0" border="1" style="border-collapse:collapse; border-color:#bbb; width:100%; max-width:1200px;">
                  <thead style="background:#f2f2f2;">
                    <tr>
                      <th align="left">Equipment</th>
                      <th align="left">Last cal.</th>
                      <th align="left">Calibrated by</th>
                      <th align="left">Certificate</th>
                      <th align="left">Expire on</th>
                      <th align="left">Status</th>
                      <th align="left">Note</th>
                    </tr>
                  </thead>
                  <tbody>
                    {''.join(rows_html)}
                  </tbody>
                </table>
                <p style="margin-top:14px; color:#666; font-size:11px;">
                  This message is automatically generated by the system.
                </p>
              </body>
            </html>
            """

            # Invia come HTML
            try:
                utils.send_email(recipients=recipients, subject=subject, body=body, is_html=True)
                log.info("Email calibrazioni inviata con successo a %d destinatari", len(recipients))
            except Exception as e:
                log.error("Errore invio email calibrazioni: %s", e)
                return

            # Dopo invio email riuscito:
            if equip_ids_to_mark:
                ok = self.db.mark_calibration_warning_sent(equip_ids_to_mark)
                if not ok:
                    log.warning("Impossibile registrare CalibrationWarnings: %s", self.db.last_error_details)
                else:
                    log.info("Registrati %d avvisi in eqp.CalibrationWarnings", len(equip_ids_to_mark))

        except Exception as e:
            log.exception("Errore controllo calibrazioni in avvio: %s", e)

    def _not_implemented(self, title, action):
        messagebox.showinfo(
            self.lang.get('info_title', 'Informazione'),
            f"{title} - {action}: funzione in sviluppo.",
            parent=self
        )

    # Locazioni
    def open_kanban_locations_create(self):
        KanbanLocationCreateForm(self, self.db, self.lang)

    def open_kanban_locations_modify(self):
        KanbanLocationModifyForm(self, self.db, self.lang)

    def open_kanban_locations_edit(self):
        self._not_implemented('KanBan - Locazioni', 'Modifica')

    def open_kanban_locations_labels(self):
        KanbanLocationLabelsForm(self, self.db, self.lang)

    # Materiali
    def open_kanban_materials_management(self):
        KanbanMaterialsManagementForm(self, self.db, self.lang)


    def open_kanban_manage(self):
        self._not_implemented('KanBan', 'Gestione')


    def open_assign_submissions_with_login(self):
        self._execute_authorized_action(
            menu_translation_key='submenu_assign',
            action_callback=lambda: assign_submissions_gui.open_assign_submissions(self, self.db, self.lang)
        )

    def open_scrap_declaration_with_login(self):
        """Apre la finestra per la dichiarazione scarti con autenticazione e autorizzazione."""

        self._execute_authorized_action(
            menu_translation_key='submenu_scrap_declaration',
            action_callback=lambda:scarti_gui.open_scrap_declaration_window(self, self.db, self.lang)
        )

    def open_calibrations_manager_with_login(self):
        logger = logging.getLogger("TraceabilityRS")
        required = 'calibration_management'
        logger.info("Request to open CalibrationsWindow; required_permission=%r", required)
        # Chiama il login in modalità "gatekeeper"
        user = self._execute_simple_login(required_permission=required)
        logger.info("Login result for calibrations: %s", "OK" if user else "FAILED")

        # Questo `if` è il controllo di sicurezza.
        # Il codice al suo interno viene eseguito solo se _execute_simple_login
        # restituisce un oggetto utente valido (login riuscito).
        if user:
            print(f"Login riuscito per l'utente {user.name}. Apertura finestra...")
            try:
                # Ora che l'utente è autenticato, possiamo creare la finestra.
                CalibrationsWindow(self, self.db, self.lang)
            except Exception as e:
                logging.getLogger("TraceabilityRS").exception("Error opening CalibrationsWindow: %s", e)
                messagebox.showerror("Errore", f"Impossibile aprire il modulo di calibrazione: {e}")

        else:
            # Questo blocco viene eseguito se l'utente chiude la finestra di login
            # o non ha i permessi.
            print("Login fallito o annullato. Accesso al modulo negato.")

    def open_line_stoppage_report(self):
            """Apre la finestra per generare il report dei fermi linea."""
            LineStoppageReportForm(self, self.db, self.lang)

    def open_verification_association_with_login(self):
        """Apre la verifica associazione dopo il login"""
        self._execute_simple_login(
            action_callback=lambda user_name: self.traceability_manager.open_verification_association(user_name)
        )

    def open_manage_customers_with_login(self):
        """Apre la gestione clienti dopo il login"""
        self._execute_simple_login(
            action_callback=lambda user_name: self.traceability_manager.open_manage_customers(user_name)
        )

    def open_define_products_with_login(self):
        """Apre la definizione prodotti dopo il login"""
        self._execute_simple_login(
            action_callback=lambda user_name: self.traceability_manager.open_define_products(user_name)
        )

    def open_manage_links_with_login(self):
        """Apre la gestione collegamenti dopo il login"""
        self._execute_simple_login(
            action_callback=lambda user_name: self.traceability_manager.open_manage_links()
        )

    def _trigger_update(self, version_info):
        """Lancia l'updater e chiude l'applicazione."""
        source = version_info.MainPath
        destination = os.path.dirname(sys.executable)
        exe_name = os.path.basename(sys.executable)
        updater_path = os.path.join(destination, "updater.exe")

        if not os.path.exists(updater_path):
            messagebox.showerror("Errore Critico", "File updater.exe non trovato! Impossibile aggiornare.", parent=self)
            return

        subprocess.Popen([updater_path, source, destination, exe_name])
        self._on_closing(force_quit=True)  # Chiude l'app senza chiedere conferma

    def _periodic_version_check(self):
        """Controlla periodicamente la presenza di nuove versioni."""
        print("Controllo periodico versione in corso...")

        app_name = os.path.basename(sys.executable)
        version_info = self.db.fetch_latest_version_info(app_name)

        # Se trova una nuova versione, mostra il dialogo
        if version_info and is_update_needed(APP_VERSION, version_info.Version):
            dialog = UpdateNotificationDialog(self, self.lang, version_info.Version, APP_VERSION)
            self.wait_window(dialog)

            if dialog.result == 'now':
                self._trigger_update(version_info)
                return  # Interrompe il ciclo di controllo
            elif dialog.result == 'later':
                # Ripianifica il controllo tra 15 minuti
                remind_interval_ms = 15 * 60 * 1000
                self.periodic_check_job_id = self.after(remind_interval_ms, self._periodic_version_check)
                return
            elif dialog.result == 'ignore':
                # Interrompe il controllo per questa sessione
                print("Controllo versione silenziato per questa sessione.")
                return

        # Se non ci sono aggiornamenti, ripianifica il controllo tra 120 minuti
        default_interval_ms = 120 * 60 * 1000
        self.periodic_check_job_id = self.after(default_interval_ms, self._periodic_version_check)

    def open_company_manager_with_login(self):
        """Apre la finestra di gestione delle compagnie dopo il login."""
        self._execute_simple_login(
            action_callback=lambda user_name: tools_gui.open_company_manager(self, self.db, self.lang, user_name)
        )

    def open_brand_manager_with_login(self):
        """Apre la finestra di gestione dei brand dopo il login."""
        self._execute_simple_login(
            action_callback=lambda user_name: maintenance_gui.open_brand_manager(self, self.db, self.lang, user_name)
        )

    def open_missing_action_report(self):
        """Esegue il report Missing Action e lo esporta in Excel."""
        # Chiama direttamente la funzione per generare il report, senza login
        maintenance_gui.generate_missing_action_report(self, self.db, self.lang)

    def open_xls_settings_with_login(self):
        """Apre la finestra per configurare la mappatura dei file Excel."""
        self._execute_authorized_action(  # Usiamo il login con permessi
            menu_translation_key='submenu_shipping_settings',  # Riusiamo questo permesso
            action_callback=lambda: operations_gui.open_xls_settings_window(self, self.db, self.lang, None)
        )

    def open_shipping_settings_with_login(self):
        """Apre la finestra per gestire le impostazioni di spedizione."""
        self._execute_authorized_action(  # Usiamo il login con permessi
            menu_translation_key='submenu_shipping_settings',
            action_callback=lambda: operations_gui.open_shipping_settings_window(self, self.db, self.lang, None)
        )

    def open_shipping_window_with_login(self):
        """Apre la finestra per il caricamento del report spedizioni."""
        self._execute_simple_login(
            action_callback=lambda user_name: operations_gui.open_shipping_report_window(self, self.db, self.lang,
                                                                                         user_name)
        )

    def open_shipping_report_window_with_login(self):
        """Apre la finestra per il caricamento del report spedizioni dopo un login semplice."""
        self._execute_simple_login(
            action_callback=lambda user_name: operations_gui.open_shipping_report_window(self, self.db, self.lang,
                                                                                         user_name)
        )

    def _flash_birthday_message(self, message):
        """Crea un effetto flashing con cambio colore per il messaggio di auguri."""
        # Se il testo è attualmente visibile, lo nasconde
        if self.birthday_label.cget("text"):
            self.birthday_label.config(text="")
        else:
            # Altrimenti, lo mostra con un nuovo colore casuale
            random_color = random.choice(self.flash_colors)
            self.birthday_label.config(text=message, foreground=random_color)

        # Ripianifica se stessa dopo 750 millisecondi (circa 3/4 di secondo)
        self.birthday_flash_job_id = self.after(750, lambda: self._flash_birthday_message(message))

    def _check_for_birthdays(self):
        """Controlla i compleanni e avvia l'avviso appropriato (fisso o scorrevole)."""
        # Ferma sempre un eventuale avviso precedente
        self._stop_birthday_display()
        if hasattr(self, 'birthday_label'):
            self.birthday_label.config(text="")

        try:
            # ... (la logica per leggere le impostazioni e trovare i compleanni rimane invariata)
            pre_alert_days = int(self.db.fetch_setting('Sys_BirthDay_Prealler'))
            post_alert_days = int(self.db.fetch_setting('Sys_BirthDay_PostAllert'))
            image_path = os.path.join(
                self.db.fetch_setting('Sys_Pics_Directory'),
                self.db.fetch_setting('Sys_BirthDay_Allert')
            )
        except (ValueError, TypeError, AttributeError):
            return False
        if not image_path or not os.path.isfile(image_path): return False
        today = datetime.now().date()
        employees = self.db.fetch_all_active_employees_birthdays()
        celebrating = []
        for emp in employees:
            bday = emp.EmployeeBirthDate
            bday_this_year = bday.replace(year=today.year)
            if timedelta(days=0) <= bday_this_year - today <= timedelta(days=pre_alert_days):
                celebrating.append(emp)
            elif timedelta(days=0) <= today - bday_this_year <= timedelta(days=post_alert_days):
                celebrating.append(emp)

        # --- LOGICA MODIFICATA ---
        if len(celebrating) == 1:
            # Caso 1: Un solo festeggiato -> Testo lampeggiante
            employee = celebrating[0]
            message = f"LA MULȚI ANI {employee.EmployeeName.upper()} ({employee.EmployeeSurname.upper()}) !!!"
            self._display_special_image(image_path, message)
            self._flash_birthday_message(message)
            duration_ms = 2 * 60 * 1000
            self.birthday_stop_job_id = self.after(duration_ms, self._stop_birthday_display)
            return True

        elif len(celebrating) > 1:
            # Caso 2: Più festeggiati -> Testo scorrevole
            messages = [f"LA MULȚI ANI {emp.EmployeeName.upper()} ({emp.EmployeeSurname.upper()}) !!!" for emp in
                        celebrating]
            # Unisce i messaggi con un separatore visivo
            full_message = "    •••    ".join(messages)

            self._display_special_image(image_path, "Compleanni di Oggi!")  # Un messaggio generico sull'immagine
            self._start_scrolling_message(full_message)
            duration_ms = 2 * 60 * 1000
            self.birthday_stop_job_id = self.after(duration_ms, self._stop_birthday_display)
            return True

        return False

    def _start_scrolling_message(self, message):
        """Prepara e avvia l'animazione della scritta scorrevole."""
        # Aggiunge spazi alla fine per creare un loop fluido
        self.scrolling_text = message + " " * 20
        self.scrolling_position = 0

        # Cambia il colore del testo per una migliore visibilità
        self.birthday_label.config(foreground="#FFD700")  # Colore oro

        # Avvia il primo frame dell'animazione
        self._scroll_text()

    def _scroll_text(self):
        """Esegue un singolo passo dell'animazione di scrolling."""
        # Crea il testo da visualizzare ruotando la stringa originale
        display_text = self.scrolling_text[self.scrolling_position:] + self.scrolling_text[:self.scrolling_position]
        self.birthday_label.config(text=display_text)

        # Incrementa la posizione per il prossimo frame
        self.scrolling_position += 1
        if self.scrolling_position >= len(self.scrolling_text):
            self.scrolling_position = 0

        # Ripianifica il prossimo frame dopo 150 millisecondi
        self.scrolling_job_id = self.after(150, self._scroll_text)

    def _stop_birthday_display(self):

        if self.birthday_flash_job_id:
            self.after_cancel(self.birthday_flash_job_id)
            self.birthday_flash_job_id = None

        # Ferma il ciclo del testo scorrevole, se attivo
        if self.scrolling_job_id:
            self.after_cancel(self.scrolling_job_id)
            self.scrolling_job_id = None

        # Pulisce l'etichetta degli auguri e ripristina il colore
        if hasattr(self, 'birthday_label'):
            self.birthday_label.config(text="", foreground="black")

        # Rimuove l'immagine speciale e riavvia lo slideshow standard
        self._setup_slideshow()

    def _display_special_image(self, image_path, text):
        """Carica un'immagine, ci scrive sopra del testo e la visualizza."""
        try:
            if self.slideshow_job_id:
                self.after_cancel(self.slideshow_job_id)

            image = Image.open(image_path)
            w, h = self.slideshow_label.winfo_width(), self.slideshow_label.winfo_height()
            if w <= 1 or h <= 1:
                self.after(200, lambda: self._display_special_image(image_path, text))
                return

            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("arial.ttf", 48)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            position = ((image.width - text_width) / 2, (image.height - text_height) * 0.85)

            draw.text(position, text, font=font, fill="white", stroke_width=2, stroke_fill="black")
            resized_image = ImageOps.fit(image, (w, h), Image.Resampling.LANCZOS)
            self.slideshow_photo = ImageTk.PhotoImage(resized_image)
            self.slideshow_label.config(image=self.slideshow_photo)
        except Exception as e:
            print(f"ERRORE: Impossibile visualizzare l'immagine speciale: {e}")
            self._setup_slideshow()

    def open_add_interruption_window_with_login(self):
        """Apre la finestra per dichiarare un'interruzione di produzione."""
        self._execute_simple_login(
            action_callback=lambda user_name: operations_gui.open_add_interruption_window(self, self.db, self.lang,
                                                                                          user_name)
        )

    def open_maintenance_times_with_login(self):
        """Apre la finestra per gestire i tempi di manutenzione."""
        self._execute_simple_login(
            action_callback=lambda user_name: tools_gui.open_maintenance_times_manager(self, self.db, self.lang,
                                                                                       user_name)
        )

    def open_add_interruption_window(self):
        """Apre la finestra per dichiarare un'interruzione di produzione."""
        self._execute_simple_login(
            action_callback=lambda user_name: operations_gui.open_add_interruption_window(self, self.db, self.lang,
                                                                                          user_name)
        )

    def _post_startup_tasks(self):
        #logger.debug("POST: skipped by debug")
        print("DEBUG: Eseguo le operazioni post-avvio...")
        self._update_clock()
        logger.info('Avviato check versione programma')
        self.periodic_check_job_id = self.after(120000, self._periodic_version_check)
        logger.info('Avviato controllo compleanni')
        is_birthday = self._check_for_birthdays()
        if not is_birthday:
            self._setup_slideshow()

        # DOPO:
        logger.info('Avviato controllo calibrazioni effettuate')
        self.after(500, self._check_calibration_warnings_startup_async)
        logger.info('Avviato controllo quantita kanban')
        self._schedule_kanban_refill_check()

    def _setup_slideshow(self):
        """Legge le impostazioni e avvia il ciclo dello slideshow."""
        folder_path = self.db.fetch_setting('SlideshowFolderPath')
        interval_min_str = self.db.fetch_setting('SlideshowIntervalMinutes')

        if not folder_path or not os.path.isdir(folder_path):
            self.slideshow_label.config(text="Percorso immagini non configurato o non valido.", foreground="white")
            return

        try:
            interval_min = int(interval_min_str)
            self.slideshow_interval_ms = interval_min * 60 * 1000
        except (ValueError, TypeError):
            pass

        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        try:
            self.image_files = [
                os.path.join(folder_path, f) for f in os.listdir(folder_path)
                if f.lower().endswith(valid_extensions)
            ]
        except Exception as e:
            print(f"Errore durante la lettura della cartella immagini: {e}")

        if not self.image_files:
            self.slideshow_label.config(text="Nessuna immagine trovata nella cartella specificata.", foreground="white")
        else:
            self._cycle_image()

    def _cycle_image(self):
        """Cambia l'indice dell'immagine, la disegna e si riprogramma."""
        if not self.image_files:
            return

        self._draw_current_image()
        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)

        # --- CORREZIONE QUI ---
        # Salva l'ID del prossimo ciclo per poterlo annullare
        self.slideshow_job_id = self.after(self.slideshow_interval_ms, self._cycle_image)

    def _draw_current_image(self, event=None):  # Aggiunto 'event=None' per la compatibilità con bind
        """Funzione dedicata a disegnare l'immagine corrente alla dimensione corretta."""
        if not self.image_files:
            return

        image_path = self.image_files[self.current_image_index]
        w, h = self.slideshow_label.winfo_width(), self.slideshow_label.winfo_height()

        if w <= 1 or h <= 1:
            return

        try:
            image = Image.open(image_path)
            resized_image = ImageOps.fit(image, (w, h), Image.Resampling.LANCZOS)
            self.slideshow_photo = ImageTk.PhotoImage(resized_image)
            self.slideshow_label.config(image=self.slideshow_photo)
        except Exception as e:
            print(f"Errore nel disegnare l'immagine {image_path}: {e}")

    def _update_clock(self):
        """Aggiorna l'etichetta dell'orologio ogni secondo."""
        # Formato: Giorno/Mese/Anno Ora:Minuti:Secondi
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.clock_label.config(text=now_str)

        # Richiama se stessa dopo 1000 millisecondi (1 secondo)
        self.clock_label.after(1000, self._update_clock)

    def open_add_maintenance_tasks_with_login(self):
        """Richiede il login e poi apre la finestra per aggiungere/gestire i task."""
        # This action modifies data, so it requires a simple login.
        self._execute_simple_login(
            action_callback=lambda user_name: maintenance_gui.open_add_maintenance_tasks(self, self.db, self.lang,
                                                                                         user_name)
        )

    def open_manage_permissions_with_login(self):
        self._execute_authorized_action(
            menu_translation_key='submenu_permissions',  # Chiave per accedere alla gestione
            action_callback=lambda: permissions_gui.open_manage_permissions_window(self, self.db, self.lang)
        )

    def open_view_permissions_with_login(self):
        self._execute_authorized_action(
            menu_translation_key='submenu_permissions',  # Stessa chiave, per ora
            action_callback=lambda: permissions_gui.open_view_permissions_window(self, self.db, self.lang)
        )

    def open_doc_types_manager_with_login(self):
        """Richiede il login e poi apre la finestra di gestione dei tipi di documento."""
        # Nota: usiamo una nuova chiave 'submenu_doc_types' per un eventuale permesso dedicato
        self._execute_authorized_action(
            menu_translation_key='submenu_doc_types',
            action_callback=lambda: tools_gui.open_doc_types_manager(self, self.db, self.lang)
        )

    def _open_general_docs_viewer(self, category_id, category_name):
        """Apre la finestra di visualizzazione dei documenti in modalità SOLA LETTURA (senza login)."""
        # L'utente non è loggato, quindi passiamo None come user_name
        general_docs_gui.open_general_docs_viewer(
            self, self.db, self.lang, category_id, category_name, user_name=None, view_only=True
        )

    def _open_general_docs_viewer_with_login(self, category_id, category_name):
        """Richiede il login e poi apre la finestra di GESTIONE (lettura/scrittura)."""
        self._execute_simple_login(
            action_callback=lambda user_name: general_docs_gui.open_general_docs_viewer(
                self, self.db, self.lang, category_id, category_name, user_name, view_only=False
            )
        )

    def open_insert_form(self):
        """Apre la finestra di inserimento documenti dopo un login semplice."""

        def action(user_name):
            # Crea e mostra la finestra di inserimento
            form = InsertDocumentForm(self, self.db, user_name, self.lang)
            form.grab_set()

        self._execute_simple_login(action_callback=action)

    def open_view_form(self):
        """Apre la finestra per visualizzare i documenti di produzione."""
        view_form = ViewDocumentForm(self, self.db, self.lang)
        view_form.transient(self)
        view_form.grab_set()
        self.wait_window(view_form)

    def _execute_simple_login(self, action_callback=None, required_permission=None):
        logger.info("_execute_simple_login called; required_permission=%r", required_permission)

        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)

        if not login_form.clicked_login:
            logger.info("Login window closed without login.")
            return None

        user_id = login_form.user_id
        logger.info("LoginWindow returned user_id=%r", user_id)

        password = login_form.password
        user = self.db.authenticate_and_get_user(user_id, password)

        if not user:
            logger.info("Authentication failed for user_id=%r", user_id)
            messagebox.showerror(self.lang.get('login_title'),
                                 self.lang.get('login_auth_failed'), parent=self)
            return None

        logger.debug("Authenticated as %r; permissions=%s", user.name,
                     sorted(user.permissions))

        if required_permission and not user.has_permission(required_permission):
            logger.info("Permission check FAILED for %r -> required=%r",
                         user.name, required_permission)
            messagebox.showwarning(
                self.lang.get('access_denied', "Accesso Negato"),
                self.lang.get('permission_missing', "Non si dispone delle autorizzazioni per questa operazione."),
                parent=self
            )
            return None

        if isinstance(action_callback, collections.abc.Callable):
            # Passa il nome utente come da pattern esistente
            action_callback(user.name)

        return user

    def _execute_authorized_action(self, menu_translation_key, action_callback):
        logger.debug("_execute_authorized_action called; menu_translation_key=%r", menu_translation_key)

        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)

        if not login_form.clicked_login:
            return False

        user_id = login_form.user_id
        logger.debug("LoginWindow returned user_id=%r for authorized action %r", user_id, menu_translation_key)
        password = login_form.password

        auth_result = self.db.authenticate_and_authorize(user_id, password, menu_translation_key)

        if auth_result is None:
            messagebox.showerror(self.lang.get('login_title'), self.lang.get('login_auth_failed'), parent=self)
            return False
        elif auth_result.AuthorizedUsedId is None:
            logger.debug("User %r authenticated but NOT authorized for %r", user_id, menu_translation_key)
            messagebox.showwarning(
                self.lang.get('auth_access_denied_title', "Accesso Negato"),
                self.lang.get('auth_access_denied_message',
                              "Non si dispone delle autorizzazioni necessarie per accedere a questa funzione."),
                parent=self
            )
            return False
        else:
            logger.debug("User %r authorized for %r; executing action.", user_id, menu_translation_key)
            try:
                self.last_authenticated_user_name = auth_result.EmployeeName
            except Exception:
                self.last_authenticated_user_name = None

            self._temp_authorized_user_id = user_id

            action_callback()
            return True

    def open_maint_cycles_manager_with_login(self):
        self._execute_authorized_action(
            menu_translation_key='submenu_maint_cycles',
            action_callback=lambda: tools_gui.open_maint_cycles_manager(self, self.db, self.lang)
        )

    def open_new_submission_form(self):
        """Apre la finestra di inserimento nuova segnalazione (senza login)."""
        submissions_gui.open_new_submission_form(self, self.db, self.lang)

    def open_brands_manager_with_login(self):
        """Richiede il login e poi apre la finestra di gestione dei brand."""
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)
        authenticated_user = login_form.authenticated_user_name
        if authenticated_user:
            tools_gui.open_brands_manager(self, self.db, self.lang)

    def open_suppliers_manager_with_login(self):
        self._execute_authorized_action(
            menu_translation_key='submenu_suppliers',
            action_callback=lambda: tools_gui.open_suppliers_manager(self, self.db, self.lang)
        )

    def open_suppliers_manager(self):
        """Apre la finestra di gestione dei fornitori."""
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)
        authenticated_user = login_form.authenticated_user_name
        if authenticated_user:
            tools_gui.open_suppliers_manager(self, self.db, self.lang)

    def _save_language_setting(self, lang_code):
        """Salva la lingua corrente nel file di configurazione."""
        try:
            with open("lang.conf", "w") as f:
                f.write(lang_code)
        except Exception as e:
            print(f"Impossibile salvare le impostazioni della lingua: {e}")

    def _load_language_setting(self):
        """Carica la lingua dal file di configurazione, se esiste."""
        try:
            with open("lang.conf", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return 'it'  # Lingua di default se il file non esiste
        except Exception as e:
            print(f"Impossibile leggere le impostazioni della lingua: {e}")
            return 'it'  # Ritorna al default in caso di errore

    def open_fill_templates_with_login(self):
        """Apre la finestra per compilare le schede dopo un login semplice."""
        self._execute_simple_login(
            action_callback=lambda user_name: maintenance_gui.open_fill_templates(self, self.db, self.lang, user_name)
        )

    def check_version(self):
        """
        Controlla se l'app è eseguita dalla sorgente, poi verifica la versione
        e, se necessario, lancia l'updater.
        Restituisce False se l'app deve chiudersi, altrimenti True.
        """
        try:
            app_name = os.path.basename(sys.executable)
            version_info = self.db.fetch_latest_version_info(app_name)

            if not version_info or not version_info.Version or not version_info.MainPath:
                print("Informazioni di versione non trovate o incomplete nel DB. Controllo saltato.")
                return True

            source_path = os.path.normpath(version_info.MainPath)
            current_path = os.path.normpath(os.path.dirname(sys.executable))

            if source_path.lower() == current_path.lower():
                title = self.lang.get("error_running_from_source_title", "Esecuzione non Permessa")
                message = self.lang.get(
                    "error_running_from_source_message",
                    "L'applicazione non può essere eseguita direttamente dal percorso sorgente sul server.\n\n"
                    "Si prega di lanciare la copia installata localmente."
                )
                messagebox.showerror(title, message, parent=self)
                self.db.disconnect()
                self.destroy()
                self.should_exit = True  # Set the flag
                return False

            if is_update_needed(APP_VERSION, version_info.Version):
                title = self.lang.get("upgrade_required_title", "Aggiornamento Richiesto")
                message = self.lang.get(
                    "force_upgrade_message",
                    "È disponibile una nuova versione ({0}). La versione attuale è obsoleta ({1}).\n\n"
                    "Il programma si chiuderà per avviare l'aggiornamento automatico.",
                    version_info.Version, APP_VERSION
                )
                messagebox.showinfo(title, message, parent=self)

                destination = os.path.dirname(sys.executable)
                exe_name = os.path.basename(sys.executable)
                updater_path = os.path.join(destination, "updater.exe")

                if not os.path.exists(updater_path):
                    messagebox.showerror("Errore Critico", "File updater.exe non trovato! Impossibile aggiornare.",
                                         parent=self)
                    self.db.disconnect()
                    self.destroy()
                    self.should_exit = True  # Set the flag
                    return False

                subprocess.Popen([updater_path, source_path, destination, exe_name])
                self.db.disconnect()
                self.destroy()
                self.should_exit = True  # Set the flag
                return False

            print(f"Versione applicazione ({APP_VERSION}) aggiornata.")
            return True

        except Exception as e:
            print(f"Errore imprevisto durante il controllo versione: {e}")
            return True

    def _create_widgets(self):
        # --- PRIMA: Crea la Barra di Stato Inferiore ---
        status_bar = ttk.Frame(self, style="Card.TFrame", padding=5)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Contenitore per Logo e Orologio, allineato a destra
        bottom_right_frame = ttk.Frame(status_bar)
        bottom_right_frame.pack(side=tk.RIGHT)

        # Logo (ora in basso a destra)
        if PIL_AVAILABLE:
            try:
                image = Image.open("logo.png")
                image.thumbnail((100, 100))
                self.logo_image = ImageTk.PhotoImage(image)
                self.logo_label = ttk.Label(bottom_right_frame, image=self.logo_image)
                self.logo_label.pack()
            except Exception as e:
                print(f"Errore caricamento logo: {e}")

        # Orologio (ora sotto il logo)
        self.clock_label = ttk.Label(bottom_right_frame, font=("Helvetica", 9), justify=tk.RIGHT)
        self.clock_label.pack()

        # --- NUOVA ETICHETTA PER GLI AUGURI (al centro) ---
        self.birthday_label = ttk.Label(status_bar, text="", font=("Helvetica", 10, "bold"), anchor="center")
        # Questo pack fa sì che l'etichetta si espanda per riempire lo spazio centrale
        self.birthday_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # --- DOPO: Crea l'Area Centrale per lo Slideshow ---
        # Ora questo label si espanderà per riempire tutto lo spazio RIMANENTE
        self.slideshow_label = ttk.Label(self, background="black")
        self.slideshow_label.pack(fill=tk.BOTH, expand=True)

        # Associa il ridimensionamento al disegno dell'immagine
        self.slideshow_label.bind('<Configure>', lambda e: self._draw_current_image())

    def open_calibrations_manager_with_login(self):
        """
        Questa funzione agisce da "ponte". Prima esegue il login
        e SOLO SE ha successo, apre la finestra.
        """
        # Chiama il login in modalità "gatekeeper", richiedendo un permesso specifico.
        # La funzione _execute_simple_login restituirà l'utente se il login
        # e la verifica dei permessi vanno a buon fine, altrimenti None.
        user_che_ha_fatto_login = self._execute_simple_login(
            required_permission='calibration_management'
        )

        # L'if controlla che il login sia andato a buon fine.
        if user_che_ha_fatto_login:
            # Solo ora, con la certezza che l'utente è autorizzato,
            # creiamo e apriamo la finestra delle calibrazioni.
            try:
                CalibrationsWindow(self, self.db, self.lang)
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile aprire il modulo di calibrazione: {e}")

    def _create_menu(self):
        """Crea la struttura completa dei menu con gerarchia organizzata"""
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # Inizializza tutti i menu principali
        self._init_main_menus()

        # Inizializza i sottomenu complessi
        self._init_production_submenus()
        self._init_tools_submenus()
        self._init_help_submenus()

        # Aggiungi i menu principali alla barra
        self._add_main_menus_to_bar()

    def _init_main_menus(self):
        """Inizializza i menu principali"""
        self.document_menu = tk.Menu(self.menubar, tearoff=0)
        self.general_docs_menu = tk.Menu(self.menubar, tearoff=0)
        self.operations_menu = tk.Menu(self.menubar, tearoff=0)
        self.maintenance_menu = tk.Menu(self.menubar, tearoff=0)
        self.submissions_menu = tk.Menu(self.menubar, tearoff=0)
        self.tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu = tk.Menu(self.menubar, tearoff=0)

    def _init_production_submenus(self):
        """Inizializza la gerarchia completa del menu Produzione"""
        # Menu principale Produzione
        self.production_submenu = tk.Menu(self.operations_menu, tearoff=0)

        # Sottomenu di Produzione
        self.declarations_submenu = tk.Menu(self.production_submenu, tearoff=0)

        # Gerarchia KanBan
        self.kanban_root_submenu = tk.Menu(self.production_submenu, tearoff=0)
        self.kanban_locations_submenu = tk.Menu(self.kanban_root_submenu, tearoff=0)
        self.kanban_materials_submenu = tk.Menu(self.kanban_root_submenu, tearoff=0)
        self.kanban_core_submenu = tk.Menu(self.kanban_root_submenu, tearoff=0)

        # Tracciabilità
        self.traceability_submenu = tk.Menu(self.production_submenu, tearoff=0)
        self.fct_transfer_submenu = tk.Menu(self.traceability_submenu, tearoff=0)

        # Calibrazioni
        self.calibrations_submenu = tk.Menu(self.production_submenu, tearoff=0)

        # Coating - Struttura organizzata
        self.coating_submenu = tk.Menu(self.production_submenu, tearoff=0)
        self.coating_materials_submenu = tk.Menu(self.coating_submenu, tearoff=0)

        # Verifiche Prodotti
        self.product_checks_submenu = tk.Menu(self.production_submenu, tearoff=0)

        # Rapporti
        self.reports_submenu = tk.Menu(self.production_submenu, tearoff=0)
        self.operativity_submenu = tk.Menu(self.reports_submenu, tearoff=0)

    def _init_tools_submenus(self):
        """Inizializza i sottomenu di Strumenti"""
        self.permissions_submenu = tk.Menu(self.tools_menu, tearoff=0)
        self.materials_submenu = tk.Menu(self.tools_menu, tearoff=0)

    def _init_help_submenus(self):
        """Inizializza i sottomenu di Aiuto"""
        self.language_menu = tk.Menu(self.help_menu, tearoff=0)
        self.language_menu.add_command(label="Italiano", command=lambda: self._change_language('it'))
        self.language_menu.add_command(label="English", command=lambda: self._change_language('en'))
        self.language_menu.add_command(label="Română", command=lambda: self._change_language('ro'))
        self.language_menu.add_command(label="Deutsch", command=lambda: self._change_language('de'))
        self.language_menu.add_command(label="Svenska", command=lambda: self._change_language('sv'))

    def _add_main_menus_to_bar(self):
        """Aggiunge i menu principali alla barra dei menu"""
        self.menubar.add_cascade(label=self.lang.get('menu_documents', "Documenti di Produzione"),
                                 menu=self.document_menu)
        self.menubar.add_cascade(label=self.lang.get('menu_general_docs', "Documenti Generali"),
                                 menu=self.general_docs_menu)
        self.menubar.add_cascade(label=self.lang.get('menu_operations', "Operazioni"), menu=self.operations_menu)
        self.menubar.add_cascade(label=self.lang.get('menu_maintenance', "Manutenzione"), menu=self.maintenance_menu)
        self.menubar.add_cascade(label=self.lang.get('menu_submissions', "Segnalazioni"), menu=self.submissions_menu)
        self.menubar.add_cascade(label=self.lang.get('menu_tools', "Strumenti"), menu=self.tools_menu)
        self.menubar.add_cascade(label=self.lang.get('menu_help', "Aiuto"), menu=self.help_menu)

    def update_texts(self):
        """Aggiorna tutti i testi della UI principale con struttura organizzata"""
        self.title(self.lang.get('app_title'))

        # Aggiorna tutti i menu in sequenza
        self._update_document_menu()
        self._update_general_docs_menu()
        self._update_operations_menu()
        self._update_maintenance_menu()
        self._update_submissions_menu()
        self._update_tools_menu()
        self._update_help_menu()

        # Aggiorna le etichette della barra principale
        self._update_main_menubar()

    def _update_document_menu(self):
        """Aggiorna il menu Documenti di Produzione"""
        self.document_menu.delete(0, 'end')
        self.document_menu.add_command(label=self.lang.get('menu_insert_doc'), command=self.open_insert_form)
        self.document_menu.add_command(label=self.lang.get('menu_view_doc'), command=self.open_view_form)
        self.document_menu.add_separator()
        self.document_menu.add_command(label=self.lang.get('menu_quit'), command=self._on_closing)

    def _update_general_docs_menu(self):
        """Aggiorna il menu Documenti Generali"""
        self.general_docs_menu.delete(0, 'end')
        if self.doc_categories:
            for category in self.doc_categories:
                category_submenu = tk.Menu(self.general_docs_menu, tearoff=0)
                category_name = self.lang.get(category.TranslationKey, category.NomeCategoria)
                self.general_docs_menu.add_cascade(label=category_name, menu=category_submenu)

                cmd_edit = lambda cid=category.CategoriaId, cname=category_name: \
                    self._open_general_docs_viewer_with_login(cid, cname)

                category_submenu.add_command(
                    label=self.lang.get('submenu_add_edit', "Aggiungi/Modifica"),
                    command=cmd_edit
                )

                cmd_view = lambda cid=category.CategoriaId, cname=category_name: \
                    self._open_general_docs_viewer(cid, cname)

                category_submenu.add_command(
                    label=self.lang.get('submenu_view', "Visualizza"),
                    command=cmd_view
                )

    def _update_operations_menu(self):
        """Aggiorna il menu Operazioni con tutta la gerarchia Produzione"""
        self.operations_menu.delete(0, 'end')
        self.operations_menu.add_cascade(label=self.lang.get('submenu_production_ops', "Produzione"),
                                         menu=self.production_submenu)

        # Aggiorna tutti i sottomenu di Produzione
        self._update_production_submenu()

        self.operations_menu.add_separator()
        self.operations_menu.add_command(label=self.lang.get('submenu_materials_ops', "Materiali"), state="disabled")
        self.operations_menu.add_command(label=self.lang.get('submenu_hr', "Risorse Umane"), state="disabled")

    def _update_production_submenu(self):
        """Aggiorna il sottomenu Produzione con tutte le sezioni"""
        self.production_submenu.delete(0, 'end')

        # 1. Dichiarazioni
        self.production_submenu.add_cascade(label=self.lang.get('submenu_declarations', "Dichiarazioni"),
                                            menu=self.declarations_submenu)
        self._update_declarations_submenu()

        # 2. KanBan
        self.production_submenu.add_cascade(label=self.lang.get('submenu_kanban', 'KanBan'),
                                            menu=self.kanban_root_submenu)
        self._update_kanban_submenus()

        # 3. Tracciabilità
        self.production_submenu.add_cascade(label=self.lang.get('submenu_traceability', "Tracciabilità"),
                                            menu=self.traceability_submenu)
        self._update_traceability_submenu()

        # 4. Calibrazioni
        self.production_submenu.add_cascade(label=self.lang.get('submenu_calibrations', "Calibrazioni"),
                                            menu=self.calibrations_submenu)
        self._update_calibrations_submenu()

        # 5. Coating - Struttura organizzata
        self.production_submenu.add_cascade(label=self.lang.get('menu_coating', "Coating"),
                                            menu=self.coating_submenu)
        self._update_coating_submenu()

        # 6. Verifiche Prodotti
        self.production_submenu.add_cascade(label=self.lang.get('menu_product_checks', "Verifiche"),
                                            menu=self.product_checks_submenu)
        self._update_product_checks_submenu()

        # 7. Rapporti
        self.production_submenu.add_cascade(label=self.lang.get('submenu_reports_prod', "Rapporti"),
                                            menu=self.reports_submenu)
        self._update_reports_submenu()

    def _update_declarations_submenu(self):
        """Aggiorna il sottomenu Dichiarazioni"""
        self.declarations_submenu.delete(0, 'end')
        self.declarations_submenu.add_command(
            label=self.lang.get('submenu_interruptions', "Interruzioni di produzione"),
            command=self.open_add_interruption_window_with_login
        )
        self.declarations_submenu.add_separator()
        self.declarations_submenu.add_command(
            label=self.lang.get('submenu_scrap_validation', "Validazione scarti"),
            command=self.open_scrap_validation_with_login
        )
        self.declarations_submenu.add_command(
            label=self.lang.get('submenu_scrap_declaration', "Dichiarazione scarti"),
            command=self.open_scrap_declaration_with_login
        )

    def _update_kanban_submenus(self):
        """Aggiorna tutta la gerarchia KanBan"""
        self.kanban_root_submenu.delete(0, 'end')
        self.kanban_locations_submenu.delete(0, 'end')
        self.kanban_materials_submenu.delete(0, 'end')
        self.kanban_core_submenu.delete(0, 'end')

        # Locazioni KanBan
        self.kanban_locations_submenu.add_command(
            label=self.lang.get('action_create', 'Crea'),
            command=self.open_kanban_locations_create
        )
        self.kanban_locations_submenu.add_command(
            label=self.lang.get('menu_locations_modify', 'Modifica...'),
            command=self.open_kanban_locations_modify
        )
        self.kanban_locations_submenu.add_command(
            label=self.lang.get('action_labels', 'Etichette'),
            command=self.open_kanban_locations_labels
        )
        self.kanban_locations_submenu.add_separator()
        self.kanban_locations_submenu.add_command(
            label=self.lang.get('printer_setup_menu', 'Impostazioni stampante...'),
            command=self.open_printer_setup
        )

        # Materiali KanBan
        self.kanban_materials_submenu.add_command(
            label=self.lang.get('menu_materials_mgmt', 'Materiali - Gestione'),
            command=self.open_kanban_materials_management
        )
        self.kanban_materials_submenu.add_command(
            label=self.lang.get('menu_rules_mgmt', 'Gestione regole'),
            command=self.open_kanban_rules_management
        )
        self.kanban_materials_submenu.add_command(
            label=self.lang.get('submenu_report_single', 'Report'),
            command=self.open_kanban_materials_report
        )

        # Core KanBan
        self.kanban_core_submenu.add_command(
            label=self.lang.get('kanban_move', 'Movimenta'),
            command=self.open_kanban_move
        )
        self.kanban_core_submenu.add_command(
            label=self.lang.get('kanban_verify', 'Verifica'),
            command=self._schedule_kanban_refill_check
        )
        self.kanban_core_submenu.add_command(
            label=self.lang.get('submenu_manage', 'Gestione'),
            command=self.open_kanban_manage
        )

        # Assembla gerarchia KanBan
        self.kanban_root_submenu.add_cascade(
            label=self.lang.get('submenu_kanban_locations', 'Locazioni'),
            menu=self.kanban_locations_submenu
        )
        self.kanban_root_submenu.add_cascade(
            label=self.lang.get('submenu_kanban_materials', 'Materiali'),
            menu=self.kanban_materials_submenu
        )
        self.kanban_root_submenu.add_cascade(
            label=self.lang.get('submenu_kanban_core', 'KanBan'),
            menu=self.kanban_core_submenu
        )

    def _update_traceability_submenu(self):
        """Aggiorna il sottomenu Tracciabilità"""
        self.traceability_submenu.delete(0, 'end')

        # Clienti Finali
        customers_submenu = tk.Menu(self.traceability_submenu, tearoff=0)
        self.traceability_submenu.add_cascade(label=self.lang.get('submenu_final_customers', "Clienti Finali"),
                                              menu=customers_submenu)
        customers_submenu.add_command(label=self.lang.get('submenu_manage_customers', "Gestisci Clienti"),
                                      command=self.open_manage_customers_with_login)

        # Prodotti Finali
        products_submenu = tk.Menu(self.traceability_submenu, tearoff=0)
        self.traceability_submenu.add_cascade(label=self.lang.get('submenu_final_products', "Prodotti Finali"),
                                              menu=products_submenu)
        products_submenu.add_command(label=self.lang.get('submenu_define_products', "Definisci Prodotti"),
                                     command=self.open_define_products_with_login)

        # Collegamenti Prodotti
        links_submenu = tk.Menu(self.traceability_submenu, tearoff=0)
        self.traceability_submenu.add_cascade(label=self.lang.get('submenu_link_products', "Collega Prodotti"),
                                              menu=links_submenu)
        links_submenu.add_command(label=self.lang.get('submenu_manage_links', "Gestisci Collegamenti"),
                                  command=self.open_manage_links_with_login)

        # Verifica Associazione
        self.traceability_submenu.add_command(
            label=self.lang.get('verification_association', "Verifica Associazione"),
            command=self.open_verification_association_with_login
        )

        # FCT Transfer
        self.traceability_submenu.add_cascade(
            label=self.lang.get('menu_fct_transfer', "FCT Transfer"),
            menu=self.fct_transfer_submenu
        )
        self.fct_transfer_submenu.delete(0, 'end')
        self.fct_transfer_submenu.add_command(
            label=self.lang.get('menu_fct_settings', "Settings"),
            command=self._open_fct_settings
        )
        self.fct_transfer_submenu.add_command(
            label=self.lang.get('menu_fct_run', "Run"),
            command=self._toggle_fct_execution
        )

    def _update_calibrations_submenu(self):
        """Aggiorna il sottomenu Calibrazioni"""
        self.calibrations_submenu.delete(0, 'end')
        self.calibrations_submenu.add_command(
            label=self.lang.get('submenu_manage_calibrations', "Gestisci Calibrazioni"),
            command=self.open_calibrations_manager_with_login
        )

    def _update_coating_submenu(self):
        """Aggiorna il sottomenu Coating con struttura organizzata"""
        self.coating_submenu.delete(0, 'end')

        # Gestione Materiali Coating
        self.coating_submenu.add_cascade(
            label=self.lang.get('submenu_coating_materials', "🧰 Gestione Materiali"),
            menu=self.coating_materials_submenu
        )
        self.coating_materials_submenu.delete(0, 'end')

        # ✅ SEPARARE I DUE MENU
        self.coating_materials_submenu.add_command(
            label=self.lang.get('submenu_coating_types', "🎨 Gestione Tipi Vernice"),
            command=self.open_coating_types_with_login
        )
        self.coating_materials_submenu.add_command(
            label=self.lang.get('submenu_coating_thickness_specs', "📐 Gestione Specifiche Spessore"),
            command=self.open_coating_thickness_specs_with_login
        )

        # Controlli Qualità
        self.coating_submenu.add_separator()
        self.coating_submenu.add_command(
            label=self.lang.get('submenu_coating_viscosity', "🧪 Controllo Viscosità"),
            command=self.open_coating_viscosity_with_login
        )
        self.coating_submenu.add_command(
            label=self.lang.get('submenu_coating_thickness', "📏 Controllo Spessore"),
            command=self.open_coating_thickness_with_login
        )

        # Rapporti
        self.coating_submenu.add_separator()
        self.coating_submenu.add_command(
            label=self.lang.get('submenu_coating_reports', "📊 Rapporti"),
            command=self.open_coating_reports_with_login
        )

    def _update_product_checks_submenu(self):
        """Aggiorna il sottomenu Verifiche Prodotti"""
        self.product_checks_submenu.delete(0, 'end')

        self.product_checks_submenu.add_command(
            label=self.lang.get('submenu_manage_product_checks', "Gestione Prodotti"),
            command=lambda: self._execute_authorized_action(
                'manage_product_check',
                lambda: self._open_product_checks_management()
            )
        )

        self.product_checks_submenu.add_command(
            label=self.lang.get('submenu_manage_check_rules', "Gestione Regole"),
            command=lambda: self._execute_authorized_action(
                'manage_check_rules',
                lambda: self._open_check_tasks_management()
            )
        )

        self.product_checks_submenu.add_separator()
        self.product_checks_submenu.add_command(
            label=self.lang.get('submenu_verify_products', "Verifiche"),
            command=lambda: self._execute_authorized_action(
                'verify_product_check',
                lambda: self._open_product_verification()
            )
        )

        self.product_checks_submenu.add_separator()
        self.product_checks_submenu.add_command(
            label=self.lang.get('submenu_verification_reports', "Rapporti"),
            command=lambda: messagebox.showinfo(
                self.lang.get('info', 'Informazione'),
                self.lang.get('feature_coming_soon', 'Funzionalità in arrivo')
            ),
            state='disabled'
        )

    def _update_reports_submenu(self):
        """Aggiorna il sottomenu Rapporti"""
        self.reports_submenu.delete(0, 'end')

        # Operatività
        self.reports_submenu.add_cascade(label=self.lang.get('submenu_operativity', "Operativita'"),
                                         menu=self.operativity_submenu)
        self.operativity_submenu.delete(0, 'end')

        shipping_submenu = tk.Menu(self.operativity_submenu, tearoff=0)
        self.operativity_submenu.add_cascade(label=self.lang.get('submenu_shipping', "Spedizioni"),
                                             menu=shipping_submenu)
        shipping_submenu.delete(0, 'end')
        shipping_submenu.add_command(label=self.lang.get('upload_report_label', "Carica Report"),
                                     command=self.open_shipping_report_window_with_login)
        shipping_submenu.add_command(label=self.lang.get('submenu_shipping_settings', "Impostazioni Spedizione"),
                                     command=self.open_shipping_settings_with_login)
        shipping_submenu.add_command(label=self.lang.get('submenu_xls_settings', "Impostazioni XLS"),
                                     command=self.open_xls_settings_with_login)

        # Altri rapporti
        self.reports_submenu.add_command(
            label=self.lang.get('submenu_line_stoppage_reports', "Rapporti di fermo linea"),
            command=self.open_line_stoppage_report
        )

        self.reports_submenu.add_command(
            label=self.lang.get("scrap_reports", "Rapporto Scarti"),
            command=self.open_scrap_reports
        )

    def _update_maintenance_menu(self):
        """Aggiorna il menu Manutenzione"""
        self.maintenance_menu.delete(0, 'end')

        # Gestione Macchine
        machine_submenu = tk.Menu(self.maintenance_menu, tearoff=0)
        self.maintenance_menu.add_cascade(label=self.lang.get('submenu_machines'), menu=machine_submenu)
        machine_submenu.add_command(label=self.lang.get('submenu_add_machine'),
                                    command=self.open_add_machine_with_login)
        machine_submenu.add_command(label=self.lang.get('submenu_edit_machine'),
                                    command=self.open_edit_machine_with_login)
        machine_submenu.add_command(label=self.lang.get('submenu_view_machines'),
                                    command=lambda: maintenance_gui.open_view_machines(self, self.db, self.lang))
        machine_submenu.add_separator()
        machine_submenu.add_command(label=self.lang.get('submenu_brand_management', "Gestione Brand"),
                                    command=self.open_brand_manager_with_login)
        machine_submenu.add_command(label=self.lang.get('submenu_company_management', "Gestione Compagnie"),
                                    command=self.open_company_manager_with_login)

        # Task di Manutenzione
        tasks_submenu = tk.Menu(self.maintenance_menu, tearoff=0)
        self.maintenance_menu.add_cascade(
            label=self.lang.get('submenu_maintenance_tasks_header', 'Task di Manutenzione'), menu=tasks_submenu)
        tasks_submenu.add_command(label=self.lang.get('submenu_manage_maint_task', "Gestione Task di Manutenzione"),
                                  command=self.open_add_maintenance_tasks_with_login)

        # Voci principali
        self.maintenance_menu.add_command(label=self.lang.get('submenu_fill_templates'),
                                          command=self.open_fill_templates_with_login)
        self.maintenance_menu.add_separator()
        self.maintenance_menu.add_command(label=self.lang.get('submenu_reports', "Report Panoramica"),
                                          command=lambda: maintenance_gui.open_reports(self, self.db, self.lang))
        self.maintenance_menu.add_command(label=self.lang.get('submenu_missing_action', "Missing Action Report"),
                                          command=self.open_missing_action_report)

    def _update_submissions_menu(self):
        """Aggiorna il menu Segnalazioni"""
        self.submissions_menu.delete(0, 'end')
        self.submissions_menu.add_command(label=self.lang.get('submenu_new_submission', "Nuova Segnalazione"),
                                          command=self.open_new_submission_form)
        self.submissions_menu.add_command(
            label=self.lang.get('submenu_assign', 'Assegna'),
            command=self.open_assign_submissions_with_login
        )
        self.submissions_menu.add_command(
            label=self.lang.get('menu_submissions_management', "Gestione"),
            command=lambda: self._execute_authorized_action(
                'management_submissions',
                lambda: self._open_submissions_management()
            )
        )

    def _update_tools_menu(self):
        """Aggiorna il menu Strumenti"""
        self.tools_menu.delete(0, 'end')

        # Autorizzazioni
        self.tools_menu.add_cascade(label=self.lang.get('submenu_permissions', "Autorizzazioni"),
                                    menu=self.permissions_submenu)
        self.permissions_submenu.delete(0, 'end')
        self.permissions_submenu.add_command(
            label=self.lang.get('submenu_special_permissions', "Autorizzazioni Speciali"),
            command=self.open_manage_permissions_with_login)
        self.permissions_submenu.add_command(
            label=self.lang.get('submenu_view_permissions', "Visualizza Autorizzazioni"),
            command=self.open_view_permissions_with_login)

        self.tools_menu.add_separator()

        # Materiali
        self.tools_menu.add_cascade(label=self.lang.get('menu_materials', "Materiali"), menu=self.materials_submenu)
        self.materials_submenu.delete(0, 'end')
        self.materials_submenu.add_command(label=self.lang.get('submenu_manage', "Gestione"),
                                           command=self.open_manage_materials_with_login)
        self.materials_submenu.add_command(label=self.lang.get('submenu_view', "Visualizza"),
                                           command=self.open_view_materials)

        # Altri strumenti
        self.tools_menu.add_command(
            label=self.lang.get('submenu_scrap_types', 'Tipi scrap'),
            command=self.open_scrap_types_with_login
        )

        self.tools_menu.add_separator()
        self.tools_menu.add_command(label=self.lang.get('submenu_suppliers', "Produttori"),
                                    command=self.open_suppliers_manager_with_login)
        self.tools_menu.add_command(label=self.lang.get('submenu_maint_cycles', "Cicli Manutenzione"),
                                    command=self.open_maint_cycles_manager_with_login)
        self.tools_menu.add_command(label=self.lang.get('submenu_doc_types', "Aggiungi Tipo Documento"),
                                    command=self.open_doc_types_manager_with_login)
        self.tools_menu.add_command(label=self.lang.get('submenu_maint_times', "Tempi Manutenzione"),
                                    command=self.open_maintenance_times_with_login)

    def _update_help_menu(self):
        """Aggiorna il menu Aiuto"""
        self.help_menu.delete(0, 'end')
        self.help_menu.add_cascade(label=self.lang.get('menu_language'), menu=self.language_menu)
        about_menu_label = f"{self.lang.get('menu_about')} {APP_VERSION}"
        self.help_menu.add_command(label=about_menu_label, command=self._show_about)

    def _update_main_menubar(self):
        """Aggiorna le etichette della barra dei menu principale"""
        try:
            self.menubar.delete(0, 'end')
            self._add_main_menus_to_bar()
            self.config(menu=self.menubar)
            self.update_idletasks()
        except tk.TclError:
            pass

    def open_coating_thickness_with_login(self):
        """Apre la finestra di controllo spessore coating dopo login"""

        def action(user_name):
            try:
                from coating_gui import CoatingThicknessMeasurementWindow
                logger.debug(f"[main.py] Apertura CoatingThicknessMeasurementWindow con user_name: '{user_name}'")
                window = CoatingThicknessMeasurementWindow(
                    parent=self,
                    conn_str=self.db.conn_str,
                    username=user_name,  # ✅ Parametro corretto: username
                    language_code=self.lang.current_language
                )
                window.show()
                logger.info(f"Aperta finestra Coating Thickness da utente: {user_name}")
            except Exception as e:
                logger.error(f"Errore apertura controllo spessore coating: {e}")
                messagebox.showerror(
                    self.lang.get('error', 'Errore'),
                    f"Errore apertura controllo spessore: {e}"
                )

        self._execute_simple_login(action_callback=action)

    def open_scrap_reports(self):
        try:
            # Usa self direttamente come parent
            scrap_reports_gui.ScrapReportsWindow(self, self.db, self.lang)
        except Exception as e:
            logger.error(f"Errore apertura rapporti scarti: {e}")

    def _open_submissions_management(self, user_id=None):
        """Apre la finestra di gestione segnalazioni"""
        # 🔍 DEBUG: Stampa tutti gli attributi che contengono "user" o "employee"
        print("\n=== ATTRIBUTI DISPONIBILI ===")
        for attr in dir(self):
            if not attr.startswith('_'):  # Escludi attributi privati
                if 'user' in attr.lower() or 'employee' in attr.lower() or 'logged' in attr.lower():
                    try:
                        value = getattr(self, attr)
                        if not callable(value):  # Escludi metodi
                            print(f"  {attr} = {value}")
                    except:
                        pass
        print("=============================\n")
        import submissions_management_gui
        user_id = getattr(self, '_temp_authorized_user_id', None)

        submissions_management_gui.SubmissionsManagementWindow(
            self, self.db, self.lang, user_id
        )

    # ✅ ===== METODI COATING =====
    # def open_coating_settings_with_login(self):
    #     """Apre la finestra di gestione tipi vernice con autenticazione autorizzata"""
    #
    #     def action():
    #         try:
    #             from coating_gui import CoatingSettingsWindow
    #             window = CoatingSettingsWindow(
    #                 parent=self,
    #                 conn_str=self.db.conn_str,
    #                 language_code=self.lang.current_language
    #             )
    #             window.show()
    #             logger.info("Aperta finestra Coating Settings")
    #         except Exception as e:
    #             logger.error(f"Errore apertura Coating Settings: {e}")
    #             messagebox.showerror(
    #                 self.lang.get('error', "Errore"),
    #                 f"{self.lang.get('window_open_error', 'Impossibile aprire la finestra')}: {str(e)}"
    #             )
    #
    #     self._execute_authorized_action('submenu_coating_materials_manage', action)
    def open_coating_types_with_login(self):
        """Apre la finestra di gestione tipi vernice con autenticazione autorizzata"""

        def action():
            try:
                from coating_gui import CoatingSettingsWindow
                window = CoatingSettingsWindow(
                    parent=self,
                    conn_str=self.db.conn_str,
                    language_code=self.lang.current_language
                )
                window.show()
                logger.info("Aperta finestra Gestione Tipi Vernice")
            except Exception as e:
                logger.error(f"Errore apertura Gestione Tipi Vernice: {e}")
                messagebox.showerror(
                    self.lang.get('error', "Errore"),
                    f"{self.lang.get('window_open_error', 'Impossibile aprire la finestra')}: {str(e)}"
                )

        self._execute_authorized_action('submenu_coating_types', action)

    def open_coating_thickness_specs_with_login(self):
        """Apre la finestra di gestione specifiche spessore con autenticazione autorizzata"""

        def action():
            try:
                from coating_gui import CoatingThicknessSettingsWindow
                window = CoatingThicknessSettingsWindow(
                    parent=self,
                    conn_str=self.db.conn_str,
                    language_code=self.lang.current_language
                )
                window.show()
                logger.info("Aperta finestra Gestione Specifiche Spessore")
            except Exception as e:
                logger.error(f"Errore apertura Gestione Specifiche Spessore: {e}")
                messagebox.showerror(
                    self.lang.get('error', "Errore"),
                    f"{self.lang.get('window_open_error', 'Impossibile aprire la finestra')}: {str(e)}"
                )

        self._execute_authorized_action('submenu_coating_thickness_specs', action)

    def open_coating_viscosity_with_login(self):
        """Apre la finestra di registrazione viscosità con login semplice"""

        def action(user_name):
            try:
                from coating_gui import CoatingViscosityWindow
                logger.debug(f"[main.py] Apertura CoatingViscosityWindow con user_name: '{user_name}'")
                window = CoatingViscosityWindow(
                    parent=self,
                    conn_str=self.db.conn_str,
                    username=user_name,  # ✅ Parametro corretto: username (non user_name)
                    language_code=self.lang.current_language
                )
                window.show()
                logger.info(f"Aperta finestra Coating Viscosity da utente: {user_name}")
            except Exception as e:
                logger.error(f"Errore apertura Coating Viscosity: {e}")
                messagebox.showerror(
                    self.lang.get('error', "Errore"),
                    f"{self.lang.get('window_open_error', 'Impossibile aprire la finestra')}: {str(e)}"
                )

        self._execute_simple_login(action_callback=action)

    def open_coating_reports_with_login(self):
        """Apre la finestra dei report coating (senza login richiesto)"""
        try:
            from coating_gui import CoatingReportsWindow
            window = CoatingReportsWindow(
                parent=self,
                conn_str=self.db.conn_str,
                language_code=self.lang.current_language
            )
            window.show()
            logger.info("Aperta finestra Coating Reports")
        except Exception as e:
            logger.error(f"Errore apertura Coating Reports: {e}")
            messagebox.showerror(
                self.lang.get('error', "Errore"),
                f"{self.lang.get('window_open_error', 'Impossibile aprire la finestra')}: {str(e)}"
            )

    # ✅ ===== FINE METODI COATING =====
    def stop_fct_loop(self):
        """Ferma il loop FCT e invia notifica email"""
        if self.fct_loop_running:
            self.fct_loop_running = False
            # Cancella il timer se esiste
            if hasattr(self, 'fct_timer_id') and self.fct_timer_id:
                self.after_cancel(self.fct_timer_id)
                self.fct_timer_id = None

            # Invia email in background
            self._send_fct_stop_notification()

            # Aggiorna UI
            if hasattr(self, 'fct_status_label'):
                self.fct_status_label.config(text=self.lang.get('fct_stopped', 'FCT Loop Fermato'))

    def _send_fct_stop_notification(self):
        """Invia notifica email in background quando FCT loop viene fermato"""
        import threading

        def send_email_thread():
            try:
                # Recupero dei destinatari dal database
                recipients = utils.get_email_recipients(self.db.conn, 'Sys_fct_settings')

                if not recipients:
                    logging.info("Nessun destinatario configurato per notifiche FCT")
                    return

                # Prepara il messaggio
                subject = self.lang.get('fct_loop_stopped_subject', 'FCT Transfer Loop Fermato')
                body = self.lang.get(
                    'fct_loop_stopped_body',
                    f'Il loop FCT Transfer è stato fermato dall\'utente {getattr(self, "current_user", "N/A")} alle {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                )

                # Invio dell'email
                utils.send_email(
                    recipients=recipients,
                    subject=subject,
                    body=body
                )

                logging.info(f"Notifica FCT stop inviata a: {recipients}")

            except Exception as e:
                logging.error(f"Errore nell'invio della notifica FCT: {str(e)}")

        # Avvia il thread in background
        thread = threading.Thread(target=send_email_thread, daemon=True)
        thread.start()

    def open_scrap_types_with_login(self):
        # Usa il gate "per menù" con chiave di traduzione dedicata
        self._execute_authorized_action(
            menu_translation_key='submenu_scrap_types',
            action_callback=lambda: scarti_gui.open_scrap_reasons_manager(self, self.db, self.lang)
        )

    def _change_language(self, lang_code):
        """Cambia la lingua, aggiorna la UI, salva l'impostazione e mostra una notifica."""
        self.lang.set_language(lang_code)
        self.update_texts()
        self._save_language_setting(lang_code)

        # Mostra un messaggio per informare l'utente
        messagebox.showinfo(
            self.lang.get('lang_change_title', "Language Changed"),
            self.lang.get('lang_change_message',
                          "The language has been updated. Please reopen any open windows to apply the changes."),
            parent=self
        )

    def _open_fct_settings(self):
        """Apre la finestra di configurazione FCT Transfer (con controllo login)"""
        ok = self._execute_authorized_action(
            menu_translation_key='menu_fct_settings',
            action_callback=lambda: fct_transfer.FCTTransferSettingsWindow(
                self,
                self.db,
                self.lang,
                self.fct_config
            )
        )
        if not ok:
            return

    def _toggle_fct_execution(self):
        """Avvia o ferma l'esecuzione FCT Transfer"""
        if not self.fct_config.bat_file_path:
            messagebox.showwarning(
                self.lang.get('warning', "Attenzione"),
                self.lang.get('fct_configure_first', "Configurare prima il file batch in Settings"),
                parent=self
            )
            return

        # Verifica stato attuale
        is_running, instances = self.fct_manager.check_bat_running_status()

        if not self.fct_manager.is_running:
            # Avvia esecuzione
            if is_running:
                # Già in esecuzione su altra istanza
                messagebox.showinfo(
                    self.lang.get('info', "Informazione"),
                    self.lang.get('fct_already_running', "Batch già in esecuzione su un'altra istanza"),
                    parent=self
                )
                # Cambia comunque il menu in Stop (per coerenza UI)
                self._update_fct_menu_label("Stop")
            else:
                # Avvia nuova esecuzione
                if self.fct_manager.start_bat_execution():
                    self._update_fct_menu_label("Stop")
                    messagebox.showinfo(
                        self.lang.get('success', "Successo"),
                        self.lang.get('fct_started', "Esecuzione FCT Transfer avviata"),
                        parent=self
                    )
                else:
                    messagebox.showerror(
                        self.lang.get('error', "Errore"),
                        self.lang.get('fct_start_error', "Errore durante l'avvio"),
                        parent=self
                    )
        else:
            # Ferma esecuzione
            _, active_instances = self.fct_manager.check_bat_running_status()

            if len(active_instances) == 0:
                # Nessuna istanza attiva (stato inconsistente)
                self.fct_manager.is_running = False
                self._update_fct_menu_label("Run")

            elif len(active_instances) == 1:
                # Una sola istanza: ferma direttamente
                if self.fct_manager.stop_bat_execution():
                    self._update_fct_menu_label("Run")
                    messagebox.showinfo(
                        self.lang.get('success', "Successo"),
                        self.lang.get('fct_stopped', "Esecuzione FCT Transfer fermata"),
                        parent=self
                    )

            else:
                # Multiple istanze: chiedi quale fermare
                dialog = fct_transfer.FCTTransferStopDialog(self, self.lang, active_instances)
                self.wait_window(dialog)

                if dialog.selected_instances:
                    # Ferma le istanze selezionate
                    for inst in dialog.selected_instances:
                        self.fct_manager.stop_bat_execution(inst['DateStart'])

                    # Verifica se ci sono ancora istanze attive
                    _, remaining = self.fct_manager.check_bat_running_status()
                    if not remaining:
                        self._update_fct_menu_label("Run")

                    messagebox.showinfo(
                        self.lang.get('success', "Successo"),
                        self.lang.get('fct_instances_stopped', f"{len(dialog.selected_instances)} istanze fermate"),
                        parent=self
                    )

    def _update_fct_menu_label(self, label_key: str):
        """Aggiorna l'etichetta del menu Run/Stop"""
        if hasattr(self, 'fct_menu') and self.fct_run_menu_index is not None:
            new_label = self.lang.get(f'menu_fct_{label_key.lower()}', label_key)
            self.fct_menu.entryconfig(
                self.fct_run_menu_index,
                label=new_label
            )

    def _show_about(self):
        """Mostra la finestra di dialogo 'About' con le informazioni del software."""
        about_title = f"{self.lang.get('about_title')} - v{APP_VERSION}"
        about_template = self.lang.get_raw('about_message')
        # Assicurati che il template nel DB usi {version} e {developer}
        about_message = about_template.replace('{version}', APP_VERSION).replace('{developer}', APP_DEVELOPER)

        messagebox.showinfo(
            about_title,
            about_message,
            parent=self
        )

    def open_manage_materials_with_login(self):
        self._execute_simple_login(
            action_callback=lambda user_name: materials_gui.open_manage_materials(self, self.db, self.lang, user_name)
        )

    def open_view_materials(self):
        """Apre la finestra di visualizzazione materiali (senza login)."""
        # Passiamo 'None' come user_name perché non c'è autenticazione
        materials_gui.open_view_materials(self, self.db, self.lang, user_name=None)

    def open_edit_machine_with_login(self):
        def action(user_name):
            self.authenticated_user_for_maintenance = user_name
            maintenance_gui.open_edit_machine(self, self.db, self.lang)

        self._execute_simple_login(action_callback=action)

    def open_add_machine_with_login(self):
        """Apre la finestra per aggiungere una macchina dopo un login semplice."""
        self._execute_simple_login(
            action_callback=lambda user_name: maintenance_gui.open_add_machine(self, self.db, self.lang)
        )

    def _on_closing(self, force_quit=False):
        """Gestisce la chiusura dell'applicazione."""
        # Ferma tutti i timer attivi
        if self.slideshow_job_id: self.after_cancel(self.slideshow_job_id)
        if self.birthday_flash_job_id: self.after_cancel(self.birthday_flash_job_id)
        if self.birthday_stop_job_id: self.after_cancel(self.birthday_stop_job_id)
        if self.periodic_check_job_id: self.after_cancel(self.periodic_check_job_id)

        self._stop_product_check_background_task()

        if force_quit or messagebox.askokcancel(self.lang.get('quit_title'), self.lang.get('quit_message')):
            self.db.disconnect()
            self.destroy()

class UpdateNotificationDialog(tk.Toplevel):
    """Dialogo per notificare un nuovo aggiornamento e chiedere l'azione desiderata."""

    def __init__(self, parent, lang, new_version, current_version):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
        self.title(lang.get('update_available_title', "Aggiornamento Disponibile"))
        self.result = None  # 'now', 'later', o 'ignore'

        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")

        message = lang.get('update_notification_message',
                           "È stata rilasciata una nuova versione del programma ({0}).\n"
                           "La tua versione attuale è la {1}.\n\n"
                           "Cosa vuoi fare?", new_version, current_version)

        ttk.Label(main_frame, text=message, justify=tk.LEFT).pack(pady=10)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text=lang.get('update_now_btn', "Aggiorna Ora"),
                   command=self._on_now).pack(side="left", padx=10)
        ttk.Button(btn_frame, text=lang.get('remind_later_btn', "Ricorda tra 15 min"),
                   command=self._on_later).pack(side="left", padx=10)
        ttk.Button(btn_frame, text=lang.get('ignore_session_btn', "Ignora per questa sessione"),
                   command=self._on_ignore).pack(side="left", padx=10)

    def _on_now(self):
        self.result = 'now'
        self.destroy()

    def _on_later(self):
        self.result = 'later'
        self.destroy()

    def _on_ignore(self):
        self.result = 'ignore'
        self.destroy()

if __name__ == "__main__":
    app = App()
    if not app.should_exit:
        app.mainloop()
