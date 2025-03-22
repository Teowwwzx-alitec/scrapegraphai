from src.imports import *


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
                print("Login page content:\n", response.text[:2000])
                raise ValueError("CSRF token not found in page")
            return csrf_element[0]
        except Exception as e:
            print(f"CSRF extraction failed: {str(e)}")
            raise

    async def authenticate(self):
        try:
            from playwright.async_api import async_playwright
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()

                await page.goto(f"{Config.ODOO_LOCAL_URL}/web/login")

                # Enter username and password
                await page.fill('input[name="login"]', Config.ODOO_USERNAME)
                await page.fill('input[name="password"]', Config.ODOO_PASSWORD)

                # Wait for the button to be visible
                await page.wait_for_selector('button.btn.btn-primary[type="submit"]', state="visible", timeout=5000)

                # Click login button
                await page.click('button.btn.btn-primary[type="submit"]', force=True)

                # Wait for navigation and load state
                # await page.wait_for_load_state("networkidle")

                # Get cookies
                playwright_cookies = await context.cookies()

                # Convert Playwright cookies to requests cookies
                requests_cookies = {}
                for cookie in playwright_cookies:
                    requests_cookies[cookie["name"]] = cookie["value"]
                
                # Update the session cookies
                self.session.cookies.update(requests_cookies)

                await browser.close()

        except Exception as e:
            print(f"Playwright authentication error: {str(e)}")
            raise

    # def authenticate(self):
    #     try:
    #         csrf_token = self.get_csrf_token()
    #         print(f"Obtained CSRF: {csrf_token[:15]}...")
    #         payload = {
    #             'csrf_token': csrf_token,
    #             'login': Config.ODOO_USERNAME,
    #             'password': Config.ODOO_PASSWORD,
    #             'redirect': '/web'
    #         }
    #         response = self.session.post(
    #             f"{Config.ODOO_LOCAL_URL}/web/login",
    #             data=payload,
    #             headers={
    #                 'User-Agent': 'Mozilla/5.0',
    #                 'Origin': Config.ODOO_LOCAL_URL,
    #                 'Referer': f"{Config.ODOO_LOCAL_URL}/web/login",
    #                 'X-Requested-With': 'XMLHttpRequest'
    #             },
    #             allow_redirects=True
    #         )
    #         print(f"Auth response: {response.status_code}")
    #         print(f"Cookies: {self.session.cookies.get_dict()}")
    #         if not self._is_authenticated(response):
    #             print("Auth check failed. Response content:")
    #             print(response.text[:2000])
    #             raise Exception("Authentication validation failed")
    #     except Exception as e:
    #         print(f"Authentication error: {str(e)}")
    #         raise

    def _is_authenticated(self, response):
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
        except Exception:
            pass
        return auth_success

    def get_cookies_for_playwright(self):
        """
        Convert requests cookies to a list of dicts that Playwright accepts.
        """
        cookies = []
        parsed_url = urlparse(Config.ODOO_LOCAL_URL)
        hostname = parsed_url.hostname
        
        # for cookie in self.session.cookies:
        #     cookies.append({
        #         "name": cookie.name,
        #         "value": cookie.value,
        #         "domain": hostname,  # Force domain to match the hostname
        #         "path": cookie.path if cookie.path else "/",
        #         "expires": cookie.expires if cookie.expires else -1,
        #         "httpOnly": bool(cookie._rest.get("HttpOnly", False)),
        #         "secure": cookie.secure,
        #         "sameSite": "Lax"  # Adjust if necessary
        #     })

        for cookie_name, cookie_value in self.session.cookies.items():
            cookie = self.session.cookies.get(cookie_name)
            cookies.append({
                "name": cookie_name,
                "value": cookie_value,
                "domain": hostname,
                "path": cookie.path if hasattr(cookie, 'path') else "/",
                "expires": cookie.expires if hasattr(cookie, 'expires') else -1,
                "httpOnly": cookie.has_nonstandard_attr('HttpOnly') if hasattr(cookie, 'has_nonstandard_attr') else False,
                "secure": cookie.secure if hasattr(cookie, 'secure') else False,
                "sameSite": cookie.get('samesite', 'Lax') if hasattr(cookie, 'get') else 'Lax'
            })
        return cookies
