from fastapi import FastAPI, UploadFile, File
import uuid
import os

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # só pra testar: salvar o arquivo em /tmp
    os.makedirs("/tmp/uploads", exist_ok=True)
    filename = f"/tmp/uploads/{uuid.uuid4()}_{file.filename}"

    with open(filename, "wb") as f:
        f.write(await file.read())

    return {"message": "arquivo recebido", "path": filename}
