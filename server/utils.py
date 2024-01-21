import json
import os

from constants import USER_FOLDER

def read_files(path):
    lines = []

    if os.path.exists(f"{path}"):
            with open(f"{path}", "r") as annuaire_file:
                # separate each line of the file in an array []
                lines = annuaire_file.readlines()
                for i in range(len(lines)):
                    # remove \n at the end of each line
                    lines[i] = lines[i].replace("\n", "")
                annuaire_file.close()
    else:
        print(f"File {path} doesn't exists")
        lines = False

    return lines


def edit_file(path, line, content):
    try:
        lines = read_files(path)
        lines[line] = content
        with open(f"{path}", "w") as annuaire_file:
            for line in lines:
                annuaire_file.write(line + "\n")
            return True
    except Exception as e:
        print(f"An error occured while editing file: {e}")
        return False


def remove_line(filename, index):
    with open(filename, 'r') as file:
        lines = file.readlines()

    if index < len(lines):
        del lines[index]

    with open(filename, 'w') as file:
        file.writelines(lines)


def is_admin(username):
    is_admin = False
    # check with username if he has admin rights in user_info.txt
    if os.path.exists(f"{USER_FOLDER}/{username}/user_info.txt"):
        with open(f"{USER_FOLDER}/{username}/user_info.txt", "r") as user_info_file:
            # while we don't reach the end of the file, we read the next line to check if it's "isAdmin=True"
            lines = user_info_file.readlines()
            for line in lines:
                if line.strip() == "isAdmin=True":
                    is_admin = True
                    break
            user_info_file.close()
    return is_admin


def convert_and_transmit_data(client_socket, request_type, data):
    try:
        request = {"type": request_type, "data": data}
        client_socket.send(json.dumps(request).encode('utf-8'))
        print(f"Sending Request: {request_type} to {client_socket.getpeername()}")
    except Exception as e:
        print("An Unknow Error Has Occured while sending request")
        print(e)


def receive_and_convert_data(client_socket):
    json_content = False

    content = client_socket.recv(1024).decode('utf-8')
    try:
        json_content = json.loads(content)
    except(Exception):
        print(f"Couldn't convert received data:\n{content}")
    return json_content
