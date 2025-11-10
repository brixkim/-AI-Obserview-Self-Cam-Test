import asyncio
import time
import os
import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from ultralytics import YOLO

APP_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(APP_DIR, "index.html")

app = FastAPI()
model = YOLO("./models/yolov12n-face.onnx", task="detect")

@app.get("/", response_class=HTMLResponse)
def home():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return f.read()

def bytes_to_bgrimage(b: bytes):
    arr = np.frombuffer(b, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img

def bgr_to_jpeg_bytes(img):
    ok, buf = cv2.imencode(".jpg", img)
    return buf.tobytes() if ok else None

def predict_bgr(frame_bgr: np.ndarray) -> np.ndarray:
    # mean_val = float(frame_bgr.mean()) if frame_bgr is not None else -1
    # print(f"[IN] frame {frame_bgr.shape if frame_bgr is not None else None} mean={mean_val:.1f}")
    # t0 = time.time()
    results = model.predict(source=frame_bgr, verbose=False)
    annotated = results[0].plot()
    # print(f"[PRED] {time.time() - t0:.3f}s")
    return annotated

@app.websocket("/ws/infer")
async def ws_infer(ws: WebSocket):
    await ws.accept()
    print("[WS] connected")
    try:
        while True:
            data = await ws.receive_bytes()
            # print(f"[WS] recv {len(data)} bytes")
            frame = bytes_to_bgrimage(data)
            loop = asyncio.get_event_loop()
            annotated = await loop.run_in_executor(None, predict_bgr, frame)
            out = bgr_to_jpeg_bytes(annotated)
            # print(f"[WS] send {len(out)} bytes")
            await ws.send_bytes(out)
    except WebSocketDisconnect:
        print("[WS] disconnected")
