import os
import time

from config import (NOME_PASTA_DE_VIDEOS)
from utilitarios import *
from whisper_service import transcrever_video
from audio_service import converter_video_para_audio

def medir_tempo(func, *args):
    inicio = time.time()
    resultado = func(*args)
    tempo = time.time() - inicio

    return resultado, tempo

def processar_video(modelo, video, idioma):
    caminho_video = os.path.join(NOME_PASTA_DE_VIDEOS, video)

    ja_processado, caminho_txt = verificar_video_foi_processado(video)

    if ja_processado:
        gerar_log(f"SKIP - {video}")
        return

    print(f"Transcrevendo: {video}")

    caminho_audio = converter_video_para_audio(caminho_video)

    texto, tempo = medir_tempo(transcrever_video, modelo, caminho_audio, idioma)
    os.remove(caminho_audio)

    salvar_transcricao(texto, caminho_txt)

    gerar_log(f"OK - {video} - {tempo:.2f}s")