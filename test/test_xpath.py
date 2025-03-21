import asyncio
from playwright.async_api import async_playwright

async def xpath_scraper(url: str, output_file: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(url, wait_until="networkidle")
            
            # Get all elements using XPath
            elements = await page.locator("xpath=//*").all()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for idx, element in enumerate(elements, 1):
                    outer_html = await element.evaluate('element => element.outerHTML')
                    f.write(f"Element {idx}:\n{outer_html}\n{'='*50}\n")
                    
            print(f"Saved {len(elements)} elements to {output_file}")

        finally:
            await browser.close()

if __name__ == "__main__":
    target_url = "http://localhost:8070/web#action=370&model=stock.picking.type&view_type=kanban&cids=1&menu_id=181"  # Replace with your URL
    asyncio.run(xpath_scraper(target_url, "xpath_elements.txt"))


