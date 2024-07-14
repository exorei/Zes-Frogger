@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

echo Running check_and_install_dependencies.py...
python check_and_install_dependencies.py
IF %ERRORLEVEL% NEQ 0 (
    echo There was an error running check_and_install_dependencies.py. Exiting...
    pause
    EXIT /B 1
)

echo.
echo All dependencies are installed. Proceeding with compilation...
echo.

REM Create hook file for tkinterdnd2
echo Creating hook file for tkinterdnd2...
echo from PyInstaller.utils.hooks import collect_data_files > hook-tkinterdnd2.py
echo datas = collect_data_files('tkinterdnd2') >> hook-tkinterdnd2.py

REM Create the spec file if it does not exist
IF NOT EXIST "ZES-FROGGER-SINGLE.spec" (
    echo Creating spec file...
    (
        echo ^# -*- mode: python ; coding: utf-8 -*-
        echo from PyInstaller.utils.hooks import collect_data_files
        echo tkinterdnd2_datas = collect_data_files('tkinterdnd2')
        echo
        echo a = Analysis(
        echo     ['ZES-FROGGER-SINGLE.py'],
        echo     pathex=[],
        echo     binaries=[],
        echo     datas=tkinterdnd2_datas,
        echo     hiddenimports=['tkinterdnd2'],
        echo     hookspath=['.'],  ^# Specify the path to the hook file
        echo     hooksconfig={},
        echo     runtime_hooks=[],
        echo     excludes=[],
        echo     noarchive=False,
        echo     optimize=0,
        echo )
        echo pyz = PYZ(a.pure)
        echo
        echo exe = EXE(
        echo     pyz,
        echo     a.scripts,
        echo     a.binaries,
        echo     a.datas,
        echo     [],
        echo     name='ZES-FROGGER-SINGLE',
        echo     debug=False,
        echo     bootloader_ignore_signals=False,
        echo     strip=False,
        echo     upx=True,
        echo     upx_exclude=[],
        echo     runtime_tmpdir=None,
        echo     console=False,
        echo     disable_windowed_traceback=False,
        echo     argv_emulation=False,
        echo     target_arch=None,
        echo     codesign_identity=None,
        echo     entitlements_file=None,
        echo     icon=['frogger.ico'],
        echo )
    ) > ZES-FROGGER-SINGLE.spec
)

REM Run PyInstaller with the specified spec file
echo Running PyInstaller...
pyinstaller ZES-FROGGER-SINGLE.spec
IF %ERRORLEVEL% NEQ 0 (
    echo PyInstaller failed. Exiting...
    pause
    EXIT /B 1
)

echo Build completed. Press any key to exit...
pause
EXIT /B 0
