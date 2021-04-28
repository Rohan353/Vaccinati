# client file

import socket
import csv
import time
import threading

# declare constants

HOST = input('ENTER SERVER IP - ENTER 0 UNLESS OTHERWISE REQUIRED : ')
if HOST == '0':
    HOST = 'vaccinati.ddns.net'
if HOST == '1':  # developer mode for localhost
    HOST = '127.0.0.1'
PORT = int(input('ENTER SERVER PORT - ENTER 0 UNLESS OTHERWISE REQUIRED : '))
if PORT == 0:
    PORT = 5001
if PORT == '1':
    # developer mode for localhost (router forwards port 5001 >> 5006)
    PORT = 5006
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'
ADDR = (HOST, PORT)

# blockchain constants

waiting_list = []


# open socket and connect

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket has been successfully opened')

try:
    s.connect(ADDR)
    print('Successfully connected to server')
except:
    print('ERROR CODE 01 - UNABLE TO CONNECT - CHECK GITHUB FOR HELP')


# put query responses here


def handle_server():

    while True:
        message = s.recv(1024).decode(FORMAT)


############################################

def blockchain_stats():
    pass


def mine_blockchain():
    pass


def add_block():
    pass


def start():
    choice = int(input(
        'Would you like to 1 - Look at Blockchain Stats, 2 - Mine Blockchain, 3 - Add New Block : '))


# threading and start
server_thread = threading.Thread(target=handle_server)

server_thread.start()

start()
