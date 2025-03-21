import asyncio
import json
import os
import aiofiles  # For asynchronous file operations
from playwright.async_api import async_playwright
from aioconsole import ainput  # Async input replacement
from src.config import Config
from scrapegraphai.graphs import SmartScraperGraph  # For AI analysis


# Basic scraper that extracts title and HTML content from a page
class BasicModuleScraper:
    def __init__(self, page, module_name: str):
        self.page = page  # Playwright page instance
        self.module_name = module_name  # Name of the Odoo module
        self.data = {}

    async def extract_content(self):
        """
        Extracts the page title and raw HTML content.
        """
        await self.page.wait_for_load_state("networkidle")
        title = await self.page.title()
        html = await self.page.content()
        self.data = {
            "url": self.page.url,
            "title": title,
            "html": html[:5000] + "..."  # Store partial HTML for analysis
        }
        return self.data

    async def save_data(self, output_dir: str, page_num: int):
        """
        Saves the extracted content as a JSON file in the specified output directory.
        """
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"page_{page_num}.json")
        async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(self.data, indent=2, ensure_ascii=False))
        print(f"Saved page structure to {file_path}")

async def scrapegraphai_analysis(prompt, source, config):
    """
    Runs AI analysis using SmartScraperGraph and returns the result.
    """
    print("Running ScrapeGraphAI analysis...")
    try:
        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=source,
            config=config
        )
        # Run the AI analysis in a separate thread to avoid blocking the event loop.
        result = await asyncio.to_thread(smart_scraper_graph.run)
        print("AI analysis completed.", result)
        return result
    except (json.JSONDecodeError, Exception) as e:
        print(f"AI analysis error: {e}")
        return []   



# Asynchronously load menu selectors data from a JSON file.
async def load_menu_selectors(module_name):
    file_path = os.path.join("odoo", "odoo17", module_name, "list_of_menu_selectors.json")
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"available": [], "done": []}  # Default empty structure

# Asynchronously save menu selectors data to a JSON file.
async def save_menu_selectors(module_name, data):
    file_path = os.path.join("odoo", "odoo17", module_name, "list_of_menu_selectors.json")
    async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, indent=2))

