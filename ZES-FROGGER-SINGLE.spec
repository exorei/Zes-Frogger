# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

# Collect data files for tkinterdnd2
tkinterdnd2_datas = collect_data_files('tkinterdnd2')

a = Analysis(
    ['ZES-FROGGER-SINGLE.py'],
    pathex=[],
    binaries=[],
    datas=tkinterdnd2_datas,
    hiddenimports=['tkinterdnd2'],
    hookspath=['.'],  # Specify the path to the hook file
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
    name='ZES-FROGGER-SINGLE',
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
    icon=['frogger.ico'],
)
