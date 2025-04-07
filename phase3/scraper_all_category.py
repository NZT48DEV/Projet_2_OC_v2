import requests
import os
import sys
import re
import csv
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

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


def scrape_books_parallel(book_urls):
    results = []

    def process_url(index, url):
        try:
            print(f"Livre {index + 1}/{len(book_urls)} : {url}")
            soup = fetch_page(url)
            return extract_book_data(soup, url)
        except Exception as e:
            print(f"[ERREUR] Livre non traité ({url}) : {e}")
            return None

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = {
        executor.submit(process_url, index, url): url
        for index, url in enumerate(book_urls)
        }
        for future in as_completed(future_to_url):
            result = future.result()
            if result:
                results.append(result)

    return results


def main():
    start_time = time.time()
    with requests.Session() as session:
        print(f"\nDébut du scraping de toutes les catégories/livres du site.\n")
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
        all_books_data = scrape_books_parallel(book_urls)
        duration = time.time() - start_time
        print(f"Durée d'exécution : {duration:.2f} secondes")

if __name__ == "__main__":
    main()