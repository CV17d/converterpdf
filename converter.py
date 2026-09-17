"""
Motor de conversión de PDF a Word (.docx)
Utiliza pdf2docx para reconstrucción precisa de texto, tablas e imágenes.
"""
import os
try:
    import pymupdf as fitz
except ImportError:
    import fitz  # PyMuPDF fallback

from pdf2docx import Converter


def parse_page_ranges(range_str: str, total_pages: int):
    """
    Parsea una cadena como '1-3, 5, 7-10' a una lista de índices base-0.
    """
    if not range_str or range_str.strip() == "":
        return None  # Todas las páginas

    pages = set()
    parts = range_str.split(",")
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            bounds = part.split("-")
            if len(bounds) == 2:
                try:
                    start_p = int(bounds[0].strip())
                    end_p = int(bounds[1].strip())
                    for p in range(max(1, start_p), min(total_pages, end_p) + 1):
                        pages.add(p - 1)
                except ValueError:
                    pass
        else:
            try:
                p = int(part)
                if 1 <= p <= total_pages:
                    pages.add(p - 1)
            except ValueError:
                pass

    return sorted(list(pages)) if pages else None


def get_pdf_metadata(pdf_path: str):
    """
    Obtiene información básica del PDF (páginas, tamaño, título).
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No se encontró el archivo: {pdf_path}")

    file_size_bytes = os.path.getsize(pdf_path)
    file_size_mb = round(file_size_bytes / (1024 * 1024), 2)

    doc = fitz.open(pdf_path)
    is_encrypted = doc.is_encrypted
    page_count = len(doc)
    metadata = doc.metadata or {}
    title = metadata.get("title") or os.path.splitext(os.path.basename(pdf_path))[0]
    doc.close()

    return {
        "page_count": page_count,
        "size_bytes": file_size_bytes,
        "size_mb": file_size_mb,
        "is_encrypted": is_encrypted,
        "title": title
    }


def convert_pdf_to_docx(pdf_path: str, docx_path: str = None, page_range_str: str = None, start: int = 0, end: int = None):
    """
    Convierte un PDF a formato Word (.docx).
    
    :param pdf_path: Ruta al archivo PDF.
    :param docx_path: Ruta del archivo .docx de salida. Si es None, reemplaza la extensión por .docx.
    :param page_range_str: Cadena opcional como '1-3, 5'.
    :param start: Página inicial (base-0).
    :param end: Página final (base-0, exclusiva).
    :return: Ruta del archivo generado .docx.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"El archivo '{pdf_path}' no existe.")

    if not docx_path:
        base, _ = os.path.splitext(pdf_path)
        docx_path = f"{base}.docx"

    meta = get_pdf_metadata(pdf_path)
    if meta.get("is_encrypted"):
        raise ValueError("El archivo PDF está protegido con contraseña. Debe desprotegerlo antes de convertir.")

    total_pages = meta["page_count"]
    if total_pages == 0:
        raise ValueError("El archivo PDF no contiene ninguna página.")

    cv = Converter(pdf_path)
    try:
        pages = parse_page_ranges(page_range_str, total_pages)
        if pages is not None:
            # Convertir páginas específicas
            cv.convert(docx_path, pages=pages)
        else:
            # Convertir todas o rango start/end
            cv.convert(docx_path, start=start, end=end if end is not None else total_pages)
    finally:
        cv.close()

    if not os.path.exists(docx_path):
        raise RuntimeError("No se pudo generar el archivo DOCX.")

    return docx_path
