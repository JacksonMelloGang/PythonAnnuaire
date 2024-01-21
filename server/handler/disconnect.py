def handle_disconnect(client_socket):
    # close the connection & invalidate token
    client_socket.close()
    print(f"Connexion fermée avec {client_socket.getpeername()}")    