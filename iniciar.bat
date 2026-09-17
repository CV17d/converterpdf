@echo off
title DocuMorph - Suite de Conversion de Documentos
color 0b

echo ========================================================
echo        DOCUMORPH - SUITE DE CONVERSION DE DOCUMENTOS
echo ========================================================
echo.

python -c "import flask, pdf2docx, fitz" >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Se detectaron dependencias pendientes.
    echo Instalando automaticamente dependencias requeridas...
    echo.
    python -m pip install -r requirements.txt
    echo.
)

echo Iniciando servidor local y abriendo interfaz en el navegador...
echo http://127.0.0.1:5000
echo.
python app.py
pause
