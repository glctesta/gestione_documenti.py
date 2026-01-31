"""
Script per aggiornare SOLO il loop di caricamento dati
"""

# Leggi il file
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\orders\orders_reports_window.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Trova e sostituisci il loop di caricamento dati
for i, line in enumerate(lines):
    # Cerca il commento specifico nel loop
    if 'Separa data e ora' in line or ('date_to_ship = row.DateToship' in line):
        # Torna indietro di 2 linee per trovare "for row in rows:"
        loop_start = i - 1
        # Sostituisci le linee dal loop fino alla chiusura della parentesi
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
        # Sostituisci le 14 linee vecchie (dal for row fino alla chiusura della insert)
        lines[loop_start:loop_start+14] = new_loop_lines
        break

# Scrivi il file aggiornato
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\orders\orders_reports_window.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Loop di caricamento dati aggiornato con successo!")
