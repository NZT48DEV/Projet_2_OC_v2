# Système de Surveillance des Prix – Books Online

Ce projet a pour objectif de développer une version bêta d’un système de surveillance des prix pour Books Online. Il s’agit d’un script Python qui scrape une page produit choisie sur le site [Books to Scrape](http://books.toscrape.com/) et en extrait diverses informations afin de générer un fichier CSV contenant les données collectées.


## Fonctionnalités

Le script récupère les informations suivantes pour chaque produit :
- **product_page_url** : URL de la page produit
- **universal_product_code (upc)** : Code universel du produit
- **title** : Titre du produit
- **price_including_tax** : Prix TTC
- **price_excluding_tax** : Prix HT
- **number_available** : Nombre d’exemplaires disponibles
- **product_description** : Description du produit
- **category** : Catégorie du produit
- **review_rating** : Note attribuée par les utilisateurs
- **image_url** : URL de l’image du produit


## Prérequis

- Python 3.12.1 ou supérieur
- Les packages listés dans le fichier `requirements.txt`


## Installation

1. **Cloner le repository :**
    
    git clone https://github.com/NZT48DEV/Projet_2_OC_v2.git

    cd Projet_2_OC_v2


2. **Créer et activer un environnement virtuel (optionnel mais recommandé) :**
    
    python -m venv env

    source env/bin/activate  # Sur Linux/Mac

    env\Scripts\activate     # Sur Windows


3. **Installer les dépendances :**
    
    pip install -r requirements.txt


## Utilisation

1. **Exécuter le script de scraping :**
    
    python scraper.py

    Le script va se connecter à la page produit choisie, extraire les informations et écrire les données dans un fichier CSV.


2. **Vérifier le fichier CSV généré :**

    Le fichier CSV contiendra une ligne d’en-tête suivie des données collectées.


## Structure du Repository

Projet_2_OC_v2/

├── scraper.py           # Script principal de scraping

├── requirements.txt     # Liste des dépendances

├── README.md            # Ce fichier de documentation

└── .gitignore           # Fichier pour ignorer l’environnement virtuel et les CSV


## Ressources Complémentaires
- Documentation Python : https://docs.python.org/3/
- Documentation Requests : https://requests.readthedocs.io/en/latest/
- Documentation BeautifulSoup : https://www.crummy.com/software/BeautifulSoup/bs4/doc/


## Remarques

Ce projet constitue une première version (bêta) et pourra être amélioré avec des fonctionnalités supplémentaires telles que :

L'extraction des données pour toute une catégorie de livre (P2)
L'extraction des données de toutes les catégories et les informations produit de tous les livres (P3)
Télécharger et enregistrer le fichier image de chaque page Produit que vous consultez (P4)
