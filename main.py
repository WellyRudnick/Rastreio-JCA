import os
import sys
import subprocess
import requests
import webview

# Controle de Versão Interno
CURRENT_VERSION = "1.0"

# Cole aqui o link RAW do seu Gist (o arquivo versao.json)
UPDATE_URL = "https://gist.githubusercontent.com/WellyRudnick/6a3147cc920c8d0b0557fd923b516fc9/raw/783285e19527d476dfb82b0e6b005569c1a2a065/verssao.json"

def check_for_updates():
    try:
        # Puxa o JSON do Gist
        response = requests.get(UPDATE_URL, timeout=5)
        data = response.json()
        
        latest_version = data.get("versao")
        download_url = data.get("link_download")
        
        # Se a versão do GitHub for diferente da versão atual, inicia a atualização
        if latest_version and latest_version != CURRENT_VERSION:
            download_and_update(download_url)
            
    except Exception as e:
        # Se der erro (ex: sem internet), ele ignora e abre o sistema normalmente
        print(f"Falha ao checar atualizações: {e}")

def download_and_update(download_url):
    try:
        # Pega o caminho exato de onde o RastreioFrota.exe está rodando
        exe_path = sys.executable
        new_exe_path = exe_path + ".new" # Cria um nome temporário
        
        # Faz o download do novo .exe
        response = requests.get(download_url, stream=True)
        with open(new_exe_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Cria o script .bat ninja para fazer a troca dos arquivos
        bat_path = os.path.join(os.path.dirname(exe_path), "update.bat")
        with open(bat_path, "w") as bat_file:
            bat_file.write(f"""@echo off
timeout /t 2 /nobreak > NUL
del /f /q "{exe_path}"
move /y "{new_exe_path}" "{exe_path}"
start "" "{exe_path}"
del "%~f0"
""")
        
        # Executa o .bat de forma invisível no Windows
        subprocess.Popen([bat_path], creationflags=subprocess.CREATE_NO_WINDOW)
        
        # Encerra o aplicativo atual imediatamente para liberar o .exe velho
        sys.exit()
        
    except Exception as e:
        print(f"Erro no processo de atualização: {e}")

if __name__ == '__main__':
    # A sacada ninja: getattr(sys, 'frozen', False) verifica se o código está rodando
    # como um .exe compilado. Isso evita que ele tente atualizar enquanto você
    # está apenas programando e testando no VS Code.
    if getattr(sys, 'frozen', False):
        check_for_updates()

    # Depois de checar (ou se não tiver atualização), carrega a interface HTML normal
    # Esta linha garante que o PyInstaller ache o HTML dentro do arquivo temporário dele
    if hasattr(sys, '_MEIPASS'):
        html_path = os.path.join(sys._MEIPASS, 'Rastreio.html')
    else:
        html_path = os.path.abspath('Rastreio.html')

    # Cria e inicia a janela
    webview.create_window('Rastreio de Veículos', html_path, width=1280, height=720)
    webview.start()