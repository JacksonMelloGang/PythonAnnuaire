import os

from constants import ERROR_TYPE, USER_FOLDER, RESPONSE_OK_TYPE
from utils import convert_and_transmit_data, remove_line


def handle_remove_contact_request(client_socket, data):
    if("contact_index" not in data["data"]):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Missing Contact Line Number or New Contact Info"})
        return

    # check if user has access to directory, if yes, edit contact in directory (edit entry in {user}_annuaire.txt)
    username = data["data"]["username"]
    contact_index = data["data"]["contact_index"]

    # check if user_folder exists in user_files folder
    if not os.path.exists(f"{USER_FOLDER}/{username}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Erreur 215 - l'Utilisateur n'existe pas"})
        return

    # check if {user}_annuaire.txt exists in user_folder
    if not os.path.exists(f"{USER_FOLDER}/{username}/{username}_annuaire.txt"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": f"{username}_annuaire.txt Not Found in {USER_FOLDER}/{username}"})
        return

    remove_line(f"{USER_FOLDER}/{username}/{username}_annuaire.txt", contact_index)

    convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "Contact Successfully Edited"})
