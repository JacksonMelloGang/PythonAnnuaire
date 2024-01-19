import socket
import json
import time

username = ""
password = ""
logged_in = False

class Client:

    def __init__(self):
        self.socket = None
        self.token = None
        self.connected = False
        self.user_connected = False

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
            json_content = json.load(content)
        except(Exception):
            print(f"Couldn't Convert Received Data {content}")
            
        return json_content

    def login(self, username, password):
        if(self.connected == False):
            print("You are not logged to the server")
            return self.user_connected

        if(self.user_connected == True):
            print("You are already logged in")
            return self.user_connected

        self.convert_and_transmit_data("CONNEXION", {"username": username, "password": password})
        response = self.receive_and_convert_data()
        if(response[type] == "CONNEXION_OK"):
            print("Identifiant Vérifié, Bienvenue.")

            self.token = response["token"]
            self.user_connected = True
        else:
            print("Identifiant invalide !")

        return self.user_connected


    def disconnect_from_server(self):
        if(self.connected == False):
            print("You are not logged to the server")
            return
        
        self.convert_and_transmit_data("DISCONNECT", {})
        response = self.receive_and_convert_data()
        if(response[type] == "DISCONNECT_OK"):
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
    
def ask_username():
    while(username == ""):
        username = input("Username: ")

def ask_password():
    while(password == ""):
        password = input("Password: ")

def ask_menu_choice():
    print("1. Afficher mon annuaire")
    print("2. Ajouter un contact")
    print("3. Supprimer un contact")
    print("4. Rechercher un contact")
    print("5. Quitter")

    choice = input("Choice: ")
    return choice

def ask_contact_information():
    print("Veuillez entrer les informations du contact")
    name = input("Nom: ")
    first_name = input("Prénom: ")
    phone = input("Téléphone: ")
    email = input("Email: ")
    contact = {"name": name, "first_name": first_name, "phone": phone, "email": email}
    
    return contact

def ask_annuaire_contacts(client, annuaire_name):
    client.convert_and_transmit_data("DATA_REQUEST", {"token": client.get_token(), "data": {"annaire": annuaire_name}})

def main():
    client = Client()
    client.establish_connection("localhost", 5555)

    if(client.get_connection_status() == False):
        print("Couldn't connect to the server")
        return


    # Connected to the server, now asking for credentials
    while(logged_in == False):
        ask_username()
        ask_password()

        logged_in = client.login(username, password)

        if(logged_in == False):
            print("Couldn't Log In, Try Again")
            return


    # Logged in, now displaying the menu and asking for user input    
    while True:

        # Displaying the menu
        choice = ask_menu_choice()
        match(choice):
            case 1:
                # Afficher mon annuaire
                client.convert_and_transmit_data("DATA_REQUEST", {"id": username, "token": client.get_token()})
                break
            case 2:
                # Ajouter un contact
                contact = ask_contact_information()

                client.convert_and_transmit_data("ADD_CONTACT", {"id": username, "token": client.get_token(), "contact": contact})
                break
            case 3:
                # Supprimer un contact

                break
            case 4:
                # Rechercher un contact

                break
            case 5:
                # Quitter
                break
            case _:
                print("Invalid Choice")
                break

if __name__ == "__main__":
    main()
