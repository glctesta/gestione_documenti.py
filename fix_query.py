"""
Script per aggiornare la query in _load_shipping_rules
"""

# Leggi il file
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\orders\orders_reports_window.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Sostituisci la query vecchia con quella nuova
old_query_section = """            query = \"\"\"
            SELECT DybamicShippingRuleId, QtyToShip, DateToship, ShipTo, AddBayUser, DateOut
            FROM [Traceability_RS].[dbo].[DynamicShippingRules]
            WHERE DynamicProductionOrderID = ?
            ORDER BY DateToship
            \"\"\""""

new_query_section = """            query = \"\"\"
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

content = content.replace(old_query_section, new_query_section)

# Sostituisci il loop di caricamento dati
old_loop_section = """            # Popola treeview
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

new_loop_section = """            # Popola treeview
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

content = content.replace(old_loop_section, new_loop_section)

# Scrivi il file aggiornato
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\orders\orders_reports_window.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Query e loop di caricamento dati aggiornati con successo!")
