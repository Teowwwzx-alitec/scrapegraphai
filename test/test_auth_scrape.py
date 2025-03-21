import sys
import asyncio
from playwright.async_api import async_playwright
from lxml import html
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse
from src.config import Config


class OdooSession:
    def __init__(self):
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def get_csrf_token(self):
            try:
                response = self.session.get(
                    f"{Config.ODOO_LOCAL_URL}/web/login",
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                response.raise_for_status()
                
                tree = html.fromstring(response.content)
                
                csrf_element = tree.xpath('//input[@name="csrf_token"]/@value')
                if not csrf_element:
                    # Alternative location for some configurations
                    csrf_element = tree.xpath('//meta[@name="csrf_token"]/@content')
                
                if not csrf_element:
                    print("Login page content:\n", response.text[:2000])  # Debug
                    raise ValueError("CSRF token not found in page")
                    
                return csrf_element[0]
                
            except Exception as e:
                print(f"CSRF extraction failed: {str(e)}")
                raise

    def authenticate(self):
        try:
            csrf_token = self.get_csrf_token()
            print(f"Obtained CSRF: {csrf_token[:15]}...")

            payload = {
                'csrf_token': csrf_token,
                'login': Config.ODOO_USERNAME,
                'password': Config.ODOO_PASSWORD,
                'redirect': '/web'
            }

            response = self.session.post(
                f"{Config.ODOO_LOCAL_URL}/web/login",
                data=payload,
                headers={
                    'User-Agent': 'Mozilla/5.0',
                    'Origin': Config.ODOO_LOCAL_URL,
                    'Referer': f"{Config.ODOO_LOCAL_URL}/web/login",
                    'X-Requested-With': 'XMLHttpRequest'
                },
                allow_redirects=True  # Critical for following post-login flow
            )

            print(f"Auth response: {response.status_code}")
            print(f"Cookies: {self.session.cookies.get_dict()}")
            
            if not self._is_authenticated(response):
                print("Auth check failed. Response content:")
                print(response.text[:2000])  # Show diagnostic output
                raise Exception("Authentication validation failed")

        except Exception as e:
            print(f"Authentication error: {str(e)}")
            raise

    def _is_authenticated(self, response):
            # Multiple verification methods
            auth_success = (
                response.history and 
                any('web/login' not in r.url for r in response.history)
            )

            if 'session_id' in self.session.cookies:
                print("Session cookie present")
                auth_success = True
                
            try:
                tree = html.fromstring(response.content)
                if tree.xpath('//div[@id="oe_main_menu_navbar"]'):
                    print("Found main menu navbar")
                    auth_success = True
            except:
                pass
            
            return auth_success
    
    def get_cookies_for_playwright(self):
        """
        Convert requests cookies to a list of dicts that Playwright accepts.
        Playwright requires fields like: name, value, domain, path.
        """
        cookies = []
        # Extract the hostname from the URL
        parsed_url = urlparse(Config.ODOO_LOCAL_URL)
        hostname = parsed_url.hostname  # e.g., "localhost"
        for cookie in self.session.cookies:
            cookies.append({
                "name": cookie.name,
                "value": cookie.value,
                # Force the domain to match the hostname from the configuration.
                "domain": hostname,
                "path": cookie.path if cookie.path else "/",
                "expires": cookie.expires if cookie.expires else -1,
                "httpOnly": bool(cookie._rest.get("HttpOnly", False)),
                "secure": cookie.secure,
                "sameSite": "Lax"  # Adjust if necessary
            })
        return cookies

    

async def run_authenticated_playwright(module_name: str, playwright_cookies: list, output_file: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        # Create a context with the base URL and add the authenticated cookies.
        context = await browser.new_context(base_url=Config.ODOO_LOCAL_URL)
        await context.add_cookies(playwright_cookies)

        page = await context.new_page()
        # Navigate to the dashboard to verify login.
        await page.goto(f"{Config.ODOO_LOCAL_URL}/web", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        print("Dashboard loaded, verifying login status...")
        try:
            await page.wait_for_selector(".o_main_navbar", timeout=5000)
            print("Login successful in Playwright!")
        except Exception as e:
            print("Could not verify login in Playwright:", e)
        
        # Navigate to the module page (Inventory in this example).
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
        
        # Use XPath to scrape all elements on the page.
        print("Scraping all elements using XPath...")
        elements = await page.locator("xpath=//*").all()
        with open(output_file, 'w', encoding='utf-8') as f:
            for idx, element in enumerate(elements, 1):
                outer_html = await element.evaluate('element => element.outerHTML')
                f.write(f"Element {idx}:\n{outer_html}\n{'='*50}\n")
        print(f"Saved {len(elements)} elements to {output_file}")

        # Keep the browser open for a few seconds to review (optional).
        await asyncio.sleep(5)
        await context.close()
        await browser.close()

async def main():
# First, authenticate via requests.
    odoo = OdooSession()
    try:
        print("Starting authentication with requests...")
        odoo.authenticate()
        print("Requests authentication successful!")
    except Exception as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)

    # Convert requests cookies to a format Playwright can use.
    playwright_cookies = odoo.get_cookies_for_playwright()
    print("Converted cookies for Playwright:", playwright_cookies)

    module_name = "Inventory"
    output_file = "inventory_elements.txt"
    await run_authenticated_playwright(module_name, playwright_cookies, output_file)

if __name__ == "__main__":
    asyncio.run(main())
