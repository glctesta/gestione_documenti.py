# File: orders/orders_manager.py
"""
Manager per la gestione degli ordini dinamici di vendita
"""
import logging
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class OrdersManager:
    """Gestisce le operazioni CRUD per gli ordini dinamici"""
    
    def __init__(self, db_connection):
        """
        Inizializza il manager degli ordini
        
        Args:
            db_connection: Oggetto Database con engine SQLAlchemy
        """
        self.db = db_connection
        # Usa npi_engine che ha pool_pre_ping=True e connection pooling corretto.
        # db.engine è basato su una singola connessione pyodbc raw che può
        # diventare stale dopo periodi di inattività (SQL Server chiude la connessione).
        engine = getattr(self.db, 'npi_engine', None) or self.db.engine
        self.session_factory = sessionmaker(
            bind=engine,
            expire_on_commit=False,
            autoflush=True,
            autocommit=False
        )

    def _get_session(self):
        """Crea una nuova sessione per ogni operazione.
        
        pool_pre_ping=True sull'engine gestisce automaticamente le connessioni
        stale/chiuse dal server, quindi non è necessario un SELECT 1 manuale.
        """
        try:
            return self.session_factory()
        except Exception as e:
            logger.error(f"Errore nella creazione della sessione: {e}")
            raise
    
    def get_all_dynamic_orders(self, days_limit: int = 100, linked_filter: str = 'All') -> List[Dict]:
        """
        Recupera tutti gli ordini dinamici con i dati dei prodotti
        
        Args:
            days_limit: Numero di giorni dalla data odierna per filtrare ShipDateRequest (default 100)
            linked_filter: Filtro per ordini collegati ('All', 'Yes', 'No')
        
        Returns:
            Lista di dizionari con i dati degli ordini
        """
        # Costruisci la query base
        base_query = """
            SELECT s.[DynamicSaleOrderId]
                  ,[SONumber]
                  ,[CustomerName]
                  ,[ItemCode]
                  ,[ItemName]
                  ,[ShipDateRequest]
                  ,[QtyOrder]
                  ,[QtyToShip]
                  ,[QtyStock]
                  ,[Currency]
                  ,[UnitPrice]
                  ,[LastUpdate]
                  ,iif(isnull(p.idorder ,0)=0,'No','Yes') as Linked
              FROM [Traceability_RS].[dyn].[DynamicSaleOrders] S 
              LEFT JOIN [Traceability_RS].[dyn].[DynamicProductionOrders] P 
                ON p.DynamicSaleOrderId=s.DynamicSaleOrderId
              WHERE datediff(DAY,getdate(),s.ShipDateRequest) < :days_limit
                AND CHARINDEX('ECORE',[CustomerName],1) = 0
        """
        
        # Aggiungi filtro Linked se necessario
        if linked_filter == 'Yes':
            base_query += "                AND isnull(p.idorder, 0) <> 0\n"
        elif linked_filter == 'No':
            base_query += "                AND isnull(p.idorder, 0) = 0\n"
        
        base_query += "              ORDER BY s.sonumber"
        
        query = text(base_query)
        
        session = self._get_session()
        try:
            result = session.execute(query, {'days_limit': days_limit})
            orders = []
            for row in result:
                orders.append({
                    'DynamicSaleOrderId': row[0],
                    'SONumber': row[1],
                    'CustomerName': row[2],
                    'ProductCode': row[3],
                    'ProductName': row[4],
                    'ShipDateRequest': row[5],
                    'QtyOrder': row[6],
                    'QtyToShip': row[7],
                    'QtyStock': row[8],
                    'Currency': row[9],
                    'UnitPrice': row[10],
                    'LastUpdate': row[11],
                    'Linked': row[12]
                })
            return orders
        except Exception as e:
            logger.error(f"Errore nel recupero ordini: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
    
    def check_order_exists(self, so_number: str) -> Optional[int]:
        """
        Verifica se un ordine esiste già nel database
        
        Args:
            so_number: Numero dell'ordine di vendita
            
        Returns:
            DynamicSaleOrderId se esiste, None altrimenti
        """
        query = text("""
            SELECT DynamicSaleOrderId 
            FROM [Traceability_RS].[dyn].[DynamicSaleOrders]
            WHERE SONumber = :so_number
        """)
        
        session = self._get_session()
        try:
            result = session.execute(query, {'so_number': so_number})
            row = result.fetchone()
            return row[0] if row else None
        except Exception as e:
            logger.error(f"Errore nella verifica ordine {so_number}: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
    
    def insert_order(self, order_data: Dict) -> int:
        """
        Inserisce un nuovo ordine nel database
        
        Args:
            order_data: Dizionario con i dati dell'ordine
            
        Returns:
            ID del nuovo ordine inserito
        """
        # Usa OUTPUT INSERTED per recuperare il nuovo ID nello stesso result set
        # (SCOPE_IDENTITY con due statement separati non funziona con pyodbc/SQLAlchemy:
        #  il driver chiude il result dopo l'INSERT e non arriva alla SELECT)
        insert_query = text("""
            INSERT INTO [Traceability_RS].[dyn].[DynamicSaleOrders]
            (
                SONumber,
                CustomerName,
                ItemCode,
                ItemName,
                ShipDateRequest,
                QtyOrder,
                QtyToShip,
                QtyStock,
                Currency,
                UnitPrice
            )
            OUTPUT INSERTED.DynamicSaleOrderId
            VALUES
            (
                :so_number,
                :customer_name,
                :item_code,
                :item_name,
                :ship_date,
                :qty_order,
                :qty_to_ship,
                :qty_stock,
                :currency,
                :unit_price
            )
        """)
        
        session = self._get_session()
        try:
            result = session.execute(insert_query, {
                'so_number': order_data.get('SONumber'),
                'customer_name': order_data.get('CustomerName'),
                'item_code': order_data.get('ItemCode'),
                'item_name': order_data.get('ItemName'),
                'ship_date': order_data.get('ShipDateRequest'),
                'qty_order': order_data.get('QtyOrder'),
                'qty_to_ship': order_data.get('QtyToShip'),
                'qty_stock': order_data.get('QtyStock'),
                'currency': order_data.get('Currency'),
                'unit_price': order_data.get('UnitPrice')
            })
            
            # OUTPUT INSERTED restituisce l'ID direttamente nel result set
            row = result.fetchone()
            new_id = int(row[0]) if row else None
            
            session.commit()
            logger.info(f"Ordine {order_data.get('SONumber')} inserito con successo (ID: {new_id})")
            return new_id
        except Exception as e:
            logger.error(f"Errore nell'inserimento ordine {order_data.get('SONumber')}: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
    
    def update_order_quantities(self, so_number: str, qty_to_ship: float, qty_stock: float) -> bool:
        """
        Aggiorna le quantità di un ordine esistente
        
        Args:
            so_number: Numero dell'ordine di vendita
            qty_to_ship: Quantità rimanente da spedire
            qty_stock: Quantità in stock
            
        Returns:
            True se l'aggiornamento è riuscito
        """
        query = text("""
            UPDATE [Traceability_RS].[dyn].[DynamicSaleOrders]
            SET 
                QtyToShip = :qty_to_ship,
                QtyStock = :qty_stock
            WHERE SONumber = :so_number
        """)
        
        session = self._get_session()
        try:
            session.execute(query, {
                'so_number': so_number,
                'qty_to_ship': qty_to_ship,
                'qty_stock': qty_stock
            })
            session.commit()
            logger.info(f"Ordine {so_number} aggiornato con successo")
            return True
        except Exception as e:
            logger.error(f"Errore nell'aggiornamento ordine {so_number}: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
    
    def import_from_excel_data(self, excel_rows: List[Dict], user_name: str) -> Dict:
        """
        Importa gli ordini da dati Excel
        
        Args:
            excel_rows: Lista di dizionari con i dati delle righe Excel
            user_name: Nome dell'utente che esegue l'importazione
            
        Returns:
            Dizionario con statistiche dell'importazione
        """
        stats = {
            'inserted': 0,
            'updated': 0,
            'errors': 0,
            'error_details': []
        }
        
        for row in excel_rows:
            try:
                so_number = row.get('SONumber')
                if not so_number:
                    continue
                
                # Verifica se l'ordine esiste già
                existing_id = self.check_order_exists(so_number)
                
                if existing_id:
                    # UPDATE delle quantità
                    self.update_order_quantities(
                        so_number,
                        row.get('QtyToShip', 0),
                        row.get('QtyStock', 0)
                    )
                    stats['updated'] += 1
                else:
                    # INSERT nuovo ordine
                    self.insert_order(row)
                    stats['inserted'] += 1
                    
            except Exception as e:
                stats['errors'] += 1
                stats['error_details'].append({
                    'so_number': row.get('SONumber', 'N/A'),
                    'error': str(e)
                })
                logger.error(f"Errore importazione riga {row}: {e}", exc_info=True)
        
        logger.info(f"Importazione completata: {stats['inserted']} inseriti, {stats['updated']} aggiornati, {stats['errors']} errori")
        return stats
    
    def get_sale_orders_for_matching(self, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Recupera gli ordini di vendita con le quantità assegnate per il matching
        
        Args:
            filters: Dizionario opzionale con filtri (so_number, customer, product, date_from, date_to, assignment_status)
                assignment_status: 'fully_assigned' = solo ordini completamente assegnati
                                  'not_fully_assigned' = solo ordini non completamente assegnati
                                  None = tutti gli ordini
            
        Returns:
            Lista di dizionari con i dati degli ordini e le quantità assegnate
        """
        # Base query
        query_str = """
            SELECT  
                d.[DynamicSaleOrderId],
                d.[SONumber],
                d.[CustomerName],
                d.[ItemCode],
                d.[ItemName],
                d.[ShipDateRequest],
                d.[QtyOrder],
                ISNULL(SUM(po.Qty), 0) as QtyAssigned
            FROM [Traceability_RS].[dyn].[DynamicSaleOrders] d
            LEFT JOIN [Traceability_RS].[dyn].[DynamicProductionOrders] po
                ON d.DynamicSaleOrderId = po.DynamicSaleOrderId
            WHERE 1=1
        """
        
        params = {}
        
        # Applica filtri
        if filters:
            if filters.get('so_number'):
                query_str += " AND d.SONumber LIKE :so_number"
                params['so_number'] = f"%{filters['so_number']}%"
            
            if filters.get('customer'):
                query_str += " AND d.CustomerName LIKE :customer"
                params['customer'] = f"%{filters['customer']}%"
            
            if filters.get('product'):
                query_str += " AND (d.ItemCode LIKE :product OR d.ItemName LIKE :product)"
                params['product'] = f"%{filters['product']}%"
            
            if filters.get('date_from'):
                query_str += " AND d.ShipDateRequest >= :date_from"
                params['date_from'] = filters['date_from']
            
            if filters.get('date_to'):
                query_str += " AND d.ShipDateRequest <= :date_to"
                params['date_to'] = filters['date_to']
        
        query_str += """
            GROUP BY 
                d.[DynamicSaleOrderId],
                d.[SONumber],
                d.[CustomerName],
                d.[ItemCode],
                d.[ItemName],
                d.[ShipDateRequest],
                d.[QtyOrder]
        """
        
        # 🆕 Filtro per stato di assegnazione (va dopo GROUP BY con HAVING)
        if filters and filters.get('assignment_status'):
            if filters['assignment_status'] == 'fully_assigned':
                # Solo ordini completamente assegnati (QtyOrder == QtyAssigned)
                query_str += " HAVING d.[QtyOrder] = ISNULL(SUM(po.Qty), 0)"
            elif filters['assignment_status'] == 'not_fully_assigned':
                # Solo ordini non completamente assegnati (QtyOrder > QtyAssigned)
                query_str += " HAVING d.[QtyOrder] > ISNULL(SUM(po.Qty), 0)"
        
        query_str += " ORDER BY d.SONumber, d.ShipDateRequest"
        
        query = text(query_str)
        
        session = self._get_session()
        try:
            result = session.execute(query, params)
            orders = []
            for row in result:
                orders.append({
                    'DynamicSaleOrderId': row[0],
                    'SONumber': row[1],
                    'CustomerName': row[2],
                    'ItemCode': row[3],
                    'ItemName': row[4],
                    'ShipDateRequest': row[5],
                    'QtyOrder': row[6],
                    'QtyAssigned': row[7]
                })
            return orders
        except Exception as e:
            logger.error(f"Errore nel recupero ordini per matching: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_available_production_orders(self, product_code: Optional[str] = None) -> List[Dict]:
        """
        Recupera gli ordini di produzione con quantità ancora disponibile (non interamente assegnata).

        Un ordine di produzione può essere associato a più ordini di vendita finché
        la somma delle qty assegnate è inferiore alla sua quantità totale (col_quantity).

        Args:
            product_code: Filtro opzionale per ProductCode (usa LIKE con % alla fine)

        Returns:
            Lista di dizionari con i dati degli ordini di produzione disponibili,
            includendo RemainingQty e TotalQty.
        """
        query_str = """
            SELECT
                o.IdOrder,
                o.OrderNumber,
                p.ProductCode + ' [' + p.ProductName + ']' AS Product,
                ISNULL(o.col_quantity, 0) AS TotalQty,
                ISNULL(o.col_quantity, 0)
                    - ISNULL((
                        SELECT SUM(dpo.Qty)
                        FROM [Traceability_RS].[dyn].[DynamicProductionOrders] dpo
                        WHERE dpo.IdOrder = o.IdOrder
                    ), 0) AS RemainingQty
            FROM [Traceability_RS].dbo.orders o
            LEFT JOIN [Traceability_RS].dbo.Products p
                ON p.IDProduct = o.IDProduct
            WHERE LEFT(o.OrderNumber, 2) = 'PR'
        """

        params = {}

        # Aggiungi filtro ProductCode se fornito (LIKE con % alla fine)
        if product_code:
            query_str += " AND p.ProductCode LIKE :product_code"
            params['product_code'] = f"{product_code}%"

        # Filtra solo PO con quantità ancora disponibile (tramite AND nella WHERE)
        query_str += """
            AND (
                ISNULL(o.col_quantity, 0)
                - ISNULL((
                    SELECT SUM(dpo.Qty)
                    FROM [Traceability_RS].[dyn].[DynamicProductionOrders] dpo
                    WHERE dpo.IdOrder = o.IdOrder
                ), 0)
            ) > 0
            ORDER BY o.OrderNumber
        """

        query = text(query_str)

        session = self._get_session()
        try:
            result = session.execute(query, params)
            orders = []
            for row in result:
                orders.append({
                    'IdOrder': row[0],
                    'OrderNumber': row[1],
                    'Product': row[2] or '',
                    'TotalQty': float(row[3]) if row[3] is not None else 0.0,
                    'RemainingQty': float(row[4]) if row[4] is not None else 0.0,
                })
            return orders
        except Exception as e:
            logger.error(f"Errore nel recupero ordini produzione disponibili: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()

    
    def create_production_association(self, association_data: Dict) -> int:
        """
        Crea un'associazione tra ordine di vendita e ordine di produzione
        
        Args:
            association_data: Dizionario con DynamicSaleOrderId, IdOrder, Qty
            
        Returns:
            ID della nuova associazione
        """
        # Usa OUTPUT INSERTED invece di SCOPE_IDENTITY() per compatibilità con SQLAlchemy/pyodbc
        insert_query = text("""
            INSERT INTO [Traceability_RS].[dyn].[DynamicProductionOrders]
            (
                DynamicSaleOrderId,
                IdOrder,
                Qty,
                DateIn
            )
            OUTPUT INSERTED.DynamicProductionOrderID
            VALUES
            (
                :dynamic_sale_order_id,
                :id_order,
                :qty,
                GETDATE()
            )
        """)
        
        session = self._get_session()
        try:
            result = session.execute(insert_query, {
                'dynamic_sale_order_id': association_data.get('DynamicSaleOrderId'),
                'id_order': association_data.get('IdOrder'),
                'qty': association_data.get('Qty')
            })
            
            # Con OUTPUT INSERTED, l'ID viene restituito direttamente nel primo result set
            row = result.fetchone()
            new_id = int(row[0]) if row else None
            
            session.commit()
            logger.info(f"Associazione creata con successo (ID: {new_id})")
            return new_id
        except Exception as e:
            logger.error(f"Errore nella creazione associazione: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_production_associations(self, dynamic_sale_order_id: int) -> List[Dict]:
        """
        Recupera le associazioni esistenti per un ordine di vendita
        
        Args:
            dynamic_sale_order_id: ID dell'ordine di vendita
            
        Returns:
            Lista di dizionari con i dati delle associazioni
        """
        query = text("""
            SELECT 
                po.DynamicProductionOrderID,
                po.IdOrder,
                o.OrderNumber,
                p.ProductCode + ' [' + p.ProductName + ']' AS Product,
                po.Qty,
                po.DateIn
            FROM [Traceability_RS].[dyn].[DynamicProductionOrders] po
            LEFT JOIN [Traceability_RS].dbo.orders o
                ON o.IdOrder = po.IdOrder
            LEFT JOIN [Traceability_RS].dbo.Products p
                ON p.IDProduct = o.IDProduct
            WHERE po.DynamicSaleOrderId = :dynamic_sale_order_id
            ORDER BY po.DateIn DESC
        """)
        
        session = self._get_session()
        try:
            result = session.execute(query, {'dynamic_sale_order_id': dynamic_sale_order_id})
            associations = []
            for row in result:
                associations.append({
                    'DynamicProductionOrderID': row[0],
                    'IdOrder': row[1],
                    'OrderNumber': row[2],
                    'Product': row[3] or '',
                    'Qty': row[4],
                    'DateIn': row[5]
                })
            return associations
        except Exception as e:
            logger.error(f"Errore nel recupero associazioni: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
    
    def delete_production_association(self, dynamic_production_order_id: int) -> bool:
        """
        Elimina un'associazione tra ordine di vendita e ordine di produzione
        
        Args:
            dynamic_production_order_id: ID dell'associazione da eliminare
            
        Returns:
            True se l'eliminazione è riuscita
        """
        delete_query = text("""
            DELETE FROM [Traceability_RS].[dyn].[DynamicProductionOrders]
            WHERE DynamicProductionOrderID = :id
        """)
        
        session = self._get_session()
        try:
            session.execute(delete_query, {'id': dynamic_production_order_id})
            session.commit()
            logger.info(f"Associazione {dynamic_production_order_id} eliminata con successo")
            return True
        except Exception as e:
            logger.error(f"Errore nell'eliminazione associazione: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_customers_list(self) -> List[str]:
        """
        Recupera la lista dei clienti univoci
        
        Returns:
            Lista di nomi clienti
        """
        query = text("""
            SELECT DISTINCT CustomerName
            FROM [Traceability_RS].[dyn].[DynamicSaleOrders]
            WHERE CustomerName IS NOT NULL
            ORDER BY CustomerName
        """)
        
        session = self._get_session()
        try:
            result = session.execute(query)
            customers = [row[0] for row in result if row[0]]
            return customers
        except Exception as e:
            logger.error(f"Errore nel recupero lista clienti: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_all_associations(self, so_number_filter: Optional[str] = None) -> List[Dict]:
        """
        Recupera tutte le associazioni ordini vendita-produzione
        
        Args:
            so_number_filter: Filtro opzionale per numero ordine
            
        Returns:
            Lista di dizionari con i dati delle associazioni
        """
        query_str = """
            SELECT 
                dso.SONumber,
                dso.CustomerName,
                dso.ItemCode + ' [' + dso.ItemName + ']' AS SaleProduct,
                o.OrderNumber AS ProductionOrder,
                p.ProductCode + ' [' + p.ProductName + ']' AS ProductionProduct,
                dpo.Qty,
                dpo.DateIn
            FROM [Traceability_RS].[dyn].[DynamicProductionOrders] dpo
            INNER JOIN [Traceability_RS].[dyn].[DynamicSaleOrders] dso
                ON dpo.DynamicSaleOrderId = dso.DynamicSaleOrderId
            LEFT JOIN [Traceability_RS].dbo.orders o
                ON o.IdOrder = dpo.IdOrder
            LEFT JOIN [Traceability_RS].dbo.Products p
                ON p.IDProduct = o.IDProduct
            WHERE 1=1
        """
        
        params = {}
        if so_number_filter:
            query_str += " AND dso.SONumber LIKE :so_number"
            params['so_number'] = f"%{so_number_filter}%"
        
        query_str += " ORDER BY dso.SONumber, dpo.DateIn DESC"
        
        query = text(query_str)
        
        session = self._get_session()
        try:
            result = session.execute(query, params)
            associations = []
            for row in result:
                associations.append({
                    'SONumber': row[0],
                    'CustomerName': row[1],
                    'SaleProduct': row[2],
                    'ProductionOrder': row[3],
                    'ProductionProduct': row[4] or '',
                    'Qty': row[5],
                    'DateIn': row[6]
                })
            return associations
        except Exception as e:
            logger.error(f"Errore nel recupero associazioni: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_workload_by_product(self) -> List[Dict]:
        """
        Recupera i carichi di lavoro aggregati per prodotto
        
        Returns:
            Lista di dizionari con le statistiche per prodotto
        """
        query = text("""
            SELECT 
                dso.ItemCode + ' [' + dso.ItemName + ']' AS Product,
                SUM(dso.QtyOrder) AS TotalOrdered,
                ISNULL(SUM(dpo.Qty), 0) AS TotalAssigned,
                SUM(dso.QtyOrder) - ISNULL(SUM(dpo.Qty), 0) AS TotalRemaining,
                COUNT(DISTINCT dso.DynamicSaleOrderId) AS OrdersCount,
                AVG(dso.UnitPrice * dso.QtyOrder) AS AvgValue
            FROM [Traceability_RS].[dyn].[DynamicSaleOrders] dso
            LEFT JOIN [Traceability_RS].[dyn].[DynamicProductionOrders] dpo
                ON dso.DynamicSaleOrderId = dpo.DynamicSaleOrderId
            GROUP BY dso.ItemCode, dso.ItemName
            ORDER BY TotalRemaining DESC
        """)
        
        session = self._get_session()
        try:
            result = session.execute(query)
            workload = []
            for row in result:
                workload.append({
                    'Product': row[0],
                    'TotalOrdered': row[1] or 0,
                    'TotalAssigned': row[2] or 0,
                    'TotalRemaining': row[3] or 0,
                    'OrdersCount': row[4] or 0,
                    'AvgValue': row[5] or 0
                })
            return workload
        except Exception as e:
            logger.error(f"Errore nel recupero carichi di lavoro: {e}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
