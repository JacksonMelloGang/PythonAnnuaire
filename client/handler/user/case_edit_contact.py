import time

from utils.constants import EDIT_CONTACT_TYPE, RESPONSE_OK_TYPE
from utils.contact.ask_contact import ask_server_annuaire_contacts
from utils.contact.ask_contact_info import ask_contact_information
from utils.display.list_contacts import list_contacts
from utils.utils import clear


def case_edit_contact(annuaire_name, client):
    # Modifier un contact
    contacts = ask_server_annuaire_contacts(client, annuaire_name)
    contact_index = 0

    if (contacts == False or len(contacts) == 0):
        print("Vous n'avez aucun contact dans votre annuaire")
        time.sleep(1)
        clear()
        return

    print("Voici les contacts dans votre annuaire:")
    list_contacts(contacts)

    # ask for contact index and check if valid
    try:
        contact_index = input("Veuillez entrer le numéro du contact à modifier: ")
        contact_index = int(contact_index) - 1

        # check if valid number
        if (contact_index < 0 or contact_index > len(contacts)):
            print("Invalid Number")
            print("Retour au menu.")
            time.sleep(1)
            clear()
            return

        # ask for new contact information
        contact = ask_contact_information()

        # send request to server
        client.convert_and_transmit_data(EDIT_CONTACT_TYPE,
                                         {"token": client.get_token(), "username": client.get_username(),
                                          "annuaire_name": annuaire_name, "contact_index": contact_index,
                                          "new_contact_info": contact})
        response = client.receive_and_convert_data()

        if (response["type"] == RESPONSE_OK_TYPE):
            print("Contact Modifié avec succès")
            time.sleep(1)
            clear()
        else:
            print("Une erreur est survenue lors de la modification du contact")
            print(response["data"]["message"])
            time.sleep(3)
            clear()

    except(Exception):
        print("Invalid Number")
        print("Retour au menu.")
        time.sleep(1)
        clear()
        return
