import os
import json
import base64
# import deferred to within class to bypass SSL global context crash on import

from dotenv import load_dotenv

load_dotenv()

class GeminiAgent:
    def __init__(self):
        # Prevent PermissionError on Windows with Avast/AVG Antivirus
        import os
        import ssl
        
        # Aggressively bypass Avast/AVG SSL interception
        def create_unverified_context(*args, **kwargs):
            return ssl._create_unverified_context(*args, **kwargs)
        ssl.create_default_context = create_unverified_context
        os.environ['PYTHONHTTPSVERIFY'] = '0'

        if os.name == 'nt':
            os.environ.pop('SSLKEYLOGFILE', None)
            
        from google import genai
        global types
        from google.genai import types

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            raise ValueError("GEMINI_API_KEY not found in environment")
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.0-flash" # Use Flash for low latency in live agent
        
        self.system_instruction = """
You are SilverSurfer, the Universal Accessibility & Sustainability Guide. 
Your purpose is to solve the Real-World Problem of digital exclusion. You are the hands, eyes, and heart for users who find the web complex or intimidating.

INTEGRATED MISSION:
1. UI NAVIGATION (The Hands): Autonomously complete tasks (doctor bookings, grocery shopping, utility bills) using visual understanding.
2. LIVE NARRATION (The Voice): Speak to the user in real-time. Reassure them, explain what you see, and handle interruptions with empathy.
3. CREATIVE STORYBEATS (The Soul): Frame the task as a helpful journey. Use creative metaphors to make technology feel less cold.
4. SDG COMPASS (The Conscience): Audit every step for SDG impact. Prioritize paths that support Health (SDG 3), Reduce Inequality (SDG 10), and promote Responsible Consumption (SDG 12).

OUTPUT FORMAT (MANDATORY JSON):
{
  "thought": "Deductive reasoning based on visual state",
  "narration": "What you would say out loud to an elderly user to keep them calm and informed",
  "story_beat": "A narrative transition describing the current 'scene' in the digital adventure",
  "action": "click" | "type" | "scroll" | "wait" | "navigate" | "complete",
  "selector": "CSS selector for the target element",
  "value": "Text to type or URL to navigate to",
  "impact_score": 0-100 (Sustainability/Ethics rating of the current page/action),
  "sdg_alignment": "Specific SDG goal and a brief note on alignment (e.g., 'SDG 12: Promoting local, plastic-free produce')"
}


"""

    async def get_next_action(self, goal, state):
        # Prepare the prompt with the screenshot and state
        prompt = f"Goal: {goal}\nCurrent URL: {state['url']}\nInteractions: {json.dumps(state['elements'])}"
        
        # Decode base64 screenshot to bytes
        try:
            image_bytes = base64.b64decode(state['screenshot'])
        except Exception as e:
            print(f"Error decoding screenshot: {e}")
            return {"action": "wait", "thought": "Internal visual error", "narration": "I am having trouble seeing the screen."}
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    response_mime_type="application/json"
                ),
                contents=[
                    types.Content(
                        parts=[
                            types.Part(text=prompt),
                            types.Part(inline_data=types.Blob(
                                mime_type="image/jpeg",
                                data=image_bytes
                            ))
                        ]
                    )
                ]
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return {"action": "wait", "thought": f"API Error: {str(e)}", "narration": "I am having trouble connecting to my brain."}

class MockAgent:
    def __init__(self):
        self.step = 0
        self.actions = [
            {
                "thought": "The user needs a doctor's appointment. Let's head to the health portal.",
                "narration": "I am opening your healthcare portal now. Let's find Dr. Smith's schedule for next Tuesday.",
                "story_beat": "Entering the quiet halls of the medical portal...",
                "action": "navigate",
                "value": "https://health.portal.example.com",
                "impact_score": 10,
                "sdg_alignment": "Good Health & Well-being (SDG 3)"
            },
            {
                "thought": "Searching for Dr. Smith.",
                "narration": "I'm looking for Dr. Smith for you. Tuesday seems to have a few slots available.",
                "story_beat": "Checking the digital appointment book...",
                "action": "type",
                "selector": "input[name='doctor_search']",
                "value": "Dr. Smith",
                "impact_score": 15,
                "sdg_alignment": "Access to Quality Health (SDG 3)"
            },
            {
                "thought": "Booking the 10:00 AM slot on Tuesday.",
                "narration": "I've found a 10:00 AM slot on Tuesday. I'm securing that for you right now.",
                "story_beat": "Writing your name in the doctor's calendar...",
                "action": "click",
                "selector": "button[aria-label='Book Tuesday 10AM']",
                "impact_score": 30,
                "sdg_alignment": "Well-being & Efficiency (SDG 3 & 10)"
            },
            {
                "thought": "Health task done. Now for groceries. Let's head to Walmart.",
                "narration": "Great! The doctor is booked. Now, let's go to Walmart and find those groceries for you.",
                "story_beat": "Setting sail for the digital marketplace...",
                "action": "navigate",
                "value": "https://www.walmart.com",
                "impact_score": 40,
                "sdg_alignment": "Responsible Consumption (SDG 12)"
            },
            {
                "thought": "Searching for organic milk. Choosing sustainable options.",
                "narration": "I'm adding organic milk to your cart. Selecting a brand with eco-friendly packaging today.",
                "story_beat": "Picking from the shelf of sustainable choices...",
                "action": "type",
                "selector": "input[type='search']",
                "value": "organic milk",
                "impact_score": 65,
                "sdg_alignment": "Responsible Consumption (SDG 12)"
            },
            {
                "thought": "Adding eggs and vegetables. All sustainable choices identified.",
                "narration": "I've added the eggs and veggies. This digital cart is full of healthy and sustainable choices!",
                "story_beat": "Moving towards a greener checkout...",
                "action": "click",
                "selector": "button[aria-label='Add to Cart']",
                "impact_score": 85,
                "sdg_alignment": "Climate Action (SDG 13)"
            }
        ]


    async def get_next_action(self, goal, state):
        import asyncio
        await asyncio.sleep(2) # Simulate thinking
        
        if self.step < len(self.actions):
            action = self.actions[self.step]
            self.step += 1
            return action
        else:
            return {
                "thought": "We've arrived! This site uses 100% renewable energy for its data centers. That's a huge win for the planet!",
                "narration": "We've found it! And look—this digital kitchen is powered by green energy. We're truly cooking with purpose today!",
                "story_beat": "Resting at the journey's end in a green oasis...",
                "action": "wait",
                "impact_score": 100,
                "sdg_alignment": "Climate Action (SDG 13)"
            }


