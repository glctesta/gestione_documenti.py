"""
Script per rimuovere le linee duplicate 583-584
"""

# Leggi il file
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\orders\orders_reports_window.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Rimuovi le linee 583-584 (indici 582-583 in Python)
# Linea 583: "                    date_out\r\n"
# Linea 584: "                ))\r\n"
del lines[582:584]

# Scrivi il file pulito
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\orders\orders_reports_window.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Linee duplicate 583-584 rimosse con successo!")
print("   Il file ora dovrebbe essere senza errori di indentazione")
