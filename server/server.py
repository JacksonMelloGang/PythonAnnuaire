import socket
import threading
import os

import json
import secrets

USER_FOLDER = "./user_files"
valid_token = {}

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


def convert_and_transmit_data(client_socket, request_type, data):
    try:
        request = {"type": request_type, "data": data}            
        client_socket.send(json.dumps(request).encode('utf-8'))
        print(f"Sending Request: {request_type} to {client_socket.getpeername()}")
    except Exception as e:
        print("An Unknow Error Has Occured while sending request")
        print(e)


def receive_and_convert_data(client_socket):
    json_content = False

    content = client_socket.recv(1024).decode('utf-8')
    try:
        json_content = json.loads(content)
    except(Exception):
        print(f"Couldn't convert received data:\n{content}")
    return json_content

def create_new_user_folder(username, password, is_user_admin = False):
    try:
        # create folder for user, and if user_info.txt doesn't exist, create it and write password in it
        os.makedirs(f"{USER_FOLDER}/{username}", exist_ok=True)
        with open(f"{USER_FOLDER}/{username}/user_info.txt", "w") as user_info_file:
            user_info_file.write(password)
            user_info_file.write("\n")
            user_info_file.write(f"isAdmin={is_user_admin}")
            user_info_file.close()
        # create username_annuaire.txt in user folder
        with open(f"{USER_FOLDER}/{username}/{username}_annuaire.txt", "w") as user_annuaire_file:
            user_annuaire_file.write("")
            user_annuaire_file.close()
            return True
    except Exception as e:
        print(f"An error occured while creating new user folder: {e}")
        return False
        

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
        return False, None

    # get name of every folder in ./user_files
    user_folders = os.listdir(USER_FOLDER)

    # check if username is in user_folders, check if file user_info.txt exists in it and if yes, access file user_info.txt to get password at first line
    if username in user_folders and os.path.exists(f"{USER_FOLDER}/{username}/user_info.txt"):
        with open(f"{USER_FOLDER}/{username}/user_info.txt", "r") as user_info_file:
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

def is_admin(username):
    # check with username if he has admin rights in user_info.txt
    if os.path.exists(f"{USER_FOLDER}/{username}/user_info.txt"):
        with open(f"{USER_FOLDER}/{username}/user_info.txt", "r") as user_info_file:
            # while we don't reach the end of the file, we read the next line to check if it's "isAdmin=True"
            while True:
                next_line = user_info_file.readline()
                if not next_line:
                    break
                if next_line == "isAdmin=True":
                    return True

def handle_disconnect(client_socket):
    # close the connection & invalidate token
    client_socket.close()
    print(f"Connexion fermée avec {client_socket.getpeername()}")    
 

def handle_user_list_request(client_socket, data):
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

    # send request with user list
    convert_and_transmit_data(client_socket, LIST_USERS_TYPE, {"user_list": user_folders})

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

def read_files(path):
    lines = []

    if os.path.exists(f"{path}"):
            with open(f"{path}", "r") as annuaire_file:
                # separate each line of the file in an array []
                lines = annuaire_file.readlines()
                for i in range(len(lines)):
                    # remove \n at the end of each line
                    lines[i] = lines[i].replace("\n", "")
                annuaire_file.close()
    else:
        print(f"File {path} doesn't exists")
        lines = False

    return lines

def edit_file(path, line, content):
    try:
        lines = read_files(path)
        lines[line - 1] = content
        with open(f"{path}", "w") as annuaire_file:
            annuaire_file.writelines(lines)
            annuaire_file.close()
            return True
    except Exception as e:
        print(f"An error occured while editing file: {e}")
        return False


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
        
    
 
def handle_add_contact_request(client_socket, data):
    username = data["data"]["username"]

    if("contact" not in data["data"]):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Missing Contact Info"})
        return
    
    if("name" not in data["data"]["contact"] or "first_name" not in data["data"]["contact"] or "email" not in data["data"]["contact"] or "phone" not in data["data"]["contact"] or "address" not in data["data"]["contact"]):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Missing Contact Info"})
        return

    # check if user_folder exists in user_files folder
    if not os.path.exists(f"{USER_FOLDER}/{username}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Username Doesn't Exists"})
        return
    
    # check if {user}_annuaire.txt exists in user_folder
    if not os.path.exists(f"{USER_FOLDER}/{username}/{username}_annuaire.txt"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": f"{username}_annuaire.txt Not Found in {USER_FOLDER}/{username}"})
        return
    
    try: 
        # open {user}_annuaire.txt and append contact to it
        with open(f"{USER_FOLDER}/{username}/{username}_annuaire.txt", "a") as annuaire_file:
            contact = data["data"]["contact"]
            annuaire_file.write(f"{contact['name']},{contact['first_name']},{contact['email']},{contact['phone']},{contact['address']}\n")
            annuaire_file.close()

            convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "Contact Added Successfully"})
    except Exception as e:
        print(f"An error occured while adding contact: {e}")
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured While Adding Contact"})    

