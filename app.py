from fastapi import FastAPI, UploadFile, File
from moviepy.editor import VideoFileClip
import uuid
import os

app = FastAPI()

UPLOAD_DIR = "/tmp/uploads"
CLIPS_DIR = "/tmp/clips"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CLIPS_DIR, exist_ok=True)

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    # Salvar arquivo original
    original_name = f"{uuid.uuid4()}_{file.filename}"
    input_path = os.path.join(UPLOAD_DIR, original_name)

    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Carrega vídeo
    clip = VideoFileClip(input_path)

    duration = clip.duration
    clips_paths = []

    # Cortar em partes de 30 segundos
    chunk_size = 30

    part = 0
    start = 0

    while start < duration:
        end = min(start + chunk_size, duration)
        
        output_name = f"{uuid.uuid4()}_clip_{part}.mp4"
        output_path = os.path.join(CLIPS_DIR, output_name)

        subclip = clip.subclip(start, end)
        subclip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        clips_paths.append(output_path)

        part += 1
        start += chunk_size

    clip.close()

    return {
        "message": "Clipes gerados com sucesso!",
        "clips": clips_paths
    }
