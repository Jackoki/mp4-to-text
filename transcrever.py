import os

NOME_PASTA_DE_VIDEOS = "videos"
NOME_PASTA_DE_TRANSCRICOES = "transcricoes"

def preparar_pastas():
    os.makedirs(NOME_PASTA_DE_VIDEOS, exist_ok=True)
    os.makedirs(NOME_PASTA_DE_TRANSCRICOES, exist_ok=True)


def carregar_modelo():
    import whisper
    return whisper.load_model("base")


def obter_videos(pasta):
    return [f for f in os.listdir(pasta) if f.endswith(".mp4")]


def transcrever_video(modelo, caminho_video):
    return modelo.transcribe(caminho_video)


def salvar_transcricao(texto, caminho_saida):
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(texto)


def processar_video(modelo, pasta_videos, pasta_transcricoes, video):
    caminho_video = os.path.join(pasta_videos, video)

    resultado = transcrever_video(modelo, caminho_video)
    texto = resultado["text"]

    nome_txt = os.path.splitext(video)[0] + ".txt"
    caminho_txt = os.path.join(pasta_transcricoes, nome_txt)

    salvar_transcricao(texto, caminho_txt)

    print(f"Transcrição salva: {nome_txt}")


def main():
    print("Carregando modelo e pastas...")

    preparar_pastas()
    model_whisper = carregar_modelo()

    videos = obter_videos(NOME_PASTA_DE_VIDEOS)

    if not videos:
        print("Nenhum vídeo na pasta de vídeos")
        return

    for video in videos:
        print(f"\nTranscrevendo: {video}")
        processar_video(model_whisper, NOME_PASTA_DE_VIDEOS, NOME_PASTA_DE_TRANSCRICOES, video)

    print("\nFinalizado.")


if __name__ == "__main__":
    main()