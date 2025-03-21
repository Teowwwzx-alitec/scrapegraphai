import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

USER_DATA_DIR = Path(__file__).parent / "browser_data"
LOGIN_URL = "https://logintest.steps.sg/"
SUCCESS_URL = "https://logintest.steps.sg/web#action=menu&cids=1"
CREDENTIALS = {
    "username": "admin",
    "password": "admin"
}

async def main():
    async with async_playwright() as p:
        # Launch persistent context
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=["--no-sandbox"]
        )
        
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        # Check if already logged in
        if not page.url.startswith(SUCCESS_URL):
            await page.goto(LOGIN_URL)
            
            # Fill login form
            await page.fill('input[name="username"]', CREDENTIALS["username"])
            await page.fill('input[name="password"]', CREDENTIALS["password"])
            await page.click('button[type="submit"]')
            
            # Wait for navigation (login completion)
            try:
                await page.wait_for_url(SUCCESS_URL, timeout=15000)
            except:
                if "blank" in await page.evaluate("document.body.innerText"):
                    await page.goto(SUCCESS_URL)

        # Verify successful login
        await page.wait_for_selector(".oe_application", timeout=20000)
        
        # Explore modules (example)
        print("Exploring modules...")
        menus = await page.query_selector_all(".oe_menu_text")
        for idx, menu in enumerate(menus[:5]):  # First 5 menus
            name = await menu.inner_text()
            print(f"Clicking menu {idx+1}: {name}")
            await menu.click()
            await page.wait_for_timeout(1000)  # Wait for content load
            await page.go_back()

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
