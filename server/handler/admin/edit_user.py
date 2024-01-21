import os

from constants import USER_FOLDER, ERROR_TYPE, RESPONSE_OK_TYPE
from utils import is_admin, convert_and_transmit_data, edit_file


def handle_edit_user_request(client_socket, data):
    username = data['data']['username']
    user_to_edit = data['data']['user_to_edit']

    new_username = data['data']['new_username']
    new_password = data['data']['new_password']
    new_user_admin = data['data']['new_is_admin']

    if(not is_admin(username)):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Erreur 243 - Vous n'êtes pas autorisé à effectuer cette action"})
        return

    # check if username exists in user_files folder
    if not os.path.exists(f"{USER_FOLDER}/{user_to_edit}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Erreur 215 - l'Utilisateur n'existe pas"})
        return

    try:
        # rename folder with new username
        os.rename(f"{USER_FOLDER}/{user_to_edit}", f"{USER_FOLDER}/{new_username}")
        # rename annuaire_file.txt
        os.rename(f"{USER_FOLDER}/{new_username}/{user_to_edit}_annuaire.txt", f"{USER_FOLDER}/{new_username}/{new_username}_annuaire.txt")

        # edit user_info.txt and change first line with new password
        try:
            with open(f"{USER_FOLDER}/{new_username}/user_info.txt", "r") as user_info_file:
                lines = user_info_file.readlines()
                lines[0] = new_password
                lines[1] = f"isAdmin={new_user_admin}"
                user_info_file.close()

                edit_file(f"{USER_FOLDER}/{new_username}/user_info.txt", 0, lines[0])
                edit_file(f"{USER_FOLDER}/{new_username}/user_info.txt", 1, lines[1])
        except Exception as e:
            print(f"An error occured while editing user_info.txt: {e}")
            convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured While Editing User"})
            return

        convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "User Edited Successfully"})
    except Exception as e:
        print(f"An error occured while editing user folder: {e}")
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured While Removing User"})
