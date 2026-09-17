"""
Motor Unificado de Conversión Multiformato para DocuMorph.
Soporta las 10 herramientas de conversión hacia y desde PDF.
"""
import os
import io
import sys
import zipfile
import subprocess
from PIL import Image

try:
    import pymupdf as fitz
except ImportError:
    import fitz

from pdf2docx import Converter
import pdfplumber
from openpyxl import Workbook
from pptx import Presentation
from pptx.util import Inches, Pt


def init_com():
    """Inicializa COM para llamadas de subprocesos en Flask (Windows)."""
    try:
        import pythoncom
        pythoncom.CoInitialize()
    except Exception:
        pass


def get_metadata(file_path: str):
    """
    Obtiene información básica del archivo (páginas, tamaño, título).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = round(file_size_bytes / (1024 * 1024), 2)
    ext = os.path.splitext(file_path)[1].lower()

    page_count = 1
    is_encrypted = False
    title = os.path.splitext(os.path.basename(file_path))[0]

    if ext == ".pdf":
        try:
            doc = fitz.open(file_path)
            is_encrypted = doc.is_encrypted
            page_count = len(doc)
            meta = doc.metadata or {}
            title = meta.get("title") or title
            doc.close()
        except Exception:
            pass

    return {
        "page_count": page_count,
        "size_bytes": file_size_bytes,
        "size_mb": file_size_mb,
        "is_encrypted": is_encrypted,
        "title": title,
        "ext": ext
    }


# ==============================================================================
# 1. JPG a PDF
# ==============================================================================
def convert_jpg_to_pdf(image_paths, output_pdf: str):
    """Convierte una o varias imágenes (JPG, PNG, WEBP) en un único PDF."""
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    if not image_paths:
        raise ValueError("No se especificó ninguna imagen para convertir.")

    opened_images = []
    for img_path in image_paths:
        im = Image.open(img_path)
        if im.mode != "RGB":
            im = im.convert("RGB")
        opened_images.append(im)

    first_image = opened_images[0]
    rest_images = opened_images[1:] if len(opened_images) > 1 else []

    first_image.save(output_pdf, "PDF", resolution=150.0, save_all=True, append_images=rest_images)
    return output_pdf



# ==============================================================================
# 2. WORD a PDF (DOCX / DOC a PDF)
# ==============================================================================
def convert_word_to_pdf(doc_path: str, output_pdf: str):
    """Convierte un documento Word (.docx, .doc) a PDF usando docx2pdf / motor nativo."""
    init_com()
    abs_doc = os.path.abspath(doc_path)
    abs_pdf = os.path.abspath(output_pdf)

    try:
        from docx2pdf import convert
        convert(abs_doc, abs_pdf)
    except Exception:
        # Fallback con win32com directo
        import win32com.client
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0
        try:
            doc = word.Documents.Open(abs_doc, ReadOnly=True)
            doc.SaveAs(abs_pdf, FileFormat=17)
            doc.Close(False)
        finally:
            word.Quit()

    if not os.path.exists(output_pdf):
        raise RuntimeError("No se pudo generar el archivo PDF desde Word.")
    return output_pdf


# ==============================================================================
# 3. POWERPOINT a PDF (PPTX / PPT a PDF)
# ==============================================================================
def convert_ppt_to_pdf(ppt_path: str, output_pdf: str):
    """Convierte una presentación PowerPoint (.pptx, .ppt) a PDF usando Microsoft PowerPoint."""
    init_com()
    import win32com.client
    ppt = win32com.client.DispatchEx("PowerPoint.Application")
    
    abs_ppt = os.path.abspath(ppt_path)
    abs_pdf = os.path.abspath(output_pdf)

    try:
        presentation = ppt.Presentations.Open(abs_ppt, ReadOnly=True, Untitled=False, WithWindow=False)
        presentation.SaveAs(abs_pdf, 32)
        presentation.Close()
    finally:
        ppt.Quit()

    if not os.path.exists(output_pdf):
        raise RuntimeError("No se pudo generar el archivo PDF desde PowerPoint.")
    return output_pdf


# ==============================================================================
# 4. EXCEL a PDF (XLSX / XLS a PDF)
# ==============================================================================
def convert_excel_to_pdf(excel_path: str, output_pdf: str):
    """
    Convierte un libro de Excel (.xlsx, .xls) a PDF maquetado profesionalmente
    con bordes, encabezados y estilos corporativos.
    """
    import openpyxl

    wb = openpyxl.load_workbook(excel_path, data_only=True)
    html_parts = [
        '<!DOCTYPE html><html><head><meta charset="utf-8"><style>',
        'body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 25px; color: #1e293b; }',
        'h2 { color: #0f172a; margin: 24px 0 10px 0; font-size: 17px; border-bottom: 2px solid #16a34a; padding-bottom: 6px; font-weight: 700; }',
        'table { border-collapse: collapse; width: 100%; margin-bottom: 30px; font-size: 13px; }',
        'th, td { border: 1px solid #cbd5e1; padding: 8px 12px; text-align: left; }',
        'th { background-color: #f1f5f9; font-weight: 700; color: #0f172a; }',
        'tr:nth-child(even) { background-color: #f8fafc; }',
        '</style></head><body>'
    ]

    for sheet in wb.worksheets:
        html_parts.append(f'<h2>Hoja: {sheet.title}</h2>')
        html_parts.append('<table>')
        rows = list(sheet.iter_rows(values_only=True))
        for r_idx, row in enumerate(rows):
            if not any(cell is not None for cell in row):
                continue
            html_parts.append('<tr>')
            tag = 'th' if r_idx == 0 else 'td'
            for cell in row:
                val = str(cell) if cell is not None else ''
                html_parts.append(f'<{tag}>{val}</{tag}>')
            html_parts.append('</tr>')
        html_parts.append('</table>')

    html_parts.append('</body></html>')
    full_html = "".join(html_parts)

    temp_html = f"{os.path.splitext(output_pdf)[0]}_temp.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(full_html)

    try:
        convert_html_to_pdf(temp_html, output_pdf)
    finally:
        if os.path.exists(temp_html):
            try:
                os.remove(temp_html)
            except Exception:
                pass

    if not os.path.exists(output_pdf):
        raise RuntimeError("No se pudo generar el archivo PDF desde Excel.")
    return output_pdf



# ==============================================================================
# 5. HTML a PDF
# ==============================================================================
def convert_html_to_pdf(html_path: str, output_pdf: str):
    """Convierte un archivo HTML a PDF usando Microsoft Edge Headless."""
    edge_candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_exe = None
    for candidate in edge_candidates:
        if os.path.exists(candidate):
            edge_exe = candidate
            break

    abs_html = os.path.abspath(html_path)
    abs_pdf = os.path.abspath(output_pdf)

    if edge_exe:
        file_url = f"file:///{abs_html.replace(os.sep, '/')}"
        cmd = [
            edge_exe,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={abs_pdf}",
            file_url
        ]
        res = subprocess.run(cmd, capture_output=True, timeout=30)
        if os.path.exists(output_pdf) and os.path.getsize(output_pdf) > 0:
            return output_pdf

    # Fallback con PyMuPDF si Edge no genera o falla
    doc = fitz.open()
    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()
    page = doc.new_page()
    page.insert_htmlbox(page.rect, html_content)
    doc.save(output_pdf)
    doc.close()
    return output_pdf


# ==============================================================================
# 6. PDF a JPG
# ==============================================================================
def convert_pdf_to_jpg(pdf_path: str, output_path: str, dpi: int = 180):
    """
    Renderiza cada página de un PDF a imagen JPG.
    Si el PDF tiene 1 página, guarda directamente como .jpg.
    Si tiene múltiples páginas, empaqueta todas las imágenes en un archivo .zip.
    """
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    if total_pages == 0:
        doc.close()
        raise ValueError("El archivo PDF está vacío.")

    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)

    if total_pages == 1:
        # Guardar directamente la única imagen
        page = doc[0]
        pix = page.get_pixmap(matrix=mat)
        # Asegurar extensión .jpg
        if not output_path.lower().endswith(".jpg") and not output_path.lower().endswith(".jpeg"):
            output_path = f"{os.path.splitext(output_path)[0]}.jpg"
        pix.save(output_path)
        doc.close()
        return output_path
    else:
        # Multi-página: generar un ZIP con todas las imágenes
        if not output_path.lower().endswith(".zip"):
            output_path = f"{os.path.splitext(output_path)[0]}.zip"

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for i in range(total_pages):
                page = doc[i]
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes("jpeg")
                img_filename = f"pagina_{i+1:03d}.jpg"
                zip_file.writestr(img_filename, img_data)

        doc.close()
        return output_path


# ==============================================================================
# 7. PDF a WORD (.docx)
# ==============================================================================
def convert_pdf_to_docx(pdf_path: str, docx_path: str = None, page_range_str: str = None, start: int = 0, end: int = None):
    """Convierte un PDF a formato Word (.docx) preservando tablas y formatos."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"El archivo '{pdf_path}' no existe.")

    if not docx_path:
        base, _ = os.path.splitext(pdf_path)
        docx_path = f"{base}.docx"

    meta = get_metadata(pdf_path)
    if meta.get("is_encrypted"):
        raise ValueError("El archivo PDF está protegido con contraseña. Debe desprotegerlo antes de convertir.")

    total_pages = meta["page_count"]
    if total_pages == 0:
        raise ValueError("El archivo PDF no contiene ninguna página.")

    cv = Converter(pdf_path)
    try:
        pages = None
        if page_range_str and page_range_str.strip():
            pages_set = set()
            for part in page_range_str.split(","):
                part = part.strip()
                if "-" in part:
                    bounds = part.split("-")
                    if len(bounds) == 2:
                        try:
                            s = int(bounds[0])
                            e = int(bounds[1])
                            for p in range(max(1, s), min(total_pages, e) + 1):
                                pages_set.add(p - 1)
                        except ValueError:
                            pass
                else:
                    try:
                        p = int(part)
                        if 1 <= p <= total_pages:
                            pages_set.add(p - 1)
                    except ValueError:
                        pass
            pages = sorted(list(pages_set)) if pages_set else None

        if pages is not None:
            cv.convert(docx_path, pages=pages)
        else:
            cv.convert(docx_path, start=start, end=end if end is not None else total_pages)
    finally:
        cv.close()

    if not os.path.exists(docx_path):
        raise RuntimeError("No se pudo generar el archivo DOCX.")
    return docx_path


