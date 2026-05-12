import subprocess
import os

def converter_video_para_audio(caminho_video):
    nome_base = os.path.splitext(caminho_video)[0]

    caminho_audio = f"{nome_base}.wav"

    comando = [
        "ffmpeg",
        "-i", caminho_video,
        "-ar", "16000",
        "-ac", "1",
        "-vn",
        caminho_audio,
        "-y"
    ]

    subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return caminho_audio