from utils.utils import clear


def ask_admin_menu_choice(min_max=(1, 4)):
    clear()

    print("1. Ajouter un utilisateur")
    print("2. Supprimer un utilisateur")
    print("3. Modifier un utilisateur")
    print("4. Quitter")

    choice = input("Votre choix: ")

    try:
        int(choice)
    except(Exception):
        print("Invalid Number")
        ask_admin_menu_choice()

    if (int(choice) < min_max[0] or int(choice) > min_max[1]):
        print("Invalid Choice")
        ask_admin_menu_choice()

    return choice