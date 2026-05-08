import os
import time
from tqdm import tqdm
from faster_whisper import WhisperModel
from concurrent.futures import ThreadPoolExecutor, as_completed

NOME_PASTA_DE_VIDEOS = "videos"
NOME_PASTA_DE_TRANSCRICOES = "transcricoes"
LOG_FILE = "log.txt"


# ------------------ SETUP ------------------

def preparar_pastas():
    os.makedirs(NOME_PASTA_DE_VIDEOS, exist_ok=True)
    os.makedirs(NOME_PASTA_DE_TRANSCRICOES, exist_ok=True)


def carregar_modelo():
    return WhisperModel("base", device="cpu", compute_type="int8")


def obter_videos(pasta):
    return [f for f in os.listdir(pasta) if f.endswith(".mp4")]


# ------------------ UTILITÁRIOS ------------------

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


# ------------------ WHISPER ------------------

def transcrever_video(modelo, caminho_video):
    segments, info = modelo.transcribe(caminho_video)

    linhas = []
    for seg in segments:
        linhas.append(f"[{seg.start:.2f} - {seg.end:.2f}] {seg.text}")

    return "\n".join(linhas)


def medir_tempo(func, *args):
    start = time.time()
    resultado = func(*args)
    tempo = time.time() - start
    return resultado, tempo


# ------------------ PIPELINE DE PROCESSAMENTO ------------------

def processar_video(modelo, video):
    caminho_video = os.path.join(NOME_PASTA_DE_VIDEOS, video)

    ja_processado, caminho_txt = verificar_video_foi_processado(video)

    if ja_processado:
        print(f"[SKIP] {video}")
        gerar_log(f"SKIP - {video}")
        return

    print(f"Transcrevendo: {video}")

    texto, tempo = medir_tempo(transcrever_video, modelo, caminho_video)

    salvar_transcricao(texto, caminho_txt)

    print(f"OK: {video} ({tempo:.2f}s)")
    gerar_log(f"OK - {video} - {tempo:.2f}s")


# ------------------ PARALELISMO ------------------

def processar_videos_em_paralelo(modelo, videos, max_workers=2):
    print(f"Iniciando processamento paralelo ({max_workers} workers)...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(processar_video, modelo, video)
            for video in videos
        ]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"[ERRO] {e}")
                gerar_log(f"ERRO - {e}")


# ------------------ MAIN ------------------

def main():
    print("Iniciando sistema...")

    preparar_pastas()
    modelo = carregar_modelo()

    videos = obter_videos(NOME_PASTA_DE_VIDEOS)

    if not videos:
        print("Nenhum vídeo encontrado")
        return

    processar_videos_em_paralelo(modelo, videos, max_workers=2)

    print("\nFinalizado.")


# ------------------ EXECUÇÃO ------------------

if __name__ == "__main__":
    main()