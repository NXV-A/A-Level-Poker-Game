import socket
from _thread import *

server = '0.0.0.0'
port = 6778

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)
    
s.listen(2)
print("Waiting for a connection, server started")


def threaded_client(conn):
    pass

while True:
    conn, addr = s.accept()
    print('The bluetooth device is a connected-uh successfulay to:', addr)
    
    s
    