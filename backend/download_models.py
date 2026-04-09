from huggingface_hub import hf_hub_download
import os

REPO_ID = os.getenv("HUGGINGFACE_REPO_ID")

def download_models():
    base_dir = os.path.dirname(__file__)
    model_dir = os.path.join(base_dir, "models")

    os.makedirs(model_dir, exist_ok=True)

    files = [
        "e4e_ffhq_encode.pt",
        "gan_attribution_model.pkl",
        "gan_scaler.pkl",
        "gan_label_encoder.pkl"
    ]

    for file in files:
        file_path = os.path.join(model_dir, file)

        if not os.path.exists(file_path):
            print(f"Downloading {file}...")

            hf_hub_download(
                repo_id=REPO_ID,
                filename=file,
                local_dir=model_dir,
                local_dir_use_symlinks=False
            )

        else:
            print(f"{file} already exists. Skipping.")