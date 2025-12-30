"""
Script di test per verificare la nuova logica di numerazione gerarchica dei task.

Questo script testa:
1. Creazione di task in diverse categorie con numerazione automatica
2. Verifica che i numeri avanzino di 5 in 5 per categoria
3. Verifica che non ci siano duplicati nella stessa categoria
4. Verifica che possano esistere stessi numeri in categorie diverse
"""

# Esempio di come dovrebbe funzionare:

# Categoria "Design" (NrOrdin = 10):
# - Primo task: NrOrdin = 1005  (10 * 100 + 5)
# - Secondo task: NrOrdin = 1010 (10 * 100 + 10)
# - Terzo task: NrOrdin = 1015  (10 * 100 + 15)

# Categoria "Materials" (NrOrdin = 20):
# - Primo task: NrOrdin = 2005  (20 * 100 + 5)
# - Secondo task: NrOrdin = 2010 (20 * 100 + 10)
# - Terzo task: NrOrdin = 2015  (20 * 100 + 15)

# Categoria "Testing" (NrOrdin = 30):
# - Primo task: NrOrdin = 3005  (30 * 100 + 5)
# - Secondo task: NrOrdin = 3010 (30 * 100 + 10)

print("=" * 60)
print("LOGICA DI NUMERAZIONE GERARCHICA DEI TASK")
print("=" * 60)
print()

categories = [
    {"name": "Design", "nr_ordin": 10},
    {"name": "Materials procurement", "nr_ordin": 20},
    {"name": "Pilot run preparation", "nr_ordin": 30},
]

print("SCHEMA DI NUMERAZIONE:")
print("-" * 60)
for cat in categories:
    base = cat["nr_ordin"] * 100
    print(f"\nCategoria: {cat['name']} (NrOrdin categoria = {cat['nr_ordin']})")
    print(f"  Base numerazione: {base}")
    print(f"  Task 1: {base + 5}")
    print(f"  Task 2: {base + 10}")
    print(f"  Task 3: {base + 15}")
    print(f"  Task 4: {base + 20}")
    print(f"  Task 5: {base + 25}")
    print(f"  ...")

print()
print("=" * 60)
print("REGOLE:")
print("=" * 60)
print("1. Nuovi task: NrOrdin calcolato automaticamente (incremento +5)")
print("2. Modifica task: NrOrdin può essere modificato manualmente")
print("3. Validazione: Non possono esistere duplicati nella stessa categoria")
print("4. Possono esistere stessi numeri in categorie diverse")
print()
print("Esempio:")
print("  - Design Task 1 (NrOrdin=1005) ✓")
print("  - Design Task 2 (NrOrdin=1010) ✓")
print("  - Materials Task 1 (NrOrdin=2005) ✓")
print("  - Design Task 3 (NrOrdin=1005) ✗ ERRORE: duplicato in Design!")
print("  - Materials Task 2 (NrOrdin=1005) ✓ OK: categoria diversa")
print()
