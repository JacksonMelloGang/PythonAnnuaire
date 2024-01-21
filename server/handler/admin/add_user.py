import os

from constants import USER_FOLDER, RESPONSE_OK_TYPE, ERROR_TYPE
from utils import convert_and_transmit_data


def handle_add_user_request(client_socket, data):
    new_username = data["data"]["new_username"]
    new_password = data["data"]["new_password"]
    new_user_admin = data["data"]["new_user_admin"]

    # check if username already exists in user_files folder
    if os.path.exists(f"{USER_FOLDER}/{new_username}"):
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Erreur 214 - l'Utilisateur Existe Déjà"})
        return

    # create new user folder
    success = create_new_user_folder(new_username, new_password, new_user_admin)
    if(success):
        convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "Code 210 - Utilisateur Ajouté Avec Succès"})
    else:
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "Une Erreur Est Survenue Lors de la Création de l'Utilisateur"})


def create_new_user_folder(username, password, is_user_admin = False):
    try:
        # create folder for user, and if user_info.txt doesn't exist, create it and write password in it
        os.makedirs(f"{USER_FOLDER}/{username}", exist_ok=False)
        with open(f"{USER_FOLDER}/{username}/user_info.txt", "w") as user_info_file:
            user_info_file.write(password)
            user_info_file.write("\n")
            user_info_file.write(f"isAdmin={is_user_admin}")
            user_info_file.write("\n")
            user_info_file.close()
        # create username_annuaire.txt in user folder
        with open(f"{USER_FOLDER}/{username}/{username}_annuaire.txt", "w") as user_annuaire_file:
            user_annuaire_file.write("")
            user_annuaire_file.close()
        # create shared_to_me.txt and shared_by_me.txt in user folder
        with open(f"{USER_FOLDER}/{username}/share_to_user.txt", "w") as shared_to_me_file:
            shared_to_me_file.write("")
            shared_to_me_file.close()
        with open(f"{USER_FOLDER}/{username}/shared_by_me.txt", "w") as shared_by_me_file:
            shared_by_me_file.write("")
            shared_by_me_file.close()
        
        return True
    except OSError as err:
        print("Couldn't create user because it already exists !")
        return False
    except Exception as e:
        print(f"An error occured while creating new user folder: {e}")
        return False


