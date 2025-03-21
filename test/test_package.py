# src/dependency_test.py

import importlib
import importlib.metadata

# List of tuples: (module_name to import, package name for version lookup)
dependencies = [
    ("dotenv", "python-dotenv"),
    ("playwright", "playwright"),
    ("openai", "openai"),
    ("scrapegraphai", "scrapegraphai"),
    ("openrouter", "openrouter"),
    ("aiohttp", "aiohttp"),
    ("yaml", "PyYAML"),
    ("pytest", "pytest"),
    ("pytest_asyncio", "pytest-asyncio"),
]

print("Dependency Test Report:\n" + "="*30)
for module_name, package_name in dependencies:
    try:
        # Attempt to import the module
        module = importlib.import_module(module_name)
        try:
            # Try to get version using the package name
            version = importlib.metadata.version(package_name)
        except Exception:
            version = "unknown"
        print(f"Module '{module_name}' (package: '{package_name}') is installed, version: {version}")
    except ModuleNotFoundError:
        print(f"Module '{module_name}' (package: '{package_name}') is NOT installed!")
print("="*30)
