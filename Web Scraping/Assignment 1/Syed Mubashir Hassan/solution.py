import requests
from bs4 import BeautifulSoup
import json
import re
import time
import csv

def scrape_thriftbooks(base_url, output_file):
    print(f"Starting scraping for {output_file}...")

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['title', 'condition', 'buy_price'])

        page = 1
        previous_titles = set()  # track titles we've seen before

        while True:
            print(f"Scraping page {page}...")
            url = base_url.format(page=page)

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

                        if not works:
                            print(f"No more books found on page {page}. Stopping.")
                            break  # stop if no books

                        # Check if data is repeating
                        current_titles = {item.get('title', '') for item in works}
                        if current_titles.issubset(previous_titles):
                            print(f"Same books detected again on page {page}. Stopping.")
                            break  # stop if books are repeating

                        previous_titles.update(current_titles)

                        for item in works:
                            title = item.get('title', 'N/A')
                            condition = item.get('buyNowCondition', 'N/A')
                            buy_price = item.get('buyNowPrice', 'N/A')

                            writer.writerow([title, condition, buy_price])
                    else:
                        print(f"No matching JSON data found on page {page}.")
                        break

                else:
                    print(f"Script tag not found on page {page}.")
                    break

            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                break

            page += 1
            time.sleep(1)

    print(f"Scraping complete for {output_file}\n")

# Define URLs
urls = [
    {
        'url': 'https://www.thriftbooks.com/browse/?14236col#b.s=mostPopular-desc&b.p={page}&b.pp=50&b.col&b.f.t%5B%5D=14236&b.list',
        'filename': 'thrift_books_data_1.csv'
    },
    {
        'url': 'https://www.thriftbooks.com/browse/?15464col#b.s=mostPopular-desc&b.p={page}&b.pp=50&b.col&b.f.t%5B%5D=15464&b.list',
        'filename': 'thrift_books_data_2.csv'
    }
]

# Run for each URL
for entry in urls:
    scrape_thriftbooks(entry['url'], entry['filename'])

print("All scraping done.")
