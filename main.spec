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
    'updater.exe'  # Updater per aggiornamenti automatici
]

for file in files_to_include:
    if os.path.exists(file):
        datas_list.append((file, '.'))

# Aggiungi la directory npi se esiste
if os.path.exists('npi'):
    datas_list.append(('npi', 'npi'))

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
    ],
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
