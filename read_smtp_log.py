# -*- coding: utf-8 -*-
"""Legge smtp_debug.log (UTF-16) e stampa le righe diagnostiche chiave"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'smtp_debug.log')

try:
    with open(log_file, 'r', encoding='utf-16') as f:
        lines = f.readlines()
except UnicodeError:
    with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

print(f"Totale righe nel log: {len(lines)}\n")
print("=" * 70)
print("OUTPUT COMPLETO:")
print("=" * 70)
for line in lines:
    print(line, end='')
