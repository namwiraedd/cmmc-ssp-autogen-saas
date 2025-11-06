# backend/app/main.py
import os
import uuid
from fastapi import FastAPI, UploadFile, File, Depends, WebSocket, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from app.auth import get_current_user
from app.storage import S3Client
from app.processor import DocumentProcessor
from app.ssp_generator import SSPGenerator
from app.deps import get_db_session

app = FastAPI(title="CMMC SSP Generator MVP")

s3 = S3Client()
processor = DocumentProcessor(s3_client=s3)
ssp_gen = SSPGenerator(s3_client=s3)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), user=Depends(get_current_user)):
    # store original
    uid = str(uuid.uuid4())
    key = f"{user.tenant_id}/{uid}/{file.filename}"
    await s3.upload_stream(key, await file.read(), metadata={"uploaded_by": user.username})
    task_id = await processor.enqueue_parse(key, user=user, task_id=uid)
    return {"task_id": task_id, "s3_key": key}

@app.get("/download/{task_id}")
async def download_ssp(task_id: str, user=Depends(get_current_user)):
    # returns generated SSP docx
    path = await ssp_gen.get_ssp_for_task(task_id, user=user)
    if not path:
        raise HTTPException(404, "Not found")
    return FileResponse(path, filename=f"SSP_{task_id}.docx")

@app.websocket("/ws/progress/{task_id}")
async def ws_progress(websocket: WebSocket, task_id: str, user=Depends(get_current_user)):
    await websocket.accept()
    try:
        async for status in processor.stream_status(task_id, user=user):
            await websocket.send_json(status)
    finally:
        await websocket.close()

@app.get("/health")
async def health():
    return {"status": "ok"}
