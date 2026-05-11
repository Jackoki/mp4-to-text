import os
import time

from config import (NOME_PASTA_DE_VIDEOS)
from utilitarios import *
from whisper_service import transcrever_video

def medir_tempo(func, *args):
    inicio = time.time()
    resultado = func(*args)
    tempo = time.time() - inicio

    return resultado, tempo

def processar_video(modelo, video):
    caminho_video = os.path.join(NOME_PASTA_DE_VIDEOS, video)

    ja_processado, caminho_txt = (verificar_video_foi_processado(video))

    if ja_processado:
        print(f"[SKIP] {video}")
        gerar_log(f"SKIP - {video}")
        return

    print(f"Transcrevendo: {video}")

    texto, tempo = medir_tempo(transcrever_video,modelo,caminho_video)

    salvar_transcricao(texto, caminho_txt)

    print(f"OK: {video} ({tempo:.2f}s)")
    gerar_log(f"OK - {video} - {tempo:.2f}s")