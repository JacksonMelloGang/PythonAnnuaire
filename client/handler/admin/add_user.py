import time

from utils.constants import ADD_USER_TYPE, RESPONSE_OK_TYPE
from utils.utils import clear


def case_add_user(client):
    # Add User
    new_username = input("Nom d'utilisateur: ").strip()
    new_password = input("Mot de passe: ").strip()
    new_user_admin = input("Admin? (y/n): ").strip()
    if (new_user_admin == "y"):
        new_user_admin = True
    else:
        new_user_admin = False
    client.convert_and_transmit_data(ADD_USER_TYPE, {"token": client.get_token(), "username": client.get_username(),
                                                     "new_username": new_username, "new_password": new_password,
                                                     "new_user_admin": new_user_admin})
    request = client.receive_and_convert_data()
    if (request["type"] == RESPONSE_OK_TYPE):
        print("Utilisateur ajouté avec succès")
    else:
        print("Une erreur est survenue lors de la création de l'utilisateur")
        print(request["data"]["message"])
    time.sleep(2)
    clear()
