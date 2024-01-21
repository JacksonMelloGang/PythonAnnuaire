import os

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
USER_FOLDER = os.path.join(SCRIPT_DIRECTORY, "user_files")
valid_token = {}
CONNEXION_TYPE = "CONNEXION" # Provided => {"username": "username", "password": "password"}
DISCONNECT_TYPE = "DISCONNECT" # Provided => {}
LOOK_DIRECTORY = "LOOK_DIRECTORY" # Provided => {"token": token, "data": {"annuaire": "directory_name"}}
ADD_CONTACT_TYPE = "ADD_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
EDIT_CONTACT_TYPE = "EDIT_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
REMOVE_CONTACT_TYPE = "REMOVE_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
SEARCH_CONTACT_TYPE = "SEARCH_CONTACT" # Provided => {"token": token, "data": {"annuaire": "directory_name", "contact": {"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}}}
LIST_DIRECTORIES_TYPE = "LIST_DIRECTORIES" # Provided => {"token": token, "data": {}}
LIST_USER_TO_DIRECTORY_TYPE = "LIST_USER_TO_DIRECTORY"
ADD_USER_TO_DIRECTORY_TYPE = "ADD_USER_TO_DIRECTORY" # Provided => {"token": token, "data": {"annuaire": "directory_name", "username": "username"}}
REMOVE_USER_TO_DIRECTORY_TYPE = "REMOVE_USER_TO_DIRECTORY" # Provided => {"token": token, "data": {"annuaire": "directory_name", "username": "username"}}
LIST_USERS_TYPE = "LIST_USERS" # Provided => {"token": token, "data": {}}
USER_INFO_TYPE = "USER_INFO" # Provided => {"token": token, "data": {"username": "username", "looked_user": "looked_user"}}
ADD_USER_TYPE = "ADD_USER" # Provided => {"token": token, "data": {"username": "username", "password": "password"}}
REMOVE_USER_TYPE = "REMOVE_USER" # Provided => {"token": token, "data": {"username": "username", "password": "password"}}
EDIT_USER_TYPE = "EDIT_USER" # Provided => {"token": token, "data": {"username": "username", "password": "password"}}
CONNEXION_OK_TYPE = "CONNEXION_OK" # Provided => {"message": "Valid Credentials", "token": token}
DISCONNECT_OK_TYPE = "DISCONNECT_OK" # Provided => {"message": "Disconnected Successfully"}
RESPONSE_OK_TYPE = "RESPONSE_OK" # Provided => {"data": {"annuaire": "directory_name", "contacts": [{"name": "name", "first_name": "first_name", "phone": "phone", "email": "email"}, ...]}}
ERROR_TYPE = "ERROR" # Provided => {"message": "Error Message"}
