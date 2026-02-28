import webview
import os
import sys

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    html_path = resource_path('Rastreio.html')

    webview.create_window(
        title='Rastreio de Veículos',
        url=html_path,
        width=1280,
        height=720,
        resizable=True,
        background_color="#221560",
    )

    webview.start()
    