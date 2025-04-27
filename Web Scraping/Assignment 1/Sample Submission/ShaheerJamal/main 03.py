from bs4 import BeautifulSoup
import requests
import re
import json

url = "https://www.thriftbooks.com/browse/?12529col#b.s=mostPopular-desc&b.p=1&b.pp=50&b.col&b.f.t%5B%5D=13901&b.list"

for page in range(1, 30):  # Adjust upper limit as needed
    changed_url = url + str(page)
    web = requests.get(changed_url).content
    soup = BeautifulSoup(web, 'lxml')

content = soup.find_all("script")
string = content[12].string
# print(string)


main_data = re.search(r'window\.searchStoreV2\s*=\s*(\{.*?\});', string, re.DOTALL)

books_data = {}

if main_data:
    works = main_data.group(1)
    works_json = json.loads(works)
    works = works_json.get("works")
    
# print(data)
for i in works:
    books_data.update(i)
    title = books_data["title"]
    # author = books_data[""]
    # price = books_data[""]
    # rating = books_data[""]
    # isbn = books_data[""]
    
    with open("Literature Books.csv", "a") as f:
        f.write(f"{title}\n")
        