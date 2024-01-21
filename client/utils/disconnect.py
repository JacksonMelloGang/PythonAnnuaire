from utils.constants import DISCONNECT_TYPE


def disconnect(client):
    # Quitter
    client.convert_and_transmit_data(DISCONNECT_TYPE, {"token": client.get_token(), "username": client.get_username()})
    print("Déconnecté avec succès")

