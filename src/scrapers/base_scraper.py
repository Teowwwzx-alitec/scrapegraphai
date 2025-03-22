from src.imports import *


async def xpath_scraper(page, output_file: str):
    try:
        print("Scraping all elements using XPath...")
        elements = await page.locator("xpath=//*").all()
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        content = ""
        for idx, element in enumerate(elements, 1):
            outer_html = await element.evaluate('element => element.outerHTML')
            content += f"Element {idx}:\n{outer_html}\n{'='*50}\n"
        
        await write_file(output_file, content)
        print(f"Saved {len(elements)} elements to {output_file}")
    except Exception as e:
        raise RuntimeError(f"Error during XPath scraping: {e}") from e
