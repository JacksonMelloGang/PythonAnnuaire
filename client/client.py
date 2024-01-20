import socket
import json
import time
import os

# Received Constants, used to identify the type of request: (Directory = Annuaire)
CONNEXION_TYPE = "CONNEXION" # Provided => {"username": "username", "password": "password"}
DISCONNECT_TYPE = "DISCONNECT" # Provided => {}

# Directory
LOOK_DIRECTORY = "LOOK_DIRECTORY" 
ADD_CONTACT_TYPE = "ADD_CONTACT" 
EDIT_CONTACT_TYPE = "EDIT_CONTACT" 
REMOVE_CONTACT_TYPE = "REMOVE_CONTACT"
SEARCH_CONTACT_TYPE = "SEARCH_CONTACT"

# Share Directory
LIST_DIRECTORIES_TYPE = "LIST_DIRECTORIES" 
LIST_USERS_DIRECTORY_TYPE = "LIST_USERS_DIRECTORY"
ADD_USER_TO_DIRECTORY_TYPE = "ADD_USER_TO_DIRECTORY" 
REMOVE_USER_TO_DIRECTORY_TYPE = "REMOVE_USER_TO_DIRECTORY"

# Admin
LIST_USERS_TYPE = "LIST_USERS"
USER_INFO_TYPE = "USER_INFO" 
ADD_USER_TYPE = "ADD_USER" 
REMOVE_USER_TYPE = "REMOVE_USER" 
EDIT_USER_TYPE = "EDIT_USER" 

# Sent Constants, used to identify the type of request: (Directory = Annuaire)
CONNEXION_OK_TYPE = "CONNEXION_OK" # Provided => {"message": "Valid Credentials", "token": token}
DISCONNECT_OK_TYPE = "DISCONNECT_OK" 
RESPONSE_OK_TYPE = "RESPONSE_OK" 
ERROR_TYPE = "ERROR" 

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

def ask_server_annuaire_contacts(client, annuaire_name):
    client.convert_and_transmit_data(LOOK_DIRECTORY, {"token": client.get_token(), "username": client.get_username(), "annuaire_content": annuaire_name})
    response = client.receive_and_convert_data()
    # get data from request and display it with a number before each contact (1, 2, 3, ...)
    if(response["type"] == RESPONSE_OK_TYPE):
        contacts = response["data"]["contacts"]

        return contacts
    else:
        print("Une erreur est survenue lors de la demande des contacts")
        return [] # Empty List

def ask_menu_choice(min_max = (1, 7)):
    print("1. Afficher mon annuaire")
    print("2. Ajouter un contact")
    print("3. Supprimer un contact")
    print("4. Modifier un contact")
    print("5. Rechercher un contact")
    print("6. Gérer les permissions de mon annuaire")
    print("7. Quitter")

    choice = input("Votre choix: ")

    # While choice is not a valid number or is not in the range of min_max
    try: 
        int(choice)
    except(Exception):
        print("Invalid Number")
        ask_menu_choice()
    
    if(int(choice) < min_max[0] or int(choice) > min_max[1]):
        print("Invalid Choice")
        ask_menu_choice()

    # Choice validated
    return choice

def ask_contact_information():
    print("Veuillez entrer les informations du contact")
    name = input("Nom*: ").strip()
    first_name = input("Prénom*: ").strip()
    email = input("Email*: ").strip()
    phone = input("Téléphone: ").strip()
    address = input("Adresse: ").strip()
    contact = {"name": name, "first_name": first_name, "email": email, "phone": phone, "address": address}
    
    if(name == "" or first_name == "" or email == ""):
        print("Les champs marqués d'un * sont obligatoires")
        ask_contact_information()
    
    if(len(phone) == 0 or phone == ""):
        contact[phone] = "N/A"
    
    if(len(address) == 0 or address == ""):
        contact[address] = "N/A"

    return contact

