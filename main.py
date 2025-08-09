

import os
from openai import OpenAI
import csv
from dotenv import load_dotenv
import subprocess
import tempfile
import shutil

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Defina a variável de ambiente OPENAI_API_KEY no arquivo .env")
client = OpenAI(api_key=api_key)
audio_speed = float(os.getenv("AUDIO_SPEED", "2.0"))
if not (0.5 <= audio_speed <= 2.0):
    raise RuntimeError("AUDIO_SPEED deve estar entre 0.5 e 2.0")

def compress_audio_with_ffmpeg(input_path: str, speed_factor: float) -> str:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg não encontrado no sistema. Instale o ffmpeg para usar a compactação de áudio.")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_file_path = temp_file.name
    temp_file.close()
    command = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-vn",
        "-filter:a",
        f"atempo={speed_factor}",
        "-acodec",
        "pcm_s16le",
        temp_file_path,
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise
    return temp_file_path
def extrair_horario(nome):
    parts = nome.split(" at ")
    return parts[1].rsplit(".", 1)[0] if len(parts) == 2 else nome

EXTS = {".ogg", ".mp3", ".wav", ".m4a"}
def transcribe(path):
    compressed_path = compress_audio_with_ffmpeg(path, audio_speed) if audio_speed != 1.0 else path
    try:
        with open(compressed_path, "rb") as f:
            response = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            language="pt"
            )
    finally:
        if compressed_path != path and os.path.exists(compressed_path):
            os.remove(compressed_path)
    return response.text.strip().replace("\n", " ")

def main():
    arquivos = sorted(
        [f for f in os.listdir(".") if os.path.splitext(f)[1].lower() in EXTS],
        key=extrair_horario
    )

    with open("transcricoes_api.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Horario", "Transcricao"])

        for arq in arquivos:
            print(f"Transcrevendo {arq}...")
            texto = transcribe(arq)
            horario = extrair_horario(arq)
            writer.writerow([horario, texto])

    print("✅ Transcrição concluída em transcricoes_api.csv")

if __name__ == "__main__":
    main()
