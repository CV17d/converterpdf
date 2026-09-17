"""
Herramienta de Línea de Comandos (CLI) para convertir PDF a Word (.docx).
Uso:
    python cli.py documento.pdf
    python cli.py documento.pdf -o salida.docx
    python cli.py documento.pdf --pages 1-5,8
"""
import sys
import argparse
import os
import time
from converter import convert_pdf_to_docx, get_pdf_metadata


def main():
    parser = argparse.ArgumentParser(
        description="Convertidor profesional de PDF a Microsoft Word (.docx)"
    )
    parser.add_argument("pdf", help="Ruta al archivo PDF a convertir")
    parser.add_argument("-o", "--output", help="Ruta del archivo .docx de salida (opcional)", default=None)
    parser.add_argument("-p", "--pages", help="Rango de páginas a convertir, ej: '1-3,5' (opcional)", default=None)

    args = parser.parse_args()

    if not os.path.exists(args.pdf):
        print(f"\n[ERROR] El archivo '{args.pdf}' no existe.\n")
        sys.exit(1)

    try:
        print("\n==============================================")
        print("     CONVERTIDOR DE PDF A WORD (.DOCX)        ")
        print("==============================================")
        print(f"Analizando: {os.path.basename(args.pdf)}")
        
        meta = get_pdf_metadata(args.pdf)
        print(f"- Páginas totales: {meta['page_count']}")
        print(f"- Tamaño: {meta['size_mb']} MB")
        if args.pages:
            print(f"- Páginas seleccionadas: {args.pages}")
        else:
            print("- Convirtiendo todas las páginas...")

        start_time = time.time()
        print("\nProcesando y generando documento Word...")
        docx_file = convert_pdf_to_docx(args.pdf, args.output, page_range_str=args.pages)
        elapsed = round(time.time() - start_time, 2)

        print("\n[OK] ¡Conversión completada con éxito!")
        print(f"Archivo generado: {docx_file}")
        print(f"Tiempo transcurrido: {elapsed} segundos")
        print("==============================================\n")
    except Exception as e:
        print(f"\n[ERROR] Ocurrió un error al convertir: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
