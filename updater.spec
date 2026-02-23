# -*- mode: python ; coding: utf-8 -*-
# updater.spec – PyInstaller spec per updater.exe
# Aggiornato per includere le dipendenze del sistema di ticketing automatico.

import os

_PROJECT = os.path.abspath('.')

a = Analysis(
    ['updater.py'],
    pathex=[_PROJECT],
    binaries=[],
    datas=[
        # Credenziali cifrate necessarie per lettura email destinataria dal DB
        ('encryption_key.key', '.'),
        ('db_config.enc',      '.'),
        # Credenziali email per EmailSender
        ('email_credentials.enc', '.'),
    ],
    hiddenimports=[
        # Ticketing / email
        'email_connector',
        'config_manager',
        # pyodbc – per lettura email destinataria dal DB
        'pyodbc',
        # Pillow – screenshot (opzionale)
        'PIL',
        'PIL.ImageGrab',
        'PIL.Image',
        # Cryptography – usata da email_connector e config_manager
        'cryptography',
        'cryptography.fernet',
        # SMTP
        'smtplib',
        'email',
        'email.mime',
        'email.mime.multipart',
        'email.mime.text',
        'email.mime.base',
        'email.mime.image',
        'email.encoders',
        # Standard
        'json',
        'threading',
        'traceback',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='updater',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo.ico'],
)