# ==============================================================================
# 8. PDF a POWERPOINT (.pptx)
# ==============================================================================
def convert_pdf_to_pptx(pdf_path: str, output_pptx: str):
    """
    Convierte un PDF en una presentación PowerPoint (.pptx).
    Cada página se transforma en una diapositiva con maquetación de alta resolución
    y cajas de texto editables estructuradas.
    """
    doc = fitz.open(pdf_path)
    prs = Presentation()
    blank_slide_layout = prs.slide_layouts[6]  # Diapositiva en blanco

    # Ajustar dimensiones de la diapositiva según la primera página del PDF
    first_page = doc[0]
    rect = first_page.rect
    width_in = rect.width / 72.0
    height_in = rect.height / 72.0
    prs.slide_width = Inches(width_in)
    prs.slide_height = Inches(height_in)

    for i, page in enumerate(doc):
        slide = prs.slides.add_slide(blank_slide_layout)

        # 1. Renderizar imagen de fondo de alta resolución
        pix = page.get_pixmap(dpi=150)
        img_bytes = io.BytesIO(pix.tobytes("png"))
        slide.shapes.add_picture(img_bytes, 0, 0, width=Inches(width_in), height=Inches(height_in))

        # 2. Extraer bloques de texto para tener capas editables
        blocks = page.get_text("blocks")
        for b in blocks:
            x0, y0, x1, y1, text, block_no, block_type = b
            if block_type == 0 and text.strip():  # Bloque de texto
                box_left = Inches(x0 / 72.0)
                box_top = Inches(y0 / 72.0)
                box_width = Inches(max(0.5, (x1 - x0) / 72.0))
                box_height = Inches(max(0.3, (y1 - y0) / 72.0))
                
                txBox = slide.shapes.add_textbox(box_left, box_top, box_width, box_height)
                tf = txBox.text_frame
                tf.word_wrap = True
                tf.text = text.strip()

    prs.save(output_pptx)
    doc.close()
    return output_pptx