def handle_edit_contact_request(client_socket, data):
    if("contact_index" not in data["data"] or "new_contact_info" not in data["data"]):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Missing Contact Line Number or New Contact Info"})
        return

    # check if user has access to directory, if yes, edit contact in directory (edit entry in {user}_annuaire.txt)
    username = data["data"]["username"]
    contact_index = data["data"]["contact_index"]
    new_contact_info = data["data"]["new_contact_info"]

    # check if user_folder exists in user_files folder
    if not os.path.exists(f"{USER_FOLDER}/{username}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Username Doesn't Exists"})
        return
    
    # check if {user}_annuaire.txt exists in user_folder
    if not os.path.exists(f"{USER_FOLDER}/{username}/{username}_annuaire.txt"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": f"{username}_annuaire.txt Not Found in {USER_FOLDER}/{username}"})
        return
    
    result = edit_file(f"{USER_FOLDER}/{username}/{username}_annuaire.txt", contact_index, new_contact_info)

    if(result):
        convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "Contact Edited Successfully"})
    else:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured While Editing Contact"})


def handle_remove_contact_request(client_socket, data):
    if("contact_index" not in data["data"]):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Missing Contact Line Number or New Contact Info"})
        return

    # check if user has access to directory, if yes, edit contact in directory (edit entry in {user}_annuaire.txt)
    username = data["data"]["username"]
    contact_index = data["data"]["contact_index"]
    new_contact_info = data["data"]["new_contact_info"]

    # check if user_folder exists in user_files folder
    if not os.path.exists(f"{USER_FOLDER}/{username}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Username Doesn't Exists"})
        return
    
    # check if {user}_annuaire.txt exists in user_folder
    if not os.path.exists(f"{USER_FOLDER}/{username}/{username}_annuaire.txt"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": f"{username}_annuaire.txt Not Found in {USER_FOLDER}/{username}"})
        return
    
    result = edit_file(f"{USER_FOLDER}/{username}/{username}_annuaire.txt", contact_index, new_contact_info)

    if(result):
        convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "Contact Edited Successfully"})
    else:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured While Editing Contact"})


def handle_search_contact_request(client_socket, data):
    pass

def handle_list_directories_request(client_socket, data):
    pass

def handle_add_user_to_directory_request(client_socket, data):
    pass

def handle_add_user_request(client_socket, data):
    # check if username already exists in user_files folder
    if os.path.exists(f"{USER_FOLDER}/{data['data']['new_user']}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Username Already Exists"})
        return
    
    # create new user folder
    success = create_new_user_folder(data["data"]["new_user"], data["data"]["new_password"])
    if(success):
        convert_and_transmit_data(client_socket, ADD_USER_TYPE, {"message": "User Created Successfully"})
    else:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured While Creating User"})

def handle_remove_user_request(client_socket, data):
    # check if username exists in user_files folder
    if not os.path.exists(f"{USER_FOLDER}/{data['data']['username']}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Username Doesn't Exists"})
        return
    
    # remove user folder
    try:
        os.remove(f"{USER_FOLDER}/{data['data']['username']}")
        convert_and_transmit_data(client_socket, REMOVE_USER_TYPE, {"message": "User Removed Successfully"})
    except Exception as e:
        print(f"An error occured while removing user folder: {e}")
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured While Removing User"})

def handle_edit_user_request(client_socket, data):
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
    
    # remove user folder
    try:
        os.remove(f"{USER_FOLDER}/{user_to_delete}")
        convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "User Removed Successfully"})
    except Exception as e:
        print(f"An error occured while removing user folder: {e}")
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured While Removing User"})

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
            match(request_type):
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
                    request = convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Invalid Request"})
                    client_socket.send(request)

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
