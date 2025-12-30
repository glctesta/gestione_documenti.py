"""
Script di Profiling per Startup Performance
Misura i tempi di avvio dell'applicazione main.py
"""

import time
import sys
import os

# Aggiungi il path corrente
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 80)
print("PROFILING STARTUP PERFORMANCE")
print("=" * 80)
print()

# Timing totale
total_start = time.time()

# 1. Import base
print("📦 Import moduli base...")
step_start = time.time()
import tkinter as tk
from tkinter import ttk
print(f"   ✓ tkinter: {time.time() - step_start:.3f}s")

step_start = time.time()
import pyodbc
print(f"   ✓ pyodbc: {time.time() - step_start:.3f}s")

step_start = time.time()
from datetime import datetime, timedelta
print(f"   ✓ datetime: {time.time() - step_start:.3f}s")

step_start = time.time()
import pandas as pd
print(f"   ✓ pandas: {time.time() - step_start:.3f}s")

step_start = time.time()
from PIL import Image, ImageTk
print(f"   ✓ PIL: {time.time() - step_start:.3f}s")

step_start = time.time()
from sqlalchemy import create_engine
print(f"   ✓ sqlalchemy: {time.time() - step_start:.3f}s")

print()

# 2. Import moduli custom
print("📦 Import moduli custom...")
step_start = time.time()
try:
    import general_docs_gui
    print(f"   ✓ general_docs_gui: {time.time() - step_start:.3f}s")
except Exception as e:
    print(f"   ✗ general_docs_gui: {e}")

step_start = time.time()
try:
    import maintenance_gui
    print(f"   ✓ maintenance_gui: {time.time() - step_start:.3f}s")
except Exception as e:
    print(f"   ✗ maintenance_gui: {e}")

step_start = time.time()
try:
    import materials_gui
    print(f"   ✓ materials_gui: {time.time() - step_start:.3f}s")
except Exception as e:
    print(f"   ✗ materials_gui: {e}")

step_start = time.time()
try:
    import operations_gui
    print(f"   ✓ operations_gui: {time.time() - step_start:.3f}s")
except Exception as e:
    print(f"   ✗ operations_gui: {e}")

step_start = time.time()
try:
    import permissions_gui
    print(f"   ✓ permissions_gui: {time.time() - step_start:.3f}s")
except Exception as e:
    print(f"   ✗ permissions_gui: {e}")

step_start = time.time()
try:
    import translations_manager
    print(f"   ✓ translations_manager: {time.time() - step_start:.3f}s")
except Exception as e:
    print(f"   ✗ translations_manager: {e}")

step_start = time.time()
try:
    import submissions_gui
    print(f"   ✓ submissions_gui: {time.time() - step_start:.3f}s")
except Exception as e:
    print(f"   ✗ submissions_gui: {e}")

step_start = time.time()
try:
    import tools_gui
    print(f"   ✓ tools_gui: {time.time() - step_start:.3f}s")
except Exception as e:
    print(f"   ✗ tools_gui: {e}")

step_start = time.time()
try:
    import scarti_gui
    print(f"   ✓ scarti_gui: {time.time() - step_start:.3f}s")
except Exception as e:
    print(f"   ✗ scarti_gui: {e}")

step_start = time.time()
try:
    import scrap_reports_gui
    print(f"   ✓ scrap_reports_gui: {time.time() - step_start:.3f}s")
except Exception as e:
    print(f"   ✗ scrap_reports_gui: {e}")

step_start = time.time()
try:
    import coating_gui
    print(f"   ✓ coating_gui: {time.time() - step_start:.3f}s")
except Exception as e:
    print(f"   ✗ coating_gui: {e}")

step_start = time.time()
try:
    import product_checks_gui
    print(f"   ✓ product_checks_gui: {time.time() - step_start:.3f}s")
except Exception as e:
    print(f"   ✗ product_checks_gui: {e}")

step_start = time.time()
try:
    import guests_gui
    print(f"   ✓ guests_gui: {time.time() - step_start:.3f}s")
except Exception as e:
    print(f"   ✗ guests_gui: {e}")

step_start = time.time()
try:
    import guests_report_generator
    print(f"   ✓ guests_report_generator: {time.time() - step_start:.3f}s")
except Exception as e:
    print(f"   ✗ guests_report_generator: {e}")

print()

# Timing totale
total_time = time.time() - total_start
print("=" * 80)
print(f"⏱️  TEMPO TOTALE IMPORT: {total_time:.3f}s")
print("=" * 80)
print()

# Analisi
print("📊 ANALISI:")
if total_time < 2:
    print("   ✅ Import veloci (< 2s)")
elif total_time < 5:
    print("   ⚠️  Import moderati (2-5s) - Considerare lazy loading")
else:
    print("   ❌ Import lenti (> 5s) - LAZY LOADING NECESSARIO!")

print()
print("💡 RACCOMANDAZIONI:")
print("   1. Moduli che impiegano > 0.5s dovrebbero usare lazy loading")
print("   2. Importa solo quando l'utente apre la finestra specifica")
print("   3. Usa 'import module' invece di 'from module import *'")
print()
