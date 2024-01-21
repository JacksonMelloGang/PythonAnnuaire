import os

from constants import USER_FOLDER, ERROR_TYPE, USER_INFO_TYPE
from utils import is_admin, convert_and_transmit_data


def handle_user_info_request(client_socket, data):
    # check if user is admin
    if not is_admin(data["data"]["username"]):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "You don't have admin rights"})
        return
    
    # check if user_files folder exists
    if not os.path.exists(USER_FOLDER):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "No User Found"})
        return
    
    # get name of every folder in ./user_files
    user_folders = os.listdir(USER_FOLDER)

    # check if username exists in user_files folder
    if data["data"]["looked_user"] not in user_folders:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Username Doesn't Exists"})
        return
    
    # send request with user info
    with open(f"{USER_FOLDER}/{data['data']['looked_user']}/user_info.txt", "r") as user_info_file:
        # while we don't reach the end of the file, we read the next line to check if it's "isAdmin=True"
        while True:
            next_line = user_info_file.readline()
            if not next_line:
                break
            if next_line == "isAdmin=True":
                convert_and_transmit_data(client_socket, USER_INFO_TYPE, {"user_info": {"username": data["data"]["looked_user"], "isAdmin": True}})
                return
        convert_and_transmit_data(client_socket, USER_INFO_TYPE, {"user_info": {"username": data["data"]["looked_user"], "isAdmin": False}})
        user_info_file.close()
