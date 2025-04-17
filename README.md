# Système de Surveillance des Prix – Books Online

Ce projet a pour objectif de développer une version bêta d’un système de surveillance des prix pour Books Online. Il s’agit d’un script Python capable de scraper automatiquement l’ensemble des livres de toutes les catégories du site [Books to Scrape](http://books.toscrape.com/), d’en extraire diverses informations, puis de générer un fichier CSV par catégorie contenant les données collectées dans des dossiers organisés.
Le script télécharge également les images de couverture de chaque livre, qui sont enregistrées dans des sous-dossiers dédiés à chaque catégorie.


## Fonctionnalités

Le script extrait les données suivantes pour tous les produits de toutes les catégories du site :
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

Le script génère un dossier 'CSV', un sous-dossier par catégorie avec le nom de le catégorie et un sous-dossier 'Book_Cover'.

Le script enregistre les données extraites de toutes les pages produits de la catégorie dans un fichier CSV. 

Le fichier CSV est nommé selon le format suivant : 'products_category_nomcategorie_AAAA-MM-JJ.csv'.

Le script télécharge et enregistre l'image de couverture du livre dans le sous-dossier 'Book_Cover' et l'enregistre selon le format suivant : 'nom_du_livre.jpg'


## Prérequis

- Python 3.12.1 ou supérieur
- Les packages listés dans le fichier `requirements.txt`


## Installation

1. **Cloner le repository :**
    
    git clone https://github.com/NZT48DEV/Projet_2_Scraping.git

    cd Projet_2_Scraping


2. **Créer et activer un environnement virtuel (optionnel mais recommandé) :**
    
    python -m venv env

    source env/bin/activate  # Sur Linux/Mac

    env\Scripts\activate     # Sur Windows


3. **Installer les dépendances :**
    
    pip install -r requirements.txt


## Utilisation

1. **Exécuter le script de scraping :**
    
    python menu.py

    1 - Le script va se connecter à la page produit choisie, extraire les informations et écrire les données dans un fichier CSV.
    
    2 - Le script va se connecter à la catégorie choisie, extraire toutes les pages produits, puis, extraire les informations des produits et écrire les données dans un fichier CSV.

    3 - Le script va extraire automatiquement toutes les catégories du site, récupérer les livres de chaque catégorie et créer un fichier CSV par catégorie dans le dossier phase3/CSV/<nom_catégorie>/.


2. **Sélectionner la phase souhaitée dans le menu :**

```
    === MENU DU PROJET ===
    1 - Phase 1 : Scraper un livre
    2 - Phase 2 : Scraper une catégorie
    3 - Phase 3 : Scraper toutes les catégories
    4 - Phase 4 : Scraper toutes les catégories + télécharger les images de couverture
    0 - Quitter
```


## Structure du Projet

```
Projet_2_Scraping/
├── phase1/
│   ├── scraper.py                # Script de scraping d’un seul livre
│   └── CSV/                      # Dossier contenant les fichiers CSV exportés
│
├── phase2/
│   ├── scraper_category.py       # Script de scraping des livres d’une catégorie
│   └── CSV/                      # Dossier contenant les fichiers CSV exportés de la phase2
│
├── phase3/
│   ├── scraper_all_categories.py  # Script de scraping de toutes les catégories
│   └── CSV/                       # Répertoire contenant les sous-dossiers organisés par catégorie
│       └── Categorie/             # Sous-dossiers par catégorie, chacun contenant un fichier CSV
│
├── phase4/
│   ├── scraper_all.py            # Script de scraping de toutes les catégories : télécharge et enregistre les images de couverture des livres
│   └── CSV/                      # Répertoire contenant les sous-dossiers organisés par catégorie
│       └── Categorie/            # Sous-dossiers par catégorie, chacun contenant un fichier CSV et un dossier Book_Cover
│           └── Book_Cover/       # Dossier contenant les images de couverture téléchargées pour chaque catégorie
│
├── utils/
│   ├── cleaner.py                # Fonction pour nettoyer/normaliser les noms de fichiers
│   ├── saver.py                  # Fonctions pour sauvegarder les données dans des fichiers CSV
│
├── menu.py                       # Menu CLI pour naviguer entre les phases
├── requirements.txt              # Liste des dépendances à installer
├── README.md                     # Documentation du projet
└── .gitignore                    # Ignore .env, CSV, etc.


```


## Ressources Complémentaires
- Documentation Python : https://docs.python.org/3/
- Documentation Requests : https://requests.readthedocs.io/en/latest/
- Documentation BeautifulSoup : https://www.crummy.com/software/BeautifulSoup/bs4/doc/
