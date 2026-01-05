import yt_dlp
import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton,
                             QGridLayout, QLabel, QFileDialog)
from PyQt5.QtGui import QIcon
import os

class DownloadApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Video Downloader")
        self.setGeometry(100, 100, 300, 200)
        grid = QGridLayout()
        self.setLayout(grid)
        label = QLabel('Enter URL:')
        grid.addWidget(label, 0, 0)
        self.urlEdit = QLineEdit()
        grid.addWidget(self.urlEdit, 0, 1)
        label = QLabel('Enter save path:')
        grid.addWidget(label, 1, 0)
        self.pathEdit = QLineEdit()
        self.pathEdit.setPlaceholderText("Browse...")
        grid.addWidget(self.pathEdit, 1, 1)
        button = QPushButton('Browse')
        button.clicked.connect(self.browseDirectory)
        grid.addWidget(button, 1, 2)
        button = QPushButton('Download')
        button.clicked.connect(self.downloadVideo)
        grid.addWidget(button, 2, 1)
        self.progressLabel = QLabel('Ready')
        grid.addWidget(self.progressLabel, 3, 0, 1, 2)
        self.errorLabel = QLabel('')
        grid.addWidget(self.errorLabel, 4, 0, 1, 2)
        self.show()

    def browseDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Save Directory", os.path.expanduser("~"))
        if directory:
            self.pathEdit.setText(directory)

    # Se decide la ruta en donde se descargaran los videos
    def downloadVideo(self):
        url = self.urlEdit.text()
        save_path = self.pathEdit.text()
        if not save_path:
            save_path = os.path.join(os.path.expanduser("~"), 'Videos')

        if "youtube.com" in url or "youtu.be" in url:
            # Utilizar yt_dlp para descargar videos de YouTube
            self.download_youtube_video(url, save_path)
        elif "animeflv.net" in url:
            # Utilizar requests para descargar videos de animeflv.net
            self.download_animeflv_video(url, save_path)
        elif "pixeldrain.com" in url:
            # Utilizar requests para descargar archivos de pixeldrain.com
            self.download_pixeldrain_video(url, save_path)
        else:
            self.errorLabel.setText("Error: URL no soportada")
            print("Error: URL no soportada")

    def download_youtube_video(self, url, save_path):
        try:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best[ext=mp4]',
                'outtmpl': f'{save_path}/%(title)s.%(ext)s',
                'concurrent-fragment-downloads': 10,
                'no-check-certificate': True,
                'merge_output_format': False,
                'progress_hooks': [self.progress_hook]
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f'Video descargado correctamente a {save_path}')
        except Exception as e:
            self.errorLabel.setText(f"Error al descargar el video: {e}")
            print(f"Error al descargar el video: {e}")

    def download_animeflv_video(self, url, save_path):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(os.path.join(save_path, "video.mp4"), "wb") as f:
                    total_size = int(response.headers.get('Content-Length', 0))
                    downloaded_size = 0
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        self.progressLabel.setText(f'Downloading... {downloaded_size / total_size * 100:.2f}%')
                print(f'Video descargado correctamente a {save_path}')
            else:
                self.errorLabel.setText(f"Error al descargar el video: {response.status_code}")
                print(f"Error al descargar el video: {response.status_code}")
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DownloadApp()
    sys.exit(app.exec_())
