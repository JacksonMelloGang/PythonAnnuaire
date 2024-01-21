import time

from utils.constants import ADD_USER_TO_DIRECTORY_TYPE, RESPONSE_OK_TYPE
from utils.utils import clear


def case_add_user_directory(client, annuaire_name):
    # Add User from Directory
    user_to_add = input("Nom d'utilisateur: ").strip()

    if (len(user_to_add) == 0):
        print("Nom d'utilisateur invalide")
        time.sleep(2)
        clear()
        return

    # send request to server
    client.convert_and_transmit_data(ADD_USER_TO_DIRECTORY_TYPE,
                                     {"token": client.get_token(), "username": client.get_username(),
                                      "annuaire_name": annuaire_name, "user_to_add": user_to_add})
    response = client.receive_and_convert_data()

    if (response["type"] == RESPONSE_OK_TYPE):
        print("Utilisateur ajouté avec succès")
        time.sleep(1)
        clear()
    else:
        print("Une erreur est survenue lors de l'ajout de l'utilisateur")
        print(response["data"]["message"])
        time.sleep(3)
        clear()
