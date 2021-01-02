# host/cache server

import socket
import threading
import csv
import tkinter
import datetime
import time

#### CONFIG FILE ####

PORT = str()
HOST = str()

print('Trying to open csv file')
try:
    f = open(
        r"C:\Users\Gaming Desktop\DIDI test\DIDI-2020\Code\p2p\host_config.csv.txt", 'r')
except FileNotFoundError:
    print('Cannot find config file')


with open(r"C:\Users\Gaming Desktop\DIDI test\DIDI-2020\Code\p2p\host_config.csv.txt", 'r', newline='') as config_file:
    reader = csv.DictReader(config_file)
    for row in reader:
        PORT = int(row['iport'])
        XPORT = int(row['xport'])
        HOST = (row['hostip'])

#### CONFIG FILE ####


#### CONSTANT DECLERATION ####

HEADER = 64
HOST = HOST
PORT = PORT
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'

#### CONSTANT DECLERATION ####

# cnodes = [[conn,addr,xport,connection_count]]


cnodes = list()
dnodes = 0


#### C NODE CLASS ####


def dy_min():

    while True:

        num_cnodes = len(cnodes)
        # 3 is number of connections per dnode
        try:
            min = ((dnodes*3)//num_cnodes)//2
        except:
            min = 1

        for x in cnodes:
            conn = x[0]

            message_type = 'min'.encode(FORMAT)
            message = str(min).encode(FORMAT)

            conn.send(message_type)
            conn.send(message)

        time.sleep(5)


def ordered_c_list():

    o = cnodes.copy()

    o = sorted(o, key=lambda x: x[3], reverse=False)

    return o


def lost_conn(addr):

    for x in cnodes:
        if x[1] == addr:
            x[3] += -1


def gain_conn(addr):

    for x in cnodes:
        if x[1] == addr:
            x[3] += -1


def kick_dnodes(low_conn):

    o = ordered_c_list()

    conn = o[len(o)-1][0]

    message_type = 'lose'.encode(FORMAT)
    message = ''.encode(FORMAT)

    if low_conn != conn:

        conn.send(message_type)
        conn.send(message)


def cnode_handler(conn, addr, xport):
    print(f'CNODE : {addr} has connected')

    cnodes.append([conn, addr, xport, 0])

    connected = True

    while connected:

        try:
            message_type = conn.recv(1024).decode(FORMAT)

        except:
            message_type = DISCONNECT

        # message = conn.recv(1024).decode(FORMAT) dont think i need this

        if message_type == 'l':
            lost_conn(addr)

        if message_type == 'g':
            gain_conn(addr)

        if message_type == 'll':  # under connection bracket (dy_min)
            print(f'{addr} needs more clients')
            kick_dnodes(conn)

        # PUT MORE HERE

        if message_type == DISCONNECT:
            connected = False
            for x in cnodes:
                if x[1] == addr:
                    cnodes.remove(x)

        conn.close()


#### C NODE CLASS ####


#### D NODE CLASS ####

def send_conn(conn, addr, excons):

    o = ordered_c_list()

    o = [x for x in o if x[1] not in excons]

    new_node = ''

    if o == []:
        new_node = '!NONE'

    if o != []:
        new_node = [o[0][1], o[0][2]]

    new_node = (str(new_node)).encode(FORMAT)

    conn.send(new_node)


def dnode_handler(conn, addr, dnodes):
    print(f'DNODE : {addr} has connected')

    dnodes += 1

    connected = True

    while connected:

        message_type = conn.recv(1024).decode(FORMAT)
        message = conn.recv(1024).decode(FORMAT)

        if message_type == 'n':
            ex_addrs = eval(message)
            send_conn(conn, addr, ex_addrs)

        # put any more message thingys here

        if message_type == DISCONNECT:
            connected = False

    conn.close()
    dnodes += -1


#### D NODE CLASS ####


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ADDR = (HOST, PORT)

s.bind(ADDR)


def start():
    s.listen()
    print(
        f'Cache server listening for any new connections on {HOST}, internal port: {PORT}, external port: {XPORT}')
    dynamic_minimum = threading.Thread(target=dy_min)
    dynamic_minimum.start()

    while True:
        conn, addr = s.accept()

        startup_message = conn.recv(1024).decode(
            FORMAT)  # 1 = cnode 2 = dnode

        startup_message = int(startup_message)

        if startup_message:

            if startup_message == 1:
                xport = conn.recv(1024).decode(FORMAT)
                thread = threading.Thread(
                    target=cnode_handler, args=(conn, addr, xport))
                thread.start()

            if startup_message == 2:
                thread = threading.Thread(
                    target=dnode_handler, args=(conn, addr, dnodes))
                thread.start()


print('Cache server starting up')
start()
