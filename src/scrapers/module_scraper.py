# src/scrapers/module_scraper.py

import sys
import os
import asyncio
import json
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from src.config import Config


try:
    from scrapegraphai.api import analyze_html
except ModuleNotFoundError:
    # Fallback: simple intelligent analysis using BeautifulSoup
    from bs4 import BeautifulSoup

    def analyze_html(html):
        soup = BeautifulSoup(html, "html.parser")
        # This dummy function collects all tags with text content.
        elements = {}
        for tag in soup.find_all():
            text = tag.get_text(strip=True)
            if text:
                # Save only the first occurrence per tag type
                if tag.name not in elements:
                    elements[tag.name] = {"tag": tag.name, "text": text}
        return elements
    
class ModuleScraper:
    def __init__(self, url: str = Config.ODOO_LOCAL_URL, 
                 odoo_version: str = "odoo17", 
                 module_name: str = "inventory", 
                 component: str = "base"):
        self.url = url
        self.data = {}
        self.odoo_version = odoo_version
        self.module_name = module_name
        self.component = component

    def get_output_path(self):
        # Create a structured directory: /odoo/{odoo_version}/{module_name}/{component}
        base_dir = os.path.join("odoo", self.odoo_version, self.module_name, self.component)
        os.makedirs(base_dir, exist_ok=True)
        # File name: component.json (e.g., "base.json")
        output_file = os.path.join(base_dir, f"{self.component}.json")
        return output_file

    async def scrape_page(self):
        Config.debug_print(f"Starting browser automation for URL: {self.url}")
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()

                # Navigate to the target URL with timeout from config
                await page.goto(self.url, timeout=Config.PLAYWRIGHT_TIMEOUT)
                Config.debug_print("Page loaded successfully.")

                # Wait for the page to fully load (network idle state)
                await page.wait_for_load_state("networkidle")
                Config.debug_print("Page reached network idle state.")

                # Retrieve the full HTML content of the page
                html_content = await page.content()

                # Use ScrapegraphAI to intelligently analyze the HTML content
                try:
                    recognized_elements = analyze_html(html_content)
                    if recognized_elements:
                        self.data = recognized_elements
                        Config.debug_print("Intelligent element recognition succeeded.")
                    else:
                        Config.debug_print("Intelligent element recognition returned empty result.")
                        self.data = {"error": "No elements recognized."}
                except Exception as e:
                    Config.debug_print(f"Error during intelligent element recognition: {e}")
                    self.data = {"error": str(e)}

                await browser.close()
        except PlaywrightTimeoutError as te:
            Config.debug_print(f"Timeout error while loading the page: {te}")
            self.data = {"error": str(te)}
        except Exception as e:
            Config.debug_print(f"Unexpected error during scraping: {e}")
            self.data = {"error": str(e)}

    def save_data(self):
        output_file = self.get_output_path()
        with open(output_file, "w") as f:
            json.dump(self.data, f, indent=4)
        Config.debug_print(f"Scraped data saved to {output_file}")

    async def run(self):
        await self.scrape_page()
        self.save_data()

if __name__ == "__main__":
    scraper = ModuleScraper()
    asyncio.run(scraper.run())
