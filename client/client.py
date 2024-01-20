import socket
import json
import time
import os

# Constants, used to identify the type of request: (Directory = Annuaire)
CONNEXION_TYPE = "CONNEXION" # Provided => {"username": "username", "password": "password"}
DISCONNECT_TYPE = "DISCONNECT" # Provided => {}
DATA_REQUEST_TYPE = "DATA_REQUEST" # Provided => {"token": token, "data": {"annuaire": "directory_name"}}
ADD_CONTACT_TYPE = "ADD_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
EDIT_CONTACT_TYPE = "EDIT_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
REMOVE_CONTACT_TYPE = "REMOVE_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
SEARCH_CONTACT_TYPE = "SEARCH_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
LIST_DIRECTORIES_TYPE = "LIST_DIRECTORIES" # Provided => {"token": token, "data": {}}
ADD_USER_TO_DIRECTORY_TYPE = "ADD_USER_TO_DIRECTORY" # Provided => {"token": token, "data": {"annuaire": "directory_name", "username": "username"}}


ADD_USER_TYPE = "ADD_USER" # Provided => {"token": token, "data": {"username": "username", "password": "password"}}
REMOVE_USER_TYPE = "REMOVE_USER" # Provided => {"token": token, "data": {"username": "username", "password": "password"}}
EDIT_USER_TYPE = "EDIT_USER" # Provided => {"token": token, "data": {"username": "username", "password": "password"}}
LIST_USERS_TYPE = "LIST_USERS" # Provided => {"token": token, "data": {}}   

def clear():
    # if windows, use cls instead of clear
    if(os.name == "nt"):
        os.system("cls")
    else:
        os.system("clear")

class Client:

    def __init__(self):
        self.socket = None
        self.token = None
        self.connected = False
        self.user_connected = False
        self.is_admin = False

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
        print("Sent !")

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

# End Client Class

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

def ask_server_annuaire_contacts(client, annuaire_name):
    client.convert_and_transmit_data("DATA_REQUEST", {"token": client.get_token(), "data": {"annaire": annuaire_name}})
    response = client.receive_and_convert_data()
    # get data from request and display it with a number before each contact (1, 2, 3, ...)
    if(response["type"] == "DATA_REQUEST_OK"):
        contacts = response["data"]["contacts"]
        for index, contact in enumerate(contacts):
            print(f"{index + 1}. {contact['name']} {contact['first_name']} {contact['phone']} {contact['email']}")


def ask_menu_choice(min_max = (1, 5)):

    print("1. Afficher mon annuaire")
    print("2. Ajouter un contact")
    print("3. Supprimer un contact")
    print("4. Rechercher un contact")
    print("5. Quitter")

    choice = input("Choice: ")

    # While choice is not a valid number or is not in the range of min_max
    while(choice.isdigit() == False or int(choice) < min_max[0] or int(choice) > min_max[1]):
        print("Invalid Choice")
        ask_menu_choice()

    # Choice validated
    return choice

def ask_contact_information():
    print("Veuillez entrer les informations du contact")
    name = input("Nom: ")
    first_name = input("Prénom: ")
    phone = input("Téléphone: ")
    email = input("Email: ")
    contact = {"name": name, "first_name": first_name, "phone": phone, "email": email}
    
    return contact

def ask_admin_menu_choice(min_max = (1, 4)):
    clear()
    
    print("1. Ajouter un utilisateur")
    print("2. Supprimer un utilisateur")
    print("3. Modifier un utilisateur")
    print("4. Quitter")

    choice = input("Choice: ")
    while(choice.isdigit() == False or int(choice) < min_max[0] or int(choice) > min_max[1]):
        print("Invalid Choice")
        ask_admin_menu_choice()
    
    return choice
    


def main():
    # Global Variables
    username = ""
    password = ""
    logged_in = False
    
    client = Client()
    client.establish_connection("localhost", 5555)

    if(client.get_connection_status() == False):
        print("Couldn't connect to the server")
        return
    else:
        print("Successfully connected to the server")

    # Connected to the server, now asking for credentials
    while(logged_in == False):
        while(username == ""):
            username = input("Username: ")

        while(password == ""):
            password = input("Password: ")

        logged_in = client.login(username, password)

        if(logged_in == False):
            print("Couldn't Log In, Try Again")
        else:
            print("Logged In Successfully")
            logged_in = True


    # Logged in, now displaying the menu and asking for user input    
    while True:

        if(client.is_admin == True):
            # Displaying Admin menu
            user_input = ask_admin_menu_choice()

            match(user_input):
                case 1:
                    # Add User
                    client.convert_and_transmit_data(ADD_USER_TYPE, {"token": client.get_token(), "username": "username", "password": "password"})
                    break
                case 2:
                    # Delete User
                    client.convert_and_transmit_data(REMOVE_USER_TYPE, {"token": client.get_token(), "username": "username", "password": "password"})
                    break
                case 3:
                    # Edit User
                    client.convert_and_transmit_data(EDIT_USER_TYPE, {"token": client.get_token(), "username": username, "edited_user": "password"})
                    break
                case 4:
                    # Quit
                    client.convert_and_transmit_data(DISCONNECT_TYPE, {"token": client.get_token(), "username": username})
                    break
                case _:
                    print("Invalid Choice")
                    break



        else:
            # Displaying the menu
            user_input = ask_menu_choice((1, 5))
            annuaire_name = username + "_annuaire"
            match(user_input):
                case 1:
                    # Afficher mon annuaire
                    client.convert_and_transmit_data(DATA_REQUEST_TYPE, {"token": client.get_token(), "username": username, "annuaire_name": annuaire_name})
                    break
                case 2:
                    # Ajouter un contact
                    contact = ask_contact_information()

                    client.convert_and_transmit_data(ADD_CONTACT_TYPE, {"token": client.get_token(), "username": username, "annuaire_name": annuaire_name, "contact": contact})
                    break
                case 3:
                    # Supprimer un contact
                    ask_annuaire_contacts(client, annuaire_name)

                    client.convert_and_transmit_data(REMOVE_CONTACT_TYPE, {"token": client.get_token(), "username": username, "annuaire_name": annuaire_name, "contact_line": ""})

                    break
                case 4:
                    # Rechercher un contact

                    break
                case 5:
                    # Quitter
                    client.convert_and_transmit_data(DISCONNECT_TYPE, {"token": client.get_token(), "username": username})
                    break
                case _:
                    print("Invalid Choice")
                    break

if __name__ == "__main__":
    main()
