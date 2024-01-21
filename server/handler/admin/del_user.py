import os
import shutil

from constants import USER_FOLDER, ERROR_TYPE, RESPONSE_OK_TYPE
from utils import convert_and_transmit_data


def handle_remove_user_request(client_socket, data):
    user_to_delete = data['data']['user_to_delete']
    username = data['data']['username']

    # check if username exists in user_files folder
    if not os.path.exists(f"{USER_FOLDER}/{user_to_delete}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Erreur 215 - l'Utilisateur N'existe Pas"})
        return

    if(user_to_delete == username):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Vous ne pouvez pas vous auto-supprimer"})
        return

    # remove user folder
    try:
        shutil.rmtree(f"{USER_FOLDER}/{user_to_delete}")
        convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "Code 211 - Utilisateur Supprimé Avec Succès"})
    except Exception as e:
        print(f"An error occured while removing user folder: {e}")
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Une Erreur Est Survenue Lors de la Suppression de l'Utilisateur"})
