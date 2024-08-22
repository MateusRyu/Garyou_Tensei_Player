import socket

def connect_to_mpd(host='localhost', port=6600):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

print(connect_to_mpd('localhost', 6666))
