from src.imports import *


async def navigate_to_module(module_name: str, playwright_cookies: list):
    # Start the Playwright instance explicitly.
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=False)

    # Create a new browser context with the base URL and add cookies.
    context = await browser.new_context(base_url=Config.ODOO_LOCAL_URL)
    await context.add_cookies(playwright_cookies)
    page = await context.new_page()

    # Navigate to the dashboard to verify authentication.
    await page.goto(f"{Config.ODOO_LOCAL_URL}/web", wait_until="load", timeout=10000)
    await page.wait_for_timeout(100)
    
    # Check if the o_main_navbar exists (Community version)
    navbar_exists = await page.locator('.o_main_navbar').count() > 0
    if navbar_exists:
        await page.wait_for_selector(".o_main_navbar", timeout=1000)
    
    await page.wait_for_timeout(100)

    print(f"Navigating to {module_name} module...")
    try:
        # Check if the o_navbar_apps_menu exists (Community version)
        navbar_exists = await page.locator('.o_navbar_apps_menu').count() > 0
        if navbar_exists:
            await page.click('.o_navbar_apps_menu')
            await page.wait_for_timeout(100)
            await page.click(f'.dropdown-item.o_app:has-text("{module_name}")')
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(100)
            print(f"{module_name} module page loaded.")

            # Enterprise version - construct the URL directly
            # if module_name == "Inventory":
            #     module_url = f"{Config.ODOO_LOCAL_URL}/web#action=305&model=stock.picking.type&view_type=kanban&cids=1&menu_id=167"
            # elif module_name == "Contacts":
            #     module_url = f"{Config.ODOO_LOCAL_URL}/web#action=134&model=res.partner&view_type=kanban&cids=1&menu_id=98"
            # elif module_name == "Discuss":
            #     module_url = f"{Config.ODOO_LOCAL_URL}/web#action=107&cids=1&menu_id=70"
            # else:
            #     print(f"Module {module_name} not supported yet")
            #     return page, context, browser, p
            # await page.goto(module_url, wait_until="load", timeout=10000)
            # print(f"Navigated to {module_name} using direct URL (Enterprise version).")

            if module_name == "Inventory":
                await page.wait_for_selector('//div[@class="o_caption" and contains(text(), "Inventory")]', timeout=1000)
            elif module_name == "Contacts":
                await page.wait_for_selector('//div[@class="o_caption" and contains(text(), "Contacts")]', timeout=1000)
            elif module_name == "Discuss":
                await page.wait_for_selector('//div[@class="o_caption" and contains(text(), "Discuss")]', timeout=1000)
            else:
                print(f"Module {module_name} not found")
                return page, context, browser, p

            await page.goto(module_name, wait_until="load", timeout=10000)
            print(f"Navigated to {module_name} using direct URL (Enterprise version).")

    except Exception as e:
        print(f"Error navigating to module {module_name}: {e}")
        return None
        
    # Return page, context, browser, and the Playwright instance so they can be closed later.
    return page, context, browser, p

    # # --- Inject IntroJS for a guided tour demo ---
    # print("Injecting IntroJS for a guided tour demo...")
    # try:
    #     # Inject IntroJS CSS from CDN.
    #     await page.add_style_tag(url="https://cdnjs.cloudflare.com/ajax/libs/intro.js/4.2.2/introjs.min.css")
    #     # Inject IntroJS script from CDN.
    #     await page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/intro.js/4.2.2/intro.min.js")
    #     # Wait a moment for the scripts to load.
    #     await page.wait_for_timeout(1000)
    #     # Start an IntroJS guided tour.
    #     await page.evaluate("""() => {
    #         if (typeof introJs === 'function') {
    #             introJs().setOptions({
    #                 steps: [
    #                     { intro: "Welcome to the Odoo Inventory page!" },
    #                     { element: document.querySelector('.o_main_navbar'), intro: "This is the main navigation bar." },
    #                     { element: document.querySelector('.o_app'), intro: "These are your application modules." }
    #                 ]
    #             }).start();
    #         }
    #     }""")
    #     print("IntroJS tour started. Please interact with the tour in the browser.")
    # except Exception as e:
    #     print("Error injecting IntroJS:", e)
