# DocuMorph - Suite Profesional de Conversión de Documentos (10 en 1)

Aplicación de escritorio nativa para PC (Windows) y suite de herramientas 100% local, rápida y privada para convertir entre formatos PDF, documentos ofimáticos e imágenes, sin límites y sin marcas de agua.

---

## 🖥️ ¿Cómo usar la aplicación? (Elige tu opción)

### Opción A: Descargar el programa de escritorio (.exe) listo para usar (Recomendado)
Para cualquier usuario que quiera usar el programa directamente como cualquier aplicación de PC (Word, Excel, etc.):
1. Entra a la sección de **[Releases del repositorio](https://github.com/CV17d/converterpdf/releases)**.
2. Descarga el archivo **`DocuMorph_Windows.zip`**.
3. Descomprime la carpeta y haz doble clic en **`DocuMorph.exe`**.
4. ✨ **Se abrirá una ventana de escritorio nativa e independiente** (sin terminal de comandos, sin barra de localhost y sin navegadores externos).

---

### Opción B: Clonar el repositorio
Para ejecutar directamente desde el código fuente o desarrollar mejoras:

```bash
git clone https://github.com/CV17d/converterpdf.git
cd converterpdf
```

* **En Windows (1 solo clic):**
  Haz doble clic en **`iniciar.bat`** *(instala dependencias si faltan y arranca la aplicación)*.

* **Desde consola (Windows, Mac o Linux):**
  ```bash
  pip install -r requirements.txt
  python main_gui.py
  ```

---

### Opción C: Compilar tu propio ejecutable de escritorio
Si deseas compilar la aplicación tú mismo en Windows:
- Haz doble clic en el archivo **`crear_exe.bat`**.
- Compilará la versión nativa sin consola y empaquetará el archivo `dist\DocuMorph_Windows.zip`.

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

## 🔒 Privacidad y Rendimiento
- **Ventana nativa:** Corre en su propio proceso independiente con WebView2 de alta velocidad.
- **100% privado:** Todos tus archivos se procesan en tu propia máquina sin conexión a servidores externos.
