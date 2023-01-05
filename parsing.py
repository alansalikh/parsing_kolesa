import requests
from bs4 import BeautifulSoup
from pprint import pprint

HEADERS= {
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
            "accept": "text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8" 
}

DOMEN = "https://kolesa.kz/"
URL = "https://kolesa.kz/cars/almaty/"

def get_html(url, params =''):
    return requests.get(url, headers= HEADERS, params=params)


def get_content(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('div', class_='a-list__item')
    data = []

    for i in items:
        try:
            title = i.find('div', class_='a-card__header').find('h5').get_text(strip=True)
        except:
            title = "не удалось"
            pass

        try:
            price = i.find('span', class_ = 'a-card__price').get_text(strip=True).replace('\xa0', '').replace('₸', '')
            price = int(price)

        except:
            price = "не удалось"
            pass
        # photo = i.find('picture', class_='thumb-gallery__pic thumb-gallery__pic--main').find()
        data.append(
            {
            'title': title,
            'price': price
            }
        )
    return data

def save(content: list):
    with open('data.txt', 'a') as f:
        for num, item in enumerate(content,1):
            f.write(f"№{num} - Название{item['title']}\n")
            f.write(f"       - Цена{item['price']}\n")


def parse(page):
    contents =[]
    for i in range(2, page+1):
        html = get_html(URL, params={'page': i})
        if html.status_code == 200:
            content = get_content(html)
            # contents.extend(content)
            pprint(content)
            print(f'{i} страница готова')
    print('парсинг готов')
    save(content)


parse(3)