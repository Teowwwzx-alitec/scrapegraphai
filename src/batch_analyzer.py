import sys
import os
sys.path.append(os.getcwd())

from src.imports import *

async def batch_analyzer():
    """
    Analyzes all files in the /odoo/odoo17/inventory folder using Deepseek R1.
    """
    inventory_dir = "odoo/odoo17/inventory"
    try:
        files = os.listdir(inventory_dir)
        for file in files:
            if file.endswith(".txt"):
                scraped_file = os.path.join(inventory_dir, file)
                module_name = "Inventory"  # Replace with the actual module name if needed
                print(f"Analyzing {scraped_file}...")
                try:
                    analysis_result = await analyzer(scraped_file, module_name)
                    print(f"Analysis result: {analysis_result}")
                except Exception as e:
                    print(f"Error during analysis of {scraped_file}: {e}")
    except FileNotFoundError:
        print(f"Error: Directory not found: {inventory_dir}")
    except Exception as e:
        print(f"Error during batch analysis: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(batch_analyzer())
