from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import numpy as np
import cv2
import tempfile

app = FastAPI()
model = YOLO("app/model/best.pt")  # adjust path if needed

@app.get("/")
def read_root():
    return {"status": "YOLO API is running"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            cv2.imwrite(tmp.name, image)
            results = model(tmp.name)

        boxes = results[0].boxes
        output = []
        for box in boxes:
            cls = int(box.cls.item())
            conf = float(box.conf.item())
            xyxy = box.xyxy.cpu().numpy().tolist()[0]
            output.append({
                "class": model.names[cls],
                "confidence": round(conf, 4),
                "box": [round(x, 2) for x in xyxy]
            })

        return JSONResponse(content={"predictions": output})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
