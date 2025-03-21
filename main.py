import sys
import os
import json
import asyncio
import aiofiles
from src.config import Config
from src.auth.csrf import OdooSession
from src.core.navigator import run_authenticated_navigator
from src.core.analyzer import analyzer
from src.scrapers.base_scraper import xpath_scraper


# Previously working asynchronous loader for menu selectors.
async def load_menu_selectors(module_name):
    file_path = os.path.join("odoo", "odoo17", module_name, "list_of_menu_selectors.json")
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"available": [], "done": []}

async def main():
    module_name = "Inventory"
    # Create the base output directory.
    base_output_dir = os.path.join("odoo", "odoo17", module_name)
    os.makedirs(base_output_dir, exist_ok=True)
    output_file = os.path.join(base_output_dir, "inventory_elements.txt")

    # Authenticate via requests.
    odoo = OdooSession()
    try:
        print("Starting authentication with requests...")
        odoo.authenticate()
        print("Requests authentication successful!")
    except Exception as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)

    # Convert cookies for Playwright.
    playwright_cookies = odoo.get_cookies_for_playwright()
    print("Converted cookies for Playwright:", playwright_cookies)

    # Run navigator to open the authenticated page.
    # Now unpacking four values: page, context, browser, and p (the Playwright instance)
    page, context, browser, p = await run_authenticated_navigator(module_name, playwright_cookies)

    # await run_introjs_test(page)

    # Use XPath scraper to extract HTML elements.
    await xpath_scraper(page, output_file)

    # Analyze the scraped inventory elements using OpenRouter + DeepseekR1.
    await analyzer(output_file)

    # Cleanup: close context, browser, and stop Playwright.
    try:
        await context.close()
    except Exception as e:
        print("Error closing context:", e)
    try:
        await browser.close()
    except Exception as e:
        print("Error closing browser:", e)
    try:
        await p.stop()
    except Exception as e:
        print("Error stopping playwright:", e)


if __name__ == "__main__":
    asyncio.run(main())