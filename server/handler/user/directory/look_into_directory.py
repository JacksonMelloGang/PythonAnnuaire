from constants import USER_FOLDER, ERROR_TYPE, RESPONSE_OK_TYPE
from utils import read_files, convert_and_transmit_data

import os

def handle_look_directory_request(client_socket, data):
    annuaire_file_name = data["data"]["annuaire_content"]

    # Access folder of asked user and check if {user}_annuaire.txt exists, if yes, read it and send it back
    user_folder_name = annuaire_file_name.split("_")[0]
    annuaire_path = os.path.join(USER_FOLDER, user_folder_name, f"{annuaire_file_name}_annuaire.txt")

    annuaire_content = read_files(annuaire_path)

    if annuaire_content is False:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": f"{user_folder_name}_annuaire.txt Not Found in {USER_FOLDER}/{user_folder_name}"})
        return

    # If the file is empty, set annuaire_content to []
    if len(annuaire_content) == 0:
        annuaire_content = []

    convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"annuaire": annuaire_file_name, "contacts": annuaire_content})
