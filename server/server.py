import socket
import threading
import os

import json
import secrets

user_folder = "./user_files"
valid_token = {}

# Received Constants, used to identify the type of request: (Directory = Annuaire)
CONNEXION_TYPE = "CONNEXION" # Provided => {"username": "username", "password": "password"}
DISCONNECT_TYPE = "DISCONNECT" # Provided => {}
DATA_REQUEST_TYPE = "DATA_REQUEST" # Provided => {"token": token, "data": {"annuaire_content": "directory_name"}} # NOTE: "annuaire_content" can also be "user_list" or "user_info"
ADD_CONTACT_TYPE = "ADD_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
EDIT_CONTACT_TYPE = "EDIT_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
REMOVE_CONTACT_TYPE = "REMOVE_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
SEARCH_CONTACT_TYPE = "SEARCH_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
LIST_DIRECTORIES_TYPE = "LIST_DIRECTORIES" # Provided => {"token": token, "data": {}}
ADD_USER_TO_DIRECTORY_TYPE = "ADD_USER_TO_DIRECTORY" # Provided => {"token": token, "data": {"annuaire": "directory_name", "username": "username"}}


ADD_USER_TYPE = "ADD_USER" # Provided => {"token": token, "data": {"username": "username", "password": "password"}}
REMOVE_USER_TYPE = "REMOVE_USER" # Provided => {"token": token, "data": {"username": "username", "password": "password"}}
EDIT_USER_TYPE = "EDIT_USER" # Provided => {"token": token, "data": {"username": "username", "password": "password"}}

# Sent Constants, used to identify the type of request: (Directory = Annuaire)
CONNEXION_OK_TYPE = "CONNEXION_OK" # Provided => {"message": "Valid Credentials", "token": token}
DISCONNECT_OK_TYPE = "DISCONNECT_OK" # Provided => {"message": "Disconnected Successfully"}
DATA_REQUEST_OK_TYPE = "DATA_REQUEST_OK" # Provided => {"data": {"annuaire": "directory_name", "contacts": [{"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}, ...]}}
ERROR_TYPE = "ERROR" # Provided => {"message": "Error Message"}

def convert_and_transmit_data(client_socket, request_type, data):
    try:
        request = {"type": request_type, "data": data}            
        client_socket.socket.send(json.dumps(request).encode('utf-8'))
    except(Exception):
        print("An Unknow Error Has Occured while sending request")
    print("Sent !")

def receive_and_convert_data(client_socket):
    json_content = False

    content = client_socket.socket.recv(1024).decode('utf-8')
    try:
        json_content = json.loads(content)
    except(Exception):
        print(f"Couldn't convert received data:\n{content}")
    return json_content

def create_new_user_folder(username, password):
        # create folder for user, and if user_info.txt doesn't exist, create it and write password in it
        os.makedirs(f"./user_files/{username}", exist_ok=True)
        with open(f"./user_files/{username}/user_info.txt", "w") as user_info_file:
            user_info_file.write(password)

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
        request = convert_and_transmit_data(client_socket, CONNEXION_OK_TYPE, {"message": "Valid Credentials", "token": token, "isAdmin": is_admin})
        client_socket.send(request)
    else:
        request = convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Invalid Credentials"})
        client_socket.send(request)

def authenticate_user(username, password):
    # create./user_files folder if it doesn't exist where is the program is executed    
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
        return False, None

    # get name of every folder in ./user_files
    user_folders = os.listdir(user_folder)

    # check if username is in user_folders, check if file user_info.txt exists in it and if yes, access file user_info.txt to get password at first line
    if username in user_folders and os.path.exists(f"./user_files/{username}/user_info.txt"):
        with open(f"./user_files/{username}/user_info.txt", "r") as user_info_file:
            file_password = user_info_file.readline()

            if file_password == password:
                token = secrets.token_hex(16)
                valid_token[username] = token # store token in valid_token dict

                # check if user is admin by checking the next line and look if there is "isAdmin=True"
                is_admin = False
                next_line = user_info_file.readline()
                if next_line == "isAdmin=True":
                    is_admin = True

                return True, token, is_admin
            else:
                return False, None
    else:
        return False, None
    
