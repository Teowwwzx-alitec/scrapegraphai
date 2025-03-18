import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SCRAPEGRAPHAI_API_KEY = os.getenv('SCRAPEGRAPHAI_API_KEY')
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    MODEL_NAME = "deepseek/deepseek-r1:free"
    
    # Debug mode
    DEBUG = True
    
    # Playwright configs
    PLAYWRIGHT_TIMEOUT = 30000  # 30 seconds
    
    # Configuration constants
    OPENROUTER_API_KEY = "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"

    # Odoo credentials
    ODOO_URL = "http://localhost:8070"
    ODOO_USERNAME = "zhenxiang.teow@alitec.asia"
    ODOO_PASSWORD = "123123123"

    # Common selectors
    ODOO_SELECTORS = {
        'common': {
            'navbar': '.o_main_navbar',
            'app_menu': '.o_navbar_apps_menu',
            'search': '.o_menu_search_input',
            'action_menu': '.o_cp_action_menus',
            'list_view': '.o_list_view',
            'form_view': '.o_form_view',
            'kanban_view': '.o_kanban_view'
        }
    }
    
    @staticmethod
    def debug_print(message):
        if Config.DEBUG:
            print(f"[DEBUG] {message}") 