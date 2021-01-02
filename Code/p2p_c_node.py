#  C / 'Server' node

import socket
import threading
import datetime
import tkinter
import csv
import time

#### CONFIG FILE ####

PORT = str()
HOST = str()

print('Trying to open csv file')
try:
    f = open(
        r"C:\Users\Gaming Desktop\DIDI test\DIDI-2020\Code\p2p\s_config.csv.txt", 'r')
except FileNotFoundError:
    print('Cannot find config file')


with open(r"C:\Users\Gaming Desktop\DIDI test\DIDI-2020\Code\p2p\s_config.csv.txt", 'r', newline='') as config_file:
    reader = csv.DictReader(config_file)
    for row in reader:
        PORT = int(row['iport'])
        XPORT = int(row['xport'])
        HOST = (row['hostip'])
        MYIP = (row['publicip'])


#### CONFIG FILE ####


### CONSTANT DECLERATION ###


HEADER = 64
CACHE_IP = input('What is the Cache Server\'s ip? : ')
CACHE_PORT = int(input('What is the Cache Server\'s port? : '))
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'
CACHE_SERVER = (CACHE_IP, CACHE_PORT)
STARTUP = 1

ADDR = (HOST, PORT)

### CONSTANT DECLERATION ###

cons = list()
minimum = 1


### HANDLER ###


def handle_client(conn, addr):

    connected = True
    cons.append(conn)

    while connected:

        try:
            x = conn.recv(1024).decode(FORMAT)
            # put more here

        except:
            print(f'{addr} has a problem - disconnected')

            lose_client()
            connected = False

            try:
                cons.remove(conn)
            except:
                pass


### HANDLER ###


### CACHER SERVER ###
c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_socket.connect(CACHE_SERVER)

print('Connected to cache server on {} and port {}'.format(CACHE_IP, CACHE_PORT))

print('Sending initial details')

STARTUP = str(STARTUP).encode(FORMAT)
INFO = str([MYIP, XPORT]).encode(FORMAT)

c_socket.send(STARTUP)
c_socket.send(INFO)


def gain_client():
    message = 'g'.encode(FORMAT)
    c_socket.send(message)


def lose_client():
    message = 'l'.encode(FORMAT)
    c_socket.send(message)


def listener():  # cache server listener

    while True:
        message_type = c_socket.recv(1024).decode(FORMAT)
        message = c_socket.recv(1024).decode(FORMAT)

        if message_type == 'min':
            minimum = int(message)
            print(f'New minimum is {minimum}')

        if message_type == 'lose':
            remove_connection = cons[0]
            remove_connection.close()
            cons.remove(remove_connection)


def min_checker():

    while True:
        num_cons = len(cons)

        if num_cons < minimum:

            print('At minimum connections')
            message = 'll'.encode(FORMAT)

            c_socket.send(message)

            print('Sent message')

            time.sleep(30)

        time.sleep(5)


### CACHE SERVER ###


### MAIN SOCKET ###
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)


def start():
    s.listen()
    print(f'Listeing on {HOST} IP and {PORT} Internal Port')

    cache_thread = threading.Thread(target=listener)
    cache_thread.start()

    min_thread = threading.Thread(target=min_checker)
    min_thread.start()

    while True:
        conn, addr = s.accept()
        gain_client()
        print(f'New connection from {addr}')
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print(f'Starting Server Node')
start()