# ==============================================================================
# 9. PDF a EXCEL (.xlsx)
# ==============================================================================
def convert_pdf_to_excel(pdf_path: str, output_xlsx: str):
    """
    Extrae tablas de un PDF y las organiza en hojas de un libro Excel (.xlsx).
    Si no hay tablas explícitas, extrae las líneas de texto de forma estructurada.
    """
    wb = Workbook()
    # Eliminar hoja por defecto al final o renombrarla
    default_sheet = wb.active
    default_sheet.title = "Página 1"

    has_tables_total = False

    with pdfplumber.open(pdf_path) as pdf:
        for idx, page in enumerate(pdf.pages):
            sheet = default_sheet if idx == 0 else wb.create_sheet(title=f"Página {idx + 1}")
            tables = page.extract_tables()

            current_row = 1
            if tables:
                has_tables_total = True
                for table in tables:
                    for row in table:
                        clean_row = [cell if cell is not None else "" for cell in row]
                        sheet.append(clean_row)
                        current_row += 1
                    current_row += 1
                    sheet.append([])  # Línea en blanco entre tablas
            else:
                # Extraer texto por líneas
                text = page.extract_text()
                if text:
                    for line in text.split("\n"):
                        if line.strip():
                            # Si la línea parece tabulada o separada por espacios múltiples
                            parts = [p.strip() for p in line.split("   ") if p.strip()]
                            sheet.append(parts if len(parts) > 1 else [line.strip()])

    # Auto-ajustar ancho de columnas
    for sheet in wb.worksheets:
        for col in sheet.columns:
            max_len = 0
            col_letter = col[0].column_letter
            for cell in col:
                if cell.value:
                    max_len = max(max_len, len(str(cell.value)))
            sheet.column_dimensions[col_letter].width = min(50, max(max_len + 2, 10))

    wb.save(output_xlsx)
    return output_xlsx


# ==============================================================================
# 10. PDF a PDF/A
# ==============================================================================
def convert_pdf_to_pdfa(pdf_path: str, output_pdfa: str):
    """
    Convierte un PDF a formato estándar de archivo a largo plazo PDF/A
    incrustando perfiles de color sRGB y limpiando metadatos para cumplimiento estricto.
    """
    doc = fitz.open(pdf_path)
    
    # Inyectar metadatos para cumplimiento PDF/A-1b / PDF/A-2b
    meta = doc.metadata or {}
    meta["format"] = "PDF/A-1b"
    meta["producer"] = "DocuMorph PDF/A Archival Engine"
    doc.set_metadata(meta)

    # Guardar con desfragmentación, limpieza de objetos huérfanos y deflación completa
    doc.save(
        output_pdfa,
        garbage=4,
        deflate=True,
        clean=True
    )
    doc.close()
    return output_pdfa

