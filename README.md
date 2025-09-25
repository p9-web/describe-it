# Alt Text Generator

A Python + Vue 3 app that generates suggested alt text for images using free Hugging Face models with multiple model options.

- Upload an image → instantly get alt text suggestions.
- Drag & drop or click-to-select images.
- Modern responsive UI with previews, copy buttons, and loading indicators.
- Model selection dropdown to choose between different AI models.
- Model-agnostic backend with lazy loading for memory efficiency.

## Features

- Fast, offline-ready backend with multiple Hugging Face models.
- Frontend built with Vue 3, TypeScript, and TailwindCSS v4.
- Supports multiple image uploads with progress indicators.
- Model selection between BLIP, ViT-GPT2, and GIT models.
- Copy generated alt text to clipboard.
- Lazy model loading to save memory (models load on first use).

## Requirements

- Python 3.10+
- Node.js 18+ / npm 9+
- Optional: GPU for faster image processing

## Backend Setup

1. Navigate to backend folder:
    ```bash
    cd backend
    ```

2. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the backend server:
    ```bash
    # Option 1: Using run.py from backend directory
    python run.py

    # Option 2: Using run.py from project root
    python backend/run.py

    # Option 3: Directly with uvicorn from backend/src
    cd src && uvicorn main:app --reload
    ```

4. Verify backend is running:
   - Open http://localhost:8000/docs in your browser to access FastAPI interactive docs.

## Frontend Setup

1. Navigate to frontend folder:
    ```bash
    cd frontend
    ```

2. Install Node dependencies:
    ```bash
    npm install
    ```

3. Run the frontend server:
    ```bash
    npm run dev
    ```

4. Open the app:
   - By default, Vite will serve at http://localhost:5173.

## Using the App

1. Open the frontend in your browser.
2. Select an AI model from the dropdown (BLIP is recommended).
3. Drag & drop images into the upload area _or_ click to select files.
4. Wait a few seconds while the backend processes each image.
5. See suggested alt text under each image.
6. Click "Copy" to copy the alt text to your clipboard.

## Available Models

- **BLIP** (Recommended): Salesforce's base model, ~1.8GB, reliable and balanced
- **ViT-GPT2**: Lightweight and fast, ~600MB, good for quick processing
- **GIT**: Microsoft's Generative Image-to-text, ~700MB, alternative approach

## Tips

- The first run of each model downloads weights (600MB–1.8GB depending on model).
- Model weights are cached in `~/.cache/huggingface/hub/` for future use.
- Models are lazy-loaded to save memory - only loaded when first used.
- For faster processing, use a machine with a GPU.
- To add new models, implement the `BaseCaptionModel` interface in `backend/src/models/`.

## Project Structure
    ```text
    project-root/
    ├─ backend/                 # Backend (Python + FastAPI)
    │   ├─ src/                 # Backend source code
    │   │   ├─ main.py          # FastAPI app with model registry
    │   │   └─ models/          # Model implementations
    │   │       ├─ base_model.py # Abstract base class for models
    │   │       ├─ blip_model.py # BLIP implementation
    │   │       ├─ vit_gpt2_model.py # ViT-GPT2 implementation
    │   │       └─ git_model.py  # GIT implementation
    │   └─ run.py               # Launcher script for backend
    ├─ frontend/                # Frontend (Vue 3 + Tailwind)
    │   ├─ public/              # Static files
    │   ├─ src/                 # Vue 3 app source code
    │   │   ├─ components/      # Vue components
    │   │   │   ├─ FileInput.vue # Image upload component
    │   │   │   ├─ ImgCard.vue  # Image preview card
    │   │   │   └─ ModelSelector.vue # Model selection dropdown
    │   │   └─ App.vue          # Main app component
    │   └ ...                   # Other frontend config files
    ├─ .gitignore               # Git ignore file
    └─ README.md                # Well, huhhh, the current file
    ```

## Future Improvements

- Multiple alt text suggestions per image.
- Animated drag & drop feedback.
- Add more models (CLIP, CoCa, etc.).
- Batch processing optimization.
- Fine-tuning support for domain-specific alt text.