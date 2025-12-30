#!/usr/bin/env python3
# Script per combinare tutte le traduzioni NPI in un unico file SQL

from pathlib import Path

# Leggi i tre file SQL generati
config_file = Path(r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\NPI_CONFIG_TRANSLATIONS.sql")
project_file = Path(r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\NPI_PROJECT_TRANSLATIONS.sql")
manager_file = Path(r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\NPI_MANAGER_TRANSLATIONS.sql")

# File di output combinato
output_file = Path(r"c:\Users\gtesta\PythonProjetcs\Python\PrductionDocumentation\NPI_ALL_TRANSLATIONS.sql")

with output_file.open('w', encoding='utf-8') as out:
    out.write("-- ============================================================\n")
    out.write("-- SCRIPT COMPLETO TRADUZIONI NPI\n")
    out.write("-- Generato automaticamente\n")
    out.write("-- Tabella: [Traceability_RS].[dbo].[AppTranslations]\n")
    out.write("-- ============================================================\n\n")
    
    # Config Window
    if config_file.exists():
        out.write("-- ============================================================\n")
        out.write("-- SEZIONE 1: CONFIG WINDOW (Configurazione NPI)\n")
        out.write("-- ============================================================\n\n")
        content = config_file.read_text(encoding='utf-8')
        # Rimuovi l'header del file originale
        lines = content.split('\n')
        content_without_header = '\n'.join(lines[4:])  # Salta le prime 4 righe di header
        out.write(content_without_header)
        out.write("\n\n")
    
    # Project Window
    if project_file.exists():
        out.write("-- ============================================================\n")
        out.write("-- SEZIONE 2: PROJECT WINDOW (Gestione Progetti NPI)\n")
        out.write("-- ============================================================\n\n")
        content = project_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        content_without_header = '\n'.join(lines[4:])
        out.write(content_without_header)
        out.write("\n\n")
    
    # Manager
    if manager_file.exists():
        out.write("-- ============================================================\n")
        out.write("-- SEZIONE 3: NPI MANAGER (Logica Business)\n")
        out.write("-- ============================================================\n\n")
        content = manager_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        content_without_header = '\n'.join(lines[4:])
        out.write(content_without_header)
        out.write("\n\n")
    
    out.write("-- ============================================================\n")
    out.write("-- FINE SCRIPT\n")
    out.write("-- ============================================================\n")

print(f"\n✅ Script SQL combinato generato: {output_file}")
print(f"\n📋 Riepilogo:")
print(f"   - Config Window: {config_file.stat().st_size:,} bytes")
print(f"   - Project Window: {project_file.stat().st_size:,} bytes")
print(f"   - NPI Manager: {manager_file.stat().st_size:,} bytes")
print(f"   - File combinato: {output_file.stat().st_size:,} bytes")
