import time

from utils.constants import REMOVE_USER_TYPE, RESPONSE_OK_TYPE
from utils.utils import clear


def case_del_user(client):
    # Delete User
    print("Supprimer l'utilisateur")
    user_to_delete = input("Nom d'utilisateur: ").strip()

    if (len(user_to_delete) == 0):
        print("Nom d'utilisateur invalide")
        time.sleep(2)
        clear()
        return

    if (user_to_delete == client.get_username()):
        print("Vous ne pouvez pas supprimer votre propre compte")
        time.sleep(2)
        clear()
        return

    client.convert_and_transmit_data(REMOVE_USER_TYPE, {"token": client.get_token(), "username": client.get_username(),
                                                        "user_to_delete": user_to_delete})
    request = client.receive_and_convert_data()
    if (request["type"] == RESPONSE_OK_TYPE):
        print("Utilisateur supprimé avec succès")
    else:
        print("Une erreur est survenue lors de la supression de l'utilisateur")
        print(request["data"]["message"])

    time.sleep(2)
    clear()
