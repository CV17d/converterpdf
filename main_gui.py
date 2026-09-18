"""
Lanzador de Escritorio Nativo para DocuMorph.
Abre la suite en una ventana de aplicación independiente tipo software de PC.
Sin consola negra y sin abrir navegador web externo.
"""
import os
import sys
import webview
from app import app

# Configurar soporte para rutas cuando se ejecuta como binario empaquetado (PyInstaller)
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
    app.template_folder = os.path.join(bundle_dir, 'templates')
    app.static_folder = os.path.join(bundle_dir, 'static')

def main():
    # Crear ventana nativa de escritorio (Microsoft Edge WebView2)
    window = webview.create_window(
        title="DocuMorph - Suite de Documentos",
        url=app,
        width=1120,
        height=820,
        min_size=(880, 620),
        text_select=True
    )
    # Iniciar la interfaz gráfica de escritorio
    webview.start(debug=False)

if __name__ == "__main__":
    main()
