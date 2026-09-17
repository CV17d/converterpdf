@echo off
title Instalador - DocuMorph Converter Suite
color 0a

echo ========================================================
echo       INSTALADOR DE DEPENDENCIAS - DOCUMORPH
echo ========================================================
echo.
echo Verificando Python en tu sistema...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] No se encontro Python instalado.
    echo Por favor descarga e instala Python desde https://www.python.org/
    echo Asegurate de marcar la casilla "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b 1
)

echo [OK] Python detectado correctamente.
echo.
echo Instalando todas las librerias necesarias...
echo Esto puede tomar 1 o 2 minutos en la primera ejecucion...
echo.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ========================================================
echo   INSTALACION COMPLETADA EXITOSAMENTE
echo ========================================================
echo Ya puedes iniciar la aplicacion haciendo doble clic en "iniciar.bat"
echo.
pause
