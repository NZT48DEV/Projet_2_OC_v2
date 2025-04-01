import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from datetime import date
import csv
import os


TODAY = date.today()
CSV_FOLDER = 'CSV'


def fetch_page(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, "html.parser")


def extract_book_data(soup, url):
    table = soup.find('table', class_='table table-striped')

    def get_table_value(label):
        return table.find('th', string=label).find_next_sibling('td').text

    title = soup.find('div', class_="col-sm-6 product_main").find('h1').text
    match = re.search(r'\((\d+)\s+available\)', get_table_value('Availability'))
    number_available = int(match.group(1)) if match else "Nombre non trouvé"

    review_rating_tag = soup.find('p', class_='star-rating')
    review_rating_classes = review_rating_tag.get('class') if review_rating_tag else []
    review_rating_text = next((cls.capitalize() for cls in review_rating_classes if cls != 'star-rating'), 'Zero')
    review_rating_map = {'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    review_rating = review_rating_map.get(review_rating_text, 0)

    return {
    'product_page_url': url,
    'universal_product_code': get_table_value('UPC'),
    'title': title,
    'price_including_tax': get_table_value('Price (incl. tax)'),
    'price_excluding_tax' : get_table_value('Price (excl. tax)'),
    'number_available': number_available,
    'product_description': soup.find('div', id='product_description').find_next_sibling('p').text,
    'category': soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip(),
    'review_rating': review_rating,
    'image_url': urljoin(url, soup.find('div', class_='item').find('img')['src'])
    }


def clean_filename(title, max_length=50):
    title = re.sub(r'[^\w\s-]', '', title)
    title = title.strip().replace(' ', '_')
    return title[:max_length]


def save_to_csv(book_data, folder):
    if not os.path.exists(CSV_FOLDER):
        os.makedirs(CSV_FOLDER)

    clean_title = clean_filename(book_data['title'])
    csv_fieldname = f'{clean_title}_{TODAY}.csv'
    csv_path = os.path.join(CSV_FOLDER, csv_fieldname)

    with open(csv_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=book_data.keys(), delimiter=';')
        writer.writeheader()
        writer.writerow(book_data)


def main():
    url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    soup = fetch_page(url)
    book_data = extract_book_data(soup, url)
    save_to_csv(book_data, CSV_FOLDER)
    print(f"Données exportées :", book_data['title'])

if __name__ == '__main__':
    main()