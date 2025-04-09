# Système de Surveillance des Prix – Books Online

Ce projet a pour objectif de développer une version bêta d’un système de surveillance des prix pour Books Online. Il s’agit d’un script Python capable de scraper automatiquement l’ensemble des livres de toutes les catégories du site [Books to Scrape](http://books.toscrape.com/), d’en extraire diverses informations, puis de générer un fichier CSV par catégorie contenant les données collectées dans des dossiers organisés.

Depuis la phase 4, le script télécharge également les images de couverture de chaque livre, qui sont enregistrées dans des sous-dossiers dédiés à chaque catégorie.


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

    1 - Le script va se connecter à la page produit choisie, extraire les informations et écrire les données dans un fichier CSV.
    
    2 - Le script va se connecter à la catégorie choisie, extraire toutes les pages produits, puis, extraire les informations des produits et écrire les données dans un fichier CSV.

    3 - Le script va extraire automatiquement toutes les catégories du site, récupérer les livres de chaque catégorie et créer un fichier CSV par catégorie dans le dossier phase3/CSV/<nom_catégorie>/.

    4 - Le script effectue les mêmes opérations que la phase 3, et télécharge également les images de couverture de chaque livre dans phase4/CSV/<nom_catégorie>/Book_Cover/.
    

2. **Sélectionner la phase souhaitée dans le menu :**

```
    === MENU DU PROJET ===
    1 - Phase 1 : Scraper un livre
    2 - Phase 2 : Scraper une catégorie
    3 - Phase 3 : Scraper toutes les catégories
    4 - Phase 4 : Scraper toutes les catégories + télécharger les images de couverture
    0 - Quitter
```


3. **Vérifier le fichier CSV généré :**

    Les données extraites sont automatiquement exportées dans un fichier CSV situé dans le dossier phase3/CSV/<nom_catégorie>/.


## Structure du Projet

```
Projet_2_OC_v2/
├── phase1/
│   ├── scraper.py                # Script de scraping d’un seul livre
│   └── CSV/                      # Dossier contenant les fichiers CSV exportés
│
├── phase2/
│   ├── scraper_category.py       # Script de scraping des livres d’une catégorie
│   └── CSV/                      # Dossier contenant les fichiers CSV exportés de la phase2
│
├── phase3/
│   ├── scraper_all_categories.py # Script de scraping de toutes les catégories
│   └── CSV/                      # Dossiers organisés par catégorie contenant les fichiers CSV
│
├── phase4/
│   ├── scraper_all_categories.py # Script de scraping de toutes les catégories + Télécharge/Enregistre les images de couvertures des livres
│   └── CSV/                      # Dossiers organisés par catégorie
│       └── Book_Cover/           # Dossier contenant les images de couvertures téléchargées
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


## Remarques

Ce projet comporte les fonctionnalités suivantes :

- L'extraction des données pour un livre (P1)
- L'extraction des données pour toute une catégorie de livre (P2)
- L'extraction des données de toutes les catégories et les informations produit de tous les livres (P3)
- Scraper toutes les catégories + Télécharge et enregistre le fichier image de couverture de chaque page Produit que vous consultez (P4)

