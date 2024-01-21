import time

from utils.constants import LOOK_DIRECTORY, ERROR_TYPE, RESPONSE_OK_TYPE


def ask_server_annuaire_contacts(client, annuaire_name):
    client.convert_and_transmit_data(LOOK_DIRECTORY, {"token": client.get_token(), "username": client.get_username(),
                                                      "annuaire_content": annuaire_name})
    response = client.receive_and_convert_data()

    if (response["type"] == ERROR_TYPE):
        print("Une erreur est survenue lors de la demande des contacts")
        print(response["data"]["message"])
        time.sleep(30)
        return False  # Empty List

    # get data from request and display it with a number before each contact (1, 2, 3, ...)
    if (response["type"] == RESPONSE_OK_TYPE):
        contacts = response["data"]["contacts"]

        if (len(contacts) == 0):
            print("Vous n'avez aucun contact dans votre annuaire")
            return False

        return contacts
