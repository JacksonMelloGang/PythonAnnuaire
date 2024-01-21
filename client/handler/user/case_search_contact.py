import time

from utils.constants import SEARCH_CONTACT_TYPE, RESPONSE_OK_TYPE
from utils.contact.ask_contact import ask_server_annuaire_contacts
from utils.display.list_contacts import list_contacts
from utils.utils import clear


def case_search_contact(annuaire_name, client):
    # Rechercher un contact
    contacts = ask_server_annuaire_contacts(client, annuaire_name)
    if (contacts == False):
        print("Vous n'avez aucun contact dans votre annuaire")
        time.sleep(1)
        clear()
        return

    print("Voici les contacts dans votre annuaire:")
    list_contacts(contacts)

    word_to_search = input("Veuillez entrer le nom du contact à rechercher: ").strip()

    # send request to server
    client.convert_and_transmit_data(SEARCH_CONTACT_TYPE,
                                     {"token": client.get_token(), "username": client.get_username(),
                                      "annuaire_name": annuaire_name, "word_to_search": word_to_search})
    response = client.receive_and_convert_data()

    if (response["type"] == RESPONSE_OK_TYPE):
        if ("contacts" in response["data"]):
            clear()
            print("Voici les contacts trouvés:")
            list_contacts(response["data"]["contacts"])
            print("=====================================")
        else:
            print("Aucun contact trouvé")
    else:
        print("Une erreur est survenue lors de la recherche du contact")
        print(response["data"]["message"])
        time.sleep(3)
        clear()