def verify_token(username, token):
    if username in valid_token and valid_token[username] == token:
        return True
    else:
        return False


def handle_disconnect(client_socket):
    # close the connection & invalidate token
    client_socket.close()
    print(f"Connexion fermée avec {client_socket.getpeername()}")    

def handle_annuaire_content_request(client_socket, data):
    pass

def handle_user_list_request(client_socket, data):
    pass

def handle_user_info_request(client_socket, data):
    pass

def handle_add_contact_request(client_socket, data):
    pass

def handle_edit_contact_request(client_socket, data):
    pass

def handle_remove_contact_request(client_socket, data):
    pass

def handle_search_contact_request(client_socket, data):
    pass

def handle_list_directories_request(client_socket, data):
    pass

def handle_add_user_to_directory_request(client_socket, data):
    pass

def handle_add_user_request(client_socket, data):
    pass

def handle_remove_user_request(client_socket, data):
    pass

def handle_edit_user_request(client_socket, data):
    pass

def handle_data_request(client_socket, data):
    # We have 3 type of data request, so we match the type of data request to each case, and we handle the request
    request_type = data["data"]
    match(request_type):
        case "annuaire_content":
            handle_annuaire_content_request(client_socket, data)
        case "user_list":
            handle_user_list_request(client_socket, data)
        case "user_info":
            handle_user_info_request(client_socket, data) 

def handle_client(client_socket):
    json_data = None
    request_type = None

    # Affiche l'adresse IP du client
    print(f"Accepted Connection from {client_socket.getpeername()} - IP: {client_socket.getpeername()[0]}")

    # Loop to get and send back data
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            client_socket.send(json.dumps({"type": "ERROR", "data": {"message": "Format JSON invalide"}}).encode('utf-8'))
            continue

        if(json_data is None):
            print(f"Couldn't Convert Received Data from {client_socket.getpeername()}")
            return
        
        request_type = json_data["type"]

        if(request_type is None):
            print(f"Invalid Data Type from {client_socket.getpeername()} \nReceived Data Type: {request_type}\nFull Data:\n {json_data}")
            return

        # match is equivalent of switch case in python
        match(request_type):
            case "CONNEXION":
                handle_login(client_socket, json_data["data"])
            case "DISCONNECT":
                handle_disconnect(client_socket)
            case "DATA_REQUEST":
                handle_data_request(client_socket, json_data)
            case "ADD_CONTACT":
                handle_add_contact_request(client_socket, json_data)
            case "EDIT_CONTACT":
                handle_edit_contact_request(client_socket, json_data)
            case "REMOVE_CONTACT":
                handle_remove_contact_request(client_socket, json_data)
            case "SEARCH_CONTACT":
                handle_search_contact_request(client_socket, json_data)
            case "LIST_DIRECTORIES":
                handle_list_directories_request(client_socket, json_data)
            case "ADD_USER_TO_DIRECTORY":
                handle_add_user_to_directory_request(client_socket, json_data)


            case "ADD_USER":
                handle_add_user_request(client_socket, json_data)
            case "REMOVE_USER":
                handle_remove_user_request(client_socket, json_data)
            case "EDIT_USER":
                handle_edit_user_request(client_socket, json_data)

                    
            case _: # default case
                request = convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Invalid Request"})
                client_socket.send(request)

        # Traitement des données (dans cet exemple, simplement les renvoyer)
        client_socket.send(data)

    # Close client socket when logout (we are in TCP channel, so we need to close the socket to close the connection)
    client_socket.close()
    print(f"Connexion fermée avec {client_socket.getpeername()}")


def start_server():
    host = 'localhost'
    port = 5555

    # define socket as a tcp ip socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to the host and port
    server_socket.bind((host, port))

    # listen for incoming connections (5)
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, _ = server_socket.accept()
            
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
            print("User Aborted Program, Server shutting down...")
    except Exception as e:
        print(f"An error occured: {e}")
    finally:
        server_socket.close()
        exit(0)
    
if __name__ == "__main__":
    start_server()
