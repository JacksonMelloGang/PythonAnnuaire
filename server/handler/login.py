import json
import os
import secrets

from constants import ERROR_TYPE, CONNEXION_OK_TYPE, USER_FOLDER, valid_token
from utils import convert_and_transmit_data

def handle_login(client_socket, data):
    # check if username and password are in data
    if "username" not in data or "password" not in data:
        request = convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Missing Credentials"})
        client_socket.send(json.dumps(request).encode('utf-8'))
        return

    # Logique de gestion de la connexion
    username = data["username"]
    password = data["password"]

    result, token, is_admin = authenticate_user(username, password)

    # Vérification des identifiants - À adapter en fonction de votre logique d'authentification
    if result == True:
        convert_and_transmit_data(client_socket, CONNEXION_OK_TYPE, {"message": "Valid Credentials", "token": token, "isAdmin": is_admin})
    else:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Invalid Credentials"})


def authenticate_user(username, password):
    # create./user_files folder if it doesn't exist where is the program is executed
    if not os.path.exists(USER_FOLDER):
        os.makedirs(USER_FOLDER)
        return False, None, False

    # get name of every folder in ./user_files
    user_folders = os.listdir(USER_FOLDER)

    # check if username is in user_folders, check if file user_info.txt exists in it and if yes, access file user_info.txt to get password at first line
    if username in user_folders and os.path.exists(f"{USER_FOLDER}/{username}/user_info.txt"):
        with open(f"{USER_FOLDER}/{username}/user_info.txt", "r") as user_info_file:
            # get first line of user_info.txt and compare it with password
            file_password = user_info_file.readline().strip()

            if file_password == password:
                token = secrets.token_hex(16)
                valid_token[username] = token # store token in valid_token dict
                is_admin = False

                # check if user is admin by checking the next line and look if there is "isAdmin=True"
                next_line = user_info_file.readline().strip()
                if next_line == "isAdmin=True":
                    is_admin = True

                return True, token, is_admin
            else:
                return False, None, False
    else:
        return False, None, None


def verify_token(username, token):
    if username in valid_token and valid_token[username] == token:
        return True
    else:
        return False
