import time

from utils.constants import EDIT_USER_TYPE, RESPONSE_OK_TYPE
from utils.utils import clear


def case_edit_user(client):
    # Edit User
    print("Modifier l'utilisateur")
    user_to_edit = input("Nom d'utilisateur: ")

    new_username = input("Nouveau nom d'utilisateur (laisser vide pour ne pas changer): ").strip()
    new_password = input("Nouveau mot de passe (laisser vide pour ne pas changer): ").strip()
    new_is_admin = input("Admin? (y/n): ").strip()

    if (new_is_admin == "y"):
        new_is_admin = True
    else:
        new_is_admin = False

    if (len(user_to_edit) == 0):
        print("Nom d'utilisateur invalide")
        time.sleep(2)
        clear()
        return

    if (user_to_edit == client.get_username()):
        print("Vous ne pouvez pas modifier votre propre compte")
        time.sleep(2)
        clear()
        return

    client.convert_and_transmit_data(EDIT_USER_TYPE, {"token": client.get_token(), "username": client.get_username(),
                                                      "user_to_edit": user_to_edit, "new_username": new_username,
                                                      "new_password": new_password, "new_is_admin": new_is_admin})
    request = client.receive_and_convert_data()
    if (request["type"] == RESPONSE_OK_TYPE):
        print("Utilisateur modifié avec succès")
    else:
        print("Une erreur est survenue lors de la modification de l'utilisateur")
        print(request["data"]["message"])

    time.sleep(2)
    clear()
