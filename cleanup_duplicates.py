"""
Script per rimuovere le linee duplicate nel loop
"""

# Leggi il file
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\orders\orders_reports_window.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Trova e rimuovi le linee duplicate (583-584)
new_lines = []
skip_next = False
for i, line in enumerate(lines):
    # Se troviamo la linea con "date_out" dopo la chiusura della parentesi, skippiamola
    if i > 0 and 'date_out' in line and ')' in lines[i-1] and 'AddBayUser' in lines[i-1]:
        skip_next = True
        continue
    if skip_next and '))' in line:
        skip_next = False
        continue
    new_lines.append(line)

# Scrivi il file pulito
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\orders\orders_reports_window.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ Linee duplicate rimosse con successo!")
