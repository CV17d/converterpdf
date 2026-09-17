#!/bin/bash
echo "========================================================"
echo "       DOCUMORPH - SUITE DE CONVERSIÓN DE DOCUMENTOS"
echo "========================================================"
echo ""

if ! python3 -c "import flask, pdf2docx, fitz" &> /dev/null; then
    echo "[AVISO] Instalando dependencias requeridas..."
    pip3 install -r requirements.txt
fi

echo "Iniciando servidor local en http://127.0.0.1:5000..."
python3 app.py
