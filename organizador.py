import os
import shutil
from datetime import datetime


def organizar_por_data(caminho_arquivo, destino_base):
    data_modificacao = os.path.getmtime(caminho_arquivo)
    ano = datetime.fromtimestamp(data_modificacao).strftime("%Y")

    destino = os.path.join(destino_base, ano)

    if not os.path.exists(destino):
        os.makedirs(destino)

    return destino


def organizar_arquivos(caminho):
    tipos = {
        "Imagens": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp", ".svg"],
        "PDFs": [".pdf"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
        "Audios": [".mp3", ".wav", ".ogg", ".aac", ".flac"],
        "Planilhas": [".xls", ".xlsx", ".csv", ".ods"],
        "Documentos": [".docx", ".doc", ".txt", ".odt", ".rtf"],
        "Apresentacoes": [".ppt", ".pptx", ".odp"],
        "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Executaveis": [".exe", ".msi", ".deb", ".rpm", ".bat"],
        "Codigos": [".py", ".java", ".cpp", ".c", ".js", ".html", ".css", ".php", ".sql", ".json", ".xml"]
    }

    contador = 0

    for arquivo in os.listdir(caminho):
        arquivo_caminho = os.path.join(caminho, arquivo)

        if os.path.isfile(arquivo_caminho):
            extensao = os.path.splitext(arquivo)[1].lower()
            movido = False

            for pasta, extensoes in tipos.items():
                if extensao in extensoes:
                    destino_base = os.path.join(caminho, pasta)

                    if not os.path.exists(destino_base):
                        os.makedirs(destino_base)

                    destino_final = organizar_por_data(arquivo_caminho, destino_base)
                    shutil.move(arquivo_caminho, os.path.join(destino_final, arquivo))
                    contador += 1
                    movido = True
                    break

            if not movido:
                outros = os.path.join(caminho, "Outros")
                if not os.path.exists(outros):
                    os.makedirs(outros)

                destino_final = organizar_por_data(arquivo_caminho, outros)
                shutil.move(arquivo_caminho, os.path.join(destino_final, arquivo))
                contador += 1

    return contador