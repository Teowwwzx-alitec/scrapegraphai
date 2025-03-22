from src.imports import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    modules = ["Inventory", "Stock", "Purchase", "Sale", "Account", "Hr", "Crm"]
    
    print("Available modules:")
    for idx, module in enumerate(modules, start=1):
        print(f"{idx}. {module}")
    
    user_input = input("Enter module number (e.g., 1 for 'Inventory') or type 'exit' to quit: ").strip().lower()

    if user_input == "exit":
        print("Exiting the program.")
        exit(0)
    
    try:
        module_index = int(user_input) - 1
        module_name = modules[module_index].strip()
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid module number.")
        exit(1)


    output_file = await manage_menu_selectors(module_name, "create")

    odoo = OdooSession()
    try:
        print("Starting authentication with requests...")
        await odoo.authenticate()
        print("Requests authentication successful!")
    except Exception as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)


    playwright_cookies = odoo.get_cookies_for_playwright()
    print("Converted cookies for Playwright:", playwright_cookies)

    # Run navigator to open the authenticated page.
    # Now unpacking four values: page, context, browser, and p (the Playwright instance)
    navigator_result = await navigate_to_module(module_name, playwright_cookies)

    if navigator_result is None:
        print("Navigation failed. Skipping scraping and analysis.")
        return

    page, context, browser, p = navigator_result

    # Check if the output file already exists
    if check_file_exists(output_file):
        print(f"Output file {output_file} already exists. Skipping scraping.")
        return
        
        
    # Use XPath scraper to extract HTML elements.
    await xpath_scraper(page, output_file)

    # Analyze the scraped inventory elements using OpenRouter + DeepseekR1.
    await analyzer(output_file, module_name)

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
