@echo off
title Generador de Ejecutable (.exe) - DocuMorph
color 0b

echo ========================================================
echo        COMPILADOR DE EJECUTABLE (.EXE) - DOCUMORPH
echo ========================================================
echo.
echo 1. Verificando PyInstaller...
python -m pip install pyinstaller

echo.
echo 2. Compilando aplicacion a ejecutable independiente...
echo Esto tomara entre 1 y 3 minutos...
echo.

python -m PyInstaller --name "DocuMorph" --noconfirm --onedir --clean --add-data "templates;templates" --add-data "static;static" app.py

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
echo   ¡COMPILACION COMPLETADA CON EXITO!
echo ========================================================
echo El ejecutable (.exe) se encuentra en:
echo carpeta: dist\DocuMorph\DocuMorph.exe
echo.
echo El archivo ZIP portable listo para compartir se encuentra en:
echo archivo: dist\DocuMorph_Windows.zip
echo.
pause
