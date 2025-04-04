def menu():
    """
    Affiche un menu interactif permettant de lancer différentes phases du projet.

    Options disponibles :
    1 - Phase 1 : Scraper un livre
    2 - Phase 2 : Scraper une catégorie
    0 - Quitter le programme

    L'utilisateur entre un numéro pour exécuter l'action correspondante.
    """
    while True:
        print("""
=== MENU DU PROJET ===
1 - Phase 1 : Scraper un livre
2 - Phase 2 : Scraper une catégorie
0 - Quitter
""")


        choix = input("Votre choix : ")

        if choix == '1':
            try:
                from phase1.scraper import main as phase1_main
                phase1_main()
            except Exception as e:
                print(f"[ERREUR] lors de l'exécution de la Phase 1 : {e}")
        elif choix =='2':
            try:
                from phase2.scraper_category import main as phase2_main
                phase2_main()
            except Exception as e:
                print(f"[ERREUR] lors de l'exécution de la Phase 2 : {e}")
        elif choix == '0':
            print("Fermeture du programme. À bientôt !")
            break
        else:
            print("Choix invalide, veuillez entrer un chiffre entre 0 et 2.")

if __name__ == '__main__':
    menu()
