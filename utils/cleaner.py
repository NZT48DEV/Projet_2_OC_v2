import re

def clean_filename(title, max_length=50):
    """
    Nettoie un titre pour qu'il soit utilisable comme nom de fichier.

    Args:
        title (str): Le titre à nettoyer
        max_length (int, optional): Longueur maximale du nom retourné (50 par défaut)

    Returns:
        str: Le titre nettoyé et formaté.
    """
    title = re.sub(r'[^\w\s-]', '', title)
    title = title.strip().replace(' ', '_')
    return title[:max_length]
