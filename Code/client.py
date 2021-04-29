# client file

import socket
import time
import threading
import tkinter as tk
import json
from modules import blockchain
from modules.pki import pki


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
HEADER = 64
ADDR = (HOST, PORT)

# blockchain constants

waiting_list = []
name = 'rohan'

# network constants

query_blockchain = 'qBlockchain'
query_pending = 'qPending'

state_blockchain = 'sBlockchain'
state_pending = 'sPending'

ask_blockchain = 'aBlockchain'

respond_blockchain = 'rBlockchain'

query_security = 'qSec'

confirm = b'confirm'

# open socket and connect

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket has been successfully opened')

try:
    s.connect(ADDR)
    print('Successfully connected to server')
except:
    print('ERROR CODE 01 - UNABLE TO CONNECT - CHECK GITHUB FOR HELP')


def disconnect_net():
    pass

# put query responses here


def send_blockchain():

    coded_blockchain = json.dumps(b.chain)

    smsg = coded_blockchain.encode(FORMAT)
    msg_length = len(smsg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))

    time.sleep(0.1)
    s.send(send_length)
    time.sleep(0.1)
    s.send(smsg)


def handle_server():

    print('Listening on server')

    while True:

        msg_type = s.recv(1024).decode(FORMAT)

        print('recived message {}'.format(msg_type))

        if msg_type == query_blockchain:

            # send state_blockchain through this channel

            print('Blockchain query identified')

            msg_header = s.recv(HEADER).decode(FORMAT)
            msg_length = int(msg_header)
            coded_blockchain = s.recv(msg_length).decode(FORMAT)

            new_chain = json.loads(coded_blockchain)

            print('recieved new chain')

            print(new_chain)

            b.compare_chain(new_chain)

            for block in b.chain:
                if block['identification'] in waiting_list:
                    waiting_list.remove(block['identification'])
                    print('Removed {} from waiting list'.format(
                        block['identification']))

            s.send(confirm)

        if msg_type == ask_blockchain:

            print('Sending Blockchain')

            s.send(respond_blockchain.encode(FORMAT))

            send_blockchain()

        if msg_type == state_pending:

            pending = s.recv(1024).decode(FORMAT)

            waiting_list.append(pending)

            print(f'Added {pending} to waiting list')

        if msg_type == query_security:

            encrypted_num = s.recv(4000)
            decrypted_num = pki.decrypt(key, encrypted_num)

            s.send(decrypted_num)

            print('Sent decrypted info')


############################################

def stop_mine():
    b.auth_mine = False


def blockchain_stats():
    print(b.chain)


def mine_blockchain():

    print('Mine blockchain')

    stop_button.grid(row=1, column=1)

    if waiting_list != []:

        while b.auth_mine == True:

            if waiting_list == []:
                break

            for i in waiting_list:

                b.new_block(i, name)

                time.sleep(10)

                s.send(state_blockchain.encode(FORMAT))

                send_blockchain()
    else:
        print('Nothing in waiting list')

    stop_button.destroy()


def submit_block():

    iden = str(entry_box.get())

    s.send(state_pending.encode(FORMAT))
    time.sleep(0.1)
    s.send(iden.encode(FORMAT))

    entry_box.destroy()
    submit_button.destroy()


def add_block():
    global entry_box
    global submit_button

    entry_box = tk.Entry(master=window)
    submit_button = tk.Button(
        master=window, text='submit', command=submit_block)

    entry_box.grid(row=1, column=1)
    submit_button.grid(row=2, column=1)


window = tk.Tk()
window.columnconfigure([0, 1, 2], weight=1)
window.rowconfigure([0, 1, 2, 3], weight=1)

stats_button = tk.Button(master=window, text='Stats', command=blockchain_stats)
mine_button = tk.Button(master=window, text='Mine', command=mine_blockchain)
add_button = tk.Button(master=window, text='Vaccine', command=add_block)

disconnect_button = tk.Button(
    master=window, text='Disconnect', command=disconnect_net)

stop_button = tk.Button(master=window, text='Stop Mining', command=stop_mine)

entry_box = tk.Entry(master=window)
submit_button = tk.Button(master=window, text='submit', command=submit_block)


stats_button.grid(row=0, column=0)
mine_button.grid(row=0, column=1)
add_button.grid(row=0, column=2)

disconnect_button.grid(row=3, column=1)


if __name__ == '__main__':

    key = input('What is your key')
    key = bytes(key, encoding='utf8')

    b = blockchain.Blockchain()

    message = query_blockchain.encode(FORMAT)

    # threading and start
    server_thread = threading.Thread(target=handle_server)

    server_thread.start()

    s.send(message)  # send first blockchain query
