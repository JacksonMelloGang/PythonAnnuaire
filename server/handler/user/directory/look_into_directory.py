from constants import USER_FOLDER, ERROR_TYPE, RESPONSE_OK_TYPE
from utils import read_files, convert_and_transmit_data

import os

def handle_look_directory_request(client_socket, data):
    annuaire_file_name = data["data"]["annuaire_content"].strip()
    username = data["data"]["username"].strip()

    shared_to_me_path = os.path.join(USER_FOLDER, username, "shared_to_me.txt")
    shared_to_me_content = read_files(shared_to_me_path)

    # check if user has same folder's name as the annuaire_file_name or if when reading shared_to_me user file, we don't find the name of the annuaire_content, throw error
    if(annuaire_file_name.split("_")[0] != username) and (annuaire_file_name.split("_")[0] not in shared_to_me_content):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": f"Erreur 243 - Vous n'avez pas la permission d'accéder à l'annuaire de {annuaire_file_name.split('_')[0]} !"})
        return

    # Access folder of asked user and check if {user}_annuaire.txt exists, if yes, read it and send it back
    user_folder_name = annuaire_file_name.split("_")[0]
    
    annuaire_path = os.path.join(USER_FOLDER, user_folder_name, f"{annuaire_file_name}.txt")
    print(annuaire_path)
    annuaire_content = read_files(annuaire_path)

    if annuaire_content is False:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": f"Fichier {user_folder_name} Non trouvé dans {USER_FOLDER}/{user_folder_name}"})
        return

    # If the file is empty, set annuaire_content to []
    if len(annuaire_content) == 0:
        annuaire_content = []

    convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"annuaire": annuaire_file_name, "contacts": annuaire_content})
