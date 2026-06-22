import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path
import threading
import os
import sys
import subprocess

from organizador import organizar_arquivos


# =========================
# Funções principais
# =========================

def selecionar_pasta():
    caminho = filedialog.askdirectory(title="Selecione uma pasta para organizar")

    if caminho:
        pasta_var.set(caminho)
        status_var.set("Pasta selecionada. Clique em 'Organizar Arquivos'.")
        resultado_var.set("")


def organizar_pasta():
    caminho = pasta_var.get().strip()

    if not caminho:
        messagebox.showwarning("Atenção", "Selecione uma pasta antes de organizar.")
        return

    if not Path(caminho).exists():
        messagebox.showerror("Erro", "A pasta selecionada não existe.")
        return

    bloquear_botoes()
    status_var.set("Organizando arquivos...")
    resultado_var.set("")
    barra_progresso.start(10)

    # Executa a organização em outra thread para a interface não travar
    thread = threading.Thread(target=executar_organizacao, args=(caminho,), daemon=True)
    thread.start()


def executar_organizacao(caminho):
    try:
        quantidade = organizar_arquivos(caminho)
        janela.after(0, finalizar_organizacao, quantidade, None)
    except Exception as erro:
        janela.after(0, finalizar_organizacao, 0, erro)


def finalizar_organizacao(quantidade, erro):
    barra_progresso.stop()
    liberar_botoes()

    if erro:
        status_var.set("Ocorreu um erro ao organizar os arquivos.")
        resultado_var.set("Erro na organização.")
        messagebox.showerror("Erro", f"Não foi possível organizar os arquivos:\n\n{erro}")
        return

    status_var.set("Organização concluída com sucesso!")
    resultado_var.set(f"{quantidade} arquivos foram organizados!")


def abrir_pasta():
    caminho = pasta_var.get().strip()

    if not caminho:
        messagebox.showwarning("Atenção", "Nenhuma pasta foi selecionada.")
        return

    if not Path(caminho).exists():
        messagebox.showerror("Erro", "A pasta selecionada não existe.")
        return

    try:
        if sys.platform.startswith("win"):
            os.startfile(caminho)
        elif sys.platform.startswith("darwin"):
            subprocess.Popen(["open", caminho])
        else:
            subprocess.Popen(["xdg-open", caminho])
    except Exception as erro:
        messagebox.showerror("Erro", f"Não foi possível abrir a pasta:\n\n{erro}")


def bloquear_botoes():
    botao_selecionar.config(state="disabled")
    botao_organizar.config(state="disabled")
    botao_abrir.config(state="disabled")


def liberar_botoes():
    botao_selecionar.config(state="normal")
    botao_organizar.config(state="normal")
    botao_abrir.config(state="normal")


def alternar_tela_cheia(event=None):
    estado_atual = janela.attributes("-fullscreen")
    janela.attributes("-fullscreen", not estado_atual)


def sair_tela_cheia(event=None):
    janela.attributes("-fullscreen", False)


# =========================
# Janela principal
# =========================

janela = tk.Tk()
janela.title("Smart Organizer")
janela.geometry("900x550")
janela.minsize(750, 450)
janela.resizable(True, True)

# Atalhos
janela.bind("<F11>", alternar_tela_cheia)
janela.bind("<Escape>", sair_tela_cheia)


# =========================
# Cores e estilo
# =========================

COR_FUNDO = "#F4F6F8"
COR_CARD = "#FFFFFF"
COR_TEXTO = "#1F2937"
COR_TEXTO_FRACO = "#6B7280"
COR_PRIMARIA = "#2563EB"
COR_PRIMARIA_HOVER = "#1D4ED8"

janela.configure(bg=COR_FUNDO)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TButton",
    font=("Arial", 11),
    padding=10,
    borderwidth=0
)

style.configure(
    "Primary.TButton",
    background=COR_PRIMARIA,
    foreground="white",
    font=("Arial", 11, "bold"),
    padding=12
)

style.map(
    "Primary.TButton",
    background=[("active", COR_PRIMARIA_HOVER)]
)

style.configure(
    "Secondary.TButton",
    background="#E5E7EB",
    foreground=COR_TEXTO,
    font=("Arial", 10),
    padding=10
)

