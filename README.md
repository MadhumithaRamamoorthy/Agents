ilverSurfer is an empathetic AI accessibility agent that navigates the web on behalf of elderly and non-technical users using only their voice.
A user speaks naturally — "Book a doctor appointment with Dr. Smith for next Tuesday and order milk from Walmart" — and SilverSurfer's agent persona Sylvia autonomously opens browsers, fills forms, selects calendar dates, clicks buttons, and confirms orders across multiple websites, narrating every action aloud in a warm, patient voice. The user never types, scrolls, or clicks once.
The core problem it solves: 54 million seniors in the US struggle with modern web UIs daily — tiny buttons, multi-step flows, inconsistent designs. SilverSurfer removes that barrier entirely by translating natural language intent into precise, multi-step GUI navigation using Gemini's visual understanding.
How it works technically:

Gemini Live API captures real-time interruptible voice input and transcribes it instantly
Google ADK orchestrates three coordinated agents — an Orchestrator that parses intent and builds a task queue, a Navigator sub-agent that controls a headless Playwright browser per task, and a Verifier sub-agent that visually confirms task completion
Gemini 2.0 Flash receives a screenshot of the current browser state and returns a precise action as structured JSON — click, type, scroll, navigate, or done — along with a human-friendly narration string
Playwright executes each action in a headless Chromium browser with a DOM-fallback layer for reliability
Google Cloud Text-to-Speech (Neural2 voice, 0.88x speed) reads Sylvia's narrations aloud — warm, slow, and never technical
The entire backend runs on Google Cloud Run, with secrets in Secret Manager, logs in Cloud Logging, user preferences in Firestore, and deployment automated via cloudbuild.yaml

Key design decisions driven by real user testing:
The word "Error" was removed from all narration — replaced with "Hmm, let me try a different way." A confirmation step was added before every financial transaction after a test user asked "How do I know it's not buying the wrong thing?" These weren't UX polish — they were trust-critical engineering decisions discovered only by testing with actual elderly users aged 68–79.
What makes it stand out in the UI Navigator track: SilverSurfer doesn't rely on DOM access or pre-built APIs for the target websites — Gemini Vision reads the screen exactly as a human would, making it work on any website without integration. It combines real-time voice, live visual understanding, autonomous multi-step execution, and empathetic narration into a single seamless experience that genuinely changes what the web means for millions of people.
