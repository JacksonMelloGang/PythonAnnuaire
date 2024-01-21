import os

from constants import USER_FOLDER, ERROR_TYPE, RESPONSE_OK_TYPE
from utils import convert_and_transmit_data


def handle_remove_user_from_directory_request(client_socket, data):
    # check if user_files folder exists
    if not os.path.exists(USER_FOLDER):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "No User Found"})
        return

    if "user_to_remove" not in data["data"]:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Missing User To Remove"})

    # get name of every folder in ./user_files
    user_folders = os.listdir(USER_FOLDER)
    target = data["data"]["user_to_remove"]
    username = data["data"]["username"]

    # check if username exists in user_files folder
    if target not in user_folders:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": f"Username {target} Doesn't Exists"})
        return

    target_folder = f"{USER_FOLDER}/{target}"
    user_folder = f"{USER_FOLDER}/{username}"

    # check if file shared_to_me.txt exists in target folder, if not exists, throw error
    if not os.path.exists(f"{target_folder}/shared_to_me.txt"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "shared_to_me.txt not Found"})
        return

    # check if file share_to_user.txt exists in target folder, if not exists, throw error
    if not os.path.exists(f"{target_folder}/share_to_user.txt"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "share_to_user.txt not Found"})
        return

    try:
        # read shared_to_me.txt
        with open(f"{target_folder}/shared_to_me.txt", "r") as f:
            directories = f.readlines()
            directories = [directory.strip() for directory in directories]
            f.close()

        # remove user from shared_to_me.txt
        with open(f"{target_folder}/shared_to_me.txt", "w") as f:
            for directory in directories:
                if directory != data["data"]["username"]:
                    f.write(f"{directory}\n")
            f.close()

        # read share_to_user.txt
        with open(f"{user_folder}/share_to_user.txt", "r") as f:
            directories = f.readlines()
            directories = [directory.strip() for directory in directories]
            f.close()

        # remove user from share_to_user.txt
        with open(f"{user_folder}/share_to_user.txt", "w") as f:
            for directory in directories:
                if directory != target:
                    f.write(f"{target}\n")
            f.close()

        # send directories
        convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": f"User {target} Removed from {data['data']['username']} Directory"})
    except Exception as e:
        print(f"An error occured: {e}")
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured, Please Try Again Later."})
        return
