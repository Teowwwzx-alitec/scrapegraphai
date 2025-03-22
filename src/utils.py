from src.imports import *



async def manage_menu_selectors(module_name, action):
    base_dir = join_paths("odoo", "odoo17", module_name)
    if action == 'create':
        os.makedirs(base_dir, exist_ok=True)
        output_file = join_paths(base_dir, f"{module_name}_elements.txt")
        return output_file
    elif action == 'read':
        file_path = join_paths(base_dir, "list_of_menu_selectors.json")
        try:
            content = await read_file(file_path)
            if content:
                return json.loads(content)
            else:
                return {"available": [], "done": []}
        except (FileNotFoundError, json.JSONDecodeError):
            return {"available": [], "done": []}
    else:
        raise ValueError("Invalid action specified")
    
# def create_menu_selectors_dir(module_name):
# menu_selectors_base_dir = os.path.join("odoo", "odoo17", module_name)
# os.makedirs(menu_selectors_base_dir, exist_ok=True)
# output_file = os.path.join(menu_selectors_base_dir, f"{module_name}_elements.txt")
# return output_file


# async def read_menu_selectors_dir(module_name):
#     menu_selectors_base_dir = os.path.join("odoo", "odoo17", module_name, "list_of_menu_selectors.json")
#     try:
#         async with aiofiles.open(menu_selectors_base_dir, "r", encoding="utf-8") as f:
#             content = await f.read()
#             return json.loads(content)
#     except (FileNotFoundError, json.JSONDecodeError):
#         return {"available": [], "done": []}

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


# File operations
async def read_file(file_path: str) -> str:
    """Reads a file and returns its content."""
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            return await f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


async def write_file(file_path: str, content: str) -> None:
    """Writes content to a file."""
    try:
        async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
            await f.write(content)
        print(f"Successfully wrote to {file_path}")
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")


def delete_file(file_path: str) -> None:
    """Deletes a file."""
    try:
        os.remove(file_path)
        print(f"Successfully deleted {file_path}")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")


def check_file_exists(file_path: str) -> bool:
    """Checks if a file exists."""
    return os.path.exists(file_path)


def join_paths(*args: str) -> str:
    """Joins multiple path components into a single path."""
    return os.path.join(*args)
