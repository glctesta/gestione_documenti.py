from datetime import datetime
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
from packaging import version
import tools_gui
import submissions_gui
import general_docs_gui
import permissions_gui
import materials_gui

try:
    from PIL import Image, ImageTk

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# --- CONFIGURAZIONE APPLICAZIONE ---
APP_VERSION = "1.6.1"  # Versione aggiornata
APP_DEVELOPER = "Gianluca Testa"

# --- CONFIGURAZIONE DATABASE ---
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
            self.last_error_details = str(e); return None

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
            self.last_error_details = str(e); return []

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
            self.last_error_details = str(e); return []

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
                  AND a.DateOut IS NULL; \
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
                ORDER BY a.TranslationKey; \
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
                  AND u.Pass = ?; \
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

    def add_new_brand(self, company_id, brand_name, logo_data):
        """Aggiunge un nuovo brand dopo aver controllato che non esista già."""
        check_query = "SELECT COUNT(*) FROM eqp.EquipmentBrands WHERE Brand = ?;"
        insert_query = "INSERT INTO eqp.EquipmentBrands (CompanyId, Brand, BrandLogo) VALUES (?, ?, ?);"
        try:
            count = self.cursor.execute(check_query, brand_name).fetchval()
            if count > 0:
                return False, "Errore: Esiste già un brand con questo nome."

            self.cursor.execute(insert_query, company_id, brand_name, logo_data)
            self.conn.commit()
            return True, "Brand aggiunto con successo."
        except pyodbc.Error as e:
            self.conn.rollback()
            return False, f"Errore database: {e}"

    def update_brand(self, brand_id, company_id, brand_name, logo_data):
        """Aggiorna un brand esistente."""
        query = """
                UPDATE eqp.EquipmentBrands
                SET CompanyId = ?, \
                    Brand     = ?, \
                    BrandLogo = ?
                WHERE EquipmentBrandId = ?; \
                """
        try:
            self.cursor.execute(query, company_id, brand_name, logo_data, brand_id)
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

    # --- METODO GESTIONE VERSIONI ---

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


    # NUOVO METODO: Query 1 - Recupera Piani di Manutenzione Disponibili per una macchina
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

    # NUOVO METODO: Query 2 - Recupera Compiti per un Piano di Manutenzione
    # In main.py, dentro la classe Database

    # In main.py, dentro la classe Database

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

# --- CLASSI INTERFACCIA UTENTE (GUI) ---

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
             messagebox.showerror(self.lang.get('error_title', "Errore"), "Impossibile aprire il documento.", parent=self)


