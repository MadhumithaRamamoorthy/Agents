# SilverSurfer Architecture

```mermaid
graph TD
    User((User)) -->|Goal Command| API[FastAPI Backend]
    API -->|Instruction| Brain[Gemini Agent Logic]
    Brain -->|Capture State| Browser[Playwright Browser]
    Browser -->|Screenshot + DOM| Brain
    Brain -->|Vision Analysis| Gemini((Gemini 2.0 Flash))
    Gemini -->|Next Action + Narration| Brain
    Brain -->|Execute Action| Browser
    Brain -->|Narrate Story| Voice[VoiceEngine TTS]
    Voice -->|Audio Feedback| User
    Brain -->|Update Status| API
```

### Deployment (Google Cloud):
The SilverSurfer backend is designed for containerized deployment on **Google Cloud GKE** or **Cloud Run**:
1. **Containerization**: Packaged via the provided `Dockerfile`.
2. **Orchestration**: Managed by Cloud Run for auto-scaling based on user requests.
3. **Storage**: Environment variables (API Keys) managed via **Secret Manager**.
4. **Networking**: Served over HTTPS with global load balancing for low-latency voice feedback.

