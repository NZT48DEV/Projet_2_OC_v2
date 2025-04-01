import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from datetime import date
import csv
import os

URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
TODAY = date.today()
CSV_FOLDER = 'CSV'

def clean_filename(title, max_length=50):
    title = re.sub(r'[^\w\s-]', '', title)
    title = title.strip().replace(' ', '_')
    return title[:max_length]

# Effectue une requête get sur le lien stipulé.
response = requests.get(URL)
response.encoding = 'utf-8'

# Ecrit le code HTML dans un fichier index.html
# with open('index.html', 'w') as file:
#     file.write(response.text)

# Créer une instance de BeautifulSoup pour analyser des fichiers (ici un fichier HTML avec html.parser) - [lxml-xml][html.parser][html5lib]
soup = BeautifulSoup(response.text, "html.parser")

# pretiffy permet d'afficher les indentations du HTML (facilite la lecture)
# print(soup.prettify())
product_page_url = URL

universal_product_code = soup.find('table', class_="table table-striped") \
                             .find('th', string='UPC') \
                             .find_next_sibling('td').text

title = soup.find('div', class_="col-sm-6 product_main").find('h1').text

price_including_tax = soup.find('table', class_="table table-striped") \
                          .find('th', string='Price (incl. tax)') \
                          .find_next_sibling('td').text

price_excluding_tax = soup.find('table', class_="table table-striped") \
                          .find('th', string='Price (excl. tax)') \
                          .find_next_sibling('td').text

number_available_str = soup.find('table', class_="table table-striped") \
                          .find('th', string='Availability') \
                          .find_next_sibling('td').text
match = re.search(r'\((\d+)\s+available\)', number_available_str)
if match:
    number_available = int(match.group(1))
else:
    number_available = "Nombre non trouvé"

product_description = soup.find('div', id='product_description').find_next_sibling('p').text

category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()

review_rating_tag = soup.find('p', class_='star-rating')
review_rating_classes = review_rating_tag.get('class')
review_rating_text = [cls.capitalize() for cls in review_rating_classes if cls != 'star-rating'][0]
review_rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
review_rating = review_rating_map.get(review_rating_text, 0)

image_url_relative = soup.find('div', class_='item').find('img')['src']
image_url = urljoin(URL, image_url_relative)

book_data = {
    'product_page_url': product_page_url,
    'universal_product_code': universal_product_code,
    'title': title,
    'price_including_tax': price_including_tax,
    'price_excluding_tax' : price_excluding_tax,
    'number_available': number_available,
    'product_description': product_description,
    'category': category,
    'review_rating': review_rating,
    'image_url': image_url
}

clean_title = clean_filename(book_data['title'])

if not os.path.exists(CSV_FOLDER):
    os.makedirs(CSV_FOLDER)

csv_title = f'{clean_title}_{TODAY}.csv'
csv_path = os.path.join(CSV_FOLDER, csv_title)

with open(csv_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=book_data.keys(), delimiter=';')
    writer.writeheader()
    writer.writerow(book_data)


