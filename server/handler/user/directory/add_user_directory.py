import os

from constants import USER_FOLDER, ERROR_TYPE, RESPONSE_OK_TYPE
from utils import convert_and_transmit_data


def handle_add_user_to_directory_request(client_socket, data):
    # check if  user directory exsists
    username = data["data"]["username"]
    target_username = data["data"]["user_to_add"]

    # check if username and target_username exists in user_files folder
    if not os.path.exists(f"{USER_FOLDER}/{username}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Username Doesn't Exists"})
        return
    if not os.path.exists(f"{USER_FOLDER}/{target_username}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Target Doesn't Exists"})
        return

    # check if file shared_by_user.txt exists in user_folder, if not exists, throw error
    if not os.path.exists(f"{USER_FOLDER}/{target_username}/shared_to_me.txt"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "shared_to_me.txt of target not Found"})
        return

    if not os.path.exists(f"{USER_FOLDER}/{username}/share_to_user.txt"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "share_to_user.txt of user not Found"})
        return

    # check if target is not already in shared_to_me.txt
    with open(f"{USER_FOLDER}/{target_username}/shared_to_me.txt", "r") as f:
        directories = f.readlines()
        directories = [directory.strip() for directory in directories]
        f.close()

    if username in directories:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Target is already in shared_to_me.txt"})
        return

    # check if targetis not already in share_to_user.txt
    with open(f"{USER_FOLDER}/{username}/share_to_user.txt", "r") as f:
        directories2 = f.readlines()
        directories2 = [directory.strip() for directory in directories2]
        f.close()

    if target_username in directories:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Target is already in shared_to_me.txt"})
        return

    try:
        with open(f"{USER_FOLDER}/{target_username}/shared_to_me.txt", "a") as f:
            f.write(f"{username}\n")
            f.close()

        with open(f"{USER_FOLDER}/{username}/share_to_user.txt", "a") as f:
            f.write(f"{target_username}\n")
            f.close()

        convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": f"User {target_username} Added to {username} Directory"})

    except Exception as e:
        print(f"An error occured: {e}")
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured, Please Try Again Later."})
        return
