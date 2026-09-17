# DocuMorph - Suite Profesional de Conversión de Documentos (10 en 1)

Convertidor de documentos y PDFs 100% local, privado, sin límites de tamaño y sin marcas de agua. Toda la conversión se procesa directamente en tu ordenador.

---

## 🚀 Inicio Rápido (Para cualquier persona que clone el repo)

### Requisito previo
Tener **Python 3.10 o superior** instalado ([Descargar Python](https://www.python.org/downloads/)).
> *Nota: Al instalar Python en Windows, asegúrate de marcar la casilla **"Add Python to PATH"**.*

---

### Paso a paso para usarlo:

#### 1. Clonar el repositorio
Abre tu terminal (PowerShell, CMD o Terminal) y escribe:
```bash
git clone https://github.com/CV17d/converterpdf.git
cd converterpdf
```

#### 2. Iniciar el proyecto

* **En Windows (Recomendado - 1 Clic):**
  Solo haz doble clic en el archivo **`iniciar.bat`**.
  *(El script detectará automáticamente si necesitas instalar las librerías, las instalará y abrirá tu navegador web).*

* **Desde la terminal (Windows, Mac o Linux):**
  ```bash
  # 1. Instalar librerías
  pip install -r requirements.txt

  # 2. Iniciar la aplicación
  python app.py
  ```

¡Listo! Tu navegador se abrirá automáticamente en:
👉 **`http://127.0.0.1:5000`**

---

## 🛠️ Herramientas Disponibles

| Herramienta | Entrada | Salida | Descripción |
| :--- | :--- | :--- | :--- |
| **JPG a PDF** | `.jpg`, `.png`, `.webp` | `.pdf` | Agrupa y convierte múltiples imágenes en un único PDF. |
| **WORD a PDF** | `.docx`, `.doc` | `.pdf` | Convierte documentos Word a formato PDF estándar. |
| **POWERPOINT a PDF** | `.pptx`, `.ppt` | `.pdf` | Convierte diapositivas a documento PDF en alta resolución. |
| **EXCEL a PDF** | `.xlsx`, `.xls` | `.pdf` | Convierte hojas de cálculo a PDF maquetado con bordes y estilos. |
| **HTML a PDF** | `.html`, `.htm` | `.pdf` | Renderiza páginas web o archivos HTML a PDF. |
| **PDF a JPG** | `.pdf` | `.jpg` / `.zip` | Extrae cada página en alta resolución (empaquetado ZIP si son varias). |
| **PDF a WORD** | `.pdf` | `.docx` | Reconstruye texto, tablas y formato editable en Microsoft Word. |
| **PDF a POWERPOINT** | `.pdf` | `.pptx` | Genera una presentación PowerPoint editable con cada página. |
| **PDF a EXCEL** | `.pdf` | `.xlsx` | Extrae tablas tabuladas directamente a un libro Excel. |
| **PDF a PDF/A** | `.pdf` | `.pdf` | Convierte a formato estándar ISO para archivo a largo plazo. |

---

## 💻 Uso por Línea de Comandos (CLI)
Si prefieres convertir archivos directamente desde la terminal:

```bash
# Convertir PDF a Word
python cli.py "documento.pdf" -o "salida.docx"

# Convertir solo páginas específicas (ejemplo: páginas 1 a 3 y página 5)
python cli.py "documento.pdf" --pages "1-3,5"
```

---

## 🔒 Privacidad y Seguridad
Tus documentos nunca salen de tu ordenador. No requiere conexión a internet para convertir archivos ni almacena tus datos en la nube.
