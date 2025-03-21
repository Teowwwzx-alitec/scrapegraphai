import os
import json
import requests
from typing import List

XPATH_OUTPUT_FILE = "inventory_elements.txt"
ANALYSIS_FILE = "odoo_analysis.md"
OPENROUTER_API_KEY = "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"

def read_xpath_elements() -> List[str]:
    """Read and parse XPath output file"""
    with open(XPATH_OUTPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    return [elem.split("Element ")[1].strip() for elem in content.split("="*50) if elem.strip()]

def analyze_with_deepseek(elements: List[str]) -> str:
    """Send elements to DeepSeek R1 via OpenRouter"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
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

def save_analysis(report: str):
    """Save analysis to markdown file"""
    with open(ANALYSIS_FILE, "w", encoding="utf-8") as f:
        f.write("# Odoo Structure Analysis\n\n")
        f.write(report)
    print(f"Analysis saved to {ANALYSIS_FILE}")

if __name__ == "__main__":
    
    elements = read_xpath_elements()
    print(f"Loaded {len(elements)} HTML elements")
    
    analysis = analyze_with_deepseek(elements)
    save_analysis(analysis)
