from scrapegraphai.graphs import SmartScraperGraph
from src.config import Config  # Import your OPENAI_API_KEY from config

graph_config = {
    "llm": {
        # Use your $10 credit with the more cost-effective GPT-3.5-Turbo
        "api_key": Config.OPENAI_API_KEY,
        "model": "gpt-3.5-turbo"
    }
}

# Instantiate SmartScraperGraph
smart_scraper_graph = SmartScraperGraph(
    prompt="Analyze the following HTML content from an Odoo page. Your task is to provide a brief summary of the page and extract actionable items like menu options or buttons using CSS selectors.",
    source="https://www.odoo.com/app/inventory",
    config=graph_config
)

# Run and print the result
result = smart_scraper_graph.run()
import json
print(json.dumps(result, indent=4))