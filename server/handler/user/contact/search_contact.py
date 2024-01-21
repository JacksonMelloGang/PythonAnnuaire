import os

from constants import USER_FOLDER, ERROR_TYPE, RESPONSE_OK_TYPE
from utils import convert_and_transmit_data


def handle_search_contact_request(client_socket, data):
    username = data["data"]["username"]
    annuaire_file_name = data["data"]["annuaire_name"]
    word_to_search = data["data"]["word_to_search"]
    found_lines = []

    # check if user_folder exists in user_files folder
    if not os.path.exists(f"{USER_FOLDER}/{username}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Erreur 215 - l'Utilisateur n'existe pas"})
        return

    # check if {user}_annuaire.txt exists in user_folder
    if not os.path.exists(f"{USER_FOLDER}/{username}/{username}_annuaire.txt"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": f"{username}_annuaire.txt Not Found in {USER_FOLDER}/{username}"})
        return

    # open file {user}_annuaire.txt and search for contact
    try:
        with open(f"{USER_FOLDER}/{username}/{annuaire_file_name}.txt", 'r') as annuaire_file:
            for ligne in annuaire_file:
                word_to_search = word_to_search.lower()
                ligne = ligne.lower()
                if word_to_search in ligne:
                    found_lines.append(ligne)

            if(len(found_lines) == 0):
                convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "No Contact Found"})
            else:
                convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "Contact Found", "contacts": found_lines})
    except Exception as e:
        print(f"An error occured while searching contact: {e}")
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured While Searching Contact"})
