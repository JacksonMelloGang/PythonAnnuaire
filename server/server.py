import socket
import threading
import os

import json
import secrets

user_folder = "./user_files"
valid_token = {}

def handle_login(client_socket, data):
    # Logique de gestion de la connexion
    username = data["login"]
    password = data["password"]

    result, token = authenticate_user(username, password)

    # Vérification des identifiants - À adapter en fonction de votre logique d'authentification
    if result == True:
        client_socket.send(json.dumps({"type": "CONNEXION_OK", "data": {"message": "Valid Credentials.", "token": token}})).encode('utf-8')
    else:
        client_socket.send(json.dumps({"type": "ERROR", "data": {"message": "Invalid Credentials"}}).encode('utf-8'))

def authenticate_user(username, password):
    # create./user_files folder if it doesn't exist
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # get name of every folder in ./user_files
    user_folders = os.listdir(user_folder)

    # check if username is in user_folders, check if file user_info.txt exists in it and if yes, access file user_info.txt to get password at first line
    if username in user_folders and os.path.exists(f"./user_files/{username}/user_info.txt"):
        with open(f"./user_files/{username}/user_info.txt", "r") as user_info_file:
            file_password = user_info_file.readline()

            if file_password == password:
                token = secrets.token_hex(16)
                valid_token[username] = token # store token in valid_token dict
                return True, token
            else:
                return False, None
    else:
        # create folder for user, and if user_info.txt doesn't exist, create it and write password in it
        os.makedirs(f"./user_files/{username}", exist_ok=True)
        with open(f"./user_files/{username}/user_info.txt", "w") as user_info_file:
            user_info_file.write(password)
        return False, None
    
        


def handle_disconnect(client_socket):
    # close the connection & invalid token
    client_socket.close()
    print(f"Connexion fermée avec {client_socket.getpeername()}")    

def handle_data_request(client_socket, data):
    pass

def handle_client(client_socket):
    json_data = None
    request_type = None

    # Affiche l'adresse IP du client
    print(f"Connexion acceptée de {client_socket.getpeername()} - IP: {client_socket.getpeername()[0]}")

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

        match(request_type):
            case "CONNEXION":
                handle_login(client_socket, json_data["data"])
            case "DISCONNECT":
                handle_disconnect(client_socket)
            case "DATA_REQUEST":
                handle_data_request(client_socket, json_data)
            case _:
                client_socket.send(json.dumps({"type": "ERROR", "data": {"message": "Requête non valide"}}).encode('utf-8'))

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
    
if __name__ == "__main__":
    start_server()
