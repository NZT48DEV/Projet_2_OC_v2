import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from datetime import date
import csv
import os


DATE_TODAY = date.today()
CSV_FOLDER = 'CSV'


def fetch_page(url):
    """
    Récupère et parse le contenu HTML d'une page web à partir de son URL.

    Args:
        url (str): L'URL complète de la page à récupérer.

    Returns:
        BeautifulSoup: Objet contenant l'arbre HTML de la page, prêt à être analysé.
    
    Raises:
        requests.exceptions.RequestException: En cas de problème réseau.
    """
    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"[ERREUR] Echec lors de la récupération de l'URL : {url}\n-> {e}")


def extract_book_data(soup, url):
    """
        Extrait les informations d'un livre à partir d'une page HTML analysée avec BeautifulSoup.

    Args:
        soup (BeautifulSoup): Objet BeautifulSoup représentant le contenu HTML de la page du livre.
        url (str): URL complète de la page produit

    Returns:
        dict: Dictionnaire contenant les informations extraites du livre :
            titre, prix, disponibilités, etc.
    Raises:
        RuntimeError : En cas d'échec de l'extraction d'une donnée depuis l'URL
    """
    try:
        table = soup.find('table', class_='table table-striped')

        def get_table_value(label):
            """
            Récupère une valeur dans le tableau HTML à partir d'une balise (th).

            Args:
                label (str): Le nom du champ (ex: 'UPC', 'Price (incl. tax)', etc.).

            Returns:
                str: La valeur textuelle de la cellule <td> associée. Retourne "N/A" si la cellule est vide.
            Raises:
                ValueError: Si la balise <th> correspondant au label est introuvable
                RuntimeError: En cas d'échec de l'extraction d'une ou plusieurs données.
            """
            th = table.find('th', string=label)
            if th is None:
                raise ValueError(f"[ERREUR] champ '{label}' introuvable dans le tableau")
            td = th.find_next_sibling('td')
            return td.text if td else "N/A"

        title = soup.find('div', class_="col-sm-6 product_main").find('h1').text
        match = re.search(r'\((\d+)\s+available\)', get_table_value('Availability'))
        number_available = int(match.group(1)) if match else "Nombre non trouvé"

        review_rating_tag = soup.find('p', class_='star-rating')
        review_rating_classes = review_rating_tag.get('class') if review_rating_tag else []
        review_rating_text = next((cls.capitalize() for cls in review_rating_classes if cls != 'star-rating'), 'Zero')
        review_rating_map = {'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        review_rating = review_rating_map.get(review_rating_text, 0)

        product_data = {
        'product_page_url': url,
        'universal_product_code': get_table_value('UPC'),
        'title': title,
        'price_including_tax': float(get_table_value('Price (incl. tax)').replace('£', '')),
        'price_excluding_tax' : float(get_table_value('Price (excl. tax)').replace('£', '')),
        'number_available': number_available,
        'product_description': soup.find('div', id='product_description').find_next_sibling('p').text,
        'category': soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip(),
        'review_rating': review_rating,
        'image_url': urljoin(url, soup.find('div', class_='item').find('img')['src'])
        }

        return product_data

    except Exception as e:
        raise RuntimeError(f"[ERREUR] Échec de l'extraction depuis {url} : {e}")


def clean_filename(title, max_length=50):
    """
    Nettoie un titre. 

    Args:
        title (str): Le titre à nettoyer
        max_length (int, optional): Longueur maximale du nom retourné (50 par défaut)

    Returns:
        str: Le titre nettoyé.
    """
    title = re.sub(r'[^\w\s-]', '', title)
    title = title.strip().replace(' ', '_')
    return title[:max_length]


def save_to_csv(book_data, folder):
    """
    Sauvegarde les données d'un livre dans un fichier CSV.

    Args:
        book_data (dict[str, any]): Dictionnaire contenant les données du livre (titre, prix, catégorie, etc.)
        folder (str): Nom ou chemin du dossier où sera créé le fichier CSV.
    Side Effects: 
        Crée un fichier CSV dans le dossier spécifié
    Raises:
        Exception: En cas d'erreur lors de la création du dossier ou de l'écriture du fichier.
    """
    try:
        phase1_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(phase1_dir, "CSV")

        os.makedirs(csv_path, exist_ok=True)

        clean_title = clean_filename(book_data['title'])
        csv_fieldname = f'{clean_title}_{DATE_TODAY}.csv'
        csv_file = os.path.join(csv_path, csv_fieldname)

        with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=book_data.keys(), delimiter=';')
            writer.writeheader()
            writer.writerow(book_data)
        return csv_fieldname
    except Exception as e:
        print(f"[ERREUR]Impossible d'enregistrer le fichier CSV :\n-> {e}")


def main():
    """
    Fonction principale du script.

    Enchaîne les étapes de récupération, d'extraction et de sauvegarde des données
    d'un livre à partir d'une URL donnée.
    """
    url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

    try:
        soup = fetch_page(url)
        book_data = extract_book_data(soup, url)
        csv_fieldname = save_to_csv(book_data, CSV_FOLDER)
        print(f"\nLes données du livre : '{book_data['title']}' ont étaient exportées vers {CSV_FOLDER}/{csv_fieldname}")
    except Exception as e:
        print(f"[ERREUR] : {e}")


if __name__ == '__main__':
    main()