# impl-env
import os
import sys
import torch
from PIL import Image
import torchvision.transforms as transforms

# Add repo path
BASE_DIR = r"D:\VIT Projects\Sem 4 Project\Implementation\gan-attribution-app\backend"
sys.path.append(os.path.join(BASE_DIR, "UniversalFakeDetect"))

from models import get_model

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# -----------------------------
# Load UniversalFakeDetect
# -----------------------------
ARCH = "CLIP:ViT-L/14"

MODEL_PATH = os.path.join(
    BASE_DIR,
    "UniversalFakeDetect",
    "pretrained_weights",
    "fc_weights.pth"
)

model = get_model(ARCH)

state_dict = torch.load(MODEL_PATH, map_location="cpu")
model.fc.load_state_dict(state_dict)

model.eval()
model.to(DEVICE)

print("UniversalFakeDetect loaded.")

# -----------------------------
# Image transform
# -----------------------------
MEAN = [0.48145466, 0.4578275, 0.40821073]
STD  = [0.26862954, 0.26130258, 0.27577711]

transform = transforms.Compose([
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=MEAN, std=STD),
])


# -----------------------------
# Detection Function
# -----------------------------
def detect_fake(image_path):

    print("Running deepfake detection...")

    img = Image.open(image_path).convert("RGB")
    img = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        pred = model(img)
        prob = torch.sigmoid(pred).item()

    return prob