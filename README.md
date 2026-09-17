# DocuMorph - Convertidor de PDF a Word (.docx)

Herramienta profesional y privada para convertir archivos PDF a documentos de Microsoft Word editables (.docx). Reconstruye párrafos, fuentes, formatos, tablas e imágenes de forma 100% local.

---

## Modos de Uso

### 1. Interfaz Web (Recomendado)
Puedes iniciar la interfaz web de dos formas:

- **Con un clic (Windows)**: Haz doble clic en el archivo `iniciar.bat`.
- **Desde la terminal**:
  ```bash
  python app.py
  ```
El navegador se abrirá automáticamente en `http://127.0.0.1:5000`.

#### Características de la Web:
- **Arrastrar y soltar (Drag & Drop)**: Arrastra cualquier archivo PDF al área señalada.
- **Rango de Páginas**: Puedes convertir todo el documento o elegir páginas específicas (ej. `1-3, 5`).
- **Barra de Progreso y Estados en Vivo**: Visualiza cada paso del proceso de análisis y reconstrucción.
- **Modo Oscuro / Claro**: Cambia el tema con el botón superior derecho.
- **Historial de Sesión**: Descarga de nuevo cualquier archivo convertido durante la sesión.

---

### 2. Línea de Comandos (CLI)
Para conversiones rápidas desde PowerShell o CMD:

```bash
# Conversión básica (genera archivo con el mismo nombre y extensión .docx)
python cli.py "documento.pdf"

# Especificar nombre o ruta de salida
python cli.py "documento.pdf" -o "salida.docx"

# Convertir solo páginas específicas (ejemplo: páginas 1 a 3 y página 5)
python cli.py "documento.pdf" --pages "1-3,5"
```

---

## Requisitos y Dependencias
Todas las dependencias están instaladas en tu entorno Python:
- `pdf2docx`
- `PyMuPDF`
- `python-docx`
- `Flask`
