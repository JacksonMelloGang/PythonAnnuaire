import socket
import json
import threading
import secrets  # Pour la génération de tokens aléatoires

from utils import Observer, Observable, ObservableList

class Annuaire:
    def __init__(self, filename):
        self.filename = filename
        self.contacts = []



class Utilisateur:
    def __init__(self, username, password, isadmin):
        self.username = username
        self.password = password
        self.annuaire = Annuaire()
        self.isadmin = isadmin
        self.utilisateurs_autorisee = []

    def autoriser_acces(self, user):
        self.utilisateurs_autorisee.append(user)
        return True

    def retirer_acces(self, user):
        self.utilisateurs_autorisee.remove(user)




# Dictionnaire pour stocker les tokens associés aux identifiants des utilisateurs
user_tokens = {}

def generate_token():
    return secrets.token_hex(16)  # Génère un token aléatoire (32 caractères hexadécimaux)

def handle_auth_request(data):
    # Implémentez la logique d'authentification ici.
    # Si l'authentification réussit, générez un token et associez-le à l'identifiant de l'utilisateur.
    # Retournez le token dans la réponse.
    # Si l'authentification échoue, retournez une réponse avec l'erreur correspondante.
    
    # Exemple simple pour l'illustration, remplacez ceci par votre propre logique d'authentification.
    if data.get("username") == "user123" and data.get("password") == "pass123":
        token = generate_token()
        user_tokens[data.get("username")] = token
        return {"status": "success", "token": token}
    else:
        return {"status": "failure", "error": "Invalid credentials"}

def handle_data_request(data):
    # Implémentez la logique pour récupérer des données ici.
    # Vérifiez le token dans le dictionnaire user_tokens avant de traiter la requête.
    user_id = data.get("id", None)
    token = data.get("token", None)
    
    if user_id is not None and token is not None and user_tokens.get(user_id) == token:
        return {"id": user_id, "value": "some_data"}
    else:
        return {"error": "Invalid token or user ID"}

def handle_disconnect(data):
    # Implémentez la logique de déconnexion ici.
    # Invalide le token associé à l'identifiant de l'utilisateur.
    user_id = data.get("id", None)
    if user_id is not None:
        user_tokens.pop(user_id, None)
        return {"status": "success", "message": "User disconnected"}
    else:
        return {"status": "failure", "error": "Invalid user ID"}

def handle_client(client_socket):
    request = client_socket.recv(1024).decode("utf-8")

    if request:
        response_data = handle_request(request)
        response = json.dumps(response_data)
        client_socket.send(response.encode("utf-8"))

    client_socket.close()

def handle_request(request):
    request_data = json.loads(request)

    if request_data["type"] == "AUTH":
        return handle_auth_request(request_data["data"])
    elif request_data["type"] == "DATA_REQUEST":
        return handle_data_request(request_data["data"])
    elif request_data["type"] == "DISCONNECT":
        return handle_disconnect(request_data["data"])
    else:
        return {"error": "Invalid request type"}

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 5555))
    server_socket.listen(5)
    print("Server listening on port 5555...")

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