def ask_admin_menu_choice(min_max = (1, 4)):
    clear()
    
    print("1. Ajouter un utilisateur")
    print("2. Supprimer un utilisateur")
    print("3. Modifier un utilisateur")
    print("4. Quitter")

    choice = input("Votre choix: ")

    try:
        int(choice)
    except(Exception):
        print("Invalid Number")
        ask_admin_menu_choice()

    if(int(choice) < min_max[0] or int(choice) > min_max[1]):
        print("Invalid Choice")
        ask_admin_menu_choice()
    
    return choice

def ask_permission_menu(min_max = (1, 4)):
    clear()
    
    print("1. Lister les utilisateurs ayant accès a mon annuaire")
    print("2. Ajouter un utilisateur à mon annuaire")
    print("3. Supprimer un utilisateur de mon annuaire")
    print("4. Quitter")

    choice = input("Votre choix: ")

    try:
        int(choice)
    except(Exception):
        print("Invalid Number")
        ask_permission_menu()

    if(int(choice) < min_max[0] or int(choice) > min_max[1]):
        print("Invalid Choice")
        ask_permission_menu()
    
    return choice



def list_contacts(contacts):
    time.sleep(1)
    for index, contact in enumerate(contacts):
        contact_info = contact.split(",")
        contact_name = ""
        contact_first_name = ""
        contact_email = ""
        contact_phone = ""
        contact_address = ""

        # if contact_info[x] is empty or does not exist, we set contact_name to N/A
        contact_name = "N/A" if (not contact_info or contact_info[0] == "") else contact_info[0]
        contact_first_name = "N/A" if (not contact_info or contact_info[1] == "") else contact_info[1]
        contact_email = "N/A" if (not contact_info or contact_info[2] == "") else contact_info[2]
        contact_phone = "N/A" if (not contact_info or contact_info[3] == "") else contact_info[3]
        contact_address = "N/A" if (not contact_info or contact_info[4] == "") else contact_info[4]
        
        print(f"{index + 1}. Nom: {contact_name.strip()} | Prenom: {contact_first_name.strip()} | Email: {contact_email.strip()} | Tel: {contact_phone.strip()} | Adresse: {contact_address.strip()}")

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
                    # Add User
                    new_username = input("Nom d'utilisateur: ").strip()
                    new_password = input("Mot de passe: ").strip()
                    new_user_admin = input("Admin? (y/n): ").strip()

                    if(new_user_admin == "y"):
                        new_user_admin = True
                    else:
                        new_user_admin = False

                    client.convert_and_transmit_data(ADD_USER_TYPE, {"token": client.get_token(), "username": client.get_username(), "new_username": new_username, "new_password": new_password, "new_user_admin": new_user_admin})
                    request = client.receive_and_convert_data()
                    if(request["type"] == RESPONSE_OK_TYPE):
                        print("Utilisateur ajouté avec succès")
                    else:
                        print("Une erreur est survenue lors de la création de l'utilisateur")
                        print(request["data"]["message"])

                    time.sleep(2)
                    clear()
                case 2:
                    # Delete User
                    print("Supprimer l'utilisateur")
                    user_to_delete = input("Nom d'utilisateur: ").strip()           

                    if(len(user_to_delete) == 0):
                        print("Nom d'utilisateur invalide")
                        time.sleep(2)
                        clear()
                        return

                    if(user_to_delete == client.get_username()):
                        print("Vous ne pouvez pas supprimer votre propre compte")
                        time.sleep(2)
                        clear()
                        return

                    client.convert_and_transmit_data(REMOVE_USER_TYPE, {"token": client.get_token(), "username": client.get_username(), "user_to_delete": user_to_delete})
                    request = client.receive_and_convert_data()
                    if(request["type"] == RESPONSE_OK_TYPE):
                        print("Utilisateur supprimé avec succès")
                    else:
                        print("Une erreur est survenue lors de la supression de l'utilisateur")
                        print(request["data"]["message"])
                        
                    time.sleep(2)
                    clear()
                case 3:
                    # Edit User
                    print("Modifier l'utilisateur")
                    user_to_edit = input("Nom d'utilisateur: ")

                    new_username = input("Nouveau nom d'utilisateur (laisser vide pour ne pas changer): ").strip()
                    new_password = input("Nouveau mot de passe (laisser vide pour ne pas changer): ").strip()
                    new_is_admin = input("Admin? (y/n): ").strip()

                    if(new_is_admin == "y"):
                        new_is_admin = True
                    else:
                        new_is_admin = False

                    if(len(user_to_edit) == 0):
                        print("Nom d'utilisateur invalide")
                        time.sleep(2)
                        clear()
                        return
                    
                    if(user_to_edit == client.get_username()):
                        print("Vous ne pouvez pas modifier votre propre compte")
                        time.sleep(2)
                        clear()
                        return
                    

                    client.convert_and_transmit_data(EDIT_USER_TYPE, {"token": client.get_token(), "username": client.get_username(), "user_to_edit": user_to_edit, "new_username": new_username, "new_password": new_password, "new_is_admin": new_is_admin})
                    request = client.receive_and_convert_data()
                    if(request["type"] == RESPONSE_OK_TYPE):
                        print("Utilisateur modifié avec succès")
                    else:
                        print("Une erreur est survenue lors de la modification de l'utilisateur")
                        print(request["data"]["message"])

                    time.sleep(2)
                    clear()
                case 4:
                    # Quit
                    client.convert_and_transmit_data(DISCONNECT_TYPE, {"token": client.get_token(), "username": username})
                    print("Déconnecté avec succès")
                    break                    
                case _:
                    print("Invalid Choice")
                    
        else:
            # Displaying the menu
            user_input = ask_menu_choice((1, 7))
            annuaire_name = username + "_annuaire"
            match(int(user_input)):
                case 1:
                    # Afficher mon annuaire
                    contacts = ask_server_annuaire_contacts(client, annuaire_name)

                    if(contacts == []):
                        print("Vous n'avez aucun contact dans votre annuaire")
                        time.sleep(1)
                        clear()
                    else:
                        clear()
                        print("Voici les contacts dans votre annuaire:")
                        list_contacts(contacts)
                        print("=====================================")
                    
                        
                case 2:
                    # Ajouter un contact
                    contact = ask_contact_information()

                    client.convert_and_transmit_data(ADD_CONTACT_TYPE, {"token": client.get_token(), "username": client.get_username(), "annuaire_name": annuaire_name, "contact": contact})
                    response = client.receive_and_convert_data()

                    if(response["type"] == RESPONSE_OK_TYPE):
                        print("Contact Ajouté avec succès")
                        time.sleep(1)
                        clear()
                    else:
                        print("Une erreur est survenue lors de l'ajout du contact")


                case 3:
                    # Supprimer un contact
                    contacts = ask_server_annuaire_contacts(client, annuaire_name)
                    if(contacts == False):
                        print("Vous n'avez aucun contact dans votre annuaire")
                        time.sleep(1)
                        clear()
                        return
                    
                    print("Voici les contacts dans votre annuaire:")
                    list_contacts(contacts)
                    contact_index = 0

                    # ask for contact index and check if valid
                    try:
                        contact_index = input("Veuillez entrer le numéro du contact à supprimer: ")
                        contact_index = int(contact_index) - 1

                        # check if valid number
                        if(contact_index < 0 or contact_index > len(contacts)):
                            print("Invalid Number")
                            time.sleep(1)
                            clear()
                            return                    
                    except(Exception):
                        print("Invalid Number")
                        print("Retour au menu.")
                        time.sleep(1)
                        clear()
                        return

                    client.convert_and_transmit_data(REMOVE_CONTACT_TYPE, {"token": client.get_token(), "username": client.get_username(), "annuaire_name": annuaire_name, "contact_index": contact_index})
                    response = client.receive_and_convert_data()

                    if(response["type"] == RESPONSE_OK_TYPE):
                        print("Contact Supprimé avec succès")
                        time.sleep(1)
                        clear()
                    else:
                        print("Une erreur est survenue lors de la suppression du contact")
                        print(response["data"]["message"])
                        time.sleep(3)
                        clear()

                case 4:
                    # Modifier un contact
                    contacts = ask_server_annuaire_contacts(client, annuaire_name)
                    contact_index = 0

                    if(contacts == False or len(contacts) == 0):
                        print("Vous n'avez aucun contact dans votre annuaire")
                        time.sleep(1)
                        clear()
                        return
                    
                    print("Voici les contacts dans votre annuaire:")
                    list_contacts(contacts)


                    # ask for contact index and check if valid
                    try:
                        contact_index = input("Veuillez entrer le numéro du contact à modifier: ")
                        contact_index = int(contact_index) - 1

                        # check if valid number
                        if(contact_index < 0 or contact_index > len(contacts)):
                            print("Invalid Number")
                            print("Retour au menu.")
                            time.sleep(1)
                            clear()
                            return

                        # ask for new contact information
                        contact = ask_contact_information()

                        # send request to server
                        client.convert_and_transmit_data(EDIT_CONTACT_TYPE, {"token": client.get_token(), "username": client.get_username(), "annuaire_name": annuaire_name, "contact_index": contact_index, "new_contact_info": contact})
                        response = client.receive_and_convert_data()

                        if(response["type"] == RESPONSE_OK_TYPE):
                            print("Contact Modifié avec succès")
                            time.sleep(1)
                            clear()
                        else:
                            print("Une erreur est survenue lors de la modification du contact")
                            print(response["data"]["message"])
                            time.sleep(3)
                            clear()
                            
                    except(Exception):
                        print("Invalid Number")
                        print("Retour au menu.")
                        time.sleep(1)
                        clear()
                        return

                case 5:
                    # Rechercher un contact
                    contacts = ask_server_annuaire_contacts(client, annuaire_name)
                    if(contacts == False):
                        print("Vous n'avez aucun contact dans votre annuaire")
                        time.sleep(1)
                        clear()
                        return
                    
                    print("Voici les contacts dans votre annuaire:")
                    list_contacts(contacts)

                    word_to_search = input("Veuillez entrer le nom du contact à rechercher: ").strip()

                    # send request to server
                    client.convert_and_transmit_data(SEARCH_CONTACT_TYPE, {"token": client.get_token(), "username": client.get_username(), "annuaire_name": annuaire_name, "word_to_search": word_to_search})
                    response = client.receive_and_convert_data()

                    if(response["type"] == RESPONSE_OK_TYPE):
                        if("contacts" in response["data"]):
                            clear()
                            print("Voici les contacts trouvés:")
                            list_contacts(response["data"]["contacts"])
                        else:
                            print("Aucun contact trouvé")
                    else:
                        print("Une erreur est survenue lors de la recherche du contact")
                        print(response["data"]["message"])
                        time.sleep(3)
                        clear()                   
                    
                case 6:
                    # Gérer les permissions de mon annuaire
                    # Displaying permission menu
                    user_input = ask_permission_menu((1, 4))
                    match(int(user_input)):
                        case 1:
                            # List permissions
                            client.convert_and_transmit_data(LIST_USERS_DIRECTORY_TYPE, {"token": client.get_token(), "username": client.get_username(), "annuaire_name": annuaire_name})
                            response = client.receive_and_convert_data()

                            

                            pass
                        case 2:
                            # Add User from Directory
                            pass
                        case 3:
                            # Remove User from Directory
                            pass
                        case 4:
                            # Quitter
                            client.convert_and_transmit_data(DISCONNECT_TYPE, {"token": client.get_token(), "username": username})
                            print("Déconnecté avec succès")
                            break
                case 7:
                    # Quitter
                    client.convert_and_transmit_data(DISCONNECT_TYPE, {"token": client.get_token(), "username": username})
                    print("Déconnecté avec succès")
                    break

                case _:
                    print("Invalid Choice")
                    

if __name__ == "__main__":
    try:
        main()
    except(KeyboardInterrupt):
        print("Exiting...")
        exit(0)
    except Exception as e:
        print("An Unknow Error Has Occured ", e)
        exit(1)
