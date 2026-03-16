import asyncio
import base64
from playwright.async_api import async_playwright

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False) # Headless=False for demo visibility
        self.context = await self.browser.new_context(viewport={'width': 1280, 'height': 720})
        self.page = await self.context.new_page()

    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def navigate(self, url: str):
        await self.page.goto(url, wait_until="networkidle")

    async def get_state(self):
        if not self.page or self.page.is_closed():
            return None
            
        # Capture screenshot for Gemini
        try:
            screenshot_bytes = await self.page.screenshot(type='jpeg', quality=80)
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return None
        
        # Capture a simplified DOM tree (accessibility tree would be better, but let's start simple)
        # We'll just extract interactable elements to save context tokens
        dom_snapshot = await self.page.evaluate('''() => {
            const elements = document.querySelectorAll('button, a, input, [role="button"], select, textarea');
            return Array.from(elements).map((el, index) => {
                const rect = el.getBoundingClientRect();
                return {
                    id: index,
                    tag: el.tagName,
                    text: el.innerText || el.placeholder || el.value || "",
                    attributes: {
                        name: el.getAttribute('name'),
                        id: el.getAttribute('id'),
                        aria_label: el.getAttribute('aria-label')
                    },
                    box: { x: rect.x, y: rect.y, width: rect.width, height: rect.height }
                };
            }).filter(el => el.box.width > 0 && el.box.height > 0);
        }''')
        
        return {
            "url": self.page.url,
            "title": await self.page.title(),
            "screenshot": screenshot_b64,
            "elements": dom_snapshot
        }

    async def execute_action(self, action: str, selector: str = None, value: str = None):
        try:
            if action == "click":
                # Using a more robust selector strategy or clicking by coordinates if selector is tricky
                await self.page.click(selector, timeout=5000)
            elif action == "type":
                await self.page.fill(selector, value, timeout=5000)
                await self.page.keyboard.press("Enter")
            elif action == "scroll":
                await self.page.mouse.wheel(0, 500)
            elif action == "wait":
                await asyncio.sleep(2)
            
            await self.page.wait_for_load_state("networkidle", timeout=5000)
            return True, "Action executed successfully"
        except Exception as e:
            return False, str(e)
