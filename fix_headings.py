"""
Script per completare le modifiche a orders_reports_window.py
Versione 2 - Fix completo
"""

import re

# Leggi il file
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\orders\orders_reports_window.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Trova e sostituisci le intestazioni vecchie (linee ~224-229)
for i, line in enumerate(lines):
    if "self.rules_tree.heading('QtyToShip'" in line:
        # Sostituisci le 6 linee vecchie con le nuove 9 linee
        lines[i] = "        # Intestazioni colonne\n"
        lines[i+1] = "        self.rules_tree.heading('ProdOrder', text=self.lang.get('col_prod_order', 'Ordine Prod.'))\n"
        lines[i+2] = "        self.rules_tree.heading('RequestedOn', text=self.lang.get('col_requested_on', 'Richiesto Il'))\n"
        lines[i+3] = "        self.rules_tree.heading('RequestDateToShip', text=self.lang.get('col_request_date_to_ship', 'Data Spedizione'))\n"
        lines[i+4] = "        self.rules_tree.heading('RequestQty', text=self.lang.get('col_request_qty', 'Qta Richiesta'))\n"
        lines[i+5] = "        self.rules_tree.heading('RemainOverPO', text=self.lang.get('col_remain_over_po', 'Rim. su PO'))\n"
        # Inserisci le linee mancanti
        lines.insert(i+6, "        self.rules_tree.heading('RemainOverRequest', text=self.lang.get('col_remain_over_request', 'Rim. su Richiesta'))\n")
        lines.insert(i+7, "        self.rules_tree.heading('ShipTo', text=self.lang.get('col_ship_to', 'Destinazione'))\n")
        lines.insert(i+8, "        self.rules_tree.heading('AddedBy', text=self.lang.get('col_added_by', 'Aggiunto Da'))\n")
        break

# Scrivi il file aggiornato
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\orders\orders_reports_window.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Intestazioni colonne aggiornate con successo!")
