from fastapi import FastAPI, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
from typing import Optional, Dict
from enum import Enum

# Import all available models
from .models.blip_model import BLIPModel
from .models.vit_gpt2_model import VitGPT2Model
from .models.git_model import GITModel
from .models.base_model import BaseCaptionModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ModelType(str, Enum):
    BLIP = "blip"
    VIT_GPT2 = "vit_gpt2"
    GIT = "git"

# Model registry
models: Dict[ModelType, BaseCaptionModel] = {}
model_loading_status: Dict[ModelType, str] = {}

def get_or_load_model(model_type: ModelType) -> BaseCaptionModel:
    """Lazy load models on demand to save memory"""
    if model_type not in models:
        model_loading_status[model_type] = "loading"
        try:
            if model_type == ModelType.BLIP:
                models[model_type] = BLIPModel()
            elif model_type == ModelType.VIT_GPT2:
                models[model_type] = VitGPT2Model()
            elif model_type == ModelType.GIT:
                models[model_type] = GITModel()
            else:
                raise ValueError(f"Unknown model type: {model_type}")
            model_loading_status[model_type] = "loaded"
        except Exception as e:
            model_loading_status[model_type] = f"failed: {str(e)}"
            raise
    return models[model_type]

# Load default model
models[ModelType.BLIP] = BLIPModel()
model_loading_status[ModelType.BLIP] = "loaded"

@app.get("/models")
async def get_available_models():
    """Return list of available models"""
    return {
        "models": [
            {"id": ModelType.BLIP, "name": "BLIP", "description": "Salesforce BLIP base model (Recommended)"},
            {"id": ModelType.VIT_GPT2, "name": "ViT-GPT2", "description": "Lightweight and fast"},
            {"id": ModelType.GIT, "name": "GIT", "description": "Microsoft Generative Image-to-text"},
        ]
    }

@app.get("/model-status/{model_type}")
async def get_model_status(model_type: ModelType):
    """Check if a specific model is loaded, loading, or available"""
    status = "not_loaded"
    if model_type in models:
        status = "loaded"
    elif model_type in model_loading_status:
        status = model_loading_status[model_type]

    # Estimate download size for user info
    download_sizes = {
        ModelType.BLIP: "~1.8GB",
        ModelType.VIT_GPT2: "~600MB",
        ModelType.GIT: "~700MB"
    }

    return {
        "model": model_type,
        "status": status,
        "download_size": download_sizes.get(model_type, "Unknown"),
        "cache_location": "~/.cache/huggingface/hub/"
    }

@app.post("/describe")
async def describe_image(
    file: UploadFile,
    model: Optional[str] = Form(None)
):
    try:
        # Default to BLIP if no model specified
        model_type = ModelType(model) if model else ModelType.BLIP

        # Log the request
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Processing image with model: {model_type}")

        # Process the image
        image = Image.open(BytesIO(await file.read())).convert("RGB")
        caption_model = get_or_load_model(model_type)
        alt_text = caption_model.describe(image)

        return {"alt_text": alt_text, "model_used": model_type}
    except ValueError as e:
        # Invalid model name
        raise HTTPException(status_code=400, detail=f"Invalid model: {model}. Available models: blip, vit_gpt2, git")
    except Exception as e:
        # Log the full error for debugging
        import traceback
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error processing image: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
