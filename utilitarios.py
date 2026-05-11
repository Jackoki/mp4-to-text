import os
from config import (NOME_PASTA_DE_VIDEOS, NOME_PASTA_DE_TRANSCRICOES, LOG_FILE)


def preparar_pastas():
    os.makedirs(NOME_PASTA_DE_VIDEOS, exist_ok=True)
    os.makedirs(NOME_PASTA_DE_TRANSCRICOES, exist_ok=True)

def obter_videos():
    return [f for f in os.listdir(NOME_PASTA_DE_VIDEOS)
        if f.lower().endswith(".mp4")
    ]

def verificar_video_foi_processado(video):
    nome_txt = os.path.splitext(video)[0] + ".txt"
    caminho_txt = os.path.join(NOME_PASTA_DE_TRANSCRICOES, nome_txt)

    return os.path.exists(caminho_txt), caminho_txt

def gerar_log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def salvar_transcricao(texto, caminho_saida):
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(texto)
