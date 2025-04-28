import requests
from bs4 import BeautifulSoup
import json
import re
import time

with open('thrift_books_data.csv', 'w', encoding='utf-8') as f:
    f.write('title,condition,buy_price\n')

for page in range(1, 21):
    print(f"Scraping page {page}...")
    url = f'https://www.thriftbooks.com/browse/?12529col#b.s=mostPopular-desc&b.p={page}&b.pp=50&b.col&b.f.t%5B%5D=12529&b.list'

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        scripts = soup.find_all('script')
        if len(scripts) > 12:
            script_text = scripts[12].string

            match = re.search(r'window\.searchStoreV2\s*=\s*(\{.*?\});', script_text, re.DOTALL)
            if match:
                works_json = json.loads(match.group(1))
                works = works_json.get('works', [])

                for item in works:
                    title = item.get('title', 'N/A')
                    condition = item.get('buyNowCondition', 'N/A')
                    buy_price = item.get('buyNowPrice', 'N/A')

                    with open('thrift_books_data.csv', 'a', encoding='utf-8') as f:
                        f.write(f'"{title}","{condition}","{buy_price}"\n')
        else:
            print(f"Script tag not found on page {page}")

    except Exception as e:
        print(f"Error scraping page {page}: {e}")

    time.sleep(1)

print("Scraping complete. Data saved in 'thrift_books_data.csv'")