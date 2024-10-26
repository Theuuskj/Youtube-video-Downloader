import os
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import threading

def baixar_video(url, qualidade, diretorio, progress):
    # faz o download da qualidade escolhida, tentando forçar o MP4
    #(tentar forçar, essa porra vai quebrar algum dia mano)
    print(f"Baixando o vídeo na qualidade {qualidade}...")
    caminho_video = os.path.join(diretorio, '%(title)s.%(ext)s')
    command = f"yt-dlp -o '{caminho_video}' -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' '{url}'"
    
    # Inicia o download
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Atualiza a barra de progresso (vou morrer)
    while True:
        output = process.stdout.readline()
        if output == b"" and process.poll() is not None:
            break
        if output:
            print(output.decode().strip())
            
            progress['value'] += 10  # Incrementa a barra de progresso
            root.update_idletasks()  # Atualiza a interface

    process.stdout.close()
    process.wait()
    print("Download concluído!")
    messagebox.showinfo("Concluído", "Download concluído!")

def iniciar_download():
    url = url_entry.get()
    diretorio = simpledialog.askstring("Diretório", "Digite o diretório onde deseja salvar o vídeo:")
    
    if not diretorio:
        diretorio = os.getcwd()

    # Verifica a qualidade 
    qualidade = ""
    if var_360.get():
        qualidade = "360p"
    elif var_480.get():
        qualidade = "480p"
    elif var_720.get():
        qualidade = "720p"
    else:
        messagebox.showerror("Erro", "Por favor, selecione uma qualidade de vídeo.")
        return

    # Inicia o download numa thread separada
    threading.Thread(target=baixar_video, args=(url, qualidade, diretorio, progress)).start()

# Cria a janela principal
root = tk.Tk()
root.title("Baixar Vídeo do YouTube")

# Campo para inserir o link do vídeo
tk.Label(root, text="Cole o link do vídeo aqui:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Checkbox para selecionar a qualidade
var_360 = tk.BooleanVar()
var_480 = tk.BooleanVar()
var_720 = tk.BooleanVar()

tk.Checkbutton(root, text="360p (Baixa)", variable=var_360).pack(anchor=tk.W)
tk.Checkbutton(root, text="480p (Média)", variable=var_480).pack(anchor=tk.W)
tk.Checkbutton(root, text="720p (Alta)", variable=var_720).pack(anchor=tk.W)

# Barra de progresso
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

# Botão para iniciar o download
tk.Button(root, text="Baixar Vídeo", command=iniciar_download).pack()

# Iniciar o loop da interface
root.mainloop()
