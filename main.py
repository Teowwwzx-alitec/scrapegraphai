from playwright.sync_api import sync_playwright
from src.page_recorder import TutorialRecorder
from src.config import Config
import asyncio

async def main():
    Config.debug_print("Starting tutorial recorder...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to Odoo page
        page.goto("https://your-odoo-instance.com")
        
        recorder = TutorialRecorder(page)
        
        # Example recording steps
        await recorder.record_step(
            "Click the login button at the top right", 
            "click"
        )
        await recorder.record_step(
            "Enter your username in the username field", 
            "input"
        )
        
        # Generate tutorial
        tutorial = recorder.generate_tutorial()
        
        # Save tutorial for later use
        # Implementation depends on your needs
        
        browser.close()

if __name__ == "__main__":
    asyncio.run(main())
