def detectar_idioma(modelo, caminho_audio):
    _, info = modelo.transcribe(caminho_audio,beam_size=1)

    return info.language