import os
import csv
import re
from datetime import date
from utils.cleaner import clean_filename

DATE_TODAY = date.today()

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
        phase1_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'phase1'))
        csv_path = os.path.join(phase1_dir, folder)
        os.makedirs(csv_path, exist_ok=True)

        clean_title = clean_filename(book_data['title'])
        csv_fieldname = f'{clean_title}_{DATE_TODAY}.csv'
        csv_file = os.path.join(csv_path, csv_fieldname)

        with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=book_data.keys(), delimiter=';')
            writer.writeheader()
            writer.writerow(book_data)
        print(f"\nLes données du livre : '{book_data['title']}' ont étaient exportées vers {csv_file}")
        return csv_fieldname
    except PermissionError:
        raise PermissionError(f"[ERREUR] Le fichier est déjà ouvert ailleurs (ex: Excel). Ferme-le pour pouvoir sauvegarder : {csv_path}")
    except Exception as e:
        print(f"[ERREUR] Impossible d'enregistrer le fichier CSV :\n-> {e}")


def save_category_to_csv(data_list, category_name):
    """
    Crée un dossier 'CSV' dans le dossier phase2 (s'il n'existe pas), 
    puis enregistre les données d'une catégorie de livres dans un fichier CSV.

    Args:
        data_list (list[dict[[str, any]]): Liste des dictionnaires contenant les données extraites des pages produit.
        category_name (str): Nom de la catégorie à utiliser pour nommer le fichier CSV.

    Raises:
        Exception: En cas d'erreur lors de la création du dossier ou de l'écriture du fichier CSV.
    """
    if not data_list:
        print("[INFO] Aucun livre à enregistrer.")
        return

    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        phase2_dir = os.path.join(project_root, 'phase2')
        csv_folder = os.path.join(phase2_dir, 'CSV')
        os.makedirs(csv_folder, exist_ok=True)

        csv_filename = f"products_category_{category_name}_{DATE_TODAY}.csv"
        csv_path = os.path.join(csv_folder, csv_filename)

        with open(csv_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data_list[0].keys(), delimiter=';')
            writer.writeheader()
            writer.writerows(data_list)

        print(f"[SAUVEGARDE] {len(data_list)} livres enregistrés dans : {csv_path}")
    except PermissionError:
        raise PermissionError(f"[ERREUR] Le fichier est déjà ouvert ailleurs (ex: Excel). Ferme-le pour pouvoir sauvegarder : {csv_path}")
    except Exception as e:
        print(f"[ERREUR] Échec lors de l'écriture du fichier CSV : {e}")


def save_all_categories_to_csv(all_books_data, category_name, base_dir):
    """
    Sauvegarde les données d'une catégorie de livres dans un fichier CSV,
    dans un dossier dédié à cette catégorie.

    Args:
        all_books_data (list[dict]): Liste des données extraites pour tous les livres d'une catégorie.
        category_name (str): Nom brut de la catégorie (sera nettoyé pour créer le dossier).
        base_fir (str): Chemin du répertoire de base où le dossier CSV sera créé 
                        (ex. : phase3, phase4, etc.).

    Raises:
        PermissionError: Si le fichier est déjà ouvert (ex : Excel) et ne peut pas être écrasé.
        Exception: En cas d'échec lors de la création du dossier ou de l'écriture du fichier.
    """
    if not all_books_data:
        print(f"[INFO] Aucun livre à enregistrer pour la catégorie '{category_name}'")
        return

    safe_category_name = re.sub(r'[^\w\s-]', '', category_name).strip().replace(' ', '_')
    category_folder = os.path.join(base_dir, "CSV", safe_category_name)
    os.makedirs(category_folder, exist_ok=True)

    filename = f"products_category_{safe_category_name}_{DATE_TODAY}.csv"
    csv_path = os.path.join(category_folder, filename)

    with open(csv_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_books_data[0].keys(), delimiter=';')
        writer.writeheader()
        writer.writerows(all_books_data)