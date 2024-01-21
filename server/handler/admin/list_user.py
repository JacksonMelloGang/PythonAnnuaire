import os

from constants import ERROR_TYPE, USER_FOLDER, LIST_USERS_TYPE
from handler.login import verify_token
from utils import convert_and_transmit_data, is_admin


def handle_user_list_request(client_socket, data):
    verify_token_result = verify_token(data["data"]["username"], data["data"]["token"])

    if(not verify_token_result):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Username/Token Mismatch, Please Login Again."})
        return

    # check if user is admin
    if not is_admin(data["data"]["username"]):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Erreur 243 - Vous n'êtes pas autorisé à effectuer cette action"})
        return
    
    # check if user_files folder exists
    if not os.path.exists(USER_FOLDER):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Erreur 215 - l'Utilisateur n'existe pas"})
        return
    
    # get name of every folder in ./user_files
    user_folders = os.listdir(USER_FOLDER)

    # send request with user list
    convert_and_transmit_data(client_socket, LIST_USERS_TYPE, {"message": "Code 213 - Listage des utilisateur réussis", "user_list": user_folders})
