import requests
from bs4 import BeautifulSoup

response = requests.get("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")

with open('index.html', 'w') as file:
    file.write(response.text)