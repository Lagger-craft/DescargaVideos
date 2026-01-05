import yt_dlp
import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton,
                             QGridLayout, QLabel, QFileDialog, QComboBox, QMessageBox)
from PyQt5.QtGui import QIcon
import os

class DownloadApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Video Downloader")
        self.setGeometry(100, 100, 400, 250)
        grid = QGridLayout()
        self.setLayout(grid)

        label = QLabel('Enter URL:')
        grid.addWidget(label, 0, 0)
        self.urlEdit = QLineEdit()
        grid.addWidget(self.urlEdit, 0, 1, 1, 2)

        label = QLabel('Enter save path:')
        grid.addWidget(label, 1, 0)
        self.pathEdit = QLineEdit()
        self.pathEdit.setPlaceholderText("Browse...")
        grid.addWidget(self.pathEdit, 1, 1)
        button = QPushButton('Browse')
        button.clicked.connect(self.browseDirectory)
        grid.addWidget(button, 1, 2)

        label = QLabel('Select Quality:')
        grid.addWidget(label, 2, 0)
        self.qualityCombo = QComboBox()
        grid.addWidget(self.qualityCombo, 2, 1, 1, 2)

        button = QPushButton('Get Formats')
        button.clicked.connect(self.getFormats)
        grid.addWidget(button, 3, 1)

        button = QPushButton('Download')
        button.clicked.connect(self.downloadVideo)
        grid.addWidget(button, 3, 2)

        self.progressLabel = QLabel('Ready')
        grid.addWidget(self.progressLabel, 4, 0, 1, 3)
        self.errorLabel = QLabel('')
        grid.addWidget(self.errorLabel, 5, 0, 1, 3)

        self.show()

    def browseDirectory(self):
        home_dir = os.path.expanduser("~")
        directory = QFileDialog.getExistingDirectory(self, "Select Save Directory", os.path.join(home_dir, "Videos"))
        if directory:
            self.pathEdit.setText(directory)

    def getFormats(self):
        url = self.urlEdit.text()
        if "youtube.com" in url or "youtu.be" in url:
            self.list_youtube_formats(url)
        else:
            QMessageBox.critical(self, "Error", "Only YouTube URLs are supported for format listing.")

    def list_youtube_formats(self, url):
        try:
            ydl_opts = {'quiet': True, 'noplaylist': True, 'extract_flat': False}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=False)
                formats = result.get('formats', [])
                self.qualityCombo.clear()
                seen_resolutions = set()
                for f in formats:
                    resolution = f.get('format_note')
                    if resolution and resolution not in seen_resolutions:
                        seen_resolutions.add(resolution)
                        self.qualityCombo.addItem(f"{resolution} - {f['ext']}", f['format_id'])
        except Exception as e:
            self.errorLabel.setText(f"Error retrieving formats: {e}")
            print(f"Error retrieving formats: {e}")

    def downloadVideo(self):
        url = self.urlEdit.text()
        save_path = self.pathEdit.text()
        format_id = self.qualityCombo.currentData()

        if not save_path:
            save_path = os.path.join(os.path.expanduser("~"), "Videos")

        if "youtube.com" in url or "youtu.be" in url:
            self.download_youtube_video(url, save_path, format_id)
        elif "pixeldrain.com" in url:
            self.download_pixeldrain_video(url, save_path)
        else:
            self.errorLabel.setText("Error: URL no soportada")
            print("Error: URL no soportada")

    def download_youtube_video(self, url, save_path, format_id):
        try:
            ydl_opts = {
                'format': format_id if format_id else 'best',
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'concurrent-fragment-downloads': 10,
                'progress_hooks': [self.progress_hook]
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.progressLabel.setText('Download complete')
            print(f'Video descargado correctamente a {save_path}')
        except Exception as e:
            self.errorLabel.setText(f"Error al descargar el video: {e}")
            print(f"Error al descargar el video: {e}")

    def download_pixeldrain_video(self, url, save_path):
        try:
            # Extraer el ID del archivo de la URL
            file_id = url.split('/')[-1]
            download_url = f"https://pixeldrain.com/api/file/{file_id}?download"
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                # Obtener el nombre del archivo del header Content-Disposition
                content_disposition = response.headers.get('Content-Disposition')
                if content_disposition:
                    filename = content_disposition.split('filename=')[1].strip('"')
                else:
                    filename = f"{file_id}.mp4"  # Fallback
                filepath = os.path.join(save_path, filename)
                with open(filepath, "wb") as f:
                    total_size = int(response.headers.get('Content-Length', 0))
                    downloaded_size = 0
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size > 0:
                            self.progressLabel.setText(f'Downloading... {downloaded_size / total_size * 100:.2f}%')
                self.progressLabel.setText('Download complete')
                print(f'Archivo descargado correctamente a {filepath}')
            else:
                self.errorLabel.setText(f"Error al descargar el archivo: {response.status_code}")
                print(f"Error al descargar el archivo: {response.status_code}")
        except Exception as e:
            self.errorLabel.setText(f"Error al descargar el archivo: {e}")
            print(f"Error al descargar el archivo: {e}")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            self.progressLabel.setText(f'Downloading... {d["_percent_str"]} ({d["_eta_str"]})')
        elif d['status'] == 'finished':
            self.progressLabel.setText('Download complete')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DownloadApp()
    sys.exit(app.exec_())

