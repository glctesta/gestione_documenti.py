#import configparser
# --- StdIO safeguard + Faulthandler sicuro per exe windowed ---
import sys, os, atexit
from pathlib import Path

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
import sys, os, atexit
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
import collections.abc
import scarti_gui
import tempfile
import assign_submissions_gui
import utils
import logging
import logging.config
from pathlib import Path
from logging.handlers import RotatingFileHandler


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
APP_VERSION = "1.7.4"  # Versione aggiornata
APP_DEVELOPER = "Gianluca Testa"

# # --- CONFIGURAZIONE DATABASE ---
DB_DRIVER = '{SQL Server Native Client 11.0}'
DB_SERVER = 'roghipsql01.vandewiele.local\\emsreset'
DB_DATABASE = 'Traceability_rs'
DB_UID = 'emsreset'
DB_PWD = 'E6QhqKUxHFXTbkB7eA8c9ya'
DB_CONN_STR = f'DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_UID};PWD={DB_PWD};'


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

    def fetch_card_referiments(self, label_code):
        """
        Carica i riferimenti scheda per una label (LabelCod).
        Ritorna una lista di stringhe (Referiment).
        """
        query = """
        select 
            ProductRiferiments.CodRiferimento + ' [' + ParentPhases.ParentPhaseName + ']' As Referiment
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
            eaFrom.WorkEmail AS Email
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
            SELECT idParentPhase, ParentPhaseName
            FROM Traceability_RS.dbo.ParentPhases
            WHERE (CHARINDEX('Incoming', ParentPhaseName) = 0)
              AND (CHARINDEX('Instru', ParentPhaseName) = 0)
            ORDER BY ParentPhaseName;
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

    # Sostituisci il metodo esistente con questo
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
        logger.debug("authenticate_user result for user_id=%r: %s", user_id,
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
            logger.debug("Executing permissions query with param user_id=%r", user_id)
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
            SELECT TOP 1 
                cast(c.CalibratedOn as date) As CalibratedOn, 
                cast(c.ExpireOn as date) as ExpireOn
            FROM eqp.calibrations c 
            WHERE c.equipmentid = ?
            ORDER BY c.CalibratedOn DESC
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

    def add_new_calibration(self, equipment_id, expiry_date, supplier_id, cert_number):
        """
        MODIFICATO: Inserisce una nuova calibrazione usando l'ID del fornitore (supplier_id).
        :param supplier_id: L'ID numerico del fornitore (IDSite).
        """
        query = """
            INSERT INTO eqp.calibrations 
                (EquipmentId, CalibratedOn, ExpireOn, CalibrationSupplierId, NrCertificate)
            VALUES (?, GETDATE(), ?, ?, ?)
        """
        # Nota: Ho ipotizzato che il campo nella tabella `eqp.calibrations`
        # si chiami `CertifyingBodyId`. Adattalo se ha un nome diverso.
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, equipment_id, expiry_date, supplier_id, cert_number)
            self.conn.commit()
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()

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


    #
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
                SELECT a.AuthorizedUsedId, ap.TranslationValue + ' [' + ap.LanguageCode + ']' AS MenuKey
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
                SELECT a.Translationkey, a.translationvalue
                FROM AppTranslations a
                WHERE a.LanguageCode = 'it'             -- O 'en', la lingua base per le chiavi
                  AND a.TranslationKey LIKE 'submenu_%' -- Seleziona solo chiavi di sottomenu
                  AND NOT EXISTS (SELECT 1 \
                                  FROM AutorizedUsers \
                                  WHERE TranslationKey = a.TranslationKey \
                                    AND EmployeeHireHistoryId = ? \
                                    AND DateOut IS NULL)
                ORDER BY a.translationvalue, a.TranslationKey; \
                """
        try:
            self.cursor.execute(query, employee_hire_history_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return []

    def grant_permission(self, employee_hire_history_id, translation_key):
        """Assegna un permesso a un utente."""
        query = "INSERT INTO AutorizedUsers (EmployeeHireHistoryId, TranslationKey) VALUES (?, ?);"
        try:
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

    def add_new_spare_part(self, material_part_number, material_code=None, material_description=None,
                           to_be_revizited=1):
        """Inserisce una nuova parte in eqp.SparePartMaterials e restituisce il nuovo ID."""
        # Assumiamo che la tabella abbia un IDENTITY ID (SparePartMaterialId)
        query = """
                INSERT INTO eqp.SparePartMaterials (MaterialPartNumber, MaterialCode, MaterialDescription,toberevizited)
                OUTPUT INSERTED.SparePartMaterialId 
                VALUES (?, ?, ?, 1);
                """
        try:
            # Esegui l'INSERT
            self.cursor.execute(query, material_part_number, material_code, material_description)

            # Poiché abbiamo usato OUTPUT, l'INSERT ora restituisce un risultato che possiamo leggere con fetchval().
            new_id = self.cursor.fetchval()

            if new_id:
                self.conn.commit()
                return new_id
            else:
                self.conn.rollback()
                self.last_error_details = "Inserimento riuscito ma impossibile recuperare il nuovo ID."
                return None

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
        query = "SELECT  distinct e.EquipmentId, InternalName, SerialNumber FROM eqp.Equipments E inner join [eqp].[CompitiManutenzione] CM on e.EquipmentId=cm.EquipmentId ORDER BY InternalName, SerialNumber;"
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
        # Mettila topmost per mezzo secondo e poi rimuovi il flag
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



    def open_assign_submissions_with_login(self):
        self._execute_authorized_action(
            menu_translation_key='submenu_assign',
            action_callback=lambda: assign_submissions_gui.open_assign_submissions(self, self.db, self.lang)
        )

    def open_scrap_declaration_with_login(self):
        """Apre la finestra per la dichiarazione scarti con autenticazione e autorizzazione."""
        # self._execute_authorized_action(
        #     menu_translation_key='submenu_scrap_declaration',
        #     action_callback=lambda: scarti_gui.open_scrap_declaration_window(self, self.db, self.lang)
        # )
        self._execute_authorized_action(
            menu_translation_key='submenu_scrap_declaration',
            action_callback=lambda:scarti_gui.open_scrap_declaration_window(self, self.db, self.lang)
        )
    def open_calibrations_manager_with_login(self):
        logger = logging.getLogger("TraceabilityRS")
        required = 'calibration_management'
        logger.debug("Request to open CalibrationsWindow; required_permission=%r", required)
        # Chiama il login in modalità "gatekeeper"
        user = self._execute_simple_login(required_permission=required)
        logger.debug("Login result for calibrations: %s", "OK" if user else "FAILED")

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
            duration_ms = 3 * 60 * 1000
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
            duration_ms = 3 * 60 * 1000
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
        self.periodic_check_job_id = self.after(120000, self._periodic_version_check)

        is_birthday = self._check_for_birthdays()
        if not is_birthday:
            self._setup_slideshow()

        # PRIMA: self.after(500, self._check_calibration_warnings_startup)
        # DOPO:
        self.after(500, self._check_calibration_warnings_startup_async)

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
        logger.debug("_execute_simple_login called; required_permission=%r", required_permission)

        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)

        if not login_form.clicked_login:
            logger.debug("Login window closed without login.")
            return None

        user_id = login_form.user_id
        logger.debug("LoginWindow returned user_id=%r", user_id)

        password = login_form.password
        user = self.db.authenticate_and_get_user(user_id, password)

        if not user:
            logger.debug("Authentication failed for user_id=%r", user_id)
            messagebox.showerror(self.lang.get('login_title'),
                                 self.lang.get('login_auth_failed'), parent=self)
            return None

        logger.debug("Authenticated as %r; permissions=%s", user.name,
                     sorted(user.permissions))

        if required_permission and not user.has_permission(required_permission):
            logger.debug("Permission check FAILED for %r -> required=%r",
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
        """
        Gestisce il processo di login e autorizzazione per un'azione.
        :param menu_translation_key: La chiave di traduzione del menu per il controllo permessi.
        :param action_callback: La funzione da eseguire in caso di successo.
        """
        logger.debug("_execute_authorized_action called; menu_translation_key=%r", menu_translation_key)

        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)

        # Procede solo se l'utente ha premuto "Login"
        if not login_form.clicked_login:
            return

        user_id = login_form.user_id
        logger.debug("LoginWindow returned user_id=%r for authorized action %r", user_id, menu_translation_key)
        password = login_form.password

        # Controlla autenticazione e autorizzazione
        auth_result = self.db.authenticate_and_authorize(user_id, password, menu_translation_key)

        if auth_result is None:
            # Caso 1: Username o Password errati
            messagebox.showerror(self.lang.get('login_title'), self.lang.get('login_auth_failed'), parent=self)
        elif auth_result.AuthorizedUsedId is None:
            logger.debug("User %r authenticated but NOT authorized for %r", user_id, menu_translation_key)
            # Caso 2: Utente valido, ma NON autorizzato per questa funzione
            messagebox.showwarning(self.lang.get('auth_access_denied_title', "Accesso Negato"),
                                   self.lang.get('auth_access_denied_message',
                                                 "Non si dispone delle autorizzazioni necessarie per accedere a questa funzione."),
                                   parent=self)
        else:
            logger.debug("User %r authorized for %r; executing action.", user_id, menu_translation_key)
            try:
                self.last_authenticated_user_name = auth_result.EmployeeName
            except Exception:
                self.last_authenticated_user_name = None

            action_callback()

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
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # Crea i contenitori vuoti per ogni menu principale
        self.document_menu = tk.Menu(self.menubar, tearoff=0)
        self.general_docs_menu = tk.Menu(self.menubar, tearoff=0)
        self.operations_menu = tk.Menu(self.menubar, tearoff=0)
        self.maintenance_menu = tk.Menu(self.menubar, tearoff=0)
        self.submissions_menu = tk.Menu(self.menubar, tearoff=0)
        self.tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu = tk.Menu(self.menubar, tearoff=0)

        # --- SOTTOMENU DI OPERATIONS (Ordine Corretto) ---
        # 1. Crea il sottomenu genitore "Produzione"
        self.production_submenu = tk.Menu(self.operations_menu, tearoff=0)

        # 2. ORA crea i sottomenu figli, usando production_submenu come genitore
        self.declarations_submenu = tk.Menu(self.production_submenu, tearoff=0)
        self.traceability_submenu = tk.Menu(self.production_submenu, tearoff=0)
        self.reports_submenu = tk.Menu(self.production_submenu, tearoff=0)
        self.operativity_submenu = tk.Menu(self.reports_submenu, tearoff=0)

        # Crea il contenitore per il nuovo sottomenu "Calibrazioni"
        self.calibrations_submenu = tk.Menu(self.production_submenu, tearoff=0)

        # Sottomenu di Strumenti
        self.permissions_submenu = tk.Menu(self.tools_menu, tearoff=0)
        self.materials_submenu = tk.Menu(self.tools_menu, tearoff=0)

        # Aggiunge ogni menu principale alla barra
        self.menubar.add_cascade(menu=self.document_menu)
        self.menubar.add_cascade(menu=self.general_docs_menu)
        self.menubar.add_cascade(menu=self.operations_menu)
        self.menubar.add_cascade(menu=self.maintenance_menu)
        self.menubar.add_cascade(menu=self.submissions_menu)
        self.menubar.add_cascade(menu=self.tools_menu)
        self.menubar.add_cascade(menu=self.help_menu)

        # Il sottomenu della lingua è un caso speciale, dentro il menu Aiuto
        self.language_menu = tk.Menu(self.help_menu, tearoff=0)
        self.language_menu.add_command(label="Italiano", command=lambda: self._change_language('it'))
        self.language_menu.add_command(label="English", command=lambda: self._change_language('en'))
        self.language_menu.add_command(label="Română", command=lambda: self._change_language('ro'))
        self.language_menu.add_command(label="Deutsch", command=lambda: self._change_language('de'))
        self.language_menu.add_command(label="Svenska", command=lambda: self._change_language('sv'))

    def update_texts(self):
        """Aggiorna tutti i testi della UI principale, ricostruendo tutti i menu."""
        self.title(self.lang.get('app_title'))

        # --- 1. Menu Documenti (Produzione) ---
        self.document_menu.delete(0, 'end')
        self.document_menu.add_command(label=self.lang.get('menu_insert_doc'), command=self.open_insert_form)
        self.document_menu.add_command(label=self.lang.get('menu_view_doc'), command=self.open_view_form)
        self.document_menu.add_separator()
        self.document_menu.add_command(label=self.lang.get('menu_quit'), command=self._on_closing)

        # --- 2. Menu Documenti Generali ---
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
        # --- 3. Menu Operations ---
        self.operations_menu.delete(0, 'end')
        self.operations_menu.add_cascade(label=self.lang.get('submenu_production_ops', "Produzione"),
                                         menu=self.production_submenu)
        self.production_submenu.delete(0, 'end')
        self.production_submenu.add_cascade(label=self.lang.get('submenu_declarations', "Dichiarazioni"),
                                            menu=self.declarations_submenu)
        self.declarations_submenu.delete(0, 'end')
        self.declarations_submenu.add_command(
            label=self.lang.get('submenu_interruptions', "Interruzioni di produzione"),
            command=self.open_add_interruption_window_with_login)

        # Aggiungi la nuova voce di menu per la dichiarazione degli scarti
        self.declarations_submenu.add_command(
            label=self.lang.get('submenu_scrap_declaration', "Dichiarazione scarti"),
            command=self.open_scrap_declaration_with_login
        )

        # Aggiungi il nuovo sottomenu per la tracciabilità
        self.production_submenu.add_cascade(label=self.lang.get('submenu_traceability', "Tracciabilità"),
                                            menu=self.traceability_submenu)

        self.traceability_submenu.delete(0, 'end')
        # 1. Final Customers
        customers_submenu = tk.Menu(self.traceability_submenu, tearoff=0)
        self.traceability_submenu.add_cascade(label=self.lang.get('submenu_final_customers', "Clienti Finali"),
                                              menu=customers_submenu)
        customers_submenu.delete(0, 'end')
        # Aggiungi il nuovo sottomenu per le Calibrazioni
        self.production_submenu.add_cascade(label=self.lang.get('submenu_calibrations', "Calibrazioni"),
                                            menu=self.calibrations_submenu)

        self.calibrations_submenu.delete(0, 'end')

        self.calibrations_submenu.add_command(
            label=self.lang.get('submenu_manage_calibrations', "Gestisci Calibrazioni"),
            command=self.open_calibrations_manager_with_login
        )
        customers_submenu.add_command(label=self.lang.get('submenu_manage_customers', "Gestisci Clienti"),
                                      command=self.open_manage_customers_with_login)

        # 2. Final Products
        products_submenu = tk.Menu(self.traceability_submenu, tearoff=0)
        self.traceability_submenu.add_cascade(label=self.lang.get('submenu_final_products', "Prodotti Finali"),
                                              menu=products_submenu)
        products_submenu.delete(0, 'end')
        products_submenu.add_command(label=self.lang.get('submenu_define_products', "Definisci Prodotti"),
                                     command=self.open_define_products_with_login)

        # 3. Link Products
        links_submenu = tk.Menu(self.traceability_submenu, tearoff=0)
        self.traceability_submenu.add_cascade(label=self.lang.get('submenu_link_products', "Collega Prodotti"),
                                              menu=links_submenu)

        links_submenu.delete(0, 'end')
        links_submenu.add_command(label=self.lang.get('submenu_manage_links', "Gestisci Collegamenti"),
                                  command=self.open_manage_links_with_login)
        self.traceability_submenu.add_command(
            label=self.lang.get('verification_association', "Verifica Associazione"),
            command=self.open_verification_association_with_login)

        # Aggiungi il sottomenu Rapporti (SOLO UNA VOLTA)
        self.production_submenu.add_cascade(label=self.lang.get('submenu_reports_prod', "Rapporti"),
                                            menu=self.reports_submenu)

        self.reports_submenu.delete(0, 'end')
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
        self.reports_submenu.add_command(
            label=self.lang.get('submenu_line_stoppage_reports', "Rapporti di fermo linea"),
            command=self.open_line_stoppage_report)
        self.operations_menu.add_separator()
        self.operations_menu.add_command(label=self.lang.get('submenu_materials_ops', "Materiali"), state="disabled")
        self.operations_menu.add_command(label=self.lang.get('submenu_hr', "Risorse Umane"), state="disabled")

        # --- 4. Menu Manutenzione ---
        self.maintenance_menu.delete(0, 'end')

        # Sottomenu Gestione Macchine
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

        # Sottomenu Task di Manutenzione
        tasks_submenu = tk.Menu(self.maintenance_menu, tearoff=0)
        self.maintenance_menu.add_cascade(
            label=self.lang.get('submenu_maintenance_tasks_header', 'Task di Manutenzione'), menu=tasks_submenu)
        tasks_submenu.add_command(label=self.lang.get('submenu_manage_maint_task', "Gestione Task di Manutenzione"),
                                  command=self.open_add_maintenance_tasks_with_login)

        # Voci principali del menu Manutenzione
        self.maintenance_menu.add_command(label=self.lang.get('submenu_fill_templates'),
                                          command=self.open_fill_templates_with_login)
        self.maintenance_menu.add_separator()
        self.maintenance_menu.add_command(label=self.lang.get('submenu_reports', "Report Panoramica"),
                                          command=lambda: maintenance_gui.open_reports(self, self.db, self.lang))
        self.maintenance_menu.add_command(label=self.lang.get('submenu_missing_action', "Missing Action Report"),
                                          command=self.open_missing_action_report)

        # --- 5. Menu Segnalazioni ---
        self.submissions_menu.delete(0, 'end')
        self.submissions_menu.add_command(label=self.lang.get('submenu_new_submission', "Nuova Segnalazione"),
                                          command=self.open_new_submission_form)
        self.submissions_menu.add_command(
            label=self.lang.get('submenu_assign', 'Assegna'),
            command=self.open_assign_submissions_with_login
        )
        self.submissions_menu.add_command(label=self.lang.get('submenu_view_submissions', "Visualizza Segnalazioni"),
                                          state="disabled")

        # --- 6. Menu Strumenti ---
        self.tools_menu.delete(0, 'end')
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
        self.tools_menu.add_cascade(label=self.lang.get('menu_materials', "Materiali"), menu=self.materials_submenu)
        self.materials_submenu.delete(0, 'end')
        self.materials_submenu.add_command(label=self.lang.get('submenu_manage', "Gestione"),
                                           command=self.open_manage_materials_with_login)
        self.materials_submenu.add_command(label=self.lang.get('submenu_view', "Visualizza"),
                                           command=self.open_view_materials)

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

        # --- 7. Menu Help ---
        self.help_menu.delete(0, 'end')
        self.help_menu.add_cascade(label=self.lang.get('menu_language'), menu=self.language_menu)
        about_menu_label = f"{self.lang.get('menu_about')} {APP_VERSION}"
        self.help_menu.add_command(label=about_menu_label, command=self._show_about)

        # Aggiorna le etichette dei menu principali
        try:
            self.menubar.entryconfig(1, label=self.lang.get('menu_documents', "Documenti di Produzione"))
            self.menubar.entryconfig(2, label=self.lang.get('menu_general_docs', "Documenti Generali"))
            self.menubar.entryconfig(3, label=self.lang.get('menu_operations', "Operations"))
            self.menubar.entryconfig(4, label=self.lang.get('menu_maintenance'))
            self.menubar.entryconfig(5, label=self.lang.get('menu_submissions', "Segnalazioni"))
            self.menubar.entryconfig(6, label=self.lang.get('menu_tools', "Strumenti"))
            self.menubar.entryconfig(7, label=self.lang.get('menu_help'))
        except tk.TclError:
            pass

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