# Function to automate module page traversal
async def travel_module(module_name: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        # First, navigate to the login page and perform login.
        await page.goto(f"{Config.ODOO_LOCAL_URL}/web/login", wait_until="networkidle")
        await page.wait_for_timeout(100)
        await page.click("input[name='login']")
        await page.wait_for_timeout(100)
        await page.type("input[name='login']", Config.ODOO_USERNAME, delay=50)
        await page.wait_for_timeout(100)
        await page.click("input[name='password']")
        await page.type("input[name='password']", Config.ODOO_PASSWORD, delay=50)
        await page.wait_for_timeout(100)
        await page.click("button[type='submit']")
        # Wait for confirmation of successful login.
        await page.wait_for_selector(".o_main_navbar", timeout=1000)
        await page.wait_for_timeout(100)
        print("Login successful!")

        await page.click('.o_navbar_apps_menu')
        await page.wait_for_timeout(100)

        print(f"Navigating to {module_name} module...")
        await page.click(f'.dropdown-item.o_app:has-text("{module_name}")')
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)

        # After module navigation (before AI analysis)
        current_html = await page.content()
        await page.wait_for_timeout(1000)

        # Prepare base output directory for saving page data.
        base_output_dir = os.path.join("odoo", "odoo17", module_name)
        os.makedirs(base_output_dir, exist_ok=True)
        menu_data = await load_menu_selectors(module_name)

        page_counter = 1
        
        while True:
            print(f"\n--- Processing {module_name} Page of {page_counter} ---")
            
            if not menu_data["available"]:
                print("No available menu selectors found. Running AI analysis to extract them...")
                prompt_nav = (
                    "Analyze the following HTML content from an Odoo module page. "
                    "Your task is to provide a brief summary of the page and extract actionable items like menu options or buttons using CSS selectors. "
                    "Your response MUST be valid JSON. The JSON output should be an array of objects, "
                    "where each object has the following keys: 'brief', 'name', 'selector', and 'description'.\n\n"
                    "Expected JSON format:\n"
                    "[\n"
                    "  {{\n"
                    "    \"brief\": \"This is the main inventory page.\",\n"
                    "    \"name\": \"Overview\",\n"
                    "    \"selector\": \"a.o_menu_entry_lvl_1:has-text('Transfers')\",\n"
                    "    \"description\": \"Manage stock transfers\"\n"
                    "  }}\n"
                    "]\n\n"
                )
                nav_graph_config = {
                    "llm": {
                        "api_key": Config.OPENAI_API_KEY,
                        "model": "gpt-3.5-turbo",  # Use latest model with JSON mode
                        "temperature": 0.3,
                        "response_format": {"type": "json_object"}  # Force JSON output
                    },
                    "verbose": True  # Enable debug logs
                }

                print("Running AI analysis for available menu selectors...")
                nav_result = await scrapegraphai_analysis(prompt_nav, current_html, nav_graph_config)

                print("\nRaw AI Response from ScrapeGraphAI:")
                print(nav_result)

                try:
                    available_selectors = json.loads(nav_result) if isinstance(nav_result, str) else nav_result
                except Exception as e:
                    print("Error parsing AI analysis result:", e)
                    available_selectors = []

                print("\nParsed AI Extracted Selectors:")
                print(available_selectors)
                if isinstance(available_selectors, list) and available_selectors:
                    extracted_selectors = [item.get("selector") for item in available_selectors if item.get("selector")]
                    menu_data["available"].extend(extracted_selectors)
                    print(f"Extracted available menu selectors: {extracted_selectors}")

                    user_decision = await ainput("Do you want to save the data? (yes/no): ")
                    user_decision = user_decision.strip().lower()
                    if user_decision == "yes":
                        try:
                            await save_menu_selectors(module_name, menu_data)
                        except Exception as e:
                            print(e)
                    else:
                        break
            
            print("\nAvailable Menu Selectors:", menu_data["available"])
            print("Done Menu Selectors:", menu_data["done"])
            # Prompt for navigation input: if empty, just scrape current page.
            user_input = await ainput("Press Enter an available menu selectors (or 'exit' to stop): ")
            user_input = user_input.strip().lower()
            
            if user_input == "exit":
                print("Exiting traversal.")
                break

            else:
                next_selector = user_input
                try:
                    async with page.expect_navigation(timeout=5000):  # Wait for navigation to complete
                        await page.click(next_selector)
                    await page.wait_for_load_state("networkidle")
                    await page.wait_for_timeout(2000)
                    page_counter += 1
                except Exception as e:
                    print(f"Error navigating with selector '{next_selector}': {str(e)}")
            
            # In either case, scrape the current page.
            scraper = BasicModuleScraper(page, module_name)
            await scraper.extract_content()
            await scraper.save_data(base_output_dir, page_counter)
            
            # Run AI analysis on the current page to extract interactive elements and navigation structure.
            current_url = page.url
            prompt = (
                "Extract key interactive elements and navigation structure for this page in the Inventory module. "
                "Return a JSON array with each step containing 'selector', 'action' (click/type), and 'description'."
            )
            graph_config = {
                "llm": {
                    "api_key": Config.OPENAI_API_KEY,
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.3
                },
                "verbose": False
            }
            smart_scraper_graph = SmartScraperGraph(
                prompt=prompt,
                source=current_url,
                config=graph_config
            )
            print("Running ScrapeGraphAI analysis for interactive elements...")
            result = await asyncio.to_thread(smart_scraper_graph.run)
            
            # Save AI-extracted interactive elements data.
            data = {"url": current_url, "ai_steps": result}
            output_file = os.path.join(base_output_dir, f"page_{page_counter}_ai.json")
            async with aiofiles.open(output_file, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, indent=2))
            print(f"Saved AI-based page structure to {output_file}")
            
            # Update menu tracking if a selector was used for navigation.
            if user_input != "":
                menu_data["done"].append(user_input)
                if user_input in menu_data["available"]:
                    menu_data["available"].remove(user_input)
                await save_menu_selectors(module_name, menu_data)
        
        await context.close()
        await browser.close()

if __name__ == "__main__":
    modules = ["Inventory", "stock", "purchase", "sale", "account", "hr", "crm"]
    
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
    
    asyncio.run(travel_module(module_name))