# SilverSurfer: Modular Accessibility Agent

SilverSurfer is an AI agent designed to bridge the digital divide for elderly and non-technical users. It uses **Gemini 2.0 Flash Vision** and **Playwright** to navigate complex UIs based on natural language voice commands.

## 📂 Modular Architecture
- **backend/main.py**: FastAPI orchestration server.
- **backend/agent/**: 
  - `orchestrator.py`: Multi-step reasoning (ADK Pattern).
  - `navigator.py`: Vision-to-Action loop for individual sites.
- **backend/browser/controller.py**: Playwright singleton manager.
- **frontend/**: Accessibility-first, high-contrast dashboard.

## 🚀 Getting Started
1. **API Key**: Set your `GEMINI_API_KEY` in `.env`.
2. **Install**: `pip install -r requirements.txt` and `playwright install`.
3. **Run**: `python backend/main.py`.
4. **Access**: Navigate to `http://localhost:8000`.

## ☁️ Google Cloud Deployment
SilverSurfer is Cloud-ready. Use the provided `Dockerfile` and `cloudbuild.yaml` to deploy to **Cloud Run** or **GKE**.
```bash
gcloud builds submit --config cloudbuild.yaml .
```

## 🏆 Hackathon Tracks
- **UI Navigator**: Direct visual interpretation of UI screenshots.
- **Live Agent**: Real-time voice interaction boilerplate included.
