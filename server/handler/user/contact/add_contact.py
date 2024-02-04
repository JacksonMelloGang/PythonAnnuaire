import os

from constants import ERROR_TYPE, USER_FOLDER, RESPONSE_OK_TYPE
from utils import convert_and_transmit_data


def handle_add_contact_request(client_socket, data):
    username = data["data"]["username"]

    if("contact" not in data["data"]):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Erreur 120 - Champs Obligatoire Manqué"})
        return

    if("name" not in data["data"]["contact"] or "first_name" not in data["data"]["contact"] or "email" not in data["data"]["contact"] or "phone" not in data["data"]["contact"] or "address" not in data["data"]["contact"]):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Erreur 120 - Champs Obligatoire Manqué"})
        return

    # check if user_folder exists in user_files folder
    if not os.path.exists(f"{USER_FOLDER}/{username}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Erreur 215 - l'Utilisateur N'existe Pas"})
        return

    # check if {user}_annuaire.txt exists in user_folder
    if not os.path.exists(f"{USER_FOLDER}/{username}/{username}_annuaire.txt"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": f"Erreur 233 - l'Annuaire de {username} est introuvable dans le serveur"})
        return


    contact = data["data"]["contact"]
    contact_info = f"{contact['name']},{contact['first_name']},{contact['email']},{contact['phone']},{contact['address']}\n"

    # check if contact_info is already in {user}_annuaire.txt by reading each line and comparing it to contact_info
    with open(f"{USER_FOLDER}/{username}/{username}_annuaire.txt", "r") as annuaire_file:
        for line in annuaire_file:
            # split line into contact_info with ,
            line = line.strip().split(",")
            # get name and first_name from line and compare it to contact["name"] and contact["first_name"]
            if(line[0] == contact["name"] and line[1] == contact["first_name"]):
                convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Erreur 221 - Contact Déjà Existant"})
                return
        annuaire_file.close()


    try:
        # open {user}_annuaire.txt and append contact to it in a new line
        with open(f"{USER_FOLDER}/{username}/{username}_annuaire.txt", "a") as annuaire_file:
            annuaire_file.write(f"{contact_info}")
            annuaire_file.close()

            convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "Code 220 - Contact ajouté avec succès"})
    except Exception as e:
        print(f"An error occured while adding contact: {e}")
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Une Erreur Est Survenue Lors de l'ajout du Contact"})
