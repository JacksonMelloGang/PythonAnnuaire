import time

from utils.constants import LIST_USER_TO_DIRECTORY_TYPE, RESPONSE_OK_TYPE
from utils.utils import clear


def case_list_permission(client, annuaire_name):
    # List permissions
    client.convert_and_transmit_data(LIST_USER_TO_DIRECTORY_TYPE,
                                     {"token": client.get_token(), "username": client.get_username(),
                                      "annuaire_name": annuaire_name})
    response = client.receive_and_convert_data()
    if (response["type"] == RESPONSE_OK_TYPE):
        print(response)
        if ("directories" not in response["data"]):
            print("Vous n'avez partagé l'accès à votre annuaire avec personne.")
            time.sleep(2)
            clear()
            return
        else:
            print("Voici les utilisateurs ayant accès à votre annuaire:")
            for index, directory in enumerate(response["data"]["directories"]):
                print(f"{index+1}: {directory}")
                print("=====================================")
    else:
        print("Une erreur est survenue lors de la demande des permissions")
        print(response["data"]["message"])
        time.sleep(3)
        clear()
