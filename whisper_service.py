from faster_whisper import WhisperModel

def carregar_modelo(usar_gpu):
    if usar_gpu:
        try:
            print("Carregando modelo na GPU...")
            return WhisperModel("base", device="cuda", compute_type="int8_float32")

        except Exception as e:
            print(f"Erro GPU: {e}")
            print("GPU indisponivel. Utilizando CPU...")

    print("Carregando modelo na CPU...")
    return WhisperModel("base", device="cpu", compute_type="int8")

def escolher_processamento():
    while True:
        escolha = input("Escolha a opcao:\n" "0 - CPU\n""1 - GPU (Execute em modo Administrador)\n" "Opcao: ")

        if escolha in ["0", "1"]:
            return int(escolha)

        print("\nEscolha invalida\n")

def transcrever_video(modelo, caminho_video):
    segments, _ = modelo.transcribe(caminho_video, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500))
    linhas = []

    for seg in segments:
        linhas.append(f"[{seg.start:.2f} - {seg.end:.2f}] {seg.text}")

    return "\n".join(linhas)