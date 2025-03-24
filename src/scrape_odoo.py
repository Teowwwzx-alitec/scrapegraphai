import os
import re
import json
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Base URL and version for the English docs
BASE_URL = "https://www.odoo.com"
DOC_VERSION = "17.0"
START_URL = f"{BASE_URL}/documentation/{DOC_VERSION}/applications.html"

# Folder where category JSON files will be saved
OUTPUT_FOLDER = "odoo_docs_by_category"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# A set to track visited pages (to avoid duplicates)
visited_pages = set()

def sanitize_filename(text):
    """
    Sanitizes a string to be used as a filename.
    """
    filename = re.sub(r'[^a-zA-Z0-9_-]', '_', text.strip())
    return filename.lower() + ".json"

def extract_page_content(page, url):
    """
    Uses Playwright to load the page, then extracts its title and main text content.
    """
    if url in visited_pages:
        return None  # Already scraped

    print(f"Scraping: {url}")
    try:
        page.goto(url, timeout=15000)
        # wait for JavaScript to render the page
        page.wait_for_timeout(1000)
    except Exception as e:
        print(f"Failed to retrieve {url}: {e}")
        return None

    visited_pages.add(url)
    soup = BeautifulSoup(page.content(), "html.parser")
    
    # Get title from <title>
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""
    
    # Try to get main content from a <div id="content">; fallback to entire <body>
    content_div = soup.find("div", id="content")
    if not content_div:
        content_div = soup.find("body")
    content = content_div.get_text(separator="\n", strip=True) if content_div else ""
    
    return {
        "url": url,
        "title": title,
        "content": content,
    }

def parse_toc_ul(ul_element, current_url, current_category=None):
    """
    Recursively parse a <ul> element representing the TOC.
    Returns a list of page info dicts.
    Each dict has:
      - 'category': the header under which the page is grouped
      - 'name': the page name (from link text)
      - 'url': the absolute URL of the page
      - 'path': full hierarchy as a list
    """
    pages = []
    for li in ul_element.find_all("li", recursive=False):
        a_tag = li.find("a", class_="reference internal")
        if not a_tag:
            continue

        link_text = a_tag.get_text(strip=True)
        href = a_tag.get("href", "").strip()

        if href == "#" or not href:
            # This is a header; update current_category to this header.
            new_category = link_text
            nested_ul = li.find("ul")
            if nested_ul:
                pages.extend(parse_toc_ul(nested_ul, current_url, new_category))
        else:
            abs_url = urljoin(current_url, href)
            page_category = current_category if current_category else "uncategorized"
            pages.append({
                "category": page_category,
                "name": link_text,
                "url": abs_url,
                "path": [page_category, link_text] if current_category else [link_text],
            })
            # Process any nested pages under the same category.
            nested_ul = li.find("ul")
            if nested_ul:
                pages.extend(parse_toc_ul(nested_ul, current_url, current_category))
    return pages

def build_category_mapping(page, toc_url):
    try:
        page.goto(toc_url, timeout=15000)
        page.wait_for_timeout(2000)  # wait for JS to render
    except Exception as e:
        print(f"Failed to retrieve TOC page: {toc_url} - {e}")
        return {}

    content = page.content()
    soup = BeautifulSoup(content, "html.parser")
    toc_ul = soup.select_one("nav.o_side_nav ul.current")
    if not toc_ul:
        print("TOC container not found. Check the selector.")
        print(soup.prettify()[:3000])
        return {}

    pages_list = parse_toc_ul(toc_ul, toc_url)
    mapping = {}
    for p in pages_list:
        cat = p["category"]
        mapping.setdefault(cat, []).append(p)
    return mapping

def print_category_summary(page):
    mapping = build_category_mapping(page, START_URL)
    if not mapping:
        print("No categories found.")
        return

    print("Found categories:")
    for cat, pages in mapping.items():
        print(f"  {cat} ({len(pages)} pages)")



