from concurrent.futures import (ThreadPoolExecutor, as_completed)
from processamento import processar_video
from utilitarios import gerar_log
from tqdm import tqdm

def processar_videos_normal(modelo, videos):
    print("\nIniciando processamento na GPU...")

    for video in tqdm(videos, desc="Processando vídeos"):
        try:
            processar_video(modelo, video)

        except Exception as e:
            print(f"[ERRO] {e}")
            gerar_log(f"ERRO - {e}")

def processar_videos_em_paralelo(modelo, videos, max_workers):
    print(f"\nIniciando processamento paralelo " f"({max_workers} workers)...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(processar_video, modelo, video) for video in videos]


        for future in tqdm(as_completed(futures), total=len(futures), desc="Processando vídeos"):
            try:
                future.result()

            except Exception as e:
                print(f"[ERRO] {e}")
                gerar_log(f"ERRO - {e}")