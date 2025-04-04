# Système de Surveillance des Prix – Books Online

Ce projet a pour objectif de développer une version bêta d’un système de surveillance des prix pour Books Online. Il s’agit d’un script Python capable de scraper l’ensemble des livres d’une catégorie sur le site [Books to Scrape](http://books.toscrape.com/) et en extrait diverses informations afin de générer un fichier CSV contenant les données collectées.


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
    
    python menu.py

    Le script va se connecter à la page produit choisie, extraire les informations et écrire les données dans un fichier CSV.


2. **Sélectionner la phase souhaitée dans le menu :**

```
    === MENU DU PROJET ===
    1 - Phase 1 : Scraper un livre
    2 - Phase 2 : Scraper une catégorie
    0 - Quitter
```


3. **Vérifier le fichier CSV généré :**

    Les données extraites sont automatiquement exportées dans un fichier CSV situé dans le dossier phase2/CSV/.


## Structure du Projet

```
Projet_2_OC_v2/
├── phase1/
│   ├── scraper.py           # Script de scraping d’un seul livre
│   └── CSV/                 # Dossier contenant les fichiers CSV exportés de la phase1
├── phase2/
│   ├── scraper_category.py  # Script de scraping des livres d’une catégorie
│   └── CSV/                 # Dossier contenant les fichiers CSV exportés de la phase2
├── menu.py                  # Menu CLI pour naviguer entre les phases
├── requirements.txt         # Liste des dépendances à installer
├── README.md                # Documentation du projet
└── .gitignore               # Ignore .env, CSV, etc.
```

## Ressources Complémentaires
- Documentation Python : https://docs.python.org/3/
- Documentation Requests : https://requests.readthedocs.io/en/latest/
- Documentation BeautifulSoup : https://www.crummy.com/software/BeautifulSoup/bs4/doc/


## Remarques

Ce projet constitue une première version (bêta) et pourra être amélioré avec des fonctionnalités supplémentaires telles que :

- L'extraction des données de toutes les catégories et les informations produit de tous les livres (P3)
- Télécharger et enregistrer le fichier image de chaque page Produit que vous consultez (P4)
