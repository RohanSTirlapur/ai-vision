"""
PetVision AI - FastAPI Web Application
Provides REST API endpoints for deep learning pet animal recognition
and serves the web application front-end.
"""

import os
from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from classifier import classifier, PET_CATEGORIES
from pet_data import PET_PROFILES

app = FastAPI(
    title="PetVision AI",
    description="AI-Powered Pet Animal Species Recognition API using PyTorch Deep Learning",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serves the main single-page web application."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Index HTML not found")
    return FileResponse(index_path)


@app.post("/api/analyze")
async def analyze_pet_image(
    file: UploadFile = File(...),
    model: str = Query(default="efficientnet_b0")
):
    """
    Analyzes an uploaded pet image using deep learning.
    Identifies which of the 8 pet animal categories is present.
    """
    if model not in {"efficientnet_b0", "mobilenet_v3"}:
        raise HTTPException(
            status_code=400,
            detail="Unsupported model. Choose 'efficientnet_b0' or 'mobilenet_v3'."
        )

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file.content_type}'. Please upload an image file (JPEG, PNG, WEBP)."
        )

    try:
        image_bytes = await file.read()
        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        result = classifier.classify(image_bytes, model_name=model)
        result["filename"] = file.filename
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image classification error: {str(e)}")


@app.get("/api/categories")
async def get_categories():
    """Returns the 8 supported pet animal categories with rich metadata."""
    categories_list = []
    for pet_name in PET_CATEGORIES.keys():
        profile = PET_PROFILES.get(pet_name, {})
        categories_list.append({
            "name": pet_name,
            "display_name": profile.get("display_name", pet_name),
            "emoji": profile.get("emoji", "🐾"),
            "scientific_name": profile.get("scientific_name", ""),
            "lifespan": profile.get("lifespan", ""),
            "diet": profile.get("diet", ""),
            "badge_color": profile.get("badge_color", "#3B82F6"),
            "sample_image": f"/static/samples/{pet_name.lower().replace(' ', '_')}.jpg"
        })
    return {
        "success": True,
        "count": len(categories_list),
        "supported_categories": categories_list,
        "notice": "This system exclusively classifies animal species categories. Breed identification is explicitly excluded."
    }


@app.get("/api/models")
async def get_available_models():
    """Returns information about the PyTorch classification backbones."""
    return {
        "success": True,
        "current_device": str(classifier.device).upper(),
        "models": [
            {
                "id": "efficientnet_b0",
                "name": "EfficientNet-B0",
                "type": "Deep Convolutional Neural Network (Compound Scaling)",
                "parameters": "5.3 Million",
                "default": True,
                "strengths": "State-of-the-art accuracy, balanced depth and width, optimal for animal feature extraction."
            },
            {
                "id": "mobilenet_v3",
                "name": "MobileNet-V3 Small",
                "type": "Mobile-Optimized Inverted Residual CNN",
                "parameters": "2.5 Million",
                "default": False,
                "strengths": "Ultra-low latency, highly efficient, optimized for real-time edge inference."
            }
        ]
    }


@app.get("/api/samples")
async def get_sample_images():
    """Returns available sample pet images for quick testing."""
    samples = []
    for pet_name in PET_CATEGORIES.keys():
        slug = pet_name.lower().replace(' ', '_')
        path = f"/static/samples/{slug}.jpg"
        samples.append({
            "category": pet_name,
            "title": f"Sample {pet_name}",
            "emoji": PET_PROFILES.get(pet_name, {}).get("emoji", "🐾"),
            "url": path
        })
    return {"samples": samples}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "PetVision AI",
        "backend": "FastAPI + PyTorch",
        "supported_species_count": 8
    }
