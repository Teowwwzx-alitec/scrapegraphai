import aiofiles
import json
import requests
from typing import List
from src.config import Config


ANALYSIS_FILE = "odoo_analysis.md"

async def analyzer(scraped_file: str):
    """
    Read the scraped inventory elements file and send its content for analysis
    via OpenRouter + DeepseekR1 (dummy implementation for now).
    """
    async with aiofiles.open(scraped_file, "r", encoding="utf-8") as f:
        data = await f.read()
    
    print("Analyzing scraped inventory elements using OpenRouter + DeepseekR1...")

    # Split the scraped data into individual elements.
    # Assumes each element is separated by a line of "=" characters.
    elements = data.split("=" * 50)
    # Remove empty entries and extra whitespace.
    elements = [elem.strip() for elem in elements if elem.strip()]
    
    # Generate the analysis report.
    report = analyze_with_deepseek(elements)
    
    # Save the analysis report.
    save_analysis(report, data)  # Update the function call to pass both parameters
    
    return report

def analyze_with_deepseek(elements: List[str]) -> str:
    """Send elements to DeepSeek R1 via OpenRouter"""
    headers = {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = """Analyze this Odoo XML/HTML structure and identify:
    1. Core application components (menus, views, templates)
    2. Actionable elements (buttons, links, form inputs)
    3. Business logic indicators (model references, actions)
    4. Inheritance points (xpath expressions)
    5. Security and access control elements

    Format response in Markdown with Odoo-specific technical insights."""

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "\n".join(elements[:2000])}  # Truncate for token limits
        ],
        "temperature": 0.3
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    return response.json()["choices"][0]["message"]["content"]

def save_analysis(report: str, data: str):  # Update the function definition to accept both parameters
    """Save analysis to markdown file"""
    with open(ANALYSIS_FILE, "w", encoding="utf-8") as f:
        f.write("# Odoo Structure Analysis\n\n")
        f.write(report)
    print(f"Analysis saved to {ANALYSIS_FILE}")

    analysis_result = {
        "analysis": "dummy analysis result based on scraped inventory elements",
        "element_count": len(data)
    }
    print("Analysis result:", json.dumps(analysis_result, indent=2))
    return analysis_result
