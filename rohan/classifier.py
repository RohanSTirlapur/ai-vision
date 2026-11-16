"""
PetVision AI - Deep Learning Classifier Engine
Uses PyTorch with EfficientNet-B0 and MobileNetV3 architectures.
Maps ImageNet synsets to the 8 supported pet animal species categories:
1. Dogs
2. Cats
3. Rabbits
4. Birds
5. Hamsters
6. Guinea Pigs
7. Fish
8. Turtles

Strictly focuses on SPECIES recognition, deliberately abstracting away breed details.
"""

import os
import sys
import time
import types
import io
from typing import Dict, Any, Tuple
from PIL import Image

# 1. Environment & DLL Configuration for Windows PyTorch
torch_lib = r"C:\Users\Nagarjuna N\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\lib"
if os.path.exists(torch_lib):
    try:
        os.add_dll_directory(torch_lib)
    except Exception:
        pass

# Stub unused torchvision ops that require native _C compilation
if "torchvision._meta_registrations" not in sys.modules:
    sys.modules["torchvision._meta_registrations"] = types.ModuleType("torchvision._meta_registrations")
if "torchvision._autograd_registrations" not in sys.modules:
    sys.modules["torchvision._autograd_registrations"] = types.ModuleType("torchvision._autograd_registrations")

import torch
import torchvision.models as models
from pet_data import PET_PROFILES

# 2. ImageNet Class Mapping for the 8 Pet Animal Categories
DOG_INDICES = set(range(151, 269))  # 118 dog breeds in ImageNet
CAT_INDICES = set(range(281, 286))  # Tabby, Tiger cat, Persian, Siamese, Egyptian cat
RABBIT_INDICES = {330, 331, 332}    # Wood rabbit, Hare, Angora
BIRD_INDICES = (
    set(range(7, 25)) |             # Cock, hen, ostrich, finches, buntings, robin, bulbul, jay, etc.
    set(range(80, 101)) |           # Grouse, peacock, African grey, macaw, cockatoo, lorikeet, toucan, etc.
    set(range(127, 147))            # Stork, flamingo, heron, egret, crane, sandpiper, pelican, etc.
)
HAMSTER_INDICES = {333}             # Hamster
GUINEA_PIG_INDICES = {338}          # Guinea pig
FISH_INDICES = {0, 1, 389, 390, 391, 392, 393, 394, 395, 396, 397} # Goldfish, clownfish, tench, puffer, lionfish, etc.
TURTLE_INDICES = {33, 34, 35, 36, 37} # Loggerhead, leatherback, mud turtle, terrapin, box turtle

PET_CATEGORIES = {
    "Dog": DOG_INDICES,
    "Cat": CAT_INDICES,
    "Rabbit": RABBIT_INDICES,
    "Bird": BIRD_INDICES,
    "Hamster": HAMSTER_INDICES,
    "Guinea Pig": GUINEA_PIG_INDICES,
    "Fish": FISH_INDICES,
    "Turtle": TURTLE_INDICES
}

ALL_PET_INDICES = set()
for indices in PET_CATEGORIES.values():
    ALL_PET_INDICES.update(indices)


