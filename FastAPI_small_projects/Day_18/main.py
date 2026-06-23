from fastapi import FastAPI, File, UploadFile
import os
import uuid

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload-safe")
async def upload_safe(file: UploadFile = File(...)):

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {
        "filename": unique_name,
        "message": "File uploaded safely 🚀"
    }

# Streaming version

@app.post("/upload-stream")
async def upload_stream(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:

        while chunk := await file.read(1024 * 1024):
            f.write(chunk)

    return {"message": "Stream upload complete 🚀"}

from fastapi import Form

@app.post("/upload-meta")
async def upload_meta(
    file: UploadFile = File(...),
    description: str = Form(...)
):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {
        "filename": file.filename,
        "description": description
    }