def build_category_mapping(page, toc_url):
    try:
        page.goto(toc_url, timeout=15000)
        page.wait_for_timeout(2000)  # increased timeout to 2 seconds
    except Exception as e:
        print(f"Failed to retrieve TOC page: {toc_url} - {e}")
        return {}

    # Debug: print a snippet of the rendered HTML
    content = page.content()
    print("DEBUG: Rendered page content snippet:")
    print(content[:2000])
    
    soup = BeautifulSoup(content, "html.parser")
    # Updated selector: find the TOC in the nav element
    toc_ul = soup.select_one("nav.o_side_nav ul.current")
    if not toc_ul:
        print("TOC container not found. Check the selector.")
        print("DEBUG: Full rendered HTML (first 3000 characters):")
        print(soup.prettify()[:3000])
        return {}
    
    pages_list = parse_toc_ul(toc_ul, toc_url)
    mapping = {}
    for p in pages_list:
        cat = p["category"]
        mapping.setdefault(cat, []).append(p)
    
    return mapping

def scrape_and_save_by_category(page):
    # Build mapping from TOC: top_category -> list of pages
    category_mapping = build_category_mapping(page, START_URL)
    if not category_mapping:
        print("No categories found. Exiting.")
        return

    print("Found categories:")
    for cat, pages in category_mapping.items():
        print(f"  {cat} ({len(pages)} pages)")

    # Process each category individually
    for cat, pages in category_mapping.items():
        # Create a folder for the current category.
        # The folder name is derived from the sanitized category name.
        cat_folder = os.path.join(OUTPUT_FOLDER, sanitize_filename(cat).replace('.json', ''))
        if not os.path.exists(cat_folder):
            os.makedirs(cat_folder)
            print(f"Created folder for category: {cat_folder}")
        else:
            print(f"Using existing folder: {cat_folder}")

        print(f"\nProcessing category: {cat}")
        for p in pages:
            url = p["url"]
            page_data = extract_page_content(page, url)
            if page_data:
                # Add extra info from TOC (page name and category path)
                page_data["toc_name"] = p["name"]
                page_data["toc_path"] = p["path"]
                # Save each page separately; filename based on the page's TOC name
                filename = sanitize_filename(p["name"])
                filepath = os.path.join(cat_folder, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(page_data, f, ensure_ascii=False, indent=2)
                print(f"Saved {filepath}")
            time.sleep(0.5)  # be polite




def build_toc_tree(pages_list):
    """
    Build a nested tree structure from a list of pages.
    Each page has a "path" list (e.g. [Heading, Subheading, Page]).
    The returned tree is a dict with keys "subcategories" and "pages" at each node.
    """
    root = {"subcategories": {}, "pages": []}
    for item in pages_list:
        path = item.get("path", [])
        current = root
        for level in path[:-1]:
            if level not in current["subcategories"]:
                current["subcategories"][level] = {"subcategories": {}, "pages": []}
            current = current["subcategories"][level]
        # Add the page at the leaf level.
        current["pages"].append(item)
    return root

def print_toc_tree(node, indent=0):
    """
    Recursively print the TOC tree.
    """
    prefix = "  " * indent
    # If there are pages in the current node, print them.
    for page in node.get("pages", []):
        print(f"{prefix}- Page: {page['name']} (URL: {page['url']})")
    # Then print subcategories.
    for subcat, subnode in node.get("subcategories", {}).items():
        # Count total pages under this category (directly under and in subcategories)
        direct_pages = len(subnode.get("pages", []))
        subcat_count = len(subnode.get("subcategories", {}))
        print(f"{prefix}* Category: {subcat} ({direct_pages} pages, {subcat_count} subcategories)")
        print_toc_tree(subnode, indent+1)

def print_full_toc_hierarchy(page):
    """
    Build and print the entire TOC hierarchy.
    """
    # First, get the flat mapping (each category's list of pages).
    mapping = build_category_mapping(page, START_URL)
    if not mapping:
        print("No categories found.")
        return
    # Combine all pages from all categories into one list.
    pages_list = []
    for pages in mapping.values():
        pages_list.extend(pages)
    # Build a tree structure from the flat pages list.
    tree = build_toc_tree(pages_list)
    print("TOC Hierarchy:")
    print_toc_tree(tree)




if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
            }
        )
        page = context.new_page()
        print_full_toc_hierarchy(page)
        print_category_summary(page)
        scrape_and_save_by_category(page)
        browser.close()
