import socket
import json
import time

from handler.admin.add_user import case_add_user
from handler.admin.delete_user import case_del_user
from handler.admin.edit_user import case_edit_user
from handler.perm.add_user_directory import case_add_user_directory
from handler.perm.del_user_directory import case_remove_user_directory
from handler.perm.list_permission import case_list_permission
from handler.user.case_add_contact import case_add_contact
from handler.user.case_edit_contact import case_edit_contact
from handler.user.case_list_contact import case_list_contact
from handler.user.case_rm_contact import case_del_contact
from handler.user.case_search_contact import case_search_contact
from utils.disconnect import disconnect

from utils.display.display_admin_menu import ask_admin_menu_choice
from utils.display.display_perm_menu import ask_permission_menu
from utils.display.display_user_menu import ask_menu_choice
from utils.utils import clear


class Client:

    def __init__(self):
        self.socket = None
        self.token = None
        self.connected = False
        self.user_connected = False
        self.is_admin = False
        self.username = None

    def establish_connection(self, addr, port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((addr, port))
            self.connected = True
        except(Exception):
            print("An Unknow Error has occured while logging to server")
            self.connected = False
        
    def convert_and_transmit_data(self, request_type, data):
        if(self.connected == False):
            print("You are not logged to the server")
            return

        try:
            request = {"type": request_type, "data": data}            
            self.socket.send(json.dumps(request).encode('utf-8'))
        except(Exception):
            print("An Unknow Error Has Occured while sending request")
        

    def receive_and_convert_data(self):
        json_content = False

        if(self.connected == False):
            print("You are not logged to the server")
            return

        content = self.socket.recv(1024).decode('utf-8')
        try:
            json_content = json.loads(content)
        except(Exception):
            print(f"Couldn't convert received data:\n{content}")
            
        return json_content

    def login(self, username, password):
        # Check if we opened a channel with the server
        if(self.connected == False):
            print("You are not logged to the server")
            return self.user_connected

        # Check if we are already logged in
        if(self.user_connected == True):
            print("You are already logged in")
            return self.user_connected

        self.convert_and_transmit_data("CONNEXION", {"username": username, "password": password})
        response = self.receive_and_convert_data() # get the response from the server

        # if we get a response and type response["type"] exists and is equal to CONNEXION_OK, we validate the login :)
        if(response and "type" in response and response["type"] == "CONNEXION_OK"):
            print("Identifiant Vérifié, Bienvenue.")
            time.sleep(1)
            clear()

            self.token = response["data"]["token"]
            self.username = username
            self.user_connected = True
            
            if(response["data"]["isAdmin"] == True):
                self.is_admin = True
        else:
            print(f"An Unknow error occured : {response['data']['message']}")

        return self.user_connected


    def disconnect_from_server(self):
        if(self.connected == False):
            print("You are not logged to the server")
            return
        
        self.convert_and_transmit_data("DISCONNECT", {})
        response = self.receive_and_convert_data()
        if(response["type"] == "DISCONNECT_OK"):
            print("Déconnecté avec succès")
        else:
            print("Une erreur est survenue lors de la déconnexion")

    ###############################################################
    #               GETTERS & SETTERS                             #
    ###############################################################

    def get_socket(self):
        return self.socket

    def get_token(self):
        return self.token

    def get_connection_status(self):
        return self.connected
    
    def is_user_connected(self):
        return self.user_connected
    
    def is_admin(self):
        return self.is_admin
    
    def get_username(self):
        return self.username

# End Client Class

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################


def main():
    # Global Variables
    username = ""
    password = ""
    logged_in = False
    
    client = Client()
    client.establish_connection("localhost", 5555)

    if(client.get_connection_status() == False):
        print("Erreur 101 - Connexion Impossible avec le serveur")
        return
    else:
        print("Connexion Réussie")

    # Connected to the server, now asking for credentials
    while(logged_in == False):
        while(username == ""):
            username = input("Username: ").strip()

        while(password == ""):
            password = input("Password: ").strip()

        logged_in = client.login(username, password)

        if(logged_in == False):
            print("Couldn't Log In, Try Again")
            return
        else:
            print("Logged In Successfully")
            logged_in = True


    # Logged in, now displaying the menu and asking for user input    
    while True:
        if(client.is_admin == True):
            # Displaying Admin menu
            user_input = ask_admin_menu_choice()

            match(int(user_input)):
                case 1:
                    case_add_user(client)
                case 2:
                    case_del_user(client)
                case 3:
                    case_edit_user(client)
                case 4:
                    disconnect(client)
                    break
                case _:
                    print("Invalid Choice")
                    
        else:
            # Display user menu
            user_input = ask_menu_choice((1, 7))
            annuaire_name = username + "_annuaire"
            match(int(user_input)):
                case 1:
                    case_list_contact(annuaire_name, client)
                case 2:
                    case_add_contact(annuaire_name, client)
                case 3:
                    case_del_contact(annuaire_name, client)
                case 4:
                    case_edit_contact(annuaire_name, client)
                case 5:
                    case_search_contact(annuaire_name, client)
                case 6:
                    # Gérer les permissions de mon annuaire
                    # Displaying permission menu
                    user_input = ask_permission_menu((1, 4))
                    match(int(user_input)):
                        case 1:
                            case_list_permission(client, annuaire_name)
                        case 2:
                            case_add_user_directory(client, annuaire_name)
                        case 3:
                            case_remove_user_directory(client, annuaire_name)
                        case 4:
                            disconnect(client)
                            break
                case 7:
                    disconnect(client)
                    break

                case _:
                    print("Invalid Choice")


if __name__ == "__main__":
    try:
        main()
    except(KeyboardInterrupt):
        print("Exiting...")
        exit(0)
    except(ConnectionResetError):
        print("Erreur 100 - Connexion Perdue")
        exit(1)
    except Exception as e:
        print("An Unknow Error Has Occured \n")
        print(e)
        exit(1)
