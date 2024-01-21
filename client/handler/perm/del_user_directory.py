import time

from utils.constants import REMOVE_USER_TO_DIRECTORY_TYPE
from utils.utils import clear


def case_remove_user_directory(client, annuaire_name):
    # Remove User from Directory
    user_to_remove = input("Nom d'utilisateur: ").strip()

    if (len(user_to_remove) == 0):
        print("Nom d'utilisateur invalide")
        time.sleep(2)
        clear()
        return

    # send request to server
    client.convert_and_transmit_data(REMOVE_USER_TO_DIRECTORY_TYPE,
                                     {"token": client.get_token(), "username": client.get_username(),
                                      "annuaire_name": annuaire_name, "user_to_remove": user_to_remove})
    response = client.receive_and_convert_data()
