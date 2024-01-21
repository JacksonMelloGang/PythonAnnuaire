import os

from constants import ERROR_TYPE, RESPONSE_OK_TYPE, USER_FOLDER
from utils import convert_and_transmit_data, edit_file


def handle_edit_contact_request(client_socket, data):
    if("contact_index" not in data["data"]):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Missing Contact Line Number or New Contact Info"})
        return

    # check if user has access to directory, if yes, edit contact in directory (edit entry in {user}_annuaire.txt)
    username = data["data"]["username"]
    contact_index = data["data"]["contact_index"]
    new_contact_info = data["data"]["new_contact_info"]

    # check if user_folder exists in user_files folder
    if not os.path.exists(f"{USER_FOLDER}/{username}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Erreur 215 - l'Utilisateur n'existe pas"})
        return

    # check if {user}_annuaire.txt exists in user_folder
    if not os.path.exists(f"{USER_FOLDER}/{username}/{username}_annuaire.txt"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": f"{username}_annuaire.txt Not Found in {USER_FOLDER}/{username}"})
        return

    # prepare new contact info to be written in {user}_annuaire.txt
    new_contact_info = f"{new_contact_info['name']},{new_contact_info['first_name']},{new_contact_info['email']},{new_contact_info['phone']},{new_contact_info['address']}"

    result = edit_file(f"{USER_FOLDER}/{username}/{username}_annuaire.txt", contact_index, new_contact_info)

    if result:
        convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "Contact Edited Successfully"})
    else:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured While Editing Contact"})
