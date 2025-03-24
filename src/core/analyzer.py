from src.imports import *
import os
import json

async def analyzer(scraped_file: str, module_name: str):
    """
    Read the scraped inventory elements file and send its content for analysis
    via OpenRouter + DeepseekR1 (dummy implementation for now). The analysis report
    is saved as a new file in the same directory.
    """
    # Read the scraped data from file
    data = await read_file(scraped_file)
    
    print("Analyzing scraped inventory elements using OpenRouter + DeepseekR1...")
    
    # Create an output file path in the same directory by replacing the suffix
    base_dir = os.path.dirname(scraped_file)
    base_name = os.path.basename(scraped_file)
    analysis_file = os.path.join(base_dir, base_name.replace('_elements.txt', '_analyzed.md'))
    
    # Split the scraped data into individual elements.
    # Assumes each element is separated by a line of "=" characters.
    elements = data.split("=" * 50)
    # Remove empty entries and extra whitespace.
    elements = [elem.strip() for elem in elements if elem.strip()]
    
    # Generate the analysis report.
    report = await analyze_with_deepseek_and_filter(elements)
    
    # Save the analysis report.
    await save_analysis(report, analysis_file)
    
    return report

async def analyze_with_deepseek_and_filter(elements: List[str]) -> str:
    """Send elements to DeepSeek R1 via OpenRouter and filter the results."""
    headers = {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = (
        "Analyze the following Odoo XML/HTML structure and identify the navigation bar (navbar), its components, the control panel, and the main panel. "
        "Pay close attention to the relationships between menus, submenus, control panel elements, and main panel elements. Your goal is to understand "
        "the overall structure of the page and identify all elements that contribute to navigation, actions, or data display.\n\n"
        "Specifically:\n\n"
        "**General Instructions:**\n\n"
        "1. Identify all elements that appear to be related to navigation, actions, or data display, even if they don't perfectly match the patterns described below.\n"
        "2. For any element that doesn't match a specific pattern, extract the following information:\n"
        "   * Text content (the visible name of the element)\n"
        "   * `class` attribute (the CSS classes of the element)\n"
        "   * Any other relevant attributes (e.g., `data-hotkey`, `href`, `data-id`)\n\n"
        "**Navigation Bar (Navbar):**\n\n"
        "1. Identify the element with class \"o_main_navbar\". This is the main navigation bar.\n"
        "2. Identify the menu items within the navbar. These are typically `<a>` or `<button>` elements with the class \"dropdown-item\" or similar, and are often nested within `<div>` elements with class \"o-dropdown dropdown o-dropdown--no-caret\".\n"
        "3. Identify the submenus within the menus. These are typically nested `<div>` elements with class \"dropdown-menu\" or similar.\n"
        "4. Extract the following information for each menu and submenu:\n"
        "   * Text content (the visible name of the menu item)\n"
        "   * `data-menu-xmlid` attribute (the XML ID of the menu item)\n"
        "   * `href` attribute (the URL associated with the menu item)\n\n"
        "**Control Panel:**\n\n"
        "1. Identify the element with class \"o_control_panel\". This is the main control panel.\n"
        "2. Identify the breadcrumbs within the control panel. These are typically `<div>` elements with class \"o_breadcrumb\".\n"
        "3. Identify the search bar within the control panel. This is typically an `<input>` element with class \"o_searchview_input\".\n"
        "4. Identify the pagination controls within the control panel. These are typically `<button>` elements with class \"o_pager_previous\" or \"o_pager_next\".\n"
        "5. Identify the action buttons within the control panel. These are typically `<button>` elements with class \"btn btn-primary\" or similar.\n"
        "6. Extract the following information for each control panel element:\n"
        "   * Text content (the visible name of the element)\n"
        "   * `class` attribute (the CSS classes of the element)\n"
        "   * `data-hotkey` attribute (the hotkey associated with the element)\n\n"
        "**Main Panel:**\n\n"
        "1. Identify the element that represents the main panel. This is often a `<div>` with a class indicating the view type (e.g., \"o_kanban_renderer\", \"o_list_renderer\", \"o_form_view\").\n"
        "2. Determine the view type based on the class of the main panel element.\n"
        "   * Examples:\n"
        "     * Kanban view: `o_kanban_renderer`\n"
        "     * List view: `o_list_renderer`\n"
        "     * Form view: `o_form_view`\n"
        "3. Identify the individual records or items within the view. These are typically `<div>` elements with class \"o_kanban_record\", \"o_list_record\", or similar.\n"
        "4. Extract the following information for each main panel element:\n"
        "   * View type (Kanban, List, Form, etc.)\n"
        "   * For each record:\n"
        "       * Text content of key fields\n"
        "       * `data-id` attribute (the ID of the record)\n"
        "       * Actionable elements (buttons, links) and their attributes\n\n"
        "**Last**\n\n"
        "Give a brief about it which is your understanding of the page."
    )

    payload = {
        "model": "deepseek/deepseek-r1",
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

    try:
        return response.json()["choices"][0]["message"]["content"]
    except KeyError as e:
        print(f"Error: Could not extract content from OpenRouter response. Response: {response.text}")
        return f"Error: Could not extract content from OpenRouter response. Check the logs for more details. {e}"
    except Exception as e:
        print(f"Error: An unexpected error occurred while processing the OpenRouter response. Response: {response.text}")
        return f"Error: An unexpected error occurred while processing the OpenRouter response. Check the logs for more details. {e}"

async def save_analysis(report: str, analysis_file: str):
    """Save analysis to a markdown file."""
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(analysis_file), exist_ok=True)
    
    with open(analysis_file, "w", encoding="utf-8") as f:
        f.write("# Odoo Structure Analysis\n\n")
        f.write(report)
    print(f"Analysis saved to {analysis_file}")

    analysis_result = {
        "analysis": "dummy analysis result based on scraped inventory elements",
    }
    print("Analysis result:", json.dumps(analysis_result, indent=2))
    return analysis_result
