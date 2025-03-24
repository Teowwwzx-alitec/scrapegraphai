import sys
import os
sys.path.append(os.getcwd())

from src.imports import *


async def batch_scraper():
    """
    Reads URLs from input, authenticates with CSRF token, navigates to each URL,
    and scrapes the page content.
    """
    odoo = OdooSession()
    try:
        print("Starting authentication with requests...")
        await odoo.authenticate()
        print("Requests authentication successful!")
    except Exception as e:
        print(f"Authentication failed: {e}")
        return

    playwright_cookies = odoo.get_cookies_for_playwright()
    print("Converted cookies for Playwright:", playwright_cookies)

    while True:
        url = input("Enter the URL to scrape (or type 'exit' to quit): ")
        if url.lower() == "exit":
            break

        output_file = input("Enter the output file path: ")

        try:
            p = await async_playwright().start()
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(base_url=Config.ODOO_LOCAL_URL)
            await context.add_cookies(playwright_cookies)
            page = await context.new_page()

            await page.goto(url, wait_until="load", timeout=10000)

            await xpath_scraper(page, output_file)

            # Analyze the scraped data
            module_name = "Inventory"  # Replace with the actual module name if needed
            analysis_result = await analyzer(output_file, module_name)
            print(f"Analysis result: {analysis_result}")

            await context.close()
            await browser.close()
            await p.stop()

        except Exception as e:
            print(f"Error during scraping: {e}")


async def batch_analyze_inventory():
    """
    Analyzes all files in odoo/odoo17/inventory that end with '_elements.txt'
    using the analyzer function.
    """
    directory = os.path.join("odoo", "odoo17", "inventory")
    module_name = "inventory"

    # List all files in the directory and filter by '_elements.txt' suffix
    for filename in os.listdir(directory):
        if filename.endswith("_elements.txt"):
            file_path = os.path.join(directory, filename)
            print(f"Analyzing: {file_path}")

            try:
                # Call your existing analyzer function
                analysis_result = await analyzer(file_path, module_name)
                print(f"Analysis result for {filename}:\n{analysis_result}\n")
            except Exception as e:
                print(f"Error analyzing {filename}: {e}")

def convert_md_to_json(md_directory):
    # Iterate through all files in the directory
    for filename in os.listdir(md_directory):
        if filename.endswith("_analyzed.md"):
            md_path = os.path.join(md_directory, filename)
            json_filename = filename.replace("_analyzed.md", "_analyzed.json")
            json_path = os.path.join(md_directory, json_filename)
            
            # Read the markdown file
            with open(md_path, "r", encoding="utf-8") as md_file:
                md_content = md_file.read()
            
            # Create a JSON object; you can add more keys if needed
            data = {
                "filename": filename,
                "analysis": md_content
            }
            
            # Write the JSON object to a file
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=2, ensure_ascii=False)
            
            print(f"Converted {filename} to {json_filename}")



if __name__ == "__main__":
    import asyncio
    # asyncio.run(batch_scraper())
    md_directory = os.path.join("odoo", "odoo17", "inventory")

    convert_md_to_json(md_directory)
