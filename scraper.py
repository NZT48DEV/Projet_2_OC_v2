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
    """
    Récupère et parse le contenu HTML d'une page web à partir de son URL.

    Args:
        url (str): L'URL complète de la page à récupérer.

    Returns:
        BeautifulSoup: Objet contenant l'arbre HTML de la page, prêt à être analysé.
    """
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def extract_book_data(soup, url):
    """
        Extrait les informations d'un livre à partir d'une page HTML analysée avec BeautifulSoup.

    Args:
        soup (BeautifulSoup): Objet BeautifulSoup représentant le contenu HTML de la page du livre.
        url (str): URL complète de la page produit

    Returns:
        dict: Dictionnaire contenant les informations extraites du livre :
            titre, prix, disponibilités, etc.
    """
    table = soup.find('table', class_='table table-striped')

    def get_table_value(label):
        """
        Récupère une valeur dans le tableau HTML à partir d'une balise (th).

        Args:
            label (str): Le nom du champ (ex: 'UPC', 'Price (incl. tax)', etc.).

        Returns:
            str: La valeur correspondante extraite de la cellule voisine (td).
        """
        return table.find('th', string=label).find_next_sibling('td').text

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
    'price_including_tax': get_table_value('Price (incl. tax)'),
    'price_excluding_tax' : get_table_value('Price (excl. tax)'),
    'number_available': number_available,
    'product_description': soup.find('div', id='product_description').find_next_sibling('p').text,
    'category': soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip(),
    'review_rating': review_rating,
    'image_url': urljoin(url, soup.find('div', class_='item').find('img')['src'])
    }

    return product_data


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
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

    clean_title = clean_filename(book_data['title'])
    csv_fieldname = f'{clean_title}_{TODAY}.csv'
    csv_path = os.path.join(folder, csv_fieldname)

    with open(csv_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=book_data.keys(), delimiter=';')
        writer.writeheader()
        writer.writerow(book_data)


def main():
    """
    Fonction principale du script.

    Enchaîne les étapes de récupération, d'extraction et de sauvegarde des données
    d'un livre à partir d'une URL donnée.
    """
    url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    soup = fetch_page(url)
    book_data = extract_book_data(soup, url)
    save_to_csv(book_data, CSV_FOLDER)
    print(f"Données exportées :", book_data['title'])

if __name__ == '__main__':
    main()