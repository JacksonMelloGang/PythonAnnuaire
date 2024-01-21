import socket
import threading
import os

from handler.admin.add_user import handle_add_user_request
from handler.admin.del_user import handle_remove_user_request
from handler.admin.edit_user import handle_edit_user_request
from handler.admin.list_user import handle_user_list_request
from handler.disconnect import handle_disconnect
from handler.login import verify_token, handle_login
from handler.user.contact.add_contact import handle_add_contact_request
from handler.user.contact.edit_contact import handle_edit_contact_request
from handler.user.contact.remove_contact import handle_remove_contact_request
from handler.user.contact.search_contact import handle_search_contact_request
from utils import read_files, is_admin, convert_and_transmit_data, receive_and_convert_data

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

USER_FOLDER = os.path.join(SCRIPT_DIRECTORY, "user_files")
valid_token = {}

# create USER_FOLDER if it doesn't exist
if not os.path.exists(USER_FOLDER):
    os.makedirs(USER_FOLDER)

# Received Constants, used to identify the type of request: (Directory = Annuaire)
CONNEXION_TYPE = "CONNEXION" # Provided => {"username": "username", "password": "password"}
DISCONNECT_TYPE = "DISCONNECT" # Provided => {}

# Directory
LOOK_DIRECTORY = "LOOK_DIRECTORY" # Provided => {"token": token, "data": {"annuaire": "directory_name"}}
ADD_CONTACT_TYPE = "ADD_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
EDIT_CONTACT_TYPE = "EDIT_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
REMOVE_CONTACT_TYPE = "REMOVE_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
SEARCH_CONTACT_TYPE = "SEARCH_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}

# Share Directory
LIST_DIRECTORIES_TYPE = "LIST_DIRECTORIES" # Provided => {"token": token, "data": {}}
LIST_USER_TO_DIRECTORY_TYPE = "LIST_USER_TO_DIRECTORY"
ADD_USER_TO_DIRECTORY_TYPE = "ADD_USER_TO_DIRECTORY" # Provided => {"token": token, "data": {"annuaire": "directory_name", "username": "username"}}
REMOVE_USER_TO_DIRECTORY_TYPE = "REMOVE_USER_TO_DIRECTORY" # Provided => {"token": token, "data": {"annuaire": "directory_name", "username": "username"}}

# Admin
LIST_USERS_TYPE = "LIST_USERS" # Provided => {"token": token, "data": {}}
USER_INFO_TYPE = "USER_INFO" # Provided => {"token": token, "data": {"username": "username", "looked_user": "looked_user"}}
ADD_USER_TYPE = "ADD_USER" # Provided => {"token": token, "data": {"username": "username", "password": "password"}}
REMOVE_USER_TYPE = "REMOVE_USER" # Provided => {"token": token, "data": {"username": "username", "password": "password"}}
EDIT_USER_TYPE = "EDIT_USER" # Provided => {"token": token, "data": {"username": "username", "password": "password"}}

# Sent Constants, used to identify the type of request: (Directory = Annuaire)
CONNEXION_OK_TYPE = "CONNEXION_OK" # Provided => {"message": "Valid Credentials", "token": token}
DISCONNECT_OK_TYPE = "DISCONNECT_OK" # Provided => {"message": "Disconnected Successfully"}
RESPONSE_OK_TYPE = "RESPONSE_OK" # Provided => {"data": {"annuaire": "directory_name", "contacts": [{"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}, ...]}}
ERROR_TYPE = "ERROR" # Provided => {"message": "Error Message"}


def handle_look_directory_request(client_socket, data):
    annuaire_file_name = data["data"]["annuaire_content"]
 
    # Access folder of asked user and check if {user}_annuaire.txt exists, if yes, read it and send it back
    user_folder_name = annuaire_file_name.split("_")[0]

    annuaire_content = read_files(f"{USER_FOLDER}/{user_folder_name}/{annuaire_file_name}.txt")

    if annuaire_content is  False:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": f"{user_folder_name}_annuaire.txt Not Found in {USER_FOLDER}/{user_folder_name}"})
        return
    
    # If the file is empty, set annuaire_content to []
    if len(annuaire_content) == 0:
        annuaire_content = []

    convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"annuaire": annuaire_file_name, "contacts": annuaire_content})


def handle_list_directories_request(client_socket, data):
    pass

def handle_list_user_to_directory_request(client_socket, data):
    # check if it's his directory
    username = data["data"]["username"]

    # check if user_folder exists in user_files folder
    if not os.path.exists(f"{USER_FOLDER}/{username}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Username Doesn't Exists"})
        return
    


    
    pass

def handle_add_user_to_directory_request(client_socket, data):
    pass

def handle_remove_user_from_directory_request(client_socket, data):
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
    user_to_delete = data["data"]["user_to_delete"]

    # check if username exists in user_files folder
    if user_to_delete not in user_folders:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": f"Username {user_to_delete} Doesn't Exists"})
        return
    
    pass


def handle_client(client_socket):
    json_data = None
    request_type = None

    # Affiche l'adresse IP du client
    print(f"Accepted Connection from {client_socket.getpeername()} - IP: {client_socket.getpeername()[0]}")

    # Loop to get and send back data
    while True:
        json_data = receive_and_convert_data(client_socket)
        if not json_data:
            break

        if(json_data is None):
            print(f"Couldn't Convert Received Data from {client_socket.getpeername()}")
            return
            
        request_type = json_data["type"]

        if(request_type is None):
            print(f"Invalid Data Type from {client_socket.getpeername()} \nReceived Data Type: {request_type}\nFull Data:\n {json_data}")
            return

        if(request_type == CONNEXION_TYPE):
            handle_login(client_socket, json_data["data"])
        else:
            # verify if token and username exists
            if("username" not in json_data["data"] or "token" not in json_data["data"]):
                convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Missing Token/Username"})
                return

            verify_token_result = verify_token(json_data["data"]["username"], json_data["data"]["token"])

            # Middleware, so unless we trying to connect, we verify the token sistematically
            if not verify_token_result:
                convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Username/Token Mismatch, Please Login Again."})
                client_socket.close()
                print(f"Connexion fermée avec {client_socket.getpeername()}")
                return
            #########################################################################################

            # match is equivalent of switch case in python
            print(f"Received Request Type: {request_type} from {client_socket.getpeername()}")
            match request_type:
                case "DISCONNECT":
                    handle_disconnect(client_socket)

                case "LOOK_DIRECTORY":
                    handle_look_directory_request(client_socket, json_data)
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
                case "LIST_USER_TO_DIRECTORY":
                    handle_list_user_to_directory_request(client_socket, json_data)
                case "ADD_USER_TO_DIRECTORY":
                    handle_add_user_to_directory_request(client_socket, json_data)
                case "REMOVE_USER_TO_DIRECTORY_TYPE":
                    handle_remove_user_from_directory_request(client_socket, json_data)

                case "LIST_USERS":
                    handle_user_list_request(client_socket, json_data)
                case "ADD_USER":
                    handle_add_user_request(client_socket, json_data)
                case "REMOVE_USER":
                    handle_remove_user_request(client_socket, json_data)
                case "EDIT_USER":
                    handle_edit_user_request(client_socket, json_data)
                            
                case _: # default case
                    print(f"Invalid Request from {client_socket.getpeername()}")
                    convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Invalid Request"})


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
