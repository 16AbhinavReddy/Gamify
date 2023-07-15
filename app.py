import os
import re
import numpy as np
import shutil

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import recommendation

# Define a FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the IMDb dataset
df = recommendation.load_dataset()

# Train the recommendation system
cosine_sim_combined = recommendation.train_recommendation_system(df)

# Model saved with Keras model.save()
MODEL_PATH = 'gamify.h5'

# Load your trained model
model = load_model(MODEL_PATH)


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    x = x / 255
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)
    if preds == 0:
        preds = "Among Us"
    elif preds == 1:
        preds = "Apex Legends"
    elif preds == 2:
        preds = "Fortnite"
    elif preds == 3:
        preds = "Forza Horizon"
    elif preds == 4:
        preds = "Free Fire"
    elif preds == 5:
        preds = "Genshin Impact"
    elif preds == 6:
        preds = "God of War"
    elif preds == 7:
        preds = "Minecraft"
    elif preds == 8:
        preds = "Roblox"
    elif preds == 9:
        preds = "Terraria"

    return preds


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Save the file to ./uploads
    basepath = os.path.dirname(__file__)
    file_path = os.path.join(basepath, 'uploads', file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Make prediction
    preds = model_predict(file_path, model)
    recommendations = recommendation.get_recommendations(preds, cosine_sim_combined, df)

    result = str(preds)  # Convert to string
    response = {"result": result, "recommendations": recommendations}
    return response
