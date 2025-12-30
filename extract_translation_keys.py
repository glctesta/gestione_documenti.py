"""
Script migliorato per estrarre SOLO le chiavi di traduzione dell'applicazione
Filtra le chiavi di sistema e librerie
"""
import re
import os
from pathlib import Path

# Directory del progetto
project_dir = Path(__file__).parent

# Pattern per trovare le chiamate self.lang.get('key') o lang.get('key')
pattern = r"(?:self\.)?lang\.get\(['\"](\w+)['\"]"

# Set per memorizzare tutte le chiavi uniche
translation_keys = set()

# File da escludere (librerie, venv, etc.)
exclude_dirs = {'.venv', 'venv', 'build', 'dist', '__pycache__', 'npi'}

# Scansiona solo i file Python del progetto principale
for py_file in project_dir.glob('*.py'):
    if py_file.name.startswith('extract_'):
        continue
    
    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = re.findall(pattern, content)
            translation_keys.update(matches)
            if matches:
                print(f"{py_file.name}: {len(matches)} chiavi")
    except Exception as e:
        print(f"Errore leggendo {py_file}: {e}")

# Ordina le chiavi
sorted_keys = sorted(translation_keys)

# Salva in un file
output_file = project_dir / 'app_translation_keys.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    for key in sorted_keys:
        f.write(f"{key}\n")

print(f"\n{'='*60}")
print(f"Trovate {len(sorted_keys)} chiavi di traduzione dell'applicazione")
print(f"Salvate in: {output_file}")
print(f"{'='*60}\n")

# Raggruppa per prefisso comune
prefixes = {}
for key in sorted_keys:
    prefix = key.split('_')[0] if '_' in key else 'other'
    if prefix not in prefixes:
        prefixes[prefix] = []
    prefixes[prefix].append(key)

print("Chiavi per categoria:")
for prefix in sorted(prefixes.keys()):
    print(f"  {prefix}: {len(prefixes[prefix])} chiavi")
