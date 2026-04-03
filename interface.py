import tkinter as tk
from tkinter import filedialog
from organizador import organizar_arquivos


def selecionar_pasta():
    caminho = filedialog.askdirectory()

    if caminho:
        quantidade = organizar_arquivos(caminho)
        resultado["text"] = f"{quantidade} arquivos foram organizados!"


# Interface
janela = tk.Tk()
janela.title("Smart Organizer")
janela.geometry("400x250")

titulo = tk.Label(janela, text="Organizador Inteligente de Arquivos", font=("Arial", 12))
titulo.pack(pady=10)

botao = tk.Button(janela, text="Selecionar Pasta e Organizar", command=selecionar_pasta, height=2, width=30)
botao.pack(pady=20)

resultado = tk.Label(janela, text="")
resultado.pack(pady=10)

janela.mainloop()