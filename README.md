# DescargaVideos

Una aplicación de escritorio para descargar videos desde YouTube, Pixeldrain y AnimeFLV.

## Características

- Descarga videos de YouTube con selección de calidad
- Descarga archivos de Pixeldrain
- Descarga videos de AnimeFLV (solo en versión Linux)
- Interfaz gráfica simple con PyQt5
- Progreso de descarga en tiempo real

## Requisitos

- Python 3.6+
- yt-dlp
- PyQt5
- requests

## Instalación

### Linux (Arch Linux)

1. Instala las dependencias del sistema:
   ```bash
   sudo pacman -S python python-pip python-pyqt5
   ```

2. Instala las dependencias de Python:
   ```bash
   pip install yt-dlp requests
   ```

### Windows (10/11)

1. Descarga e instala Python desde https://www.python.org/downloads/

2. Abre la línea de comandos y instala las dependencias:
   ```cmd
   pip install pyqt5 yt-dlp requests
   ```

## Uso

### Versión con Selector de Calidad (Download.py)

Esta versión permite seleccionar la calidad del video para YouTube y es compatible con Windows y Linux.

Ejecuta:
```bash
python Download.py
```

### Versión Simple (downloadLinux.py)

Esta versión es más simple, sin selector de calidad, pero soporta AnimeFLV. Recomendada para Linux.

Ejecuta:
```bash
python downloadLinux.py
```

### Instrucciones

1. Abre la aplicación.
2. Ingresa la URL del video (YouTube, Pixeldrain o AnimeFLV).
3. Selecciona el directorio de guardado (o usa el predeterminado ~/Videos).
4. Para YouTube en Download.py: haz clic en "Get Formats" para ver calidades disponibles.
5. Haz clic en "Download" para iniciar la descarga.
6. Monitorea el progreso en la etiqueta inferior.

## Notas

- Asegúrate de tener permisos de escritura en el directorio de destino.
- Las descargas de YouTube requieren yt-dlp actualizado.
- Para Pixeldrain, la URL debe ser directa al archivo.

## Licencia

Este proyecto es de código abierto. Usa bajo tu propio riesgo.