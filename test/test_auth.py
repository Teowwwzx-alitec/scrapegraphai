import sys
from lxml import html
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry



class OdooSession:
    def __init__(self):
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        # Fix adapter mount for HTTP
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def get_csrf_token(self):
        try:
            response = self.session.get(
                f"{ODOO_URL}/web/login",
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            response.raise_for_status()
            
            tree = html.fromstring(response.content)
            
            # Updated XPath based on Odoo's typical login page structure
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
                'login': CREDENTIALS[0],
                'password': CREDENTIALS[1],
                'redirect': '/web'
            }

            response = self.session.post(
                f"{ODOO_URL}/web/login",
                data=payload,
                headers={
                    'User-Agent': 'Mozilla/5.0',
                    'Origin': ODOO_URL,
                    'Referer': f"{ODOO_URL}/web/login",
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

def main():
    odoo = OdooSession()
    try:
        print("Starting authentication...")
        odoo.authenticate()
        
        print("Testing protected resource...")
        response = odoo.session.get(f"{ODOO_URL}/web")
        print(f"Dashboard status: {response.status_code}")
        
        if response.status_code == 200:
            print("Authentication successful!")
        else:
            print("Final verification failed")

    except Exception as e:
        print(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()