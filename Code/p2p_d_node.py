# D / 'Client Node'

import socket
import threading
import csv
import datetime
import tkinter
import time

### CONSTANT DECLERATION ###

HEADER = 64
CACHE_IP = input('What is the Cache Server\'s ip? : ')
CACHE_PORT = int(input('What is the Cache Server\'s port? : '))
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'
CACHE_SERVER = (CACHE_IP, CACHE_PORT)
STARTUP = 2

### CONSTANT DECLERATION ###

ex_cons = list()

### CLASS ###


class connection:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Setting up connection')
        self.setup()

    def setup(self):

        print('Receiving Server Node \n')

        c_node = recieve_c_node()

        if c_node == '!NONE':
            print('No available server nodes \n')
            time.sleep(120)

        if c_node != '!NONE':
            # [addr,xport,connection_count]
            ADDR = (c_node[0], int(c_node[1]))
            self.s.connect(ADDR)
            ex_cons.append(c_node[0])
            print('Connected to Server node \n')

        self.listen(c_node[0])

    def listen(self, addr):

        while True:
            print('Listening on Connection')
            try:
                message = self.s.recv(1024).decode(FORMAT)

                if message == DISCONNECT:
                    self.s.close()
                    ex_cons.remove(addr)
                    self.setup()

            except:
                self.s.close()
                ex_cons.remove(addr)
                self.setup()


### CLASS ###


### CACHE SERVER STUFF ###
c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c_socket.connect(CACHE_SERVER)

print('Connected to cache server on {} and port {}'.format(CACHE_IP, CACHE_PORT))

print('Sending initial details')

STARTUP = str(STARTUP).encode(FORMAT)

c_socket.send(STARTUP)


def recieve_c_node():
    message_type = 'n'.encode(FORMAT)
    message = (str(ex_cons)).encode(FORMAT)

    c_socket.send(message_type)
    c_socket.send(message)

    new_node = c_socket.recv(1024).decode(FORMAT)

    if new_node != '!NONE':
        new_node = eval(new_node)

    # [addr,xport,connection_count]

    return new_node


### THREADING ###

'''
con1 = connection()
con2 = connection()
con3 = connection()

thread1 = threading.Thread(target=con1)
thread2 = threading.Thread(target=con2)
thread3 = threading.Thread(target=con3)
'''

thread1 = threading.Thread(target=connection)
thread2 = threading.Thread(target=connection)
thread3 = threading.Thread(target=connection)

thread1.start()
thread2.start()
thread3.start()
