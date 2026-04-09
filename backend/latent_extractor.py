import sys
import os
import torch
import numpy as np
import random
from PIL import Image
from argparse import Namespace
from torchvision import transforms

# ------------------------------------------------
# Fix namespace collision with UniversalFakeDetect
# ------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
E4E_ROOT = os.path.join(BASE_DIR, "encoder4editing")

# Remove previously loaded models module (if any)
if "models" in sys.modules:
    del sys.modules["models"]

# Force encoder4editing to be first in import path
sys.path.insert(0, E4E_ROOT)

# Import exactly as encoder4editing expects
from models.psp import pSp

# ------------------------------------------------
# Device
# ------------------------------------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ------------------------------------------------
# Load e4e model
# ------------------------------------------------
E4E_CKPT = os.path.join(BASE_DIR, "models", "e4e_ffhq_encode.pt")

ckpt = torch.load(E4E_CKPT, map_location=DEVICE)

opts = ckpt["opts"]
opts["checkpoint_path"] = E4E_CKPT
opts["device"] = DEVICE
opts = Namespace(**opts)

print("Loading e4e over the pSp framework from checkpoint:", E4E_CKPT)

net = pSp(opts).to(DEVICE)
net.eval()

# ------------------------------------------------
# Deterministic Transform (MATCH TRAINING)
# ------------------------------------------------
random.seed(42)

class ResolutionAugment:
    def __init__(self, min_res=64, max_res=1024):
        self.min_res = min_res
        self.max_res = max_res

    def __call__(self, img):
        rand_res = random.randint(self.min_res, self.max_res)

        # simulate random resolution
        img = transforms.Resize((rand_res, rand_res))(img)

        # normalize back to model input size
        img = transforms.Resize((256, 256))(img)

        return img


transform = transforms.Compose([
    ResolutionAugment(64, 1024),
    transforms.ToTensor(),
    transforms.Normalize([0.5] * 3, [0.5] * 3)
])

# ------------------------------------------------
# Feature Extraction (FULL W+ LATENT)
# ------------------------------------------------
def extract_features(image_path):

    img = Image.open(image_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():

        # 🔴 USE encoder-only for consistency
        w_plus = net.encoder(img_tensor)

    w_plus = w_plus.squeeze(0).cpu().numpy()

    features = w_plus.flatten()

    print("Feature shape (should be 9216):", features.shape)

    return features