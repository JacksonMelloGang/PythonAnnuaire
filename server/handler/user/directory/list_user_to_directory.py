import os

from constants import USER_FOLDER, ERROR_TYPE, RESPONSE_OK_TYPE
from utils import convert_and_transmit_data

# list users that have access to my directory
def handle_list_user_to_directory_request(client_socket, data):
    # check if  user directory exsists
    username = data["data"]["username"]
    user_folder = f"{USER_FOLDER}/{username}"

    # check if user_folder exists in user_files folder
    if not os.path.exists(f"{USER_FOLDER}/{username}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Erreur 215 - l'Utilisateur n'existe pas"})
        return

    # check if file shared_by_user.txt exists in user_folder, if not exists, throw error
    if not os.path.exists(f"{user_folder}/share_to_user.txt"):
        convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "share_to_user.txt not Found"})
        return

    try:
        # read shared_to_me.txt
        with open(f"{user_folder}/shared_to_me.txt", "r") as f:
            directories = f.readlines()
            directories = [directory.strip() for directory in directories]
            f.close()

        # if file is empty then send ok request
        if len(directories) == 0:
            convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "No User is sharing with you"})
            return

        # send directories
        convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"directories": directories})
    except Exception as e:
        print(f"An error occured: {e}")
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured, Please Try Again Later."})
        return
