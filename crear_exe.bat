@echo off
title Generador de Aplicacion de Escritorio (.exe) - DocuMorph
color 0b

echo ========================================================
echo   COMPILADOR DE APLICACION DE ESCRITORIO (.EXE)
echo ========================================================
echo.
echo 1. Verificando librerias de empaquetado...
python -m pip install pyinstaller pywebview

echo.
echo 2. Compilando aplicacion a ejecutable de escritorio nativo...
echo (Sin consola negra, con ventana nativa de PC)
echo.

python -m PyInstaller --name "DocuMorph" --noconfirm --onedir --windowed --clean --add-data "templates;templates" --add-data "static;static" main_gui.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] La compilacion fallo.
    pause
    exit /b 1
)

echo.
echo 3. Empaquetando ejecutable en archivo ZIP portable...
python -c "import shutil; shutil.make_archive('dist/DocuMorph_Windows', 'zip', 'dist/DocuMorph')"

echo.
echo ========================================================
echo   ¡COMPILACION COMPLETADA EXITOSAMENTE!
echo ========================================================
echo La aplicacion nativa (.exe) esta lista en:
echo dist\DocuMorph\DocuMorph.exe
echo.
echo El archivo ZIP portable listo para compartir en GitHub Releases:
echo dist\DocuMorph_Windows.zip
echo.
pause
