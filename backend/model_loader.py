import os
import joblib

model = joblib.load(os.path.join("models", "gan_attribution_model.pkl"))
scaler = joblib.load(os.path.join("models", "gan_scaler.pkl"))
label_encoder = joblib.load(os.path.join("models", "gan_label_encoder.pkl"))

print("Model loaded. Expected features:", scaler.n_features_in_)