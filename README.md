# Agents
OmniChef: Gemini Live Agent Hackathon Project
1. Project Setup & Foundation
 Initialize Next.js project repository
 Setup standard layout, global CSS, and modern UI tokens (dark mode, glassmorphism)
 Install dependencies (@google/genai, lucide-react, standard frontend tools)
2. Gemini GenAI Integration (Live Agent Track)
 Implement Backend service/API routes for Gemini interaction
 Create Vision processing helper (handling base64 images from video feed)
 Create Audio processing helper (handling TTS and STT if necessary, or utilizing the Gemini Multimodal Live API features)
 Set up system prompt engineering for the Culinary Assistant persona
3. Frontend Development (Real-time Vision & Voice)
 Build User Dashboard / Main Interface
 Implement Webcam video capture and frame extraction mechanism
 Implement Audio recording and playback UI (microphone toggle, visualization)
 Build chat/transcription history component
4. Google Cloud Deployment Preparation
 Create Dockerfile and .dockerignore for containerized deployment
 Create Google Cloud configuration (e.g., Cloud Run deployment scripts)
5. Hackathon Deliverables
 Write README.md with setup instructions and submission details
 Generate Architecture Diagram (architecture.md/Mermaid)
 Prepare script/guide for the 4-minute demo video
