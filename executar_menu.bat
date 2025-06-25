@echo off
echo ==========================================
echo    SISTEMA SiCoPluE - MENU PRINCIPAL
echo ==========================================
echo.
echo Iniciando sistema...
echo.

cd /d "%~dp0"
call .venv\Scripts\activate.bat
.venv\Scripts\python.exe menu_principal.py
pause
