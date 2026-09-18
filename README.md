# DocuMorph - Suite Profesional de Conversión de Documentos (10 en 1)

Convertidor de documentos y PDFs 100% local, privado, sin límites de tamaño y sin marcas de agua. Toda la conversión se procesa directamente en tu ordenador.

---

## ⚡ ¿Cómo usar la aplicación? (Elige tu opción)

### Opción A: Descargar el ejecutable (.exe) directo (Sin instalar Python)
Ideal para usuarios finales que solo quieren usar el programa sin tocar código:
1. Ve a la pestaña de **[Releases del repositorio](https://github.com/CV17d/converterpdf/releases)**.
2. Descarga el archivo **`DocuMorph_Windows.zip`**.
3. Descomprime la carpeta y haz doble clic en **`DocuMorph.exe`**.
4. ¡El navegador se abrirá automáticamente con el convertidor listo!

---

### Opción B: Clonar el repositorio
Ideal para desarrolladores o para ejecutar desde código fuente:

```bash
git clone https://github.com/CV17d/converterpdf.git
cd converterpdf
```

* **En Windows (1 solo clic):**
  Haz doble clic en **`iniciar.bat`** *(detecta e instala librerías si faltan y abre el navegador automáticamente)*.

* **Desde consola (Windows, Mac o Linux):**
  ```bash
  pip install -r requirements.txt
  python app.py
  ```

---

### Opción C: Compilar tu propio .exe
Si quieres generar tu propio ejecutable independiente en Windows:
- Haz doble clic en el archivo **`crear_exe.bat`**.
- El script compilará la aplicación y generará la carpeta `dist\DocuMorph\DocuMorph.exe` y el archivo `dist\DocuMorph_Windows.zip`.

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
```bash
# Convertir PDF a Word
python cli.py "documento.pdf" -o "salida.docx"

# Convertir solo páginas específicas (ejemplo: páginas 1 a 3 y página 5)
python cli.py "documento.pdf" --pages "1-3,5"
```

---

## 🔒 Privacidad y Seguridad
Tus documentos nunca salen de tu ordenador. No requiere conexión a internet para convertir archivos ni almacena tus datos en la nube.
