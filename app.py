"""
Servidor Web Flask para Suite DocuMorph (10 Convertidores de Documentos).
"""
import os
import uuid
import time
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

import converter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max

TOOL_SPECS = {
    "jpg-to-pdf": {
        "name": "JPG a PDF",
        "accept": [".jpg", ".jpeg", ".png", ".webp"],
        "out_ext": ".pdf",
        "multiple": True
    },
    "word-to-pdf": {
        "name": "WORD a PDF",
        "accept": [".docx", ".doc"],
        "out_ext": ".pdf",
        "multiple": False
    },
    "ppt-to-pdf": {
        "name": "POWERPOINT a PDF",
        "accept": [".pptx", ".ppt"],
        "out_ext": ".pdf",
        "multiple": False
    },
    "excel-to-pdf": {
        "name": "EXCEL a PDF",
        "accept": [".xlsx", ".xls"],
        "out_ext": ".pdf",
        "multiple": False
    },
    "html-to-pdf": {
        "name": "HTML a PDF",
        "accept": [".html", ".htm"],
        "out_ext": ".pdf",
        "multiple": False
    },
    "pdf-to-jpg": {
        "name": "PDF a JPG",
        "accept": [".pdf"],
        "out_ext": ".jpg",
        "multiple": False
    },
    "pdf-to-word": {
        "name": "PDF a WORD",
        "accept": [".pdf"],
        "out_ext": ".docx",
        "multiple": False
    },
    "pdf-to-ppt": {
        "name": "PDF a POWERPOINT",
        "accept": [".pdf"],
        "out_ext": ".pptx",
        "multiple": False
    },
    "pdf-to-excel": {
        "name": "PDF a EXCEL",
        "accept": [".pdf"],
        "out_ext": ".xlsx",
        "multiple": False
    },
    "pdf-to-pdfa": {
        "name": "PDF a PDF/A",
        "accept": [".pdf"],
        "out_ext": ".pdf",
        "multiple": False
    },
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/info", methods=["POST"])
def inspect_file():
    """Inspecciona el archivo subido y devuelve información rápida."""
    if 'file' not in request.files:
        return jsonify({"error": "No se subió ningún archivo."}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío."}), 400

    unique_id = uuid.uuid4().hex[:8]
    safe_name = secure_filename(file.filename) or f"document_{unique_id}.bin"
    saved_filename = f"{unique_id}_{safe_name}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)
    file.save(file_path)

    try:
        meta = converter.get_metadata(file_path)
        return jsonify({
            "temp_id": saved_filename,
            "original_name": file.filename,
            "page_count": meta["page_count"],
            "size_mb": meta["size_mb"],
            "is_encrypted": meta.get("is_encrypted", False),
            "ext": meta.get("ext", "")
        })
    except Exception as e:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
        return jsonify({"error": f"Error al analizar archivo: {str(e)}"}), 400


@app.route("/api/convert", methods=["POST"])
def convert_document():
    """Ejecuta la conversión según la herramienta seleccionada."""
    tool_id = request.form.get("tool", "pdf-to-word").strip().lower()
    page_range = request.form.get("pages", "").strip()

    if tool_id not in TOOL_SPECS:
        return jsonify({"error": f"Herramienta desconocida: {tool_id}"}), 400

    spec = TOOL_SPECS[tool_id]
    uploaded_files = request.files.getlist("file")
    temp_id = request.form.get("temp_id")

    # Guardar archivos subidos
    input_paths = []
    original_base = "documento"

    if uploaded_files and len(uploaded_files) > 0 and uploaded_files[0].filename != '':
        for f in uploaded_files:
            if not f or f.filename == '':
                continue
            safe_name = secure_filename(f.filename) or f"file_{uuid.uuid4().hex[:6]}"
            saved_name = f"{uuid.uuid4().hex[:8]}_{safe_name}"
            saved_path = os.path.join(UPLOAD_DIR, saved_name)
            f.save(saved_path)
            input_paths.append(saved_path)
            original_base = os.path.splitext(f.filename)[0]
    elif temp_id:
        temp_path = os.path.join(UPLOAD_DIR, secure_filename(temp_id))
        if not os.path.exists(temp_path):
            return jsonify({"error": "El archivo temporal ha expirado o no existe."}), 404
        input_paths.append(temp_path)
        parts = os.path.basename(temp_path).split("_", 1)
        original_base = os.path.splitext(parts[1] if len(parts) > 1 else parts[0])[0]
    else:
        return jsonify({"error": "No se recibió ningún archivo para procesar."}), 400

    if not input_paths:
        return jsonify({"error": "No se encontraron archivos válidos para convertir."}), 400

    primary_input = input_paths[0]
    out_ext = spec["out_ext"]
    
    # Manejar nombres de salida
    unique_suffix = uuid.uuid4().hex[:6]
    clean_base = secure_filename(original_base) or "resultado"

    # Si PDF a JPG tiene múltiples páginas generará un .zip
    if tool_id == "pdf-to-jpg":
        meta = converter.get_metadata(primary_input)
        if meta.get("page_count", 1) > 1:
            out_ext = ".zip"

    if tool_id == "pdf-to-pdfa":
        clean_base = f"{clean_base}_pdfa"

    out_filename = f"{clean_base}_{unique_suffix}{out_ext}"
    out_filepath = os.path.join(OUTPUT_DIR, out_filename)

    start_time = time.time()

    try:
        if tool_id == "jpg-to-pdf":
            converter.convert_jpg_to_pdf(input_paths, out_filepath)
            download_friendly = f"{clean_base}.pdf"

        elif tool_id == "word-to-pdf":
            converter.convert_word_to_pdf(primary_input, out_filepath)
            download_friendly = f"{clean_base}.pdf"

        elif tool_id == "ppt-to-pdf":
            converter.convert_ppt_to_pdf(primary_input, out_filepath)
            download_friendly = f"{clean_base}.pdf"

        elif tool_id == "excel-to-pdf":
            converter.convert_excel_to_pdf(primary_input, out_filepath)
            download_friendly = f"{clean_base}.pdf"

        elif tool_id == "html-to-pdf":
            converter.convert_html_to_pdf(primary_input, out_filepath)
            download_friendly = f"{clean_base}.pdf"

        elif tool_id == "pdf-to-jpg":
            actual_out = converter.convert_pdf_to_jpg(primary_input, out_filepath)
            out_filename = os.path.basename(actual_out)
            out_ext = os.path.splitext(out_filename)[1].lower()
            download_friendly = f"{clean_base}{out_ext}"

        elif tool_id == "pdf-to-word":
            converter.convert_pdf_to_docx(primary_input, out_filepath, page_range_str=page_range)
            download_friendly = f"{clean_base}.docx"

        elif tool_id == "pdf-to-ppt":
            converter.convert_pdf_to_pptx(primary_input, out_filepath)
            download_friendly = f"{clean_base}.pptx"

        elif tool_id == "pdf-to-excel":
            converter.convert_pdf_to_excel(primary_input, out_filepath)
            download_friendly = f"{clean_base}.xlsx"

        elif tool_id == "pdf-to-pdfa":
            converter.convert_pdf_to_pdfa(primary_input, out_filepath)
            download_friendly = f"{clean_base}.pdf"

        else:
            raise ValueError(f"Herramienta no implementada: {tool_id}")

        elapsed = round(time.time() - start_time, 2)
        size_bytes = os.path.getsize(os.path.join(OUTPUT_DIR, out_filename))
        size_mb = round(size_bytes / (1024 * 1024), 2)

        return jsonify({
            "success": True,
            "filename": out_filename,
            "original_name": download_friendly,
            "download_url": f"/download/{out_filename}",
            "elapsed_seconds": elapsed,
            "size_mb": size_mb,
            "tool": tool_id
        })

    except Exception as e:
        return jsonify({"error": f"Error en la conversión: {str(e)}"}), 500


@app.route("/download/<filename>")
def download_file(filename):
    """Descarga de archivos procesados."""
    safe_name = secure_filename(filename)
    file_path = os.path.join(OUTPUT_DIR, safe_name)
    if not os.path.exists(file_path):
        return "El archivo no fue encontrado o ha expirado.", 404

    # Nombre limpio de descarga
    download_name = safe_name
    parts = safe_name.rsplit("_", 1)
    if len(parts) == 2:
        ext = os.path.splitext(safe_name)[1]
        download_name = f"{parts[0]}{ext}"

    return send_file(file_path, as_attachment=True, download_name=download_name)


def open_browser(port):
    time.sleep(1.2)
    webbrowser.open_new_tab(f"http://127.0.0.1:{port}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000, help="Puerto del servidor")
    parser.add_argument("--no-browser", action="store_true", help="No abrir navegador automáticamente")
    args = parser.parse_args()

    print(f"\n=======================================================")
    print(f" DocuMorph Suite activa en http://127.0.0.1:{args.port}")
    print(f" Presiona CTRL+C para detener el servidor")
    print(f"=======================================================\n")

    if not args.no_browser:
        Timer(1.0, open_browser, args=[args.port]).start()

    app.run(host="127.0.0.1", port=args.port, debug=False)
