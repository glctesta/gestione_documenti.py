import os, sys

# Trova automaticamente le directory Tcl/Tk
_python_base = os.path.dirname(sys.executable)
_tcl_root = os.path.join(_python_base, 'tcl')
if not os.path.isdir(_tcl_root):
    _tcl_root = r'C:\Users\gtesta\AppData\Local\Programs\Python\Python311\tcl'

_tcl_data = []
for _d in ('tcl8.6', 'tk8.6'):
    _p = os.path.join(_tcl_root, _d)
    if os.path.isdir(_p):
        _tcl_data.append((_p, _d))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('updater.exe', '.'),
        ('logo.png', '.'),
        ('logo.ico', '.'),
        ('DejaVuSans.ttf', '.'),
        ('DejaVuSans-Bold.ttf', '.'),
    ] + _tcl_data,
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='DocumentManagement',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo.ico'],
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
