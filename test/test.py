import os
import json
import aiohttp
from typing import Optional

# Configuration
SCRAPEGRAPH_API_KEY = "sgai-27cc5191-b523-409b-856a-f34ff0592279"
OPENROUTER_API_KEY = "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"

class ScrapeGraphAI:
    def __init__(self):
        self.base_url = "https://api.scrapegraphai.com/v1/smartscraper"
        self.headers = {
            "SGAI-APIKEY": SCRAPEGRAPH_API_KEY,
            "Content-Type": "application/json"
        }

    async def scrape_website(self, url: str, prompt: str, config: Optional[dict] = None):
        # Local protection workaround - use a public test URL
        test_url = "http://localhost:8070/web#action=362&active_id=1&model=stock.picking&view_type=list&cids=1&menu_id=211" if "localhost" in url else url
        
        payload = {
            "website_url": test_url,
            "user_prompt": prompt,
            "config": {
                "mode": "simple",
                "proxy": False,
                "timeout": 20
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    return await self._handle_response(response)
        except Exception as e:
            raise Exception(f"Connection error: {str(e)}")

    async def _handle_response(self, response):
        try:
            response_data = await response.json()
        except:
            response_data = await response.text()

        if response.status == 200:
            return response_data
        elif response.status == 422:
            error_msg = response_data.get('error', 'Validation failed') if isinstance(response_data, dict) else response_data
            raise Exception(f"Validation Error: {error_msg}")
        else:
            raise Exception(f"API Error {response.status}: {response_data}")

class OpenRouterAI:
    def __init__(self):
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://my-test-app.com",
            "X-Title": "Testing Console",
            "Content-Type": "application/json"
        }

    async def chat_completion(self, prompt: str, model: str = "google/gemma-7b-it"):
        payload = {
            "model": model,
            "messages": [{
                "role": "user", 
                "content": f"Briefly answer this: {prompt} (answer in 2 sentences max)"
            }]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    return await self._handle_response(response)
        except Exception as e:
            raise Exception(f"Connection error: {str(e)}")

    async def _handle_response(self, response):
        try:
            response_data = await response.json()
        except:
            response_data = await response.text()

        if response.status == 200:
            return response_data
        else:
            error_msg = response_data.get('error', {}).get('message', 'Unknown error') if isinstance(response_data, dict) else response_data
            raise Exception(f"API Error {response.status}: {error_msg}")

async def main():
    print("\nStarting tests...")
    
    # Test ScrapegraphAI with Odoo's public page
    scraper = ScrapeGraphAI()
    try:
        print("\nTesting Odoo page scraping...")
        scraped_data = await scraper.scrape_website(
            "http://localhost:8070/web#action=362&active_id=1&model=stock.picking&view_type=list&cids=1&menu_id=211",  # Public Odoo URL
            "List the core HTML elements of an Odoo web page"
        )
        print("Scraping successful. Sample output:")
        print(json.dumps(scraped_data, indent=2)[:300] + "...")
    except Exception as e:
        print(f"Scraping Error: {str(e)}")

    # Test OpenRouter with simple query
    llm = OpenRouterAI()
    try:
        print("\nTesting OpenRouter...")
        chat_response = await llm.chat_completion(
            "List the core HTML elements of an Odoo web page",
            model="meta-llama/llama-3-70b-instruct"
        )
        print("\nOpenRouter Response:")
        print(chat_response['choices'][0]['message']['content'].strip())
    except Exception as e:
        print(f"LLM Error: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