style.configure(
    "TProgressbar",
    thickness=8
)


# =========================
# Variáveis da interface
# =========================

pasta_var = tk.StringVar()
status_var = tk.StringVar(value="Selecione uma pasta para começar.")
resultado_var = tk.StringVar()


# =========================
# Layout principal
# =========================

container = tk.Frame(janela, bg=COR_FUNDO)
container.pack(fill="both", expand=True, padx=40, pady=35)

card = tk.Frame(container, bg=COR_CARD)
card.pack(fill="both", expand=True)

card.grid_columnconfigure(0, weight=1)
card.grid_rowconfigure(4, weight=1)


# =========================
# Cabeçalho
# =========================

titulo = tk.Label(
    card,
    text="Smart Organizer",
    bg=COR_CARD,
    fg=COR_TEXTO,
    font=("Arial", 26, "bold")
)
titulo.grid(row=0, column=0, pady=(35, 5), padx=30, sticky="w")

subtitulo = tk.Label(
    card,
    text="Organize automaticamente seus arquivos por categoria de forma simples e rápida.",
    bg=COR_CARD,
    fg=COR_TEXTO_FRACO,
    font=("Arial", 12)
)
subtitulo.grid(row=1, column=0, pady=(0, 25), padx=30, sticky="w")


# =========================
# Área da pasta
# =========================

area_pasta = tk.Frame(card, bg=COR_CARD)
area_pasta.grid(row=2, column=0, padx=30, sticky="ew")
area_pasta.grid_columnconfigure(0, weight=1)

label_pasta = tk.Label(
    area_pasta,
    text="Pasta selecionada",
    bg=COR_CARD,
    fg=COR_TEXTO,
    font=("Arial", 11, "bold")
)
label_pasta.grid(row=0, column=0, sticky="w", pady=(0, 5))

entrada_pasta = tk.Entry(
    area_pasta,
    textvariable=pasta_var,
    font=("Arial", 11),
    bg="#F9FAFB",
    fg=COR_TEXTO,
    relief="flat"
)
entrada_pasta.grid(row=1, column=0, sticky="ew", ipady=12)

botao_selecionar = ttk.Button(
    area_pasta,
    text="Selecionar Pasta",
    command=selecionar_pasta,
    style="Secondary.TButton"
)
botao_selecionar.grid(row=1, column=1, padx=(15, 0))


# =========================
# Botões principais
# =========================

area_botoes = tk.Frame(card, bg=COR_CARD)
area_botoes.grid(row=3, column=0, padx=30, pady=30, sticky="w")

botao_organizar = ttk.Button(
    area_botoes,
    text="Organizar Arquivos",
    command=organizar_pasta,
    style="Primary.TButton"
)
botao_organizar.grid(row=0, column=0, padx=(0, 15))

botao_abrir = ttk.Button(
    area_botoes,
    text="Abrir Pasta",
    command=abrir_pasta,
    style="Secondary.TButton"
)
botao_abrir.grid(row=0, column=1)


# =========================
# Área de status
# =========================

area_status = tk.Frame(card, bg=COR_CARD)
area_status.grid(row=4, column=0, padx=30, pady=(0, 30), sticky="nsew")
area_status.grid_columnconfigure(0, weight=1)

status = tk.Label(
    area_status,
    textvariable=status_var,
    bg=COR_CARD,
    fg=COR_TEXTO_FRACO,
    font=("Arial", 11)
)
status.grid(row=0, column=0, sticky="w", pady=(0, 12))

barra_progresso = ttk.Progressbar(
    area_status,
    mode="indeterminate"
)
barra_progresso.grid(row=1, column=0, sticky="ew", pady=(0, 20))

resultado = tk.Label(
    area_status,
    textvariable=resultado_var,
    bg=COR_CARD,
    fg=COR_PRIMARIA,
    font=("Arial", 16, "bold")
)
resultado.grid(row=2, column=0, sticky="w")


# =========================
# Rodapé
# =========================

rodape = tk.Label(
    card,
    text="Dica: pressione F11 para tela cheia e ESC para sair.",
    bg=COR_CARD,
    fg=COR_TEXTO_FRACO,
    font=("Arial", 10)
)
rodape.grid(row=5, column=0, padx=30, pady=(0, 20), sticky="w")


janela.mainloop()