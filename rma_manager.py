# File: rma_manager.py
# Backend per la gestione RMA Knowledge Base
# Database: Traceability_RS

import logging
import pyodbc
from datetime import datetime

logger = logging.getLogger(__name__)


class RmaManager:
    """
    Gestisce le operazioni CRUD per il sistema RMA Knowledge Base.
    Utilizza la connessione pyodbc esistente della classe Database.
    """

    def __init__(self, db):
        """
        Args:
            db: istanza Database (main.py) con attributi conn, cursor, conn_str
        """
        self.db = db
        self._ensure_tables()

    # ==========================================================================
    # Schema bootstrap
    # ==========================================================================
    def _ensure_tables(self):
        """Verifica che le tabelle RMA esistano. Se non esistono, le crea."""
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'RmaRecords'
            """)
            if cur.fetchone()[0] == 0:
                logger.warning("Tabelle RMA non trovate. Eseguire sql/rma_schema.sql prima.")
            else:
                logger.info("RmaManager: tabelle RMA verificate.")
            cur.close()
        except Exception as e:
            logger.error(f"RmaManager._ensure_tables: {e}")

    # ==========================================================================
    # Lookup: Tipi guasto
    # ==========================================================================
    def get_fault_types(self):
        """Ritorna lista di (RmaFaultTypeId, Code, Description) attivi."""
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT RmaFaultTypeId, Code, [Description]
                FROM Traceability_RS.dbo.RmaFaultTypes
                WHERE DateOut IS NULL
                ORDER BY [Description]
            """)
            rows = cur.fetchall()
            cur.close()
            return rows
        except Exception as e:
            logger.error(f"get_fault_types: {e}")
            return []

    def get_fault_details(self, fault_type_id=None):
        """Ritorna dettagli guasto, opzionalmente filtrati per tipo."""
        try:
            cur = self.db.conn.cursor()
            if fault_type_id:
                cur.execute("""
                    SELECT RmaFaultDetailId, RmaFaultTypeId, Code, [Description]
                    FROM Traceability_RS.dbo.RmaFaultDetails
                    WHERE DateOut IS NULL AND RmaFaultTypeId = ?
                    ORDER BY [Description]
                """, fault_type_id)
            else:
                cur.execute("""
                    SELECT RmaFaultDetailId, RmaFaultTypeId, Code, [Description]
                    FROM Traceability_RS.dbo.RmaFaultDetails
                    WHERE DateOut IS NULL
                    ORDER BY [Description]
                """)
            rows = cur.fetchall()
            cur.close()
            return rows
        except Exception as e:
            logger.error(f"get_fault_details: {e}")
            return []

    # ==========================================================================
    # Lookup: Siti produzione
    # ==========================================================================
    def get_production_sites(self):
        """Ritorna lista di (RmaProductionSiteId, Name) attivi."""
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT RmaProductionSiteId, [Name]
                FROM Traceability_RS.dbo.RmaProductionSites
                WHERE DateOut IS NULL
                ORDER BY [Name]
            """)
            rows = cur.fetchall()
            cur.close()
            return rows
        except Exception as e:
            logger.error(f"get_production_sites: {e}")
            return []

    # ==========================================================================
    # Lookup: Valori distinti per combobox
    # ==========================================================================
    def get_distinct_part_codes(self):
        """Ritorna lista di codici parte unici."""
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT DISTINCT PartCode
                FROM Traceability_RS.dbo.RmaRecords
                WHERE PartCode IS NOT NULL AND PartCode <> '' AND DateOut IS NULL
                ORDER BY PartCode
            """)
            rows = [r.PartCode for r in cur.fetchall()]
            cur.close()
            return rows
        except Exception as e:
            logger.error(f"get_distinct_part_codes: {e}")
            return []

    def get_distinct_customers(self):
        """Ritorna lista di clienti unici."""
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT DISTINCT CustomerName
                FROM Traceability_RS.dbo.RmaRecords
                WHERE CustomerName IS NOT NULL AND CustomerName <> '' AND DateOut IS NULL
                ORDER BY CustomerName
            """)
            rows = [r.CustomerName for r in cur.fetchall()]
            cur.close()
            return rows
        except Exception as e:
            logger.error(f"get_distinct_customers: {e}")
            return []

    def get_distinct_references(self):
        """Ritorna lista di riferimenti circuitali unici."""
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT DISTINCT Reference
                FROM Traceability_RS.dbo.RmaRecords
                WHERE Reference IS NOT NULL AND Reference <> '' AND DateOut IS NULL
                ORDER BY Reference
            """)
            rows = [r.Reference for r in cur.fetchall()]
            cur.close()
            return rows
        except Exception as e:
            logger.error(f"get_distinct_references: {e}")
            return []

    def get_distinct_assemblies(self):
        """Ritorna lista di assembly unici (per autocomplete)."""
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT DISTINCT Assembly
                FROM Traceability_RS.dbo.RmaRecords
                WHERE Assembly IS NOT NULL AND Assembly <> '' AND DateOut IS NULL
                ORDER BY Assembly
            """)
            rows = [r.Assembly for r in cur.fetchall()]
            cur.close()
            return rows
        except Exception as e:
            logger.error(f"get_distinct_assemblies: {e}")
            return []

    # ==========================================================================
    # Conteggio totale
    # ==========================================================================
    def get_total_count(self):
        """Ritorna il numero totale di record RMA attivi."""
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT COUNT(*)
                FROM Traceability_RS.dbo.RmaRecords
                WHERE DateOut IS NULL
            """)
            count = cur.fetchone()[0]
            cur.close()
            return count
        except Exception as e:
            logger.error(f"get_total_count: {e}")
            return 0

    # ==========================================================================
    # Ricerca record
    # ==========================================================================
    def search_records(self, filters):
        """
        Ricerca record RMA con filtri combinabili (AND).

        Args:
            filters: dict con chiavi opzionali:
                - serial_number: str (LIKE parziale)
                - part_code: str (esatto)
                - fault_text: str (LIKE su FaultDescription + FaultNotes)
                - fault_type_id: int
                - fault_detail_id: int
                - reference: str (esatto)
                - customer: str (esatto)
                - date_from: datetime
                - date_to: datetime

        Returns:
            list of pyodbc.Row
        """
        try:
            cur = self.db.conn.cursor()
            conditions = ["r.DateOut IS NULL"]
            params = []

            if filters.get('serial_number'):
                conditions.append("r.SerialNumber LIKE ?")
                params.append(f"%{filters['serial_number']}%")

            if filters.get('part_code'):
                conditions.append("r.PartCode = ?")
                params.append(filters['part_code'])

            if filters.get('fault_text'):
                conditions.append(
                    "(r.FaultDescription LIKE ? OR r.FaultNotes LIKE ?)"
                )
                text_param = f"%{filters['fault_text']}%"
                params.extend([text_param, text_param])

            if filters.get('fault_type_id'):
                conditions.append("r.RmaFaultTypeId = ?")
                params.append(filters['fault_type_id'])

            if filters.get('fault_detail_id'):
                conditions.append("r.RmaFaultDetailId = ?")
                params.append(filters['fault_detail_id'])

            if filters.get('reference'):
                conditions.append("r.Reference = ?")
                params.append(filters['reference'])

            if filters.get('customer'):
                conditions.append("r.CustomerName = ?")
                params.append(filters['customer'])

            if filters.get('date_from'):
                conditions.append("r.OrderDate >= ?")
                params.append(filters['date_from'])

            if filters.get('date_to'):
                conditions.append("r.OrderDate <= ?")
                params.append(filters['date_to'])

            where_clause = " AND ".join(conditions)

            query = f"""
                SELECT TOP 500
                    r.RmaRecordId,
                    r.SerialNumber,
                    r.PartCode,
                    r.PartDescription,
                    r.RmaNumber,
                    r.CustomerName,
                    r.FaultDescription,
                    ISNULL(ft.[Description], '') AS FaultType,
                    ISNULL(fd.[Description], '') AS FaultDetail,
                    r.Reference,
                    r.Assembly,
                    r.FaultNotes,
                    r.CorrectiveAction,
                    r.FaultCauseCode,
                    r.FaultCause,
                    r.ProductionWeek,
                    ISNULL(ps.[Name], '') AS ProductionSite,
                    r.ProcessResponsible,
                    r.WarrantyType,
                    r.Origin,
                    r.RepairTimeMinutes,
                    r.Cost,
                    r.AlreadyRepaired,
                    r.Operator,
                    r.TestType,
                    FORMAT(r.OrderDate, 'dd/MM/yyyy') AS OrderDateFmt,
                    FORMAT(r.DeliveryDate, 'dd/MM/yyyy') AS DeliveryDateFmt,
                    FORMAT(r.CloseDate, 'dd/MM/yyyy') AS CloseDateFmt,
                    r.PhotoPath,
                    r.DocumentLinks,
                    r.IDLabelCode,
                    r.IDOrder,
                    r.ProductCode,
                    r.[Source]
                FROM Traceability_RS.dbo.RmaRecords r
                LEFT JOIN Traceability_RS.dbo.RmaFaultTypes ft
                    ON ft.RmaFaultTypeId = r.RmaFaultTypeId
                LEFT JOIN Traceability_RS.dbo.RmaFaultDetails fd
                    ON fd.RmaFaultDetailId = r.RmaFaultDetailId
                LEFT JOIN Traceability_RS.dbo.RmaProductionSites ps
                    ON ps.RmaProductionSiteId = r.RmaProductionSiteId
                WHERE {where_clause}
                ORDER BY r.OrderDate DESC, r.RmaRecordId DESC
            """

            cur.execute(query, *params)
            rows = cur.fetchall()
            cur.close()
            return rows
        except Exception as e:
            logger.error(f"search_records: {e}", exc_info=True)
            return []

    # ==========================================================================
    # Dettaglio singolo record
    # ==========================================================================
    def get_record_by_id(self, rma_record_id):
        """Recupera un record RMA per ID completo."""
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT 
                    r.*,
                    ISNULL(ft.[Description], '') AS FaultTypeName,
                    ISNULL(fd.[Description], '') AS FaultDetailName,
                    ISNULL(ps.[Name], '') AS ProductionSiteName
                FROM Traceability_RS.dbo.RmaRecords r
                LEFT JOIN Traceability_RS.dbo.RmaFaultTypes ft
                    ON ft.RmaFaultTypeId = r.RmaFaultTypeId
                LEFT JOIN Traceability_RS.dbo.RmaFaultDetails fd
                    ON fd.RmaFaultDetailId = r.RmaFaultDetailId
                LEFT JOIN Traceability_RS.dbo.RmaProductionSites ps
                    ON ps.RmaProductionSiteId = r.RmaProductionSiteId
                WHERE r.RmaRecordId = ?
            """, rma_record_id)
            row = cur.fetchone()
            cur.close()
            return row
        except Exception as e:
            logger.error(f"get_record_by_id: {e}")
            return None

    # ==========================================================================
    # Inserimento nuovo record
    # ==========================================================================
    def insert_record(self, data):
        """
        Inserisce un nuovo record RMA.

        Args:
            data: dict con le chiavi corrispondenti alle colonne.

        Returns:
            int: RmaRecordId del nuovo record, oppure None in caso di errore.
        """
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                INSERT INTO Traceability_RS.dbo.RmaRecords (
                    SerialNumber, PartCode, CustomerPartCode, PartDescription,
                    RmaNumber, CustomerId, CustomerName,
                    FaultDescription, FaultCauseCode, FaultCause,
                    RmaFaultTypeId, RmaFaultDetailId,
                    Reference, Assembly, FaultNotes, CorrectiveAction,
                    ProductionWeek, RmaProductionSiteId, ProcessResponsible,
                    WarrantyType, Origin, RepairTimeMinutes, Cost, AlreadyRepaired,
                    Operator, TestType,
                    OrderDate, DeliveryDate, CloseDate, TestDate,
                    PhotoPath, DocumentLinks,
                    IDLabelCode, IDOrder, ProductCode,
                    InsertedBy, InsertedAt, [Source]
                )
                OUTPUT INSERTED.RmaRecordId
                VALUES (
                    ?, ?, ?, ?,
                    ?, ?, ?,
                    ?, ?, ?,
                    ?, ?,
                    ?, ?, ?, ?,
                    ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?,
                    ?, ?, ?, ?,
                    ?, ?,
                    ?, ?, ?,
                    ?, GETDATE(), ?
                )
            """,
                data.get('serial_number'),
                data.get('part_code'),
                data.get('customer_part_code'),
                data.get('part_description'),
                data.get('rma_number'),
                data.get('customer_id'),
                data.get('customer_name'),
                data.get('fault_description'),
                data.get('fault_cause_code'),
                data.get('fault_cause'),
                data.get('fault_type_id'),
                data.get('fault_detail_id'),
                data.get('reference'),
                data.get('assembly'),
                data.get('fault_notes'),
                data.get('corrective_action'),
                data.get('production_week'),
                data.get('production_site_id'),
                data.get('process_responsible'),
                data.get('warranty_type'),
                data.get('origin'),
                data.get('repair_time_minutes'),
                data.get('cost'),
                data.get('already_repaired'),
                data.get('operator'),
                data.get('test_type'),
                data.get('order_date'),
                data.get('delivery_date'),
                data.get('close_date'),
                data.get('test_date'),
                data.get('photo_path'),
                data.get('document_links'),
                data.get('id_label_code'),
                data.get('id_order'),
                data.get('product_code'),
                data.get('inserted_by', 'MANUAL'),
                data.get('source', 'MANUAL')
            )
            row = cur.fetchone()
            self.db.conn.commit()
            new_id = row[0] if row else None
            cur.close()
            logger.info(f"RMA record inserito: ID={new_id}, SN={data.get('serial_number')}")
            return new_id
        except Exception as e:
            logger.error(f"insert_record: {e}", exc_info=True)
            try:
                self.db.conn.rollback()
            except:
                pass
            return None

    # ==========================================================================
    # Lookup tracciabilità: da serial number a ordine/prodotto
    # ==========================================================================
    def lookup_traceability(self, label_code):
        """
        Dato un codice etichetta (serial number / label code), risale
        a ordine e prodotto usando le tabelle Traceability_RS.

        Riusa la stessa logica di get_scrap_label_info.

        Returns:
            dict con chiavi: id_label_code, id_board, order_number,
                             order_date, product_code  oppure None
        """
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT 
                    l.IDLabelCode,
                    b.IDBoard,
                    o.OrderNumber,
                    FORMAT(o.OrderDate, 'dd/MM/yyyy') AS OrderDate,
                    o.OrderQuantity,
                    p.ProductCode,
                    o.IDOrder
                FROM Traceability_RS.dbo.LabelCodes L
                INNER JOIN Traceability_RS.dbo.Boards b ON b.IDBoard = l.IDBoard
                INNER JOIN Traceability_RS.dbo.Orders o ON o.IDOrder = b.IDOrder
                INNER JOIN Traceability_RS.dbo.Products p ON p.IDProduct = o.IDProduct
                WHERE l.LabelCod = ?
            """, label_code)
            row = cur.fetchone()
            cur.close()

            if row:
                return {
                    'id_label_code': row.IDLabelCode,
                    'id_board': row.IDBoard,
                    'order_number': row.OrderNumber,
                    'order_date': row.OrderDate,
                    'order_quantity': row.OrderQuantity,
                    'product_code': row.ProductCode,
                    'id_order': row.IDOrder
                }
            return None
        except Exception as e:
            logger.error(f"lookup_traceability: {e}", exc_info=True)
            return None

    # ==========================================================================
    # Statistiche per il pannello
    # ==========================================================================
    def get_statistics(self):
        """Ritorna statistiche generali per il dashboard."""
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT 
                    COUNT(*) AS total,
                    COUNT(CASE WHEN FaultNotes IS NOT NULL AND FaultNotes <> '' THEN 1 END) AS with_solution,
                    COUNT(DISTINCT SerialNumber) AS unique_serials,
                    COUNT(DISTINCT PartCode) AS unique_parts
                FROM Traceability_RS.dbo.RmaRecords
                WHERE DateOut IS NULL
            """)
            row = cur.fetchone()
            cur.close()
            if row:
                return {
                    'total': row.total,
                    'with_solution': row.with_solution,
                    'unique_serials': row.unique_serials,
                    'unique_parts': row.unique_parts
                }
            return {'total': 0, 'with_solution': 0, 'unique_serials': 0, 'unique_parts': 0}
        except Exception as e:
            logger.error(f"get_statistics: {e}")
            return {'total': 0, 'with_solution': 0, 'unique_serials': 0, 'unique_parts': 0}
