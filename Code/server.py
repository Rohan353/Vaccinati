# server file

'''
The server is designed to be a passthrough interface, sending all data back to the client. 
This minimises the control it has over the network as a whole.
In an ideal solution, the blockchain would operate over a peer to peer network. 
However due to bugs when testing p2p topoligies over python, as well as security issues,
the blockchain will use a client-host model with one trusted host - my ddns address.

In the future, the blockchain may be migrated to a p2p model if it performs well.
'''


import socket
import threading
import csv
import time

# declare constants

HOST = '0.0.0.0'  # allow for loop back interface
PORT = 5006  # router forwards port 5001 >> 5006
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'  # disconnect code so clients can be safely disconnected
clients = set()  # save connected clients
ADDR = (HOST, PORT)

# open socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(ADDR)

# handles connections


def handle_client(conn, addr):
    print(f'{addr} connected')

    connected = True

    while connected:

        msg_type = conn.recv(1024).decode(FORMAT)
        if msg_type:  # if msg is query then sample, otherwise everyone # also if no other clients then send pickled stuff
            pass


if __name__ == '__main__':
    print('Server Starting')
    s.listen()

    while True:
        conn, addr = s.accept()
        clients.add(conn)
        # starts a new thread of the handle_client function for each client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'Active Clients = {threading.active_count()-2}')
