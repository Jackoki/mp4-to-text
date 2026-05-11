import os
import time
from faster_whisper import WhisperModel
from concurrent.futures import ThreadPoolExecutor, as_completed

NOME_PASTA_DE_VIDEOS = "videos"
NOME_PASTA_DE_TRANSCRICOES = "transcricoes"
LOG_FILE = "log.txt"


# ------------------ SETUP ------------------

def preparar_pastas():
    os.makedirs(NOME_PASTA_DE_VIDEOS, exist_ok=True)
    os.makedirs(NOME_PASTA_DE_TRANSCRICOES, exist_ok=True)


def carregar_modelo(usar_gpu):
    if usar_gpu:
        try:
            print("Carregando modelo na GPU...")
            return WhisperModel("base", device="cuda", compute_type="float16")

        except Exception:
            print("GPU indisponivel. Utilizando CPU...")

    print("Carregando modelo na CPU...")

    return WhisperModel("base", device="cpu", compute_type="int8")


def obter_videos(pasta):
    return [
        f for f in os.listdir(pasta)
        if f.lower().endswith(".mp4")
    ]


def escolher_processamento():
    while True:
        escolha = input(
            "Escolha a opcao:\n"
            "0 - CPU\n"
            "1 - GPU\n"
            "Opcao: "
        )

        if escolha in ["0", "1"]:
            return int(escolha)

        print("\nEscolha invalida\n")


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


# ------------------ PROCESSAMENTO ------------------

def processar_video(modelo, video):
    caminho_video = os.path.join(NOME_PASTA_DE_VIDEOS, video)

    ja_processado, caminho_txt = verificar_video_foi_processado(video)

    if ja_processado:
        print(f"[SKIP] {video}")
        gerar_log(f"SKIP - {video}")
        return

    print(f"\nTranscrevendo: {video}")
    start = time.time()

    texto = transcrever_video(modelo, caminho_video)
    tempo = time.time() - start
    salvar_transcricao(texto, caminho_txt)

    print(f"OK: {video} ({tempo:.2f}s)")

    gerar_log(f"OK - {video} - {tempo:.2f}s")


# ------------------ GPU ------------------

def processar_videos_normal(modelo, videos):
    print("\nIniciando processamento na GPU...")

    for video in videos:
        try:
            processar_video(modelo, video)

        except Exception as e:
            print(f"[ERRO] {e}")
            gerar_log(f"ERRO - {e}")


# ------------------ CPU PARALELO ------------------

def processar_videos_em_paralelo(modelo, videos, max_workers):
    print(f"\nIniciando processamento paralelo " f"({max_workers} workers)...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(processar_video,modelo,video)
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

    escolha = escolher_processamento()
    usar_gpu = (escolha == 1)
    modelo = carregar_modelo(usar_gpu)

    videos = obter_videos(NOME_PASTA_DE_VIDEOS)

    if not videos:
        print("Nenhum video encontrado")
        return

    if usar_gpu:
        processar_videos_normal(modelo, videos)

    else:
        workers = max(1, os.cpu_count() // 2)
        processar_videos_em_paralelo(modelo, videos, max_workers=workers)

    print("\nFinalizado.")


# ------------------ EXECUÇÃO ------------------

if __name__ == "__main__":
    main()