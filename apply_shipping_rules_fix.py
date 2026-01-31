"""
Script per applicare le modifiche a orders_reports_window.py
Esegui questo script per aggiornare automaticamente il file
"""

import re

# Leggi il file
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\orders\orders_reports_window.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Aggiorna la definizione delle colonne (linea ~214)
old_columns = "columns = ('RuleId', 'QtyToShip', 'DateToShip', 'TimeToShip', 'ShipTo', 'AddedBy', 'DateAdded')"
new_columns = """columns = ('RuleId', 'ProdOrder', 'RequestedOn', 'RequestDateToShip', 'RequestQty', 
                   'RemainOverPO', 'RemainOverRequest', 'ShipTo', 'AddedBy')"""

content = content.replace(old_columns, new_columns)

# 2. Aggiorna le intestazioni delle colonne (linee ~223-228)
old_headings = """        self.rules_tree.heading('QtyToShip', text=self.lang.get('col_qty_to_ship', 'Qtà da Spedire'))
        self.rules_tree.heading('DateToShip', text=self.lang.get('col_date_to_ship', 'Data Spedizione'))
        self.rules_tree.heading('TimeToShip', text=self.lang.get('col_time_to_ship', 'Ora'))
        self.rules_tree.heading('ShipTo', text=self.lang.get('col_ship_to', 'Destinazione'))
        self.rules_tree.heading('AddedBy', text=self.lang.get('col_added_by', 'Aggiunto Da'))
        self.rules_tree.heading('DateAdded', text=self.lang.get('col_date_added', 'Data Inserimento'))"""

new_headings = """        # Intestazioni colonne
        self.rules_tree.heading('ProdOrder', text=self.lang.get('col_prod_order', 'Ordine Prod.'))
        self.rules_tree.heading('RequestedOn', text=self.lang.get('col_requested_on', 'Richiesto Il'))
        self.rules_tree.heading('RequestDateToShip', text=self.lang.get('col_request_date_to_ship', 'Data Spedizione'))
        self.rules_tree.heading('RequestQty', text=self.lang.get('col_request_qty', 'Qta Richiesta'))
        self.rules_tree.heading('RemainOverPO', text=self.lang.get('col_remain_over_po', 'Rim. su PO'))
        self.rules_tree.heading('RemainOverRequest', text=self.lang.get('col_remain_over_request', 'Rim. su Richiesta'))
        self.rules_tree.heading('ShipTo', text=self.lang.get('col_ship_to', 'Destinazione'))
        self.rules_tree.heading('AddedBy', text=self.lang.get('col_added_by', 'Aggiunto Da'))"""

content = content.replace(old_headings, new_headings)

# 3. Aggiorna le larghezze delle colonne (linee ~230-235)
old_widths = """        self.rules_tree.column('QtyToShip', width=100, anchor=tk.E)
        self.rules_tree.column('DateToShip', width=100)
        self.rules_tree.column('TimeToShip', width=60)
        self.rules_tree.column('ShipTo', width=180)
        self.rules_tree.column('AddedBy', width=120)
        self.rules_tree.column('DateAdded', width=140)"""

new_widths = """        # Larghezze colonne
        self.rules_tree.column('ProdOrder', width=120)
        self.rules_tree.column('RequestedOn', width=100)
        self.rules_tree.column('RequestDateToShip', width=120)
        self.rules_tree.column('RequestQty', width=90, anchor=tk.E)
        self.rules_tree.column('RemainOverPO', width=90, anchor=tk.E)
        self.rules_tree.column('RemainOverRequest', width=120, anchor=tk.E)
        self.rules_tree.column('ShipTo', width=180)
        self.rules_tree.column('AddedBy', width=120)"""

content = content.replace(old_widths, new_widths)

# 4. Aggiorna la query in _load_shipping_rules (linee ~533-538)
old_query = """            query = \"\"\"
            SELECT DybamicShippingRuleId, QtyToShip, DateToship, ShipTo, AddBayUser, DateOut
            FROM [Traceability_RS].[dbo].[DynamicShippingRules]
            WHERE DynamicProductionOrderID = ?
            ORDER BY DateToship
            \"\"\""""

new_query = """            query = \"\"\"
            SELECT DybamicShippingRuleId, po.ordernumber as Prod_Order, r.datesys as RequestedOn, 
                   DateToship as RequestDateToShip, R.QtyToShip AS RequestQty, 
                   S.QtyOrder - K.Packet AS RemainOverPO,
                   r.QtyToShip - p.Noboards As RemainOverRequest, ShipTo, AddBayUser
            FROM [Traceability_RS].[dyn].[DynamicShippingRules] R
            INNER JOIN Traceability_RS.dyn.DynamicProductionOrders O on O.DynamicProductionOrderID = R.DynamicProductionOrderID
            INNER JOIN TRACEABILITY_RS.DYN.DynamicSaleOrders S on s.DynamicSaleOrderId=o.DynamicSaleOrderId
            OUTER APPLY
                (select NoBoards as Packet from traceability_rs.[dbo].[GetOrderPhaseStatus](o.idorder,9)) as K
            OUTER APPLY     
                Traceability_rs.dbo.da_eusta_fn_GetPackedBoards(o.idorder, 920, NULL) AS P
            inner join traceability_rs.dbo.Orders PO on o.idorder=po.idorder
            WHERE DynamicProductionOrderID = ?
            ORDER BY DateToship
            \"\"\""""

content = content.replace(old_query, new_query)

# 5. Aggiorna il caricamento dati nel loop (linee ~549-564)
old_loop = """            # Popola treeview
            for row in rows:
                # 🆕 Separa data e ora
                date_to_ship = row.DateToship.strftime('%d/%m/%Y') if row.DateToship else ''
                time_to_ship = row.DateToship.strftime('%H:%M') if row.DateToship else ''
                date_out = row.DateOut.strftime('%d/%m/%Y %H:%M') if row.DateOut else ''
                ship_to = row.ShipTo or ''
                
                self.rules_tree.insert('', tk.END, values=(
                    row.DybamicShippingRuleId,
                    row.QtyToShip,
                    date_to_ship,
                    time_to_ship,
                    ship_to,
                    row.AddBayUser or '',
                    date_out
                ))"""

new_loop = """            # Popola treeview
            for row in rows:
                # Formatta date
                requested_on = row.RequestedOn.strftime('%d/%m/%Y') if row.RequestedOn else ''
                request_date_to_ship = row.RequestDateToShip.strftime('%d/%m/%Y %H:%M') if row.RequestDateToShip else ''
                ship_to = row.ShipTo or ''
                
                self.rules_tree.insert('', tk.END, values=(
                    row.DybamicShippingRuleId,
                    row.Prod_Order or '',
                    requested_on,
                    request_date_to_ship,
                    row.RequestQty or 0,
                    row.RemainOverPO or 0,
                    row.RemainOverRequest or 0,
                    ship_to,
                    row.AddBayUser or ''
                ))"""

content = content.replace(old_loop, new_loop)

# Scrivi il file aggiornato
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\orders\orders_reports_window.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ File aggiornato con successo!")
print("Le modifiche applicate:")
print("1. Colonne treeview aggiornate")
print("2. Intestazioni colonne aggiornate")
print("3. Larghezze colonne aggiornate")
print("4. Query _load_shipping_rules aggiornata")
print("5. Loop caricamento dati aggiornato")
