# -*- mode: python ; coding: utf-8 -*-

import os

# Trova tutti i file necessari
datas_list = []
files_to_include = [
    'Logo.png',
    'logo.png', 
    'Logo.ico',
    'DejaVuSans.ttf',
    'DejaVuSans-Bold.ttf',
    'Frigo_acclimate.jpg',
    'config.ini',
    'email_credentials.enc',
    'email_key.key',
    'db_config.enc',  # Configurazione database criptata
    'encryption_key.key',  # Chiave per decriptare db_config.enc
    'lang.conf',
    'zebra_printer_config.json',
    'Complains_numeration.json',  # File per numerazione reclami
    'npi_notifications_config.json',  # Configurazione notifiche automatiche NPI
    'updater.exe'  # mantenuto per compatibilità retroattiva - rimpiazzato da dist/updater/ onedir
]

for file in files_to_include:
    if os.path.exists(file):
        datas_list.append((file, '.'))

# Aggiungi directory Tcl/Tk (necessarie per tkinter nell'exe compilato)
import sys
_python_base = os.path.dirname(sys.executable)
_tcl_root = os.path.join(_python_base, 'tcl')
if not os.path.isdir(_tcl_root):
    _tcl_root = r'C:\Users\gtesta\AppData\Local\Programs\Python\Python311\tcl'
for _d in ('tcl8.6', 'tk8.6'):
    _p = os.path.join(_tcl_root, _d)
    if os.path.isdir(_p):
        datas_list.append((_p, _d))

# Aggiungi la directory npi se esiste
if os.path.exists('npi'):
    datas_list.append(('npi', 'npi'))

# Aggiungi la directory manuals (manuali PDF multilingua)
if os.path.exists('manuals'):
    datas_list.append(('manuals', 'manuals'))

# Aggiungi la directory docs (manuale NPI HTML)
if os.path.exists('docs'):
    datas_list.append(('docs', 'docs'))

# Aggiungi updater come onedir (NO onefile — evita estrazione in %TEMP% che fallisce dal parent frozen)
_updater_src = os.path.join('dist', 'updater')
if os.path.isdir(_updater_src):
    # Copia l'intera cartella dist/updater/ → _internal/updater/
    for _root, _dirs, _fnames in os.walk(_updater_src):
        for _fname in _fnames:
            _abs = os.path.join(_root, _fname)
            _rel_dir = os.path.relpath(_root, 'dist')
            datas_list.append((_abs, _rel_dir))
    print(f'[spec] Incluso updater onedir da {_updater_src}')
else:
    print(f'[spec] ATTENZIONE: {_updater_src} non trovato — eseguire: pyinstaller --noconfirm --clean updater.spec')

# Kit Dashboard web (Flask) + package kit_dashboard: hidden imports
from PyInstaller.utils.hooks import collect_submodules
_web_hidden = (
    collect_submodules('flask')
    + collect_submodules('werkzeug')
    + collect_submodules('jinja2')
    + collect_submodules('click')
    + [
        'markupsafe', 'blinker', 'itsdangerous',
        'requests', 'urllib3', 'certifi', 'idna', 'charset_normalizer',
        'kit_web_server',
        'kit_dashboard',
        'kit_dashboard.server_config',
        'kit_dashboard.planning',
        'kit_dashboard.eta',
        'kit_dashboard.sync_service',
        'kit_dashboard.web_data',
        'kit_dashboard.web_templates',
        'kit_dashboard.server_watcher',
        'kit_dashboard.controller',
        'install_kit_dashboard_autostart',  # self-install della Scheduled Task dall'exe
        'fai_autocheck',  # usato da kit_dashboard.planning per T:\Planning
    ]
)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas_list,
    hiddenimports=[
        'pyodbc',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'PIL.ImageOps',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'sqlalchemy',
        'sqlalchemy.pool',
        'packaging',
        'packaging.version',
        'tkcalendar',
        'pandas',
        'matplotlib',
        'reportlab',
        'reportlab.pdfgen',
        'reportlab.lib',
        'reportlab.lib.pagesizes',
        'reportlab.platypus',
        'reportlab.pdfbase.ttfonts',
        'reportlab.pdfbase.pdfmetrics',
        'fails_daily_email',
        'fails_analysis_gui',
        'shift_handover_monitor',
        'material_consumption_gui',
        'material_consumption_report',
        'fqc_products_gui',
        'fqc_email',
    ] + _web_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DocumentManagement',
    debug=True,  # Abilitato per debug
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Abilitata temporaneamente per vedere gli errori
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Logo.ico' if os.path.exists('Logo.ico') else None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DocumentManagement',
)
