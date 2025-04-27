from bs4 import BeautifulSoup
import requests
import re
import json

base_url = "https://www.thriftbooks.com/browse/?14644col#b.s=mostPopular-desc"
page_size = "&b.p=1&b.pp=50&b.col&b.f.t%5B%5D=14644&b.list"

for page in range(1, 100):  
    current_url = base_url + str(page) + page_size
    web = requests.get(current_url).content
    soup = BeautifulSoup(web, 'lxml')

    content = soup.find_all("script")
    if len(content) < 13:  
        print(f"No more pages found. Stopped at page {page-1}")
        break
        
    string = content[12].string
    main_data = re.search(r'window\.searchStoreV2\s*=\s*(\{.*?\});', string, re.DOTALL)

    if not main_data:
        print(f"No data found on page {page}. Stopping.")
        break
        
    works_json = json.loads(main_data.group(1))
    works = works_json.get("works", [])
    
    if not works:  # If no works found, we've reached the end
        print(f"No more books found. Stopped at page {page-1}")
        break
        
    for book in works:
        title = book.get("title", "N/A")
        # Add other fields you want to extract here
        
        with open("Politics and Sciences.csv", "a", encoding='utf-8') as f:
            f.write(f"{title}\n")
    
    print(f"Processed page {page} with {len(works)} books")