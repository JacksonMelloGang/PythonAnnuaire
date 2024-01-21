import os
import shutil

from constants import USER_FOLDER, ERROR_TYPE
from utils import convert_and_transmit_data


def handle_remove_user_request(client_socket, data):
    user_to_delete = data['data']['user_to_delete']
    username = data['data']['username']

    # check if username exists in user_files folder
    if not os.path.exists(f"{USER_FOLDER}/{user_to_delete}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Username Doesn't Exists"})
        return

    if(user_to_delete == username):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "You can't delete yourself"})
        return

    # remove user folder
    try:
        shutil.rmtree(f"{USER_FOLDER}/{user_to_delete}")
        convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "User Removed Successfully"})
    except Exception as e:
        print(f"An error occured while removing user folder: {e}")
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured While Removing User"})
