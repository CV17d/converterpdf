"""
Servidor Web Flask para Convertidor de PDF a Word.
"""
import os
import uuid
import time
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from converter import convert_pdf_to_docx, get_pdf_metadata

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 150 * 1024 * 1024  # 150MB max upload


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/info", methods=["POST"])
def inspect_pdf():
    """
    Inspecciona el PDF subido para obtener metadatos rápidos (número de páginas, tamaño).
    """
    if 'file' not in request.files:
        return jsonify({"error": "No se subió ningún archivo."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío."}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "El archivo debe tener extensión .pdf"}), 400

    unique_id = uuid.uuid4().hex[:8]
    safe_name = secure_filename(file.filename)
    saved_filename = f"{unique_id}_{safe_name}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)
    file.save(file_path)

    try:
        meta = get_pdf_metadata(file_path)
        return jsonify({
            "temp_id": saved_filename,
            "original_name": file.filename,
            "page_count": meta["page_count"],
            "size_mb": meta["size_mb"],
            "is_encrypted": meta["is_encrypted"]
        })
    except Exception as e:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
        return jsonify({"error": f"Error al leer PDF: {str(e)}"}), 400


@app.route("/api/convert", methods=["POST"])
def convert_pdf():
    """
    Convierte el PDF a Word (.docx).
    Acepta o bien un archivo directamente o el 'temp_id' de una inspección previa.
    """
    page_range = request.form.get("pages", "").strip()
    pdf_path = None
    original_base = "documento"

    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        safe_name = secure_filename(file.filename)
        if not safe_name.lower().endswith(".pdf"):
            return jsonify({"error": "El archivo debe ser un PDF válido."}), 400
        unique_id = uuid.uuid4().hex[:8]
        saved_filename = f"{unique_id}_{safe_name}"
        pdf_path = os.path.join(UPLOAD_DIR, saved_filename)
        file.save(pdf_path)
        original_base = os.path.splitext(file.filename)[0]
    elif 'temp_id' in request.form:
        temp_id = request.form.get('temp_id')
        pdf_path = os.path.join(UPLOAD_DIR, secure_filename(temp_id))
        if not os.path.exists(pdf_path):
            return jsonify({"error": "El archivo temporal expiró o no existe."}), 404
        # Extraer nombre original sin prefijo uuid
        parts = os.path.basename(pdf_path).split("_", 1)
        original_base = os.path.splitext(parts[1] if len(parts) > 1 else parts[0])[0]
    else:
        return jsonify({"error": "No se proporcionó ningún archivo para convertir."}), 400

    out_docx_name = f"{secure_filename(original_base)}_{uuid.uuid4().hex[:6]}.docx"
    out_docx_path = os.path.join(OUTPUT_DIR, out_docx_name)

    start_time = time.time()
    try:
        convert_pdf_to_docx(pdf_path, out_docx_path, page_range_str=page_range if page_range else None)
        elapsed = round(time.time() - start_time, 2)
        docx_size_mb = round(os.path.getsize(out_docx_path) / (1024 * 1024), 2)

        return jsonify({
            "success": True,
            "filename": out_docx_name,
            "original_name": f"{original_base}.docx",
            "download_url": f"/download/{out_docx_name}",
            "elapsed_seconds": elapsed,
            "size_mb": docx_size_mb
        })
    except Exception as e:
        return jsonify({"error": f"Error en la conversión: {str(e)}"}), 500


@app.route("/download/<filename>")
def download_file(filename):
    """
    Permite descargar el archivo Word generado.
    """
    safe_name = secure_filename(filename)
    file_path = os.path.join(OUTPUT_DIR, safe_name)
    if not os.path.exists(file_path):
        return "El archivo no fue encontrado o ha expirado.", 404

    # Determinar nombre amigable de descarga
    download_name = safe_name
    parts = safe_name.rsplit("_", 1)
    if len(parts) == 2 and parts[1].endswith(".docx"):
        download_name = f"{parts[0]}.docx"

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
    print(f" Invocando Convertidor PDF a Word en http://127.0.0.1:{args.port}")
    print(f" Presiona CTRL+C para detener el servidor")
    print(f"=======================================================\n")

    if not args.no_browser:
        Timer(1.0, open_browser, args=[args.port]).start()

    app.run(host="127.0.0.1", port=args.port, debug=False)
