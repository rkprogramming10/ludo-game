from logging.config import listen
import socket
from threading import Thread

SERVER  = None
PORT    = None
IP_ADDRESS = None

clients = {}

def setup():
    print("\n")
    print("\t\t\t\t\t\t**** Ludo Ladder ****")
    global SERVER, PORT, IP_ADDRESS
    IP_ADDRESS = '127.0.0.1'
    PORT = 5000
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    listen(10)
    print("Server is waiting for connections...")
    # accept_connections()

setup()