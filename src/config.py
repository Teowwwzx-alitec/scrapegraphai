from src.imports import *


load_dotenv()

class Config:
    SCRAPEGRAPHAI_API_KEY = os.getenv('SCRAPEGRAPHAI_API_KEY')

    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    MODEL_NAME = "deepseek/deepseek-r1:free"
    
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Debug mode
    DEBUG = True
    
    # Playwright configs
    PLAYWRIGHT_TIMEOUT = 30000
    
    # Odoo credentials
    # ODOO_LOCAL_URL = "http://localhost:8070"
    # ODOO_LOCAL_USERNAME = "zhenxiang.teow@alitec.asia"
    # ODOO_LOCAL_PASSWORD = "123123123"

    ODOO_LOCAL_URL = "https://logintest.steps.sg/"
    ODOO_USERNAME = "admin"
    ODOO_PASSWORD = "admin"
    
    # ODOO_SERVER_URL = "https://logintest.steps.sg/"
    # ODOO_SERVER_USERNAME = "zhenxiang.teow@alitec.asia"
    # ODOO_SERVER_PASSWORD = "123123123"


    @staticmethod
    def debug_print(message):
        if Config.DEBUG:
            print(f"[DEBUG] {message}")
