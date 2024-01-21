import time

from utils.constants import LIST_USER_TO_DIRECTORY_TYPE, RESPONSE_OK_TYPE
from utils.contact.ask_contact import ask_server_annuaire_contacts
from utils.display.list_contacts import list_contacts
from utils.utils import clear


def case_list_contact(annuaire_name, client):
    # Display list of directory the user has access to
    client.convert_and_transmit_data(LIST_USER_TO_DIRECTORY_TYPE,
                                     {"token": client.get_token(), "username": client.get_username(),
                                      "annuaire_name": annuaire_name})
    response = client.receive_and_convert_data()

    # if no directories shared, only display his own
    if response["type"] == RESPONSE_OK_TYPE:
        if "directories" not in response["data"]:
            print("Vous n'avez aucun annuaire partagé avec vous, affichage du votre.")
            time.sleep(2)
            clear()

            annuaire_name = f"{client.get_username()}_annuaire"
            contacts = ask_server_annuaire_contacts(client, annuaire_name)

            if contacts != False and len(contacts) > 0:
                clear()
                print("Voici les contacts dans votre annuaire:")
                list_contacts(contacts)
                print("=====================================")
            elif contacts:
                print("Vous n'avez aucun contact dans votre annuaire")
                time.sleep(1)
                clear()
            else:
                print("Une erreur est survenue lors de la demande des contacts")
                time.sleep(1)
                clear()
        else:
            print("Voici les annuaires auquel vous y avez accès:")

            print(f"Votre annuaire: {client.get_username()}")
            for directory in response["data"]["directories"]:
                print(f"Annuaire de: {directory}")

                annuaire_target = input("Ecrivez le nom de la personne pour afficher son annuaire: ").strip()
                annuaire_name = f"{annuaire_target}_annuaire"

                # Display directory contacts
                contacts = ask_server_annuaire_contacts(client, annuaire_name)

                if not contacts:
                    print("Vous n'avez aucun contact dans votre annuaire")
                    time.sleep(1)
                    clear()
                else:
                    clear()
                    print("Voici les contacts dans l'annuaire:")
                    list_contacts(contacts)
                    print("=====================================")
    else:
        print("Une erreur est survenue lors de la demande des permissions")
        print(response["data"]["message"])
        time.sleep(3)
        clear()
