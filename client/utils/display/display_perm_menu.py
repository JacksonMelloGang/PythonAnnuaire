from utils.utils import clear


def ask_permission_menu(min_max = (1, 4)):
    clear()

    print("1. Lister les utilisateurs ayant accès a mon annuaire")
    print("2. Ajouter un utilisateur à mon annuaire")
    print("3. Supprimer un utilisateur de mon annuaire")
    print("4. Quitter")

    choice = input("Votre choix: ")

    try:
        int(choice)
    except(Exception):
        print("Invalid Number")
        ask_permission_menu()

    if(int(choice) < min_max[0] or int(choice) > min_max[1]):
        print("Invalid Choice")
        ask_permission_menu()

    return choice
