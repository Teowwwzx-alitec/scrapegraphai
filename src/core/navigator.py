import asyncio
from playwright.async_api import async_playwright
from src.config import Config


async def run_authenticated_navigator(module_name: str, playwright_cookies: list):
    # Start the Playwright instance explicitly.
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=False)
    # Create a new browser context with the base URL and add cookies.
    context = await browser.new_context(base_url=Config.ODOO_LOCAL_URL)
    await context.add_cookies(playwright_cookies)
    page = await context.new_page()
    # Navigate to the dashboard to verify authentication.
    await page.goto(f"{Config.ODOO_LOCAL_URL}/web", wait_until="networkidle")
    await page.wait_for_timeout(1000)
    print("Dashboard loaded, verifying login status...")
    try:
        await page.wait_for_selector(".o_main_navbar", timeout=5000)
        print("Login successful in Playwright!")
    except Exception as e:
        print("Could not verify login in Playwright:", e)
    # Navigate to the module page.
    print(f"Navigating to {module_name} module...")
    try:
        await page.click('.o_navbar_apps_menu')
        await page.wait_for_timeout(100)
        await page.click(f'.dropdown-item.o_app:has-text("{module_name}")')
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)
        print(f"{module_name} module page loaded.")
    except Exception as e:
        print("Error navigating to module page:", e)

    # --- Inject IntroJS for a guided tour demo ---
    print("Injecting IntroJS for a guided tour demo...")
    try:
        # Inject IntroJS CSS from CDN.
        await page.add_style_tag(url="https://cdnjs.cloudflare.com/ajax/libs/intro.js/4.2.2/introjs.min.css")
        # Inject IntroJS script from CDN.
        await page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/intro.js/4.2.2/intro.min.js")
        # Wait a moment for the scripts to load.
        await page.wait_for_timeout(1000)
        # Start an IntroJS guided tour.
        await page.evaluate("""() => {
            if (typeof introJs === 'function') {
                introJs().setOptions({
                    steps: [
                        { intro: "Welcome to the Odoo Inventory page!" },
                        { element: document.querySelector('.o_main_navbar'), intro: "This is the main navigation bar." },
                        { element: document.querySelector('.o_app'), intro: "These are your application modules." }
                    ]
                }).start();
            }
        }""")
        print("IntroJS tour started. Please interact with the tour in the browser.")
    except Exception as e:
        print("Error injecting IntroJS:", e)
        
    # Return page, context, browser, and the Playwright instance so they can be closed later.
    return page, context, browser, p
