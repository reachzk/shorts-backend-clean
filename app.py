from fastapi import FastAPI, UploadFile, File
import shutil
import os

from motion import detectar_melhores_momentos
from cutter import cortar_video

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Salvar o arquivo
    upload_folder = "/tmp/uploads"
    os.makedirs(upload_folder, exist_ok=True)

    video_path = os.path.join(upload_folder, file.filename)

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Detectar melhores momentos (baseado em movimento)
    momentos = detectar_melhores_momentos(video_path)

    # Cortar clips
    clips_paths = []
    for start, end in momentos:
        clip_out = cortar_video(video_path, start, end)
        clips_paths.append({"start": start, "end": end, "path": clip_out})

    return {
        "message": "Clipes gerados",
        "clips": clips_paths
    }
