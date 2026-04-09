from dotenv import load_dotenv
load_dotenv()

from download_models import download_models

download_models()

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import numpy as np
import random

from deepfake_detector import detect_fake
from latent_extractor import extract_features
from model_loader import model, scaler, label_encoder

random.seed(42)

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
PORT = int(os.getenv("BACKEND_PORT", 5000))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    face_path = filepath

    # -------------------------
    # Stage 1: Deepfake Detection
    # -------------------------
    fake_prob = detect_fake(face_path)
    print("Deepfake probability:", fake_prob)

    THRESHOLD = float(os.getenv("MODEL_THRESHOLD", 0.89))

    if fake_prob < THRESHOLD:
        return jsonify({
            "prediction": "Authentic Image",
            "confidence": round(1 - fake_prob, 4),
            "probabilities": {
                "Real": float(1 - fake_prob),
                "Fake": float(fake_prob)
            }
        })

    print("Fake prob:", fake_prob)

    # -------------------------
    # Stage 2: GAN Attribution
    # -------------------------
    features = extract_features(face_path)

    print("Feature shape:", features.shape)
    print("Scaler expects:", scaler.n_features_in_)

    features = scaler.transform(features.reshape(1, -1))  # ONLY ONCE

    probs = model.predict_proba(features)[0]

    pred_idx = int(np.argmax(probs))
    confidence = float(np.max(probs))

    predicted_label = label_encoder.inverse_transform([pred_idx])[0]

    probability_distribution = {
        label_encoder.inverse_transform([i])[0]: float(probs[i])
        for i in range(len(probs))
    }

    print("Predicted probabilities:", probs)
    print("Predicted label:", predicted_label)

    return jsonify({
        "prediction": predicted_label,
        "confidence": round(confidence, 4),
        "probabilities": probability_distribution,
        "deepfake_score": float(fake_prob)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)