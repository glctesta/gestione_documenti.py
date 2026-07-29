# updater.spec — builds updater as --onedir (no temp extraction = no hang)
# Output: dist/updater/ — updater.exe + le sue dipendenze SENZA la sottocartella
# '_internal' (contents_directory='.' le mette accanto all'exe). Va posizionato
# dentro _internal/updater/ dell'app principale.

block_cipher = None

a = Analysis(
    ['updater.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter', 'tkinter.ttk', 'tkinter.messagebox'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pyodbc', 'config_manager', 'email_connector'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='updater',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,    # MUST be True — console=False breaks tkinter silently on some Windows configs
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    contents_directory='.',   # niente sottocartella '_internal': dipendenze accanto a updater.exe
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='updater',
)
