
import requests
from bs4 import BeautifulSoup
import re
import json

# Do URLs ki list
urls = [
    ('https://www.thriftbooks.com/browse/?12529col#b.s=mostPopular-desc&b.p=1&b.pp=50&b.col&b.f.t%5B%5D=12529&b.list', 'thriller_books.csv')
]


condition = True

while condition:

    for url , filename in urls:
        print(url,'\n', filename)


        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')


        scripts = soup.find_all('script')
        
        # Handle edge case if script[12] does not exist
        if len(scripts) < 13:
            print(f"❌ Not enough script tags in {url}")
            continue

        json_string = scripts[12].string

        match = re.search(r'window.searchStoreV2\s*=\s*(\{.*?\});', json_string, re.DOTALL)

        if match:
            if filename == 'thriller_books.csv':
                json_data = match.group(1)
                works_json = json.loads(json_data)
                works = works_json.get('works', [])

                # Har file ka header
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Title, Condition, Price\n")

                for book in works:
                    title = book.get('title', 'N/A')
                    condition = book.get('buyNowCondition', 'N/A')
                    price = book.get('buyNowPrice', 'N/A')

                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(f"{title}, {condition}, {price}\n")
            elif filename == 'fiction_books.csv':
                sec_json_data = match.group(1)
                sec_works_json = json.loads(sec_json_data)
                sec_works = sec_works_json.get('works', [])
                sec_works.reverse()

                # print('sec_url',sec_works)
                # Har file ka header
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Title, Conditions, Price\n")

                for book in sec_works:
                    title = book.get('title', 'N/A')
                    condition = book.get('buyNowCondition', 'N/A')
                    price = book.get('buyNowPrice', 'N/A')

                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(f"{title}, {condition}, {price}\n")
            
            print(f"Data from {url} saved to {filename}")

        if filename == 'thriller_books.csv':
            urls.clear()
            urls.append(('https://www.thriftbooks.com/browse/?13006col#b.s=mostPopular-desc&b.p=1&b.pp=50&b.col&b.f.t%5B%5D=13006&b.list', 'fiction_books.csv'))
            continue
        elif urls[0][1] == 'fiction_books.csv':
            print(urls[0][1])
            condition = False
        else:
            break






    print('Data...')
    
