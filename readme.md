# 🎥 MP4 to Text - Whisper Transcription System

Sistema de transcrição automática de vídeos MP4 usando Faster-Whisper, com suporte a CPU e GPU (CUDA).

---

## 🚀 Sobre o projeto

Este projeto realiza a transcrição automática de arquivos de vídeo `.mp4`, gerando arquivos `.txt` com o conteúdo falado no vídeo.

---

## ⚙️ Funcionalidades

- 🧠 Transcrição com Whisper (Faster-Whisper)
- ⚡ Suporte a GPU (CUDA) e CPU
- 🔁 Processamento em paralelo (CPU)
- 💾 Salvamento automático das transcrições
- 📄 Sistema de logs
- ⏭️ Skip de vídeos já processados

---

## 🧰 Tecnologias

- Python 3.11+ (recomendado 3.11)
- ffmpeg
- faster-whisper
- ctranslate2
- tqdm
- CUDA 12 (opcional para GPU)
- cuDNN (opcional para GPU)

---

## 📁 Estrutura do projeto

```text
mp4-to-text/
│
├── main.py
├── config.py
├── utilitarios.py
├── whisper_service.py
├── processamento.py
├── paralelismo.py
│
├── videos/
├── transcricoes/
└── log.txt

---

## 📦 Instalação do FFmpeg

O FFmpeg é uma ferramenta utilizada para leitura e processamento de arquivos de vídeo e áudio.  
Ele pode ser necessário em alguns sistemas para garantir compatibilidade com arquivos `.mp4`.

---

## 🔎 1. Verificar se já está instalado

Abra o terminal e execute:

```bash id="check_ffmpeg"
ffmpeg -version

Se aparecer a versão, o FFmpeg já está instalado e não é necessário fazer nada.

Caso contrário, siga as instruções abaixo:
Baixe a versão para Windows:
https://www.gyan.dev/ffmpeg/builds/

Recomendado: ffmpeg-git-full

Extraia o arquivo .zip

Renomeie a pasta para algo simples, por exemplo:

C:\ffmpeg

Adicione o PATH

Abra:

Painel de Controle → Sistema → Configurações avançadas do sistema
Clique em Variáveis de Ambiente
Em “Path”, clique em Editar
Adicione:
C:\ffmpeg\bin
Testar instalação

Abra o terminal novamente e execute:

ffmpeg -version

Se aparecer informações da versão, está pronto

---

## ⚡ Instalação do CUDA (GPU NVIDIA)

Se você deseja usar a GPU para acelerar a transcrição, será necessário instalar o CUDA Toolkit e o cuDNN.

### 🔎 1. Verifique se sua GPU suporta CUDA

Execute no terminal:

```bash
nvidia-smi
Se aparecer sua placa NVIDIA, ela é compatível.

Baixe o CUDA Toolkit:

https://developer.nvidia.com/cuda-downloads

Escolha:

Sistema operacional: Windows
Versão: 12.x

Instale normalmente (Next → Next → Finish).
Depois disso, baixe o cuDNN:

https://developer.nvidia.com/cudnn

Você precisa:
Criar conta NVIDIA (gratuita)
Baixar versão compatível com CUDA 12

Depois de baixar:

Extraia o ZIP
Copie as pastas:
bin
include
lib

Para a pasta do CUDA:
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.x\ (Ou o lugar que foi instalado o CUDA)

Adicione no PATH do Windows:
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.x\bin
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.x\libnvvp
