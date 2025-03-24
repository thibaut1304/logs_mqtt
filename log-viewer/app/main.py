# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

app = FastAPI()
LOGS_DIR = Path("logs")

@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse("templates/index.html")

@app.get("/logs")
def list_logs():
    result = {}
    for subdir in LOGS_DIR.iterdir():
        if subdir.is_dir():
            files = [f.name for f in subdir.glob("*.log")]
            result[subdir.name] = files
    return result

@app.get("/logs/{folder}/{filename}")
def read_log(folder: str, filename: str):
    file_path = LOGS_DIR / folder / filename
    if file_path.exists():
        with open(file_path, "r") as f:
            return {"content": f.read()}
    return JSONResponse({"error": "Fichier introuvable"}, status_code=404)
