import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
projet_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.insert(0, projet_root)

import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from phase2.scraper_category import fetch_category_urls
from phase3.scraper_all_category import fetch_all_category_urls, scrape_books_parallel
from utils.saver import save_all_categories_to_csv
from utils.cleaner import clean_filename


URL = "https://books.toscrape.com/index.html"


def download_images_parallel(session, all_books_data, book_cover_dir):
    """
    Télécharge en parallèle les images de couverture de tous les livres d'une catégorie.

    Chaque image est enregistrée dans un dossier spécifique en fonction du nom du livre, 
    nettoyé et limité à 50 caractères. Si le fichier image existe déjà, le téléchargement est ignoré.

    Args:
        session (requests.Session): Session HTTP partagée pour réutiliser la connexion.
        all_books_data (list[dict]): Liste de dictionnaires contenant les données des livres,
                                     incluant les clés 'image_url' et 'title'.
        book_cover_dir (str): Chemin du dossier où enregistrer les images (ex : /phase4/CSV/Catégorie/Book_Cover).

    Side Effects:
        Crée le dossier `book_cover_dir` s’il n’existe pas déjà.
        Télécharge les fichiers images et les enregistre sur le disque.

    Notes:
        - Utilise un ThreadPoolExecutor pour paralléliser les téléchargements (max_workers=20).
        - Affiche une erreur pour chaque image non téléchargeable.
    """
    os.makedirs(book_cover_dir, exist_ok=True)

    # Télécharge l'image d'un seul livre si elle n'existe pas déjà localement.
    def process(book):
        image_url = book["image_url"]
        title = book["title"]
        safe_title = clean_filename(title, max_length=50)
        extension = os.path.splitext(image_url)[1] or ".jpg"
        image_path = os.path.join(book_cover_dir, f"{safe_title}{extension}")

        if os.path.exists(image_path):
            return

        try:
            response = session.get(image_url, timeout=10)
            response.raise_for_status()
            with open(image_path, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(f"[ERREUR] Téléchargement échoué ({image_url}) : {e}")

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(process, book) for book in all_books_data]
        for future in as_completed(futures):
            future.result()


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
        phase4_dir = os.path.dirname(os.path.abspath(__file__))
        book_cover_dir = os.path.join(phase4_dir, "CSV", clean_filename(category_name), "Book_Cover")
        os.makedirs(book_cover_dir, exist_ok=True)
        save_all_categories_to_csv(all_books_data, category_name, phase4_dir)
        download_images_parallel(session, all_books_data, book_cover_dir)
        duration = time.time() - start_time
        print(f"Durée d'exécution : {duration:.2f} secondes")


if __name__ == "__main__":
    main()

