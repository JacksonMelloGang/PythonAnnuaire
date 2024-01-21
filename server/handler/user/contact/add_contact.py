import os

from constants import ERROR_TYPE, USER_FOLDER, RESPONSE_OK_TYPE
from utils import convert_and_transmit_data


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
            annuaire_file.write(f"{contact['name']},{contact['first_name']},{contact['email']},{contact['phone']},{contact['address']}")
            annuaire_file.write("\n")
            annuaire_file.close()

            convert_and_transmit_data(client_socket, RESPONSE_OK_TYPE, {"message": "Contact Added Successfully"})
    except Exception as e:
        print(f"An error occured while adding contact: {e}")
        convert_and_transmit_data(client_socket, ERROR_TYPE, {"message": "An Error Occured While Adding Contact"})
