import os
import time
from tqdm import tqdm

NOME_PASTA_DE_VIDEOS = "videos"
NOME_PASTA_DE_TRANSCRICOES = "transcricoes"
LOG_FILE = "log.txt"


def preparar_pastas():
    os.makedirs(NOME_PASTA_DE_VIDEOS, exist_ok=True)
    os.makedirs(NOME_PASTA_DE_TRANSCRICOES, exist_ok=True)


def carregar_modelo():
    import whisper
    return whisper.load_model("base")


def obter_videos(pasta):
    return [f for f in os.listdir(pasta) if f.endswith(".mp4")]


def verificar_video_foi_processado(video):
    nome_txt = os.path.splitext(video)[0] + ".txt"
    caminho_txt = os.path.join(NOME_PASTA_DE_TRANSCRICOES, nome_txt)
    return os.path.exists(caminho_txt), caminho_txt


def transcrever_video(modelo, caminho_video):
    return modelo.transcribe(caminho_video)


def medir_tempo(func, *args):
    start = time.time()
    resultado = func(*args)
    tempo = time.time() - start
    return resultado, tempo


def gerar_log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def gerar_texto_com_timestamp(result):
    linhas = []

    for seg in result["segments"]:
        start = seg["start"]
        end = seg["end"]
        text = seg["text"]

        linhas.append(f"[{start:.2f} - {end:.2f}] {text}")

    return "\n".join(linhas)


def salvar_transcricao(texto, caminho_saida):
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(texto)


def processar_video(modelo, video):
    caminho_video = os.path.join(NOME_PASTA_DE_VIDEOS, video)

    ja_processado, caminho_txt = verificar_video_foi_processado(video)

    if ja_processado:
        print(f"[SKIP] {video}")
        gerar_log(f"SKIP - {video}")
        return

    print(f"Transcrevendo: {video}")

    resultado, tempo = medir_tempo(transcrever_video, modelo, caminho_video)
    texto = gerar_texto_com_timestamp(resultado)
    salvar_transcricao(texto, caminho_txt)

    print(f"OK: {video} ({tempo:.2f}s)")
    gerar_log(f"OK - {video} - {tempo:.2f}s")


def main():
    print("Iniciando sistema...")

    preparar_pastas()
    modelo = carregar_modelo()

    videos = obter_videos(NOME_PASTA_DE_VIDEOS)

    if not videos:
        print("Nenhum vídeo encontrado")
        return

    for video in tqdm(videos, desc="Transcrevendo vídeos"):
        processar_video(modelo, video)

    print("\nFinalizado.")


if __name__ == "__main__":
    main()