@echo off
title DocuMorph - Suite de Conversion de Documentos
color 0b

echo ========================================================
echo        DOCUMORPH - SUITE DE CONVERSION DE DOCUMENTOS
echo ========================================================
echo.

python -c "import flask, pdf2docx, fitz, webview" >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Se detectaron dependencias pendientes.
    echo Instalando dependencias requeridas...
    echo.
    python -m pip install -r requirements.txt
    echo.
)

echo Abriendo aplicacion de escritorio DocuMorph...
echo.
python main_gui.py
if %errorlevel% neq 0 (
    echo Iniciando modo navegador web...
    python app.py
)
pause
