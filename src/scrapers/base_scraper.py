import asyncio
from playwright.async_api import async_playwright

async def xpath_scraper(page, output_file: str):
    try:
        print("Scraping all elements using XPath...")
        elements = await page.locator("xpath=//*").all()
        with open(output_file, 'w', encoding='utf-8') as f:
            for idx, element in enumerate(elements, 1):
                outer_html = await element.evaluate('element => element.outerHTML')
                f.write(f"Element {idx}:\n{outer_html}\n{'='*50}\n")
        print(f"Saved {len(elements)} elements to {output_file}")
    except Exception as e:
        print("Error during XPath scraping:", e)
