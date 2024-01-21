import time

from client.utils.constants import ADD_CONTACT_TYPE, RESPONSE_OK_TYPE
from client.utils.contact.ask_contact_info import ask_contact_information
from client.utils.utils import clear


def case_add_contact(annuaire_name, client):
    # Ajouter un contact
    contact = ask_contact_information()
    client.convert_and_transmit_data(ADD_CONTACT_TYPE, {"token": client.get_token(), "username": client.get_username(),
                                                        "annuaire_name": annuaire_name, "contact": contact})
    response = client.receive_and_convert_data()
    if (response["type"] == RESPONSE_OK_TYPE):
        print("Contact Ajouté avec succès")
        time.sleep(1)
        clear()
    else:
        print("Une erreur est survenue lors de l'ajout du contact")
