#!/usr/bin/env python3
# Script per verificare se le modifiche al config_window sono presenti

import sys
sys.path.insert(0, r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation')

# Leggi il file direttamente
with open(r'c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\npi\windows\config_window.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Cerca le modifiche chiave
checks = {
    "Evento bind sulla combobox": "self.fields['CategoryId'].bind('<<ComboboxSelected>>', self._on_category_filter_change)",
    "Opzione 'Tutte le categorie'": "all_categories_label = self.lang.get('all_categories'",
    "Metodo _on_category_filter_change": "def _on_category_filter_change(self, event=None):",
    "Filtro in _load_tasks": "selected_category = self.fields['CategoryId'].get()"
}

print("🔍 Verifica modifiche in config_window.py:\n")
for name, search_string in checks.items():
    if search_string in content:
        print(f"✅ {name}: PRESENTE")
    else:
        print(f"❌ {name}: MANCANTE")

# Conta le occorrenze
print(f"\n📊 Statistiche:")
print(f"   - Righe totali: {len(content.splitlines())}")
print(f"   - Occorrenze 'all_categories': {content.count('all_categories')}")
print(f"   - Occorrenze '_on_category_filter_change': {content.count('_on_category_filter_change')}")
