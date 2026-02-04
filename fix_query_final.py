"""
Script finale per aggiornare la query in _load_shipping_rules
Approccio basato su sostituzione di linee specifiche
"""

# Leggi il file
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\orders\orders_reports_window.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Trova la linea con la query vecchia e sostituiscila
in_query = False
query_start_line = None
for i, line in enumerate(lines):
    # Trova l'inizio della query
    if 'SELECT DybamicShippingRuleId, QtyToShip, DateToship' in line:
        query_start_line = i
        in_query = True
        # Sostituisci la query (linee 541-545)
        new_query_lines = [
            "            SELECT DybamicShippingRuleId, po.ordernumber as Prod_Order, r.datesys as RequestedOn, \n",
            "                   DateToship as RequestDateToShip, R.QtyToShip AS RequestQty, \n",
            "                   S.QtyOrder - K.Packet AS RemainOverPO,\n",
            "                   r.QtyToShip - p.Noboards As RemainOverRequest, ShipTo, AddBayUser\n",
            "            FROM [Traceability_RS].[dyn].[DynamicShippingRules] R\n",
            "            INNER JOIN Traceability_RS.dyn.DynamicProductionOrders O on O.DynamicProductionOrderID = R.DynamicProductionOrderID\n",
            "            INNER JOIN TRACEABILITY_RS.DYN.DynamicSaleOrders S on s.DynamicSaleOrderId=o.DynamicSaleOrderId\n",
            "            OUTER APPLY\n",
            "                (select NoBoards as Packet from traceability_rs.[dbo].[GetOrderPhaseStatus](o.idorder,9)) as K\n",
            "            OUTER APPLY     \n",
            "                Traceability_rs.dbo.da_eusta_fn_GetPackedBoards(o.idorder, 920, NULL,0) AS P\n",
            "            inner join traceability_rs.dbo.Orders PO on o.idorder=po.idorder\n",
            "            WHERE DynamicProductionOrderID = ?\n",
            "            ORDER BY DateToship\n",
        ]
        # Sostituisci le 4 linee vecchie (541-544) con le nuove 14 linee
        lines[i:i+4] = new_query_lines
        break

# Trova e sostituisci il loop di caricamento dati
for i, line in enumerate(lines):
    if '# Popola treeview' in line and i > 550:  # Assicurati di essere nel posto giusto
        # Cerca le linee successive
        if 'date_to_ship = row.DateToship' in lines[i+2]:
            # Sostituisci il blocco (linee i+1 fino a i+14)
            new_loop_lines = [
                "            for row in rows:\n",
                "                # Formatta date\n",
                "                requested_on = row.RequestedOn.strftime('%d/%m/%Y') if row.RequestedOn else ''\n",
                "                request_date_to_ship = row.RequestDateToShip.strftime('%d/%m/%Y %H:%M') if row.RequestDateToShip else ''\n",
                "                ship_to = row.ShipTo or ''\n",
                "                \n",
                "                self.rules_tree.insert('', tk.END, values=(\n",
                "                    row.DybamicShippingRuleId,\n",
                "                    row.Prod_Order or '',\n",
                "                    requested_on,\n",
                "                    request_date_to_ship,\n",
                "                    row.RequestQty or 0,\n",
                "                    row.RemainOverPO or 0,\n",
                "                    row.RemainOverRequest or 0,\n",
                "                    ship_to,\n",
                "                    row.AddBayUser or ''\n",
                "                ))\n",
            ]
            # Sostituisci le linee vecchie
            lines[i+1:i+14] = new_loop_lines
            break

# Scrivi il file aggiornato
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\orders\orders_reports_window.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Query e loop aggiornati con successo!")
print("Modifiche applicate:")
print("  - Query SQL aggiornata con JOIN e OUTER APPLY")
print("  - Loop di caricamento dati aggiornato con nuove colonne")
