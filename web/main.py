from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import whisper, os, uuid, subprocess

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")

model = whisper.load_model("base")
UPLOAD_DIR = "/data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())
    path = f"{UPLOAD_DIR}/{uid}_{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    audio = path + ".wav"
    subprocess.run(["ffmpeg", "-i", path, "-ar", "16000", "-ac", "1", audio])

    result = model.transcribe(audio)
    return {"text": result["text"]}
