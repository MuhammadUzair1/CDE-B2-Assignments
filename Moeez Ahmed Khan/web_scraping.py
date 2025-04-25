import requests
from bs4 import BeautifulSoup
import json
import re

base_url = "https://www.thriftbooks.com/browse/?15013col#b.s=mostPopular-desc&b.p={page}&b.pp=50&b.col&b.f.t%5B%5D=15013&b.list"
all_works = [] 

max_pages = 50

for page in range(1, max_pages + 1):
    webUrl = base_url.format(page=page)
    content = requests.get(webUrl).content
    soup = BeautifulSoup(content, 'html.parser')

    scripts = soup.find_all('script')
    
    string = scripts[12].string

    match = re.search(r'window\.searchStoreV2\s*=\s*(\{.*?\});', string, re.DOTALL)
    if match:
        raw_json = match.group(1)
        data = json.loads(raw_json)
        works = data.get("works", [])
        print("Extracted Data:", works)
    else:
          print("Data not found.")

    with open(r"scraped_data.csv", "w") as f:
        f.write(f'Title, BuyNowPrice, format, Publisher, ReleaseDate \n')


    for work in works:
        title = work['title']
        buyNowPrice = work['buyNowPrice']
        format = work['media']
        publisher = work['publisher']
        releaseDate = work['releaseDate'] 

        with open(r"scraped_data.csv", "a") as f:
            f.write(f'{title}, {buyNowPrice}, {format} ,{publisher}, {releaseDate} \n')

    print("Data scraping completed. Saved to 'scraped_data.csv'.")
