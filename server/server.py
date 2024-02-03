import socket
import threading
import os

from constants import USER_FOLDER, CONNEXION_TYPE, ERROR_TYPE
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
from handler.user.directory.add_user_directory import handle_add_user_to_directory_request
from handler.user.directory.list_user_to_directory import handle_list_user_to_directory_request
from handler.user.directory.look_into_directory import handle_look_directory_request
from handler.user.directory.rm_user_directory import handle_remove_user_from_directory_request
from utils import convert_and_transmit_data, receive_and_convert_data

# create USER_FOLDER if it doesn't exist
if not os.path.exists(USER_FOLDER):
    try:
        os.makedirs(USER_FOLDER)
        # create default folder with name: admin, a user_info.txt in it with password at first line and isAdmin=True at 2nd line
        os.makedirs(f"{USER_FOLDER}/admin")
        with open(f"{USER_FOLDER}/admin/user_info.txt", "w") as f:
            f.write("password\n")
            f.write("isAdmin=True\n")
            f.close()
    except Exception as e:
        print(f"Couldn't Create {USER_FOLDER} Folder, Please Check Permissions and Try Again.")
        print(e)
        exit(1)

# list directory user has access to
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

                case "LOOK_DIRECTORY": # list contact of his own directory
                    handle_look_directory_request(client_socket, json_data)
                case "ADD_CONTACT":
                    handle_add_contact_request(client_socket, json_data)
                case "EDIT_CONTACT":
                    handle_edit_contact_request(client_socket, json_data)
                case "REMOVE_CONTACT":
                    handle_remove_contact_request(client_socket, json_data)
                case "SEARCH_CONTACT":
                    handle_search_contact_request(client_socket, json_data)

                case "LIST_USER_TO_DIRECTORY": # list directory accesible to users
                    handle_list_user_to_directory_request(client_socket, json_data)
                case "ADD_USER_TO_DIRECTORY":
                    handle_add_user_to_directory_request(client_socket, json_data)
                case "REMOVE_USER_TO_DIRECTORY":
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