class PetClassifier:
    """Manages PyTorch deep learning models for pet animal recognition."""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.models: Dict[str, Any] = {}
        self.transforms: Dict[str, Any] = {}
        self.categories = None
        self._load_default_model()

    def _load_default_model(self):
        """Loads EfficientNet-B0 as the primary classifier."""
        print(f"[PetVision AI] Initializing deep learning engine on device: {self.device}")
        weights = models.EfficientNet_B0_Weights.DEFAULT
        model = models.efficientnet_b0(weights=weights)
        model.to(self.device)
        model.eval()
        
        self.models["efficientnet_b0"] = model
        self.transforms["efficientnet_b0"] = weights.transforms()
        self.categories = weights.meta["categories"]
        print("[PetVision AI] EfficientNet-B0 model loaded and ready.")

    def get_model(self, model_name: str = "efficientnet_b0") -> Tuple[Any, Any]:
        """Lazy load and return requested model and transform."""
        if model_name not in self.models:
            if model_name == "mobilenet_v3":
                print("[PetVision AI] Loading MobileNet-V3 Small model...")
                weights = models.MobileNet_V3_Small_Weights.DEFAULT
                model = models.mobilenet_v3_small(weights=weights)
                model.to(self.device)
                model.eval()
                self.models["mobilenet_v3"] = model
                self.transforms["mobilenet_v3"] = weights.transforms()
            else:
                model_name = "efficientnet_b0"
        return self.models[model_name], self.transforms[model_name]

    def classify(self, image_input: Any, model_name: str = "efficientnet_b0") -> Dict[str, Any]:
        """
        Classifies an input image into one of the 8 supported pet animal categories.
        
        image_input: bytes, PIL.Image, or file-like object.
        model_name: 'efficientnet_b0' or 'mobilenet_v3'
        """
        start_time = time.perf_counter()
        
        # Load and convert image to RGB
        if isinstance(image_input, (bytes, bytearray)):
            img = Image.open(io.BytesIO(image_input)).convert("RGB")
        elif isinstance(image_input, Image.Image):
            img = image_input.convert("RGB")
        else:
            img = Image.open(image_input).convert("RGB")
            
        width, height = img.size
        
        # Select model
        model, transform = self.get_model(model_name)
        input_tensor = transform(img).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            logits = model(input_tensor)
            probs = torch.softmax(logits, dim=1)[0].cpu()

        inference_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        
        # Raw Top-1 ImageNet prediction
        top1_idx = int(probs.argmax().item())
        top1_raw_label = self.categories[top1_idx]
        top1_raw_prob = float(probs[top1_idx].item())
        
        # Aggregate raw probability mass for each of the 8 pet categories
        category_raw_probs = {}
        for pet_name, indices in PET_CATEGORIES.items():
            prob_sum = float(sum(probs[idx].item() for idx in indices))
            category_raw_probs[pet_name] = prob_sum
            
        total_pet_prob = sum(category_raw_probs.values())
        is_pet_index = top1_idx in ALL_PET_INDICES
        
        # Determine whether this image is a supported pet
        # If the model strongly sees a non-pet object (e.g. car, person, table)
        # and total pet probability is negligible, flag as unsupported
        is_supported_pet = True
        if total_pet_prob < 0.08 and not is_pet_index:
            is_supported_pet = False
            
        # Calibrated normalized probabilities among the 8 categories
        if total_pet_prob > 0:
            normalized_probs = {k: v / total_pet_prob for k, v in category_raw_probs.items()}
        else:
            normalized_probs = {k: 1.0 / len(category_raw_probs) for k in category_raw_probs}
            
        # Top predicted pet category
        best_pet = max(normalized_probs, key=normalized_probs.get)
        best_prob = normalized_probs[best_pet]
        
        # Format probability distribution sorted by probability descending
        ranked_categories = []
        for name, prob in sorted(normalized_probs.items(), key=lambda x: x[1], reverse=True):
            profile = PET_PROFILES.get(name, {})
            ranked_categories.append({
                "name": name,
                "display_name": profile.get("display_name", name),
                "emoji": profile.get("emoji", "🐾"),
                "probability": round(prob, 4),
                "percentage": round(prob * 100, 2),
                "badge_color": profile.get("badge_color", "#3B82F6")
            })

        pet_profile = PET_PROFILES.get(best_pet, {})
        
        model_display_names = {
            "efficientnet_b0": "EfficientNet-B0 (PyTorch Deep CNN)",
            "mobilenet_v3": "MobileNet-V3 Small (PyTorch Lightweight CNN)"
        }

        return {
            "success": True,
            "predicted_category": best_pet,
            "display_name": pet_profile.get("display_name", best_pet),
            "emoji": pet_profile.get("emoji", "🐾"),
            "confidence_percentage": round(best_prob * 100, 2),
            "is_supported_pet": is_supported_pet,
            "raw_detection": {
                "label": top1_raw_label.replace("_", " ").title(),
                "confidence": round(top1_raw_prob * 100, 2)
            },
            "pet_profile": pet_profile,
            "all_categories": ranked_categories,
            "diagnostics": {
                "model_name": model_display_names.get(model_name, model_name),
                "model_key": model_name,
                "device": str(self.device).upper(),
                "inference_time_ms": inference_time_ms,
                "image_resolution": f"{width} × {height} px",
                "total_pet_density": round(total_pet_prob * 100, 2)
            }
        }


# Singleton instance
classifier = PetClassifier()
