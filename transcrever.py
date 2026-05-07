import whisper
import os

PASTA_VIDEOS = "videos"
PASTA_TRANSCRICOES = "transcricoes"

os.makedirs(PASTA_VIDEOS, exist_ok=True)
os.makedirs(PASTA_TRANSCRICOES, exist_ok=True)

print("Carregando modelo...")
model = whisper.load_model("base")

videos = [f for f in os.listdir(PASTA_VIDEOS) if f.endswith(".mp4")]

if not videos:
    print("Nenhum vídeo encontrado.")
    exit()

for video in videos:
    caminho_video = os.path.join(PASTA_VIDEOS, video)

    print(f"\nTranscrevendo: {video}")

    resultado = model.transcribe(caminho_video)

    texto = resultado["text"]

    nome_txt = os.path.splitext(video)[0] + ".txt"
    caminho_txt = os.path.join(PASTA_TRANSCRICOES, nome_txt)

    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"Transcrição salva: {nome_txt}")

print("\nFinalizado.")