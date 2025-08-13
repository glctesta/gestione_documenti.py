import tkinter as tk
from tkinter import ttk, messagebox, filedialog
# Corretto l'import per coerenza
from datetime import datetime
import pyodbc
import os
import subprocess
from collections import defaultdict
import sys
import maintenance_gui
import tempfile # Assicuriamoci che tempfile sia importato (usato in fetch_and_open_document)
import re
import reportlab

# Import per gestire le immagini PNG
try:
    from PIL import Image, ImageTk

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# --- CONFIGURAZIONE APPLICAZIONE ---
APP_VERSION = "1.4.0"  # Versione aggiornata
APP_DEVELOPER = "Gianluca Testa"

# --- CONFIGURAZIONE DATABASE ---
DB_DRIVER = '{SQL Server Native Client 11.0}'
DB_SERVER = 'roghipsql01.vandewiele.local\\emsreset'
DB_DATABASE = 'Traceability_rs'
DB_UID = 'emsreset'
DB_PWD = 'E6QhqKUxHFXTbkB7eA8c9ya'
DB_CONN_STR = f'DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_UID};PWD={DB_PWD};'


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

    # NUOVO METODO: Recupera impostazioni (es. email recipients)
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

    def add_new_spare_part(self, material_part_number, material_code=None, material_description=None, to_be_revizited=1):
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
    # NUOVO METODO: Inserisce la richiesta nella tabella eqp.RequestSpareParts
    # (Assicurati che questo metodo esista o sostituisci quello precedente se presente)
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

    # NUOVO METODO: Recupera le parti di ricambio/servizi disponibili
    # (Assicurati che questo metodo esista o sostituisci quello precedente se presente)

    # NUOVO METODO: Recupera e apre il documento basato su CompitoId
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


    def fetch_and_open_maintenance_document(self, document_id):
        """Recupera i dati binari di un documento di manutenzione dal DB, lo salva temporaneamente e lo apre."""

        self.last_error_details = ""  # Resetta l'errore

        try:
            # Seleziona i dati binari (DocumentSource) e i metadati (FileType, FileName)
            sql_select = """
                         SELECT DocumentSource, FileName, FileType
                         FROM eqp.EquipmentMantainanceDocs
                         WHERE EquipmentDocumentationId = ?
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

    # NUOVO METODO: Recupera le parti di ricambio/servizi disponibili
    def fetch_spare_parts(self):
        """Recupera la lista di parti di ricambio e servizi disponibili."""
        # ATTENZIONE: Questa query assume i nomi delle colonne (SparePartMaterialId, MaterialPartNumber, PartCode, Description).
        # Modificala se i nomi reali nella tua tabella eqp.SparePartMaterials sono diversi.
        query = """
                SELECT SparePartMaterialId, MaterialPartNumber, MaterialCode, MaterialDescription
                FROM eqp.SparePartMaterials
                ORDER BY MaterialPartNumber \
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero parti di ricambio: {e}")
            self.last_error_details = str(e)
            return []

    # NUOVO METODO: Inserisce la richiesta nella tabella eqp.RequestSpareParts
    def insert_spare_part_request(self, equipment_id, spare_part_id, quantity, notes, requested_by):
        """Inserisce una nuova richiesta di parti di ricambio o intervento."""
        # ATTENZIONE: Questa query assume la struttura della tabella eqp.RequestSpareParts.
        # Ho impostato uno stato iniziale 'Open'.
        query = """
                INSERT INTO eqp.RequestSpareParts
                (EquipmentId, SparePartMaterialId, Quantity, Note, RequestedBy, DateRequest, Solved)
                VALUES (?, ?, ?, ?, ?, GETDATE(), 0) \
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

    def __init__(self, conn_str):
        self.conn_str = conn_str
        self.conn = None
        self.cursor = None
        self.last_error_details = ""

    # --- METODI DI CONNESSIONE ---

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
        if self.cursor: self.cursor.close()
        if self.conn: self.conn.close()

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

    def fetch_active_existing_maintenance_docs(self, equipment_id, intervention_id, doc_type_id):
        """
        Recupera i documenti esistenti e ATTIVI (DateOut IS NULL) per la configurazione data.
        Restituisce i risultati ordinati per data (il più recente per primo).
        """
        # Query fornita dall'utente, con l'aggiunta di AND DateOut IS NULL e DocDescription per il confronto
        query = """
                SELECT [EquipmentDocumentationId], [Filename], DateSys AS DateUpload, Uploadedby, DocDescription
                FROM [Traceability_RS].[eqp].[EquipmentMantainanceDocs]
                WHERE ProgrammedInterventionid = ?
                  AND equipmentid = ?
                  AND Equipmentmaintenancedoctypeid = ?
                  AND DateOut IS NULL -- FONDAMENTALE: Controlla solo i documenti attivi
                ORDER BY DateSys DESC \
                """
        try:
            # L'ordine dei parametri deve corrispondere ai '?' nella query
            self.cursor.execute(query, intervention_id, equipment_id, doc_type_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nella ricerca di documenti esistenti: {e}")
            self.last_error_details = str(e)
            return []

        # NUOVO METODO (Helper privato per l'invalidazione)

    def _invalidate_maintenance_docs(self, doc_ids):
        """
        Imposta DateOut = GETDATE() per una lista di EquipmentDocumentationId.
        (Eseguito all'interno della transazione principale, NON fa commit).
        """
        if not doc_ids:
            return True

        # Crea i placeholders per la clausola IN (?, ?, ...)
        placeholders = ','.join(['?'] * len(doc_ids))
        query = f"""
                   UPDATE [Traceability_RS].[eqp].[EquipmentMantainanceDocs]
                   SET DateOut = GETDATE()
                   WHERE EquipmentDocumentationId IN ({placeholders})
                   """
        try:
            self.cursor.execute(query, doc_ids)
            # Non facciamo commit qui, lo fa la funzione principale
            return True
        except pyodbc.Error as e:
            print(f"Errore nell'invalidazione documenti: {e}")
            self.last_error_details = str(e)
            # Non facciamo rollback qui, lo fa la funzione principale
            return False

    # --- METODI PER MANUTENZIONE (CORRETTI E CONSOLIDATI) ---
    # (Rimosse le definizioni multiple e duplicate presenti nel codice originale)
    def fetch_specific_maintenance_doc_types(self):
        """Recupera i tipi di documento specifici (ID 1, 2, 5)."""
        query = """
                SELECT [EquipmentMaintenanceDocTypeId]
                      ,[DocumentType]
                FROM [Traceability_RS].[eqp].[EquipmentMaintenanceDocTypes]
                WHERE [EquipmentMaintenanceDocTypeId] IN (1,2,5)
                ORDER BY [DocumentType] -- Aggiunto ordinamento per leggibilità
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero dei tipi di documento specifici: {e}")
            return []
    # NUOVO METODO: Recupera gli interventi programmati usando la query fornita dall'utente
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

    # METODO CONSOLIDATO E CORRETTO
    # Parametri aggiornati per il flusso semplificato: EquipmentId e ProgrammedInterventionId (intervention_id).
    def replace_maintenance_document(self, equipment_id, intervention_id, doc_type_id, description, file_name,
                                     file_type, binary_data, user_name, invalidate_ids=None):
        """
        Gestisce l'inserimento del nuovo documento e l'invalidazione dei vecchi in una singola transazione atomica.
        """

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

    def fetch_maintenance_doc_by_id(self, doc_id):
        """Recupera i dettagli completi di un singolo documento di manutenzione tramite il suo ID."""
        # Selezioniamo tutte le colonne (d.*) per avere accesso a tutti gli ID necessari per la sostituzione
        query = """
                SELECT d.*, e.InternalName, p.TimingDescriprion, t.DocumentType
                FROM eqp.EquipmentMantainanceDocs d
                         JOIN eqp.Equipments e ON d.EquipmentId = e.EquipmentId
                         LEFT JOIN eqp.ProgrammedInterventions p \
                                   ON d.ProgrammedInterventionId = p.ProgrammedInterventionId
                         LEFT JOIN eqp.EquipmentMaintenanceDocTypes t \
                                   ON d.EquipmentMaintenanceDocTypeId = t.EquipmentMaintenanceDocTypeId
                WHERE d.EquipmentDocumentationId = ? \
                """
        try:
            self.cursor.execute(query, doc_id)
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            return None

        # NUOVO METODO

    def invalidate_single_maintenance_doc(self, doc_id, user_name):
        """Invalida (cancella logicamente) un singolo documento impostando DateOut."""
        # (user_name è incluso nel caso si volesse aggiungere una colonna InvalidatedBy in futuro)
        query = """
                UPDATE [Traceability_RS].[eqp].[EquipmentMantainanceDocs]
                SET DateOut = GETDATE()
                WHERE EquipmentDocumentationId = ? \
                """
        try:
            self.cursor.execute(query, doc_id)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            return False

    def search_maintenance_documents(self, filters, include_inactive=False):
        """Cerca i documenti di manutenzione. Include JOIN per visualizzare i nomi descrittivi."""
        # Aggiunte JOIN per Intervento e Tipo Doc. Aggiunta DocDescription.
        query = """
                SELECT d.EquipmentDocumentationId, \
                       d.FileName, \
                       d.UploadedBy, \
                       d.DateSys, \
                       d.DocDescription, \
                       d.DateOut,
                       e.InternalName,
                       p.TimingDescriprion AS InterventionName,
                       t.DocumentType
                FROM eqp.EquipmentMantainanceDocs d
                         JOIN eqp.Equipments e ON d.EquipmentId = e.EquipmentId
                         LEFT JOIN eqp.ProgrammedInterventions p \
                                   ON d.ProgrammedInterventionId = p.ProgrammedInterventionId
                         LEFT JOIN eqp.EquipmentMaintenanceDocTypes t \
                                   ON d.EquipmentMaintenanceDocTypeId = t.EquipmentMaintenanceDocTypeId \
                """
        where_clauses = []
        params = []

        # Filtro per stato attivo (DateOut IS NULL)
        if not include_inactive:
            where_clauses.append("d.DateOut IS NULL")

        # Filtri aggiornati per la nuova UI di ricerca
        if filters.get('equipment_id'):
            where_clauses.append("d.EquipmentId = ?")
            params.append(filters['equipment_id'])

        if filters.get('intervention_id'):
            where_clauses.append("d.ProgrammedInterventionId = ?")
            params.append(filters['intervention_id'])

        if filters.get('doc_type_id'):
            where_clauses.append("d.EquipmentMaintenanceDocTypeId = ?")
            params.append(filters['doc_type_id'])

        # (Rimuoviamo i vecchi filtri 'type_id' e 'machine_name' se non più necessari, o li manteniamo se usati altrove)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        query += " ORDER BY e.InternalName, d.DateSys DESC;"
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.last_error_details = str(e)
            print(f"Errore in search_maintenance_documents: {e}")
            return []

    def fetch_maintenance_doc_types(self):
        # NOTA: Questo metodo non è più utilizzato dalla finestra semplificata, ma potrebbe servire per altre funzionalità.
        """
        Recupera i tipi di documento di manutenzione dal database.
        """
        query = """
                SELECT t.EquipmentMaintenanceDocTypeId,
                       t.ProgrammedInterventionId,
                       t.[DocumentType],
                       IIF(IsGeneral = 1, 'General doc', 'Specific doc') as GenerelType,
                       p.TimingDescriprion,
                       p.TimingValue
                FROM eqp.EquipmentMaintenanceDocTypes as t
                         INNER JOIN eqp.ProgrammedInterventions as p
                                    ON t.[ProgrammedInterventionId] = p.[ProgrammedInterventionId]
                ORDER BY [DocumentType], TimingValue;
                """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero dei tipi di documento: {e}")
            return []

    # --- METODI GESTIONE MACCHINE ---

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
        query = "SELECT EquipmentId, InternalName, SerialNumber FROM eqp.Equipments ORDER BY InternalName, SerialNumber;"
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

    # --- METODI DATI DI SUPPORTO (Brand, Tipi, Fasi) ---

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

    def add_new_equipment(self, brand_id, type_id, phase_id, serial_number, internal_name, prod_year, inv_number):
        """Salva una nuova macchina nel database."""
        query = """
                INSERT INTO eqp.Equipments
                (BrandId, EquipmentTypeId, ParentPhaseId, SerialNumber, InternalName, ProductionYear, InventoryNumber,
                 DateSys)
                VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE())
                """
        try:
            self.cursor.execute(query, brand_id, type_id, phase_id, serial_number, internal_name, prod_year, inv_number)
            self.conn.commit()
            return True
        except pyodbc.Error as e:
            self.conn.rollback()
            self.last_error_details = str(e)
            print(f"Errore durante l'inserimento della macchina: {e}")
            return False

    # --- METODI PER TRADUZIONI E AUTENTICAZIONE ---

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

    # --- METODI PER DOCUMENTI DI PRODUZIONE (Non Manutenzione) ---

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
        """Legge un file PDF e lo salva come VARBINARY(MAX) nel database."""
        try:
            # 1. Leggi il file dal tuo computer in modalità binaria ('rb')
            with open(local_file_path, 'rb') as f:
                pdf_binary_data = f.read()

            # 2. Prepara la query di INSERT
            sql_insert = """
                         INSERT INTO Traceability_RS.dbo.ProductDocuments
                         (ProductId, ParentPhaseId, documentName, DocumentRevisionNumber, DocumentData, InsertedBy,
                          InsertionDate, Validated)
                         VALUES (?, ?, ?, ?, ?, ?, GETDATE(), ?)
                         """

            # 3. Esegui la query passando i dati binari come parametro.
            self.cursor.execute(sql_insert,
                                product_id,
                                parent_phase_id,
                                doc_name,
                                revision,
                                pdf_binary_data,  # Dati del file
                                user_name,
                                validated_int)
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

    # --- METODO GESTIONE VERSIONI ---

    def fetch_latest_version(self, software_name):
        """
        Recupera la stringa della versione più recente per un dato software.
        """
        query = "SELECT Version FROM traceability_rs.dbo.SwVersions WHERE NameProgram = ? AND dateout IS NULL"
        try:
            self.cursor.execute(query, software_name)
            row = self.cursor.fetchone()
            return row.Version if row else None
        except pyodbc.Error as e:
            print(f"Errore durante il recupero della versione del software: {e}")
            return None
    # NUOVO METODO: Query 1 - Recupera Piani di Manutenzione Disponibili per una macchina
    def fetch_available_maintenance_plans(self, equipment_id):
        """Recupera i piani di manutenzione non ancora completati per un EquipmentId."""
        # MODIFICATO: Aggiunto pin.ProgrammedInterventionId che è necessario per la Query 2
        query = """
            SELECT DISTINCT pma.PianoManutenzioneId, pin.TimingDescriprion, pin.ProgrammedInterventionId
            FROM Traceability_rs.eqp.equipments AS E
            LEFT JOIN Traceability_rs.eqp.EquipmentTypes et ON e.equipmenttypeid = et.equipmenttypeid
            LEFT JOIN Traceability_rs.[eqp].[EquipmentBrands] eb ON eb.EquipmentBrandId = e.BrandId
            LEFT JOIN Traceability_rs.[eqp].[PianiManutenzioneMacchina] pma ON pma.equipmentid = e.equipmentid
            LEFT JOIN Traceability_rs.[eqp].[ProgrammedInterventions] pin ON pin.[ProgrammedInterventionId] = pma.[ProgrammedInterventionId]
            LEFT JOIN Traceability_rs.eqp.EquipmentMantainanceDocs emd ON emd.ProgrammedInterventionId = pin.ProgrammedInterventionId
            LEFT JOIN Traceability_rs.eqp.CompitiManutenzione CM ON cm.ProgrammedInterventionId = emd.ProgrammedInterventionId
            LEFT JOIN Traceability_rs.eqp.LogManutenzioni LM ON lm.compitoid = cm.compitoid
            WHERE e.equipmentid = ?
              AND (
                  CASE 
                      WHEN pin.TimingValue < 1 THEN 
                          IIF(DATEDIFF(HOUR, lm.DateStop, GETDATE()) > 8, 1, 0)
                      WHEN pin.TimingValue >= 1 THEN
                          CASE WHEN DATEDIFF(DAY, lm.DateStop, GETDATE()) > pin.TimingValue 
                               AND DATEDIFF(DAY, lm.DateStop, GETDATE()) < (
                                   SELECT TOP 1 TimingDescriprion 
                                   FROM [eqp].[ProgrammedInterventions] 
                                   WHERE TimingValue > pin.TimingValue
                                   ORDER BY TimingValue
                               )
                               THEN 1 ELSE 0 END
                      when pin.TimingValue = 0 then 1
                  END = 1
              )
              or lm.logid IS NULL 
            ORDER BY pma.PianoManutenzioneId;
                    """
        try:
            self.cursor.execute(query, equipment_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero piani manutenzione: {e}")
            self.last_error_details = str(e)
            return []

    # NUOVO METODO: Query 2 - Recupera Compiti per un Piano di Manutenzione
    def fetch_maintenance_tasks(self, programmed_intervention_id):
        """Recupera i compiti specifici per un ProgrammedInterventionId non ancora completati."""
        # Query originale fornita dall'utente
        query = """
        select cm.compitoid,  cm.nomecompito, cm.categoria,
            cm.descrizioneCompito,pin.ProgrammedInterventionId
        from Traceability_rs.eqp.equipments as E
        left join Traceability_rs.eqp.EquipmentTypes et on e.equipmenttypeid=et.equipmenttypeid
        left join Traceability_rs.[eqp].[EquipmentBrands]  eb on eb.EquipmentBrandId=e.BrandId
        left join Traceability_rs.[eqp].[PianiManutenzioneMacchina] pma on pma.equipmentid=e.equipmentid
        left join Traceability_rs.[eqp].[ProgrammedInterventions] PIn on pin.[ProgrammedInterventionId]=pma.[ProgrammedInterventionId]
        left join Traceability_rs.eqp.EquipmentMantainanceDocs emd on emd.ProgrammedInterventionId=pin.ProgrammedInterventionId
        left join Traceability_rs.eqp.CompitiManutenzione CM on cm.ProgrammedInterventionId=emd.ProgrammedInterventionId
        -- ATTENZIONE: Assicurati che lo schema per LogManutenzioni sia corretto (eqp o dbo)
        left join Traceability_rs.eqp.LogManutenzioni LM on lm.compitoid=cm.compitoid
        where pin.ProgrammedInterventionId=?
          and lm.logid is null  -- Condizione chiave: compito non ancora loggato
          and cm.compitoid IS NOT NULL -- Assicura che il compito sia valido
        -- Cambiato l'ordine per renderlo più logico (per ID compito)
        order by cm.compitoid;
        """
        try:
            self.cursor.execute(query, programmed_intervention_id)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            print(f"Errore nel recupero compiti manutenzione: {e}")
            self.last_error_details = str(e)
            return []

    # NUOVO METODO: Salva i log dei compiti completati
    def log_completed_tasks(self, equipment_id, user_name, completed_task_ids, start_time, notes=""):
        """Inserisce record in LogManutenzioni per i compiti completati in una transazione batch."""
        if not completed_task_ids:
            return True

        # ATTENZIONE: Modifica questa query se la struttura o lo schema di LogManutenzioni è diverso.
        # Ho assunto lo schema 'eqp'.
        # DataEsecuzione è impostata a GETDATE() (ora del server al momento del salvataggio).
        # StartTime è l'ora passata dalla GUI (quando la scheda è stata caricata).
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

    # NUOVO METODO: Recupera e apre il documento basato su CompitoId
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

# --- CLASSI INTERFACCIA UTENTE (GUI) ---

class LoginWindow(tk.Toplevel):
    """Finestra di autenticazione per l'utente."""

    def __init__(self, master, db_handler, lang_manager):
        super().__init__(master)
        self.db = db_handler
        self.lang = lang_manager
        self.authenticated_user_name = None

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.transient(master)
        self.grab_set()

        self._create_widgets()
        self.update_texts()

        # "Lega" l'evento <Return> (Invio) all'intera finestra.
        self.bind('<Return>', self._attempt_login_event)

    def _create_widgets(self):
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
        """Aggiorna i testi della UI in base alla lingua corrente."""
        self.title(self.lang.get('login_title'))
        self.user_id_label.config(text=self.lang.get('login_user_id'))
        self.password_label.config(text=self.lang.get('login_password'))
        self.login_button.config(text=self.lang.get('login_button'))
        self.cancel_button.config(text=self.lang.get('login_cancel_button'))

    def _attempt_login_event(self, event=None):
        """Funzione chiamata dall'evento 'bind' per poi chiamare la logica di login."""
        self._attempt_login()

    def _attempt_login(self):
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()
        if not user_id or not password:
            messagebox.showerror(self.lang.get('login_title'), self.lang.get('login_error_credentials'), parent=self)
            return

        employee_name = self.db.authenticate_user(user_id, password)
        if employee_name:
            self.authenticated_user_name = employee_name
            self.destroy()
        else:
            messagebox.showerror(self.lang.get('login_title'), self.lang.get('login_auth_failed'), parent=self)
            self.password_entry.delete(0, tk.END)

    def _on_cancel(self):
        self.authenticated_user_name = None
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
                self.docs_listbox.itemconfig(i, {'bg': '#c8e6c9'}) # Verde chiaro per validati

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
            parent_phases = self.db.fetch_parent_phases(product_id)
            if parent_phases:
                self.parent_phases_data = {p.Phase: p.IDParentPhase for p in parent_phases}
                self.parent_phase_combo.config(state="readonly", values=list(self.parent_phases_data.keys()))
            else:
                messagebox.showerror(self.lang.get('app_title'), self.lang.get('error_no_phases_found'), parent=self)

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
             messagebox.showerror(self.lang.get('error_title', "Errore"), "Impossibile aprire il documento.", parent=self)


class App(tk.Tk):
    """Classe principale dell'applicazione."""
    # NUOVO METODO LANCIATORE: Gestisce il requisito di login obbligatorio
    def open_fill_templates_with_login(self):
        """Apre la finestra di compilazione schede, richiedendo prima il login."""
        # Assicurati che LoginWindow sia definita in main.py
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)
        authenticated_user = login_form.authenticated_user_name
        if authenticated_user:
            # Chiama la funzione corretta in maintenance_gui, passando l'utente autenticato
            maintenance_gui.open_fill_templates(self, self.db, self.lang, authenticated_user)


    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        # Inizializza il database e la connessione
        self.db = Database(DB_CONN_STR)
        if not self.db.connect():
            # Mostra l'errore se la connessione fallisce all'avvio
            messagebox.showerror("Database Error", f"Impossibile connettersi al database.\n\nDetails: {self.db.last_error_details}")
            self.destroy()
            return

        # Inizializza il gestore delle lingue
        self.lang = LanguageManager(self.db)

        # 1. Controlla la versione del software
        if self.check_version() is False:
            # Se il controllo fallisce, disconnetti e distruggi la finestra prima di uscire.
            self.db.disconnect()
            self.destroy()
            return  # Interrompe l'inizializzazione

        self.logo_label = None
        self.authenticated_user_for_maintenance = None # Variabile di appoggio per modifiche macchine
        self._create_widgets()
        self._create_menu()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.update_texts()

    # --- METODI DI SUPPORTO ALL'INIZIALIZZAZIONE ---

    def check_version(self):
        """
        Controlla la versione dell'applicazione contro il database.
        Restituisce False se l'aggiornamento è obbligatorio, altrimenti True.
        """
        try:
            # Usa sys.executable, che punta sempre al file .exe in un'app compilata.
            app_name = os.path.basename(sys.executable)

            print(f"Nome eseguibile rilevato: {app_name}")
            latest_version = self.db.fetch_latest_version(app_name)

            # Se non troviamo una versione nel DB, procediamo per non bloccare l'utente
            if latest_version is None:
                print(f"Nessuna versione trovata nel database per '{app_name}'. Controllo saltato.")
                return True

            # Confronta la versione attuale con quella del DB
            if latest_version != APP_VERSION:
                # Le versioni non corrispondono, mostra un errore e blocca l'app
                title = self.lang.get("upgrade_required_title", "Aggiornamento Obbligatorio")
                # Assicurati che il messaggio di traduzione usi {0} e {1} per la formattazione se si usa .format()
                message = self.lang.get("force_upgrade_message", "Versione attuale: {0}. Versione richiesta: {1}. Aggiornare l'applicazione.", APP_VERSION, latest_version)

                messagebox.showerror(title, message)
                return False  # Indica che l'app deve chiudersi

            # Le versioni corrispondono, tutto ok
            print(f"Versione applicazione ({APP_VERSION}) aggiornata.")
            return True

        except Exception as e:
            # In caso di qualsiasi errore, non blocchiamo l'utente
            print(f"Errore imprevisto durante il controllo versione: {e}")
            return True

    def _create_widgets(self):
        if not PIL_AVAILABLE:
            print("Pillow non è installato. Impossibile visualizzare il logo.")
            return
        try:
            # Assicurati che logo.png sia nella stessa directory dell'eseguibile
            image = Image.open("logo.png")
            image.thumbnail((250, 250))
            self.logo_image = ImageTk.PhotoImage(image)
            self.logo_label = ttk.Label(self, image=self.logo_image)
            self.logo_label.pack(pady=20, expand=True)
        except FileNotFoundError:
            print("Errore: logo.png non trovato nella cartella dell'applicazione.")
        except Exception as e:
            print(f"Errore durante il caricamento del logo: {e}")

    # --- GESTIONE MENU E LINGUA ---

    def _create_menu(self):
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # Menu Documenti
        self.document_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(menu=self.document_menu)

        # Menu Manutenzione
        self.maintenance_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(menu=self.maintenance_menu)

        # Menu Help
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(menu=self.help_menu)

        # Sottomenu Lingua
        self.language_menu = tk.Menu(self.help_menu, tearoff=0)
        self.language_menu.add_command(label="Italiano", command=lambda: self._change_language('it'))
        self.language_menu.add_command(label="English", command=lambda: self._change_language('en'))
        self.language_menu.add_command(label="Română", command=lambda: self._change_language('ro'))

    def update_texts(self):
        """Aggiorna tutti i testi della UI principale."""
        self.title(self.lang.get('app_title'))

        # Menu Documenti
        self.document_menu.delete(0, 'end')
        self.document_menu.add_command(label=self.lang.get('menu_insert_doc'), command=self.open_insert_form)
        self.document_menu.add_command(label=self.lang.get('menu_view_doc'), command=self.open_view_form)
        self.document_menu.add_separator()
        self.document_menu.add_command(label=self.lang.get('menu_quit'), command=self._on_closing)

        # Aggiorna le etichette dei menu principali (usando indici 1, 2, 3)
        try:
            self.menubar.entryconfig(1, label=self.lang.get('menu_documents'))
        except tk.TclError:
            pass # Gestione errore se il menu non è ancora pronto

        # Menu Manutenzione
        #self.maintenance_menu.delete(0, 'end')
        #self.maintenance_menu.add_command(label=self.lang.get('submenu_fill_templates'),
        #                           command=self.open_fill_templates_with_login)
        # Sottomenu Gestione Macchine
        machine_submenu = tk.Menu(self.maintenance_menu, tearoff=0)
        machine_submenu.add_command(label=self.lang.get('submenu_add_machine'),
                                    command=self.open_add_machine_with_login)
        machine_submenu.add_command(label=self.lang.get('submenu_edit_machine'),
                                    command=self.open_edit_machine_with_login)
        machine_submenu.add_command(label=self.lang.get('submenu_view_machines'),
                                    command=lambda: maintenance_gui.open_view_machines(self, self.db, self.lang))
        self.maintenance_menu.add_cascade(label=self.lang.get('submenu_machines'), menu=machine_submenu)

        # Sottomenu Documenti Manutenzione
        docs_submenu = tk.Menu(self.maintenance_menu, tearoff=0)
        # Questo apre la finestra semplificata (richiede login)
        docs_submenu.add_command(label=self.lang.get('submenu_add_maint_doc'),
                                 command=self.open_add_maint_doc_with_login)
        docs_submenu.add_command(label=self.lang.get('submenu_edit_maint_doc'),
                                 command=self.open_edit_maint_doc_with_login)
        docs_submenu.add_command(label=self.lang.get('submenu_view_maint_doc'),
                                 command=lambda: maintenance_gui.open_search_maintenance_doc(self, self.db, self.lang,
                                                                                             mode='view'))
        self.maintenance_menu.add_cascade(label=self.lang.get('submenu_maintenance_docs'), menu=docs_submenu)

        # Altre voci
        #self.maintenance_menu.add_command(label=self.lang.get('submenu_fill_templates'),
        #                                  command=lambda: maintenance_gui.open_fill_templates(self, self.db, self.lang))
        self.maintenance_menu.add_command(label=self.lang.get('submenu_fill_templates'),
                                          command=self.open_fill_templates_with_login)
        self.maintenance_menu.add_command(label=self.lang.get('submenu_reports'),
                                          command=lambda: maintenance_gui.open_reports(self, self.db, self.lang))

        try:
            self.menubar.entryconfig(2, label=self.lang.get('menu_maintenance'))
        except tk.TclError:
            pass

        # Menu Help
        self.help_menu.delete(0, 'end')
        self.help_menu.add_cascade(label=self.lang.get('menu_language'), menu=self.language_menu)
        about_menu_label = f"{self.lang.get('menu_about')} {APP_VERSION}"
        self.help_menu.add_command(label=about_menu_label, command=self._show_about)

        try:
            self.menubar.entryconfig(3, label=self.lang.get('menu_help'))
        except tk.TclError:
            pass

    def _change_language(self, lang_code):
        """Cambia la lingua e aggiorna la UI."""
        self.lang.set_language(lang_code)
        self.update_texts()


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

    # Lanciatori Documenti Produzione
    def open_insert_form(self):
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)
        authenticated_user = login_form.authenticated_user_name
        if authenticated_user:
            insert_form = InsertDocumentForm(self, self.db, authenticated_user, self.lang)
            insert_form.transient(self)
            insert_form.grab_set()
            self.wait_window(insert_form)

    def open_view_form(self):
        view_form = ViewDocumentForm(self, self.db, self.lang)
        view_form.transient(self)
        view_form.grab_set()
        self.wait_window(view_form)

    # Lanciatori Manutenzione (con Login Obbligatorio dove richiesto)
    def open_add_maint_doc_with_login(self):
        # Questo garantisce il requisito di login per l'inserimento documenti importanti.
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)
        authenticated_user = login_form.authenticated_user_name
        if authenticated_user:
            # Chiama la funzione nel modulo maintenance_gui.py (che aprirà la finestra semplificata)
            maintenance_gui.open_add_maintenance_doc(self, self.db, self.lang, authenticated_user)

    def open_edit_maint_doc_with_login(self):
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)
        authenticated_user = login_form.authenticated_user_name
        if authenticated_user:
            # La finestra di ricerca gestirà il resto
            maintenance_gui.open_search_maintenance_doc(self, self.db, self.lang, mode='edit',
                                                        user_name=authenticated_user)

    def open_add_machine_with_login(self):
        """Apre la finestra di login e, se l'autenticazione ha successo, apre la finestra per aggiungere una macchina."""
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)
        authenticated_user = login_form.authenticated_user_name
        if authenticated_user:
            maintenance_gui.open_add_machine(self, self.db, self.lang)

    def open_edit_machine_with_login(self):
        """Apre la finestra di login e, se l'autenticazione ha successo, apre la finestra per modificare una macchina."""
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)
        authenticated_user = login_form.authenticated_user_name
        if authenticated_user:
            # Salva temporaneamente l'utente per passarlo alla finestra di modifica tramite maintenance_gui
            self.authenticated_user_for_maintenance = authenticated_user
            maintenance_gui.open_edit_machine(self, self.db, self.lang)



    def open_fill_templates_with_login(self):
        """Apre la finestra di compilazione schede, richiedendo prima il login."""
        # Assicurati che LoginWindow sia definita in main.py
        # 1. Mostra la finestra di Login (LoginWindow deve essere definita in main.py)
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)

        # 2. Recupera il nome utente se l'autenticazione ha successo
        authenticated_user = login_form.authenticated_user_name

        # 3. Se autenticato, apri la finestra di compilazione passando il nome utente
        if authenticated_user:
            # Chiama la funzione corretta in maintenance_gui, passando l'utente autenticato
            maintenance_gui.open_fill_templates(self, self.db, self.lang, authenticated_user)

    def _on_closing(self):
        if messagebox.askokcancel(self.lang.get('quit_title', "Quit"), self.lang.get('quit_message', "Do you want to quit?")):
            self.db.disconnect()
            self.destroy()

if __name__ == "__main__":
    app = App()
    # Esegui il mainloop solo se la finestra esiste (cioè se la connessione DB e il check versione sono riusciti)
    if app.winfo_exists():
        app.mainloop()