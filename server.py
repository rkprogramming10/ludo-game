from logging.config import listen
import socket
from threading import Thread

SERVER = None
PORT = None
IP_ADDRESS = None

clients = {}


def accept_connections():
    global SERVER
    global CLIENTS
    while True:
        player_socket, addr = SERVER.accept()
        player_name = player_socket.recv(1024).decode().strip()
        if (len(clients.keys()) == 0):
            clients[player_name] = {'player_type': 'player1'}
        else:
            clients[player_name] = {'player_type': 'player2'}

        clients[player_name]['player_socket'] = player_socket
        clients[player_name]['address'] = addr
        clients[player_name]['player_name'] = player_name
        clients[player_name]['turn'] = False
        print(f'connection established with {player_name}:{addr}')


def setup():
    print("\n")
    print("\t\t\t\t\t\t**** Ludo Ladder ****")
    global SERVER, PORT, IP_ADDRESS
    IP_ADDRESS = '127.0.0.1'
    PORT = 5000
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(10)
    print("Server is waiting for connections...")
    accept_connections()


setup()
