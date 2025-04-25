
import requests 
from bs4 import BeautifulSoup
import json
import re

# Write the headers once before the loop starts
with open(r'thrift_books_data_fiction.csv', 'w') as f:
    f.write(f'ISBN, title, condition, buy_price, publisher, release_date, media, author\n')

# Loop through pages
for page in range(1, 100):  # Adjust 100 to a higher number if needed
    print(f"Fetching page {page}...")
    url = f'https://www.thriftbooks.com/browse/?13362col#b.s=mostPopular-desc&b.p=1&b.pp=50&b.col&b.f.t%5B%5D=13362&b.list'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch page {page}")
        break

    soup = BeautifulSoup(response.content, 'html.parser')
    script_tags = soup.find_all('script')

    if len(script_tags) < 13 or script_tags[12].string is None:
        print("No valid script content found.")
        break

    script_content = script_tags[12].string
    match = re.search(r'window\.searchStoreV2\s*=\s*(\{.*?\});', script_content, re.DOTALL)

    if not match:
        print("No data match found in script.")
        break

    try:
        works_json = json.loads(match.group(1))
    except json.JSONDecodeError:
        print("JSON decoding failed.")
        break

    works = works_json.get('works', [])
    if not works:
        print("No more book data found.")
        break

    for item in works:
        # print(item)
        title = item.get('title', '')
        condition = item.get('buyNowCondition', '')
        buy_price = item.get('buyNowPrice', '')
        publisher = item.get('publisher', '')
        release_date = item.get('releaseDate', '')
        isbn = item.get('iSBN', '')
        media = item.get('media', '')
        author = item.get('authors', [{}])[0].get('authorName', '')

        with open(r'thrift_books_data_fiction.csv', 'a', encoding='utf-8') as f:
            f.write(f'{isbn}, {title}, {condition}, {buy_price}, {publisher}, {release_date}, {media}, {author}\n')

    print(f"Page {page} processed.\n")
