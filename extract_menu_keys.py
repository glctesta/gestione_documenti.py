"""
Script per estrarre tutte le menu_translation_key usate nel programma
"""
import re
from pathlib import Path

def extract_menu_keys(file_path):
    """Estrae tutte le menu_translation_key da un file Python"""
    keys = set()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern 1: menu_translation_key='key'
    pattern1 = r"menu_translation_key\s*=\s*['\"]([^'\"]+)['\"]"
    matches1 = re.findall(pattern1, content)
    keys.update(matches1)
    
    # Pattern 2: _execute_authorized_action('key', ...)
    pattern2 = r"_execute_authorized_action\s*\(\s*['\"]([^'\"]+)['\"]"
    matches2 = re.findall(pattern2, content)
    keys.update(matches2)
    
    return keys

# File da analizzare
files_to_check = [
    Path(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\main.py'),
    Path(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\npi\windows\dashboard_window.py'),
    Path(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\npi\windows\task_documents_window.py'),
]

all_keys = set()

for file_path in files_to_check:
    if file_path.exists():
        keys = extract_menu_keys(file_path)
        all_keys.update(keys)
        print(f"File: {file_path.name}")
        print(f"  Chiavi trovate: {len(keys)}")
        for key in sorted(keys):
            print(f"    - {key}")
        print()

print(f"\n{'='*60}")
print(f"TOTALE CHIAVI UNICHE: {len(all_keys)}")
print(f"{'='*60}\n")

# Salva le chiavi in un file
output_file = Path(__file__).parent / 'menu_translation_keys.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    for key in sorted(all_keys):
        f.write(f"{key}\n")

print(f"✅ Chiavi salvate in: {output_file}")
print(f"\nLista completa delle chiavi:")
for key in sorted(all_keys):
    print(f"  - {key}")
