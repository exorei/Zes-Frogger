@echo off
REM Create hook file for tkinterdnd2
echo from PyInstaller.utils.hooks import collect_data_files > hook-tkinterdnd2.py
echo datas = collect_data_files('tkinterdnd2') >> hook-tkinterdnd2.py

REM Run PyInstaller with the specified spec file
pyinstaller ZES-FROGGER-SINGLE.spec

REM Pause to keep the command window open
pause
