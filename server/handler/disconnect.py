def handle_disconnect(client_socket):
    # close the connection & invalidate token
    print(f"Connexion fermée avec {client_socket.getpeername()}")    
    client_socket.close()