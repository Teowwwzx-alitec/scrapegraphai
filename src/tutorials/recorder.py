from playwright.sync_api import Page
from ..core.recognizer import Recognizer
from config import Config

class Recorder:
    def __init__(self, page: Page):
        self.page = page
        self.recognizer = Recognizer(page)
        self.steps = []
        
    async def record_step(self, description: str, action: str):
        """Record a single tutorial step"""
        Config.debug_print(f"Recording step: {description}")
        
        element = await self.recognizer.find_element(description)
        if element:
            step = {
                "element": element,
                "description": description,
                "action": action
            }
            self.steps.append(step)
            return True
        return False
    
    def save_recording(self, output_path: str):
        """Save recorded steps"""
        return {
            "steps": self.steps,
            "total_steps": len(self.steps)
        }