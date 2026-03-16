import os
import ssl

# Aggressively bypass Avast/AVG SSL interception which causes "create_default_context" crashes
# Clear the SSLKEYLOGFILE env var which often points to restricted paths in antivirus environments
os.environ.pop('SSLKEYLOGFILE', None)

# In some environments, antivirus software attempts to set keylog_filename, causing PermissionError.
try:
    prop = ssl.SSLContext.keylog_filename
    original_fset = prop.fset
    def safe_fset(self, value):
        try:
            original_fset(self, value)
        except Exception: # Catch PermissionError or any antivirus-induced issues
            pass
    ssl.SSLContext.keylog_filename = property(prop.fget, safe_fset)
except Exception:
    pass

def create_unverified_context(*args, **kwargs):
    return ssl._create_unverified_context(*args, **kwargs)
ssl.create_default_context = create_unverified_context
os.environ['PYTHONHTTPSVERIFY'] = '0'

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import os
import asyncio

from backend.agent.orchestrator import OrchestratorAgent
from backend.agent.navigator import NavigatorAgent, MockNavigator
from backend.browser.controller import BrowserController


app = FastAPI(title="SilverSurfer API")

# Setup static files for frontend
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

orchestrator = OrchestratorAgent()

class GoalRequest(BaseModel):
    goal: str

@app.get("/")
async def read_index():
    return FileResponse("frontend/index.html")

@app.post("/start-task")
async def start_task(request: GoalRequest, background_tasks: BackgroundTasks):
    """
    Starts a new autonomous task based on user voice/text input.
    """
    background_tasks.add_task(orchestrator.run_goal, request.goal)
    return {"status": "started", "message": "SilverSurfer is on the way!"}

@app.get("/screenshot")
async def get_screenshot():
    """
    Returns a live view of the agent's browser.
    """
    browser = await BrowserController.get_instance()
    img_b64 = await browser.take_screenshot()
    return {"image": img_b64}

@app.get("/agent-status")
async def agent_status():
    """
    Returns the latest narration.
    """
    # This is a simplified fetch for the demo
    return {"status": "active", "narration": "SilverSurfer is actively processing your request..."}


if __name__ == "__main__":
    import uvicorn
    # In local testing, ensure we have the API key
    if not os.getenv("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY not set!")
    uvicorn.run(app, host="0.0.0.0", port=8000)
