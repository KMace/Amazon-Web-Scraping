import csv
from bs4 import BeautifulSoup

def get_price(web_price):
    """Refines the scraped price from amazon, as it repeats twice"""

    return web_price[0 : len(web_price) // 2]

def extractRecord(item):
    """Extract and return data from a single record"""

    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = atag.get('href')

    # price
    try:
        price = get_price(item.find('span', 'a-price').text)
    except AttributeError:
        return

    # rank and rating
    try:
        rating = item.i.text
        numberRatings = item.find('span', {'class' : 'a-size-base'}).text
    except AttributeError:
        rating, numberRatings = '', ''
    
    return (description, price, rating, numberRatings, url)

records = []

for pageNumber in range(1, 21):
    print(pageNumber)
    file = open("Amazon pages/page" + str(pageNumber) + ".html", encoding="utf-8")
    
    soup = BeautifulSoup(file, 'html.parser')
    results = soup.find_all('div', {'data-component-type' : 's-search-result'})

    for item in results:
        record = extractRecord(item)
        if record:
            records.append(record)

with open('results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'URL'])
    writer.writerows(records)