import requests
from bs4 import BeautifulSoup

# Récupération de toutes les catégories du site
# Un nouveau mode d'enregistrement avec un fichier CSV par categorie

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


def save_each_category_to_csv():
    pass


def main():
    with requests.Session() as session:
        category_urls, category_names = fetch_all_category_urls(URL, session)
        total_category = len(category_urls)
        print(f"Nombre total de catégories : {total_category}\n")
    
    for index, (category_name, category_url) in enumerate(zip(category_names, category_urls), start=1):
        print(f"Catégorie {index}: {category_name}")
        print(f"Lien de la catégorie {category_name}: {category_url}\n")

if __name__ == "__main__":
    main()