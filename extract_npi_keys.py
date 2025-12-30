#!/usr/bin/env python3
# Script per estrarre TUTTE le chiavi lang.get() dai file NPI

import re
from pathlib import Path
from collections import defaultdict

# File da analizzare
files_to_scan = [
    r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\npi\windows\config_window.py",
    r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\npi\windows\project_window.py",
    r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\npi\npi_manager.py",
]

all_keys = set()

# Pattern per trovare lang.get('key') o lang.get("key") o lang.get('key', 'default')
pattern = r"lang\.get\(['\"]([^'\"]+)['\"]"

for file_path in files_to_scan:
    try:
        content = Path(file_path).read_text(encoding='utf-8')
        matches = re.findall(pattern, content)
        all_keys.update(matches)
        print(f"✅ {Path(file_path).name}: {len(matches)} chiavi trovate")
    except Exception as e:
        print(f"❌ Errore leggendo {file_path}: {e}")

print(f"\n📊 Totale chiavi uniche trovate: {len(all_keys)}")
print("\n🔑 Chiavi trovate:")
for key in sorted(all_keys):
    print(f"   {key}")

# Salva in un file
output = Path(r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\npi_keys_found.txt")
output.write_text('\n'.join(sorted(all_keys)), encoding='utf-8')
print(f"\n💾 Chiavi salvate in: {output}")
