from utilitarios import (preparar_pastas, obter_videos)
from whisper_service import (escolher_processamento, carregar_modelo)
from paralelismo import (processar_videos_normal,processar_videos_em_paralelo)
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

    if usar_gpu:
        processar_videos_normal(modelo,videos)

    else:
        processar_videos_em_paralelo(modelo, videos, os.cpu_count())

    print("\nFinalizado.")


if __name__ == "__main__":
    main()