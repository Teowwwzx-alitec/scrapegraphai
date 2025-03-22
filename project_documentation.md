# ScrapeGraphAI Project Documentation

## Project Overview

ScrapeGraphAI is a Python project that automates the process of scraping and analyzing data from Odoo modules. It uses Playwright for browser automation, XPath for element selection, and OpenRouter + DeepseekR1 for data analysis. The project allows users to select a module from a list, authenticate with Odoo, scrape data from the selected module, analyze the scraped data, and generate a report.

## Module Breakdown

The `src` directory contains the following modules:

*   `auth`: Authentication-related modules, including CSRF protection.
*   `core`: Core logic modules, including the analyzer and navigator.
*   `scrapers`: Web scraping modules.
*   `tutorials`: Modules for generating tutorials and recording user interactions.

## File Descriptions

*   `main.py`: Entry point of the application.
*   `src/config.py`: Configuration settings.
*   `src/imports.py`: Central location for managing dependencies.
*   `src/utils.py`: Utility functions.

## Workflow

The application follows the following workflow:

1.  User selects a module.
2.  Application authenticates with Odoo.
3.  Application navigates to the selected module.
4.  Application scrapes data from the module.
5.  Application analyzes the scraped data.
6.  Application generates a report.

## Dependencies

The project uses the following dependencies:

```
# Core - Browser Automation
playwright
python-dotenv
requests
lxml
aiofiles
python-dotenv==1.0.1
playwright==1.43.0

# AI APIs (direct usage)
openai==1.66.3
scrapegraphai==1.43.0
openrouter==1.0.0

# Utils
aiohttp==3.11.14
PyYAML==6.0.1

# Testing
pytest==8.0.0
pytest-asyncio==0.23.5
```

## Configuration

The project uses the following configuration options, which are defined in `src/config.py`:

*   `SCRAPEGRAPHAI_API_KEY`: API key for ScrapeGraphAI.
*   `OPENROUTER_API_KEY`: API key for OpenRouter.
*   `MODEL_NAME`: Name of the model used for analysis (default: "deepseek/deepseek-r1:free").
*   `OPENAI_API_KEY`: API key for OpenAI.
*   `DEBUG`: Debug mode (default: True).
*   `PLAYWRIGHT_TIMEOUT`: Playwright timeout in milliseconds (default: 30000).
*   `ODOO_LOCAL_URL`: URL of the local Odoo instance (default: "http://localhost:8070").
*   `ODOO_USERNAME`: Username for Odoo authentication (default: "zhenxiang.teow@alitec.asia").
*   `ODOO_PASSWORD`: Password for Odoo authentication.
