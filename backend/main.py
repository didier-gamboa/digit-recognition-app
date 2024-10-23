from fastapi import FastAPI
from fastapi import FastAPI, Request
from tensorflow import keras
import numpy as np

# Initialization of the FastAPI Aplication
app = FastAPI()

# Load Model
model = keras.models.load_model('./models/ocr_model.h5')

@app.post("/predict")
async def predict_digit(request: Request):
    data = await request.json()
    img = np.array(data["image"])
    image_array = img.reshape(1, 28, 28, 1) / 255.0
    predicted_proba = model.predict(image_array)
    predicted_label = predicted_proba.argmax(axis=1)[0]
    return {"predicted_label": int(predicted_label),
            "predicted_proba": predicted_proba.tolist()}