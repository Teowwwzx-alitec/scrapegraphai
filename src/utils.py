from src.imports import *



def create_menu_selectors_dir(module_name):
    menu_selectors_base_dir = os.path.join("odoo", "odoo17", module_name)
    os.makedirs(menu_selectors_base_dir, exist_ok=True)
    output_file = os.path.join(menu_selectors_base_dir, f"{module_name}_elements.txt")
    return output_file


async def read_menu_selectors_dir(module_name):
    menu_selectors_base_dir = os.path.join("odoo", "odoo17", module_name, "list_of_menu_selectors.json")
    try:
        async with aiofiles.open(menu_selectors_base_dir, "r", encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"available": [], "done": []}

def create_output_dir():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_base_dir = "output"
    dirs = {
        'screenshots': os.path.join(output_base_dir, timestamp, 'screenshots'),
        'structure': os.path.join(output_base_dir, timestamp, 'structure'),
        'recordings': os.path.join(output_base_dir, timestamp, 'recordings')
    }
    for dir_path in dirs.values():
        os.makedirs(dir_path, exist_ok=True)
