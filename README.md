# DocuMorph - Suite Profesional de Conversión de Documentos

Suite de herramientas 100% local, rápida y privada para convertir entre formatos PDF y documentos ofimáticos e imágenes, sin marcas de agua ni límites de tamaño.

---

## 🛠️ Herramientas Incluidas (10 en 1)

### 📥 Convertir hacia PDF
1. **JPG a PDF**: Agrupa y convierte imágenes (`.jpg`, `.jpeg`, `.png`, `.webp`) en un solo documento PDF con alta calidad.
2. **WORD a PDF**: Convierte documentos (`.docx`, `.doc`) a PDF con fidelidad tipográfica.
3. **POWERPOINT a PDF**: Convierte presentaciones (`.pptx`, `.ppt`) a PDF en alta resolución.
4. **EXCEL a PDF**: Convierte hojas de cálculo (`.xlsx`, `.xls`) a PDF corporativo con tablas bordeadas y encabezados.
5. **HTML a PDF**: Convierte páginas web y archivos (`.html`, `.htm`) a PDF mediante Microsoft Edge Headless.

### 📤 Convertir desde PDF
6. **PDF a JPG**: Extrae todas las páginas del PDF en imágenes JPG de alta definición (empaqueta en ZIP si son múltiples).
7. **PDF a WORD**: Reconstruye el documento en Microsoft Word editable (`.docx`) preservando tablas, estilos y párrafos.
8. **PDF a POWERPOINT**: Genera una presentación (`.pptx`) con diapositivas editables a partir de cada página.
9. **PDF a EXCEL**: Detecta y extrae tablas de datos estructurados directamente a un libro de Microsoft Excel (`.xlsx`).
10. **PDF a PDF/A**: Convierte a formato estándar ISO PDF/A (PDF/A-1b) para conservación documental a largo plazo.

---

## 🚀 Cómo Iniciar la Suite

### 1. Interfaz Web (Recomendado)
- **Windows (1 Clic)**: Haz doble clic en [`iniciar.bat`](file:///C:/Users/HP/.gemini/antigravity-ide/scratch/pdf-to-word/iniciar.bat).
- **Desde Consola**:
  ```bash
  python app.py
  ```
El navegador se abrirá automáticamente en `http://127.0.0.1:5000`.

### 2. Conversión por Terminal (CLI)
```bash
# PDF a Word
python cli.py "documento.pdf" -o "salida.docx"
```

---

## 🔒 Privacidad y Seguridad
Todos los procesos se ejecutan estrictamente en tu ordenador local. Ningún documento o información viaja a internet o servidores externos.
