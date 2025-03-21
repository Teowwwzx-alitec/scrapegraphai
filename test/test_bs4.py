import requests
from bs4 import BeautifulSoup

def bs4_scraper(url: str, output_file: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(True)  # Find all elements
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for idx, element in enumerate(elements, 1):
                f.write(f"Element {idx}:\n{str(element)}\n{'='*50}\n")
                
        print(f"Saved {len(elements)} elements to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    target_url = "http://localhost:8070/web#action=370&model=stock.picking.type&view_type=kanban&cids=1&menu_id=181"  # Replace with your URL
    bs4_scraper(target_url, "bs4_elements.txt")
