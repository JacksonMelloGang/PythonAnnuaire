def ask_menu_choice(min_max=(1, 7)):
    print("1. Afficher un annuaire")
    print("2. Ajouter un contact")
    print("3. Supprimer un contact")
    print("4. Modifier un contact")
    print("5. Rechercher un contact")
    print("6. Gérer les permissions de mon annuaire")
    print("7. Quitter")

    choice = input("Votre choix: ").strip()

    # While choice is not a valid number or is not in the range of min_max
    try:
        int(choice)
    except(Exception):
        print("Invalid Number")
        ask_menu_choice()

    if (int(choice) < min_max[0] or int(choice) > min_max[1]):
        print("Invalid Choice")
        ask_menu_choice()

    # Choice validated
    return choice

