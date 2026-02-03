from flask import Flask, request, jsonify, render_template
import numpy as np
import cv2
import os
import gdown
from keras.models import load_model

# ================= CONFIG =================
MODEL_FILE = "road_anomaly_model.h5"
FILE_ID = "1FiHUDZPL1MFyG1g06_jjM4MJV2tH9rpg"
CLASS_NAMES = ['Accident', 'Fight', 'Fire', 'Snatching']
CONF_THRESHOLD = 0.85
IMG_SIZE = (224, 224)

app = Flask(__name__)

# ================= DOWNLOAD MODEL =================
def download_model():
    if not os.path.exists(MODEL_FILE):
        print("⬇️ Downloading model from Google Drive...")
        gdown.download(
            f"https://drive.google.com/uc?id={FILE_ID}",
            MODEL_FILE,
            quiet=False
        )

download_model()

# ================= LOAD MODEL =================
model = load_model(MODEL_FILE)

# ================= PREPROCESS =================
def preprocess(img):
    img = cv2.resize(img, IMG_SIZE)
    img = img.astype("float32") / 255.0
    return np.expand_dims(img, axis=0)

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})

    file = request.files["image"]
    img_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Invalid image"})

    preds = model.predict(preprocess(img), verbose=0)
    class_id = int(np.argmax(preds))
    confidence = float(np.max(preds))

    return jsonify({
        "class": CLASS_NAMES[class_id],
        "confidence": confidence,
        "emergency": 1 if confidence >= CONF_THRESHOLD else 0
    })

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
