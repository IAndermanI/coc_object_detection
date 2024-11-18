import os
import requests
from bs4 import BeautifulSoup

url = "https://clashofclans.fandom.com/wiki/Category:Buildings"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    for members_wrapper in soup.find_all('div', class_='category-page__members-wrapper'):
        for ul in members_wrapper.find_all('ul', class_='category-page__members-for-char'):
            for li in ul.find_all('li'):
                a_tag = li.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    links.append('https://clashofclans.fandom.com' + a_tag['href'])

    for index, link in enumerate(links):
        item_response = requests.get(link)

        if item_response.status_code == 200:
            item_soup = BeautifulSoup(item_response.text, 'html.parser')

            image_divs = item_soup.find_all('div', class_='flexbox-display bold-text')
            if len(image_divs) == 0:
                image_divs = item_soup.find_all('div', class_='flexbox-display')

            os.makedirs(f'images/{index}', exist_ok=True)

            for div in image_divs:
                img_tags = div.find_all('img')
                for img in img_tags:
                    try:
                        img_url = img['data-src']
                    except KeyError:
                        img_url = img['src']
                    img_name = img['data-image-key']

                    img_data = requests.get(img_url).content
                    with open(f'images/{index}/{img_name}', 'wb') as img_file:
                        img_file.write(img_data)
                    print(f"Сохранено: images/{index}/{img_name}")

        else:
            print(f"Ошибка при запросе страницы {link}: {item_response.status_code}")
else:
    print(f"Ошибка при запросе страницы: {response.status_code}")