class App(tk.Tk):
    """Classe principale dell'applicazione."""

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
            action_callback=lambda user_name: maintenance_gui.open_add_maintenance_tasks(self, self.db, self.lang, user_name)
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

    def _execute_simple_login(self, action_callback):
        """
        Gestisce il processo di login semplice per le funzioni non ristrette.
        :param action_callback: La funzione da eseguire in caso di successo.
                                Riceverà il nome dell'utente come argomento.
        """
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)

        if not login_form.clicked_login:
            return

        user_id = login_form.user_id
        password = login_form.password

        # Esegue l'autenticazione standard
        employee_name = self.db.authenticate_user(user_id, password)

        if employee_name:
            # Successo: esegue l'azione richiesta passando il nome utente
            action_callback(employee_name)
        else:
            # Fallimento: mostra l'errore
            messagebox.showerror(self.lang.get('login_title'), self.lang.get('login_auth_failed'), parent=self)

    def _execute_authorized_action(self, menu_translation_key, action_callback):
        """
        Gestisce il processo di login e autorizzazione per un'azione.
        :param menu_translation_key: La chiave di traduzione del menu per il controllo permessi.
        :param action_callback: La funzione da eseguire in caso di successo.
        """
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)

        # Procede solo se l'utente ha premuto "Login"
        if not login_form.clicked_login:
            return

        user_id = login_form.user_id
        password = login_form.password

        # Controlla autenticazione e autorizzazione
        auth_result = self.db.authenticate_and_authorize(user_id, password, menu_translation_key)

        if auth_result is None:
            # Caso 1: Username o Password errati
            messagebox.showerror(self.lang.get('login_title'), self.lang.get('login_auth_failed'), parent=self)
        elif auth_result.AuthorizedUsedId is None:
            # Caso 2: Utente valido, ma NON autorizzato per questa funzione
            messagebox.showwarning(self.lang.get('auth_access_denied_title', "Accesso Negato"),
                                   self.lang.get('auth_access_denied_message',
                                                 "Non si dispone delle autorizzazioni necessarie per accedere a questa funzione."),
                                   parent=self)
        else:
            # Caso 3: Successo! Esegue l'azione
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
        self.should_exit = False  # Flag to control shutdown
        self.geometry("800x600")

        # Inizializza il database
        self.db = Database(DB_CONN_STR)
        if not self.db.connect():
            messagebox.showerror("Database Error",
                                 f"Impossibile connettersi al database.\n\nDetails: {self.db.last_error_details}")
            self.destroy()
            self.should_exit = True
            return

        # Carica la lingua salvata
        initial_lang = self._load_language_setting()
        self.lang = LanguageManager(self.db)
        self.lang.set_language(initial_lang)
        self.doc_categories = self.db.fetch_doc_categories()

        # Controlla la versione (e se l'app deve chiudersi)
        if self.check_version() is False:
            # check_version already handles shutdown, we just need to stop __init__
            return

        self.logo_label = None
        self.authenticated_user_for_maintenance = None
        self._create_widgets()
        self._create_menu()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.update_texts()
        self._update_clock()  # Avvia l'orologio

    # --- METODI DI SUPPORTO ALL'INIZIALIZZAZIONE ---

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
        # --- Barra Superiore per l'Orologio ---
        header_frame = ttk.Frame(self)
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(5, 0))

        self.clock_label = ttk.Label(header_frame, font=("Helvetica", 9))
        self.clock_label.pack(side=tk.RIGHT)  # Allinea l'orologio a destra

        # --- Logo Centrale (invariato) ---
        if not PIL_AVAILABLE:
            print("Pillow non è installato. Impossibile visualizzare il logo.")
            return
        try:
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

    # In main.py, inside the App class

    def _create_menu(self):
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # Crea i contenitori vuoti per ogni menu
        self.document_menu = tk.Menu(self.menubar, tearoff=0)
        self.general_docs_menu = tk.Menu(self.menubar, tearoff=0)
        self.maintenance_menu = tk.Menu(self.menubar, tearoff=0)
        self.submissions_menu = tk.Menu(self.menubar, tearoff=0)  # Menu Segnalazioni
        self.tools_menu = tk.Menu(self.menubar, tearoff=0)  # Menu Strumenti
        self.permissions_submenu = tk.Menu(self.tools_menu, tearoff=0)
        # --- Aggiungi questo sottomenu ---
        self.materials_submenu = tk.Menu(self.tools_menu, tearoff=0)
        self.help_menu = tk.Menu(self.menubar, tearoff=0)

        # Aggiunge ogni menu come una "cascata" separata alla barra principale
        self.menubar.add_cascade(menu=self.document_menu)
        self.menubar.add_cascade(menu=self.general_docs_menu)
        self.menubar.add_cascade(menu=self.maintenance_menu)
        self.menubar.add_cascade(menu=self.submissions_menu)
        self.menubar.add_cascade(menu=self.tools_menu)
        self.menubar.add_cascade(menu=self.help_menu)

        # Il sottomenu della lingua è un caso speciale, perché è una cascata DENTRO il menu Aiuto
        self.language_menu = tk.Menu(self.help_menu, tearoff=0)
        self.language_menu.add_command(label="Italiano", command=lambda: self._change_language('it'))
        self.language_menu.add_command(label="English", command=lambda: self._change_language('en'))
        self.language_menu.add_command(label="Română", command=lambda: self._change_language('ro'))
        self.language_menu.add_command(label="Deutsch", command=lambda: self._change_language('de'))
        self.language_menu.add_command(label="Svenska", command=lambda: self._change_language('sv'))
    # In main.py, dentro la classe App

    # In main.py, dentro la classe App

    def update_texts(self):
        """Aggiorna tutti i testi della UI principale, ricostruendo tutti i menu."""
        self.title(self.lang.get('app_title'))

        # 1. Menu Documenti (Produzione)
        self.document_menu.delete(0, 'end')
        self.document_menu.add_command(label=self.lang.get('menu_insert_doc'), command=self.open_insert_form)
        self.document_menu.add_command(label=self.lang.get('menu_view_doc'), command=self.open_view_form)
        self.document_menu.add_separator()
        self.document_menu.add_command(label=self.lang.get('menu_quit'), command=self._on_closing)

        # 2. Menu Documenti Generali (costruito dinamicamente)
        self.general_docs_menu.delete(0, 'end')
        if self.doc_categories:
            for category in self.doc_categories:
                category_submenu = tk.Menu(self.general_docs_menu, tearoff=0)
                category_name = self.lang.get(category.TranslationKey, category.NomeCategoria)
                self.general_docs_menu.add_cascade(label=category_name, menu=category_submenu)

                cmd_edit = lambda cid=category.CategoriaId, cname=category_name: \
                    self._open_general_docs_viewer_with_login(cid, cname)
                category_submenu.add_command(label=self.lang.get('submenu_add_edit', "Aggiungi/Modifica"),
                                             command=cmd_edit)

                cmd_view = lambda cid=category.CategoriaId, cname=category_name: \
                    self._open_general_docs_viewer(cid, cname)
                category_submenu.add_command(label=self.lang.get('submenu_view', "Visualizza"), command=cmd_view)

        # 3. Menu Manutenzione (con ricostruzione dei sottomenu)
        self.maintenance_menu.delete(0, 'end')

        # Ricrea Sottomenu Gestione Macchine
        machine_submenu = tk.Menu(self.maintenance_menu, tearoff=0)
        machine_submenu.add_command(label=self.lang.get('submenu_add_machine'),
                                    command=self.open_add_machine_with_login)
        machine_submenu.add_command(label=self.lang.get('submenu_edit_machine'),
                                    command=self.open_edit_machine_with_login)
        machine_submenu.add_command(label=self.lang.get('submenu_view_machines'),
                                    command=lambda: maintenance_gui.open_view_machines(self, self.db, self.lang))
        self.maintenance_menu.add_cascade(label=self.lang.get('submenu_machines'), menu=machine_submenu)

        # Ricrea Sottomenu Task di Manutenzione
        tasks_submenu = tk.Menu(self.maintenance_menu, tearoff=0)
        tasks_submenu.add_command(
            label=self.lang.get('submenu_manage_maint_task', "Gestione Task di Manutenzione"),
            command=self.open_add_maintenance_tasks_with_login
        )
        self.maintenance_menu.add_cascade(
            label=self.lang.get('submenu_maintenance_tasks_header', 'Task di Manutenzione'),
            menu=tasks_submenu
        )
        # Ricrea le altre voci del menu Manutenzione
        self.maintenance_menu.add_command(label=self.lang.get('submenu_fill_templates'),
                                          command=self.open_fill_templates_with_login)
        self.maintenance_menu.add_command(label=self.lang.get('submenu_reports'),
                                          command=lambda: maintenance_gui.open_reports(self, self.db, self.lang))

        # 4. Menu Segnalazioni
        self.submissions_menu.delete(0, 'end')
        self.submissions_menu.add_command(label=self.lang.get('submenu_new_submission', "Nuova Segnalazione"),
                                          command=self.open_new_submission_form)
        self.submissions_menu.add_command(label=self.lang.get('submenu_view_submissions', "Visualizza Segnalazioni"),
                                          state="disabled")

        # 5. Menu Strumenti
        self.tools_menu.delete(0, 'end')

        # Sottomenu Autorizzazioni
        self.permissions_submenu = tk.Menu(self.tools_menu, tearoff=0)
        self.tools_menu.add_cascade(label=self.lang.get('submenu_permissions', "Autorizzazioni"),
                                    menu=self.permissions_submenu)
        self.permissions_submenu.delete(0, 'end')
        self.permissions_submenu.add_command(
            label=self.lang.get('submenu_special_permissions', "Autorizzazioni Speciali"),
            command=self.open_manage_permissions_with_login)
        self.permissions_submenu.add_command(label=self.lang.get('submenu_data_entry', "Inserimento Dati"),
                                             state="disabled")
        self.permissions_submenu.add_command(label=self.lang.get('submenu_program_use', "Utilizzo Programma"),
                                             state="disabled")
        self.permissions_submenu.add_command(
            label=self.lang.get('submenu_view_permissions', "Visualizza Autorizzazioni"),
            command=self.open_view_permissions_with_login)
        self.tools_menu.add_separator()

        # Altre voci del menu Strumenti
        self.tools_menu.add_command(label=self.lang.get('submenu_suppliers', "Produttori"),
                                    command=self.open_suppliers_manager_with_login)
        self.tools_menu.add_command(label=self.lang.get('submenu_brands', "Brand"),
                                    command=self.open_brands_manager_with_login)
        self.tools_menu.add_command(label=self.lang.get('submenu_maint_cycles', "Cicli Manutenzione"),
                                    command=self.open_maint_cycles_manager_with_login)
        self.tools_menu.add_command(label=self.lang.get('submenu_doc_types', "Aggiungi Tipo Documento"),
                                    command=self.open_doc_types_manager_with_login)
        self.tools_menu.add_cascade(label=self.lang.get('menu_materials', "Materiali"), menu=self.materials_submenu)
        self.materials_submenu.delete(0, 'end')
        self.materials_submenu.add_command(label=self.lang.get('submenu_manage', "Gestione"),
                                           command=self.open_manage_materials_with_login)
        self.materials_submenu.add_command(label=self.lang.get('submenu_view', "Visualizza"),
                                           command=self.open_view_materials)

        # 6. Menu Help
        self.help_menu.delete(0, 'end')
        self.help_menu.add_cascade(label=self.lang.get('menu_language'), menu=self.language_menu)
        about_menu_label = f"{self.lang.get('menu_about')} {APP_VERSION}"
        self.help_menu.add_command(label=about_menu_label, command=self._show_about)

        # Aggiorna le etichette dei menu principali
        try:
            self.menubar.entryconfig(1, label=self.lang.get('menu_documents', "Documenti di Produzione"))
            self.menubar.entryconfig(2, label=self.lang.get('menu_general_docs', "Documenti Generali"))
            self.menubar.entryconfig(3, label=self.lang.get('menu_maintenance'))
            self.menubar.entryconfig(4, label=self.lang.get('menu_submissions', "Segnalazioni"))
            self.menubar.entryconfig(5, label=self.lang.get('menu_tools', "Strumenti"))
            self.menubar.entryconfig(6, label=self.lang.get('menu_help'))
        except tk.TclError:
            pass

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

    # Lanciatori Documenti Produzione
    def open_add_machine_with_login(self):
        self._execute_simple_login(
            action_callback=lambda user_name: maintenance_gui.open_add_machine(self, self.db, self.lang)
        )

    def open_manage_materials_with_login(self):
        self._execute_simple_login(
            action_callback=lambda user_name: materials_gui.open_manage_materials(self, self.db, self.lang, user_name)
        )

    def open_view_materials(self):
        """Apre la finestra di visualizzazione materiali (senza login)."""
        # Passiamo 'None' come user_name perché non c'è autenticazione
        materials_gui.open_view_materials(self, self.db, self.lang, user_name=None)

    def open_add_machine_with_login(self):
        """Apre la finestra di login e, se l'autenticazione ha successo, apre la finestra per aggiungere una macchina."""
        login_form = LoginWindow(self, self.db, self.lang)
        self.wait_window(login_form)
        authenticated_user = login_form.authenticated_user_name
        if authenticated_user:
            maintenance_gui.open_add_machine(self, self.db, self.lang)

    def open_edit_machine_with_login(self):
        def action(user_name):
            self.authenticated_user_for_maintenance = user_name
            maintenance_gui.open_edit_machine(self, self.db, self.lang)

        self._execute_simple_login(action_callback=action)

    def open_fill_templates_with_login(self):
        self._execute_simple_login(
            action_callback=lambda user_name: maintenance_gui.open_fill_templates(self, self.db, self.lang, user_name)
        )

    def _on_closing(self):
        if messagebox.askokcancel(self.lang.get('quit_title', "Quit"), self.lang.get('quit_message', "Do you want to quit?")):
            self.db.disconnect()
            self.destroy()

if __name__ == "__main__":
    app = App()
    if not app.should_exit:
        app.mainloop()