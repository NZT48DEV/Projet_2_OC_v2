import requests
import os
import sys
import re
import csv
from bs4 import BeautifulSoup

if __name__ == "__main__" and __package__ is None:
    # Ajoute le dossier parent (racine du projet) à sys.path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    projet_root = os.path.abspath(os.path.join(script_dir, '..'))
    sys.path.insert(0, projet_root)

from phase1.scraper import fetch_page, extract_book_data, DATE_TODAY
from phase2.scraper_category import fetch_category_urls


URL = "https://books.toscrape.com/index.html"


def fetch_all_category_urls(category_url, session):
    urls = []
    category_names = []
    current_url = category_url

    response = session.get(current_url)
    if response.status_code != 200:
        raise Exception(f"[ERREUR HTTP] : {response.status_code} - {response.reason}")
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    side_categories = soup.find('div', class_='side_categories')
    li_elements = side_categories.find('ul').find('li').find('ul').find_all('li')

    for li in li_elements:
        a_tag = li.find('a')
        if a_tag:
            relative_url = a_tag['href'].replace("../", "")
            full_url = "https://books.toscrape.com/" + relative_url
            category_name = a_tag.text.strip()
            category_names.append(category_name)
            urls.append(full_url)
    
    return urls, category_names


def save_all_categories_to_csv(all_books_data, category_name):
    if not all_books_data:
        print(f"[INFO] Aucun livre à enregistrer pour la catégorie '{category_name}'")
        return

    try:
        safe_category_name = re.sub(r'[^\w\s-]', '', category_name).strip().replace(' ', '_')
        phase3_dir = os.path.dirname(os.path.abspath(__file__))
        category_folder = os.path.join(phase3_dir, "CSV", safe_category_name)
        os.makedirs(category_folder, exist_ok=True)

        filename = f"products_category_{safe_category_name}_{DATE_TODAY}.csv"
        csv_path = os.path.join(category_folder, filename)

        with open(csv_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=all_books_data[0].keys(), delimiter=';')
            writer.writeheader()
            writer.writerows(all_books_data)
    except Exception as e:
        print(f"[ERREUR] Echec de la sauvegarder pour la catégorie '{category_name}' : {e}")


def main():
    with requests.Session() as session:
        category_urls, category_names = fetch_all_category_urls(URL, session)
        total_category = len(category_urls)
        print(f"Nombre total de catégories : {total_category}\n")
    
    for index, (category_name, category_url) in enumerate(zip(category_names, category_urls), start=1):
        print(f"""
______________________________________________________
Catégorie [{index}] : {category_name}
Lien de la catégorie {category_name} : {category_url}
______________________________________________________

""")

        book_urls = fetch_category_urls(category_url, session)

        all_books_data = []
        for book_index, book_url in enumerate(book_urls, start=1):
            try:
                print(f"Livre {book_index}/{len(book_urls)} : {book_url}")
                soup = fetch_page(book_url)
                book_data = extract_book_data(soup, book_url)
                all_books_data.append(book_data)
                save_all_categories_to_csv(all_books_data, category_name)
            except Exception as e:
                print(f"[ERREUR] Livre non traité ({book_url}) : {e}")
        

if __name__ == "__main__":
    main()