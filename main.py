from utilitarios import (preparar_pastas, obter_videos)
from whisper_service import (escolher_processamento, carregar_modelo)
from paralelismo import (processar_videos_normal,processar_videos_em_paralelo)
from audio_service import converter_video_para_audio
from idioma_service import detectar_idioma
from config import (NOME_PASTA_DE_VIDEOS)
import os

def main():
    print("Iniciando sistema...")

    preparar_pastas()
    escolha = escolher_processamento()
    usar_gpu = escolha == 1
    modelo = carregar_modelo(usar_gpu)
    videos = obter_videos()

    print(f"\n{len(videos)} video(s) encontrado(s)")

    if not videos:
        print("Nenhum video encontrado")
        return

    primeiro_video = videos[0]

    caminho_primeiro_video = os.path.join(NOME_PASTA_DE_VIDEOS,primeiro_video)

    primeiro_audio = converter_video_para_audio(caminho_primeiro_video)

    idioma = detectar_idioma(modelo, primeiro_audio)
    os.remove(primeiro_audio)
    print(f"\nIdioma detectado: {idioma}")

    if usar_gpu:
        processar_videos_normal(modelo, videos, idioma)

    else:
        cpu_workers = max(1, (os.cpu_count() or 1) // 2)
        processar_videos_em_paralelo(modelo, videos, idioma, cpu_workers)

    print("\nFinalizado.")


if __name__ == "__main__":
    main()