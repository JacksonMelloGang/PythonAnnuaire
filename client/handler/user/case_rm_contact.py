import time

from utils.constants import REMOVE_CONTACT_TYPE, RESPONSE_OK_TYPE
from utils.contact.ask_contact import ask_server_annuaire_contacts
from utils.display.list_contacts import list_contacts
from utils.utils import clear


def case_del_contact(client, annuaire_name):
    # Supprimer un contact
    contacts = ask_server_annuaire_contacts(client, annuaire_name)
    if (contacts == False):
        print("Vous n'avez aucun contact dans votre annuaire")
        time.sleep(1)
        clear()
        return

    print("Voici les contacts dans votre annuaire:")
    list_contacts(contacts)
    contact_index = 0

    # ask for contact index and check if valid
    try:
        contact_index = input("Veuillez entrer le numéro du contact à supprimer: ")
        contact_index = int(contact_index) - 1

        # check if valid number
        if (contact_index < 0 or contact_index > len(contacts)):
            print("Invalid Number")
            time.sleep(1)
            clear()
            return
    except(Exception):
        print("Invalid Number")
        print("Retour au menu.")
        time.sleep(1)
        clear()
        return

    client.convert_and_transmit_data(REMOVE_CONTACT_TYPE,
                                     {"token": client.get_token(), "username": client.get_username(),
                                      "annuaire_name": annuaire_name, "contact_index": contact_index})
    response = client.receive_and_convert_data()

    if (response["type"] == RESPONSE_OK_TYPE):
        print("Code 222 - Contact Supprimé avec succès")
        time.sleep(1)
        clear()
    else:
        print("Une erreur est survenue lors de la suppression du contact")
        print(response["data"]["message"])
        time.sleep(3)
        clear()
