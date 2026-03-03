import os
import sys
import subprocess
import requests
import webview
import tkinter as tk
from tkinter import messagebox

CURRENT_VERSION = "1.2"
UPDATE_URL = "https://gist.githubusercontent.com/WellyRudnick/6a3147cc920c8d0b0557fd923b516fc9/raw/versao.json"

def limpar_arquivos_antigos():
    old_exe = sys.executable + ".old"
    if os.path.exists(old_exe):
        try: os.remove(old_exe)
        except: pass

def check_for_updates():
    try:
        limpar_arquivos_antigos()
        
        response = requests.get(UPDATE_URL, timeout=5)
        data = response.json()
        
        latest_version = data.get("versao")
        download_url = data.get("link_download")
        
        if latest_version and latest_version != CURRENT_VERSION:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            resposta = messagebox.askyesno(
                "Atualização Disponível", 
                f"Uma nova versão ({latest_version}) do Rastreio de Frota está disponível!\n\nDeseja baixar e atualizar agora?"
            )
            root.destroy()
            
            if resposta:
                download_and_update(download_url)
            
    except Exception as e:
        print(f"Falha ao checar atualizações: {e}")

def download_and_update(download_url):
    try:
        exe_path = sys.executable
        new_exe_path = exe_path + ".new" 
        old_exe_path = exe_path + ".old"
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        messagebox.showinfo("Baixando...", "O sistema está baixando a atualização. O aplicativo será reiniciado em instantes.")
        root.destroy()

        response = requests.get(download_url, stream=True)
        response.raise_for_status() 
        with open(new_exe_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        if os.path.exists(old_exe_path):
            try: os.remove(old_exe_path)
            except: pass
            
        os.rename(exe_path, old_exe_path) 
        os.rename(new_exe_path, exe_path) 
        
        os.environ.pop('_MEIPASS2', None)
        os.environ.pop('_MEIPASS', None)

        DETACHED_PROCESS = 0x00000008
        subprocess.Popen([exe_path], creationflags=DETACHED_PROCESS)
        
        sys.exit()
        
    except Exception as e:
        print(f"Erro no processo de atualização: {e}")

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        check_for_updates()

    if hasattr(sys, '_MEIPASS'):
        html_path = os.path.join(sys._MEIPASS, 'Rastreio.html')
    else:
        html_path = os.path.abspath('Rastreio.html')

    webview.create_window('Rastreio de Frota JCA', html_path, width=1280, height=720)
    
    # A MÁGICA AQUI: Força o uso do Edge Chromium, ignorando o .NET/WinForms bugado
    webview.start(gui='edgechromium')