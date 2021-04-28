# server file

# ASDASDA Put in authentication codes and save thingy

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
import random
import json
import pickle
from flask import Flask, request, render_template
from modules import blockchain
from modules.pki import pki


# declare constants

HOST = '0.0.0.0'  # allow for loop back interface
PORT = 5006  # router forwards port 5001 >> 5006
FORMAT = 'utf-8'
DISCONNECT = '!DISCONNECT'  # disconnect code so clients can be safely disconnected
clients = set()  # save connected clients
HEADER = 64
ADDR = (HOST, PORT)

# network constants

query_blockchain = 'qBlockchain'
query_pending = 'qPending'

state_blockchain = 'sBlockchain'
state_pending = 'sPending'

ask_blockchain = 'aBlockchain'

respond_blockchain = 'rBlockchain'

global new_blockchain
new_blockchain = {}

# open socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(ADDR)

# handles connections


def save_blockchain():
    with open('obj/' + 'host_chain' + '.pkl', 'wb') as f:
        pickle.dump(b.chain, f, pickle.HIGHEST_PROTOCOL)


def load_blockchain():
    with open('obj/' + 'host_chain' + '.pkl', 'rb') as f:

        new_chain = pickle.load(f)

        b.compare_chain(new_chain)


def handle_client(conn, addr):
    global new_blockchain

    print(f'{addr} connected')

    connected = True

    while connected:

        msg_type = conn.recv(1024).decode(FORMAT)

        print('recieved message {}'.format(msg_type))

        # if msg is query then sample, otherwise everyone # also if no other clients then send pickled stuff

        if msg_type == query_blockchain:

            num_clients = len(clients)

            if num_clients > 1:

                num_clients = num_clients//2

                search_clients = clients

                search_clients.remove(conn)

                for x in range(0, num_clients):
                    # have try except here with checking the confirm

                    c = random.choice(tuple(search_clients))

                    c.send(ask_blockchain.encode(FORMAT))

                    while True:
                        if new_blockchain != {}:
                            break

                    bchain = json.loads(new_blockchain)

                    b.compare_chain(bchain)
                    save_blockchain()

                    smsg = new_blockchain.encode(FORMAT)
                    msg_length = len(smsg)
                    send_length = str(msg_length).encode(FORMAT)
                    send_length += b' ' * (HEADER-len(send_length))

                    conn.send(query_blockchain.encode(FORMAT))
                    time.sleep(0.1)
                    conn.send(send_length)
                    time.sleep(0.1)
                    conn.send(smsg)

                    confirm = conn.recv(1024)

                    new_blockchain = {}

            else:
                print('Sending own blockchain')

                coded_blockchain = json.dumps(b.chain)

                smsg = coded_blockchain.encode(FORMAT)
                msg_length = len(smsg)
                send_length = str(msg_length).encode(FORMAT)
                send_length += b' ' * (HEADER-len(send_length))

                conn.send(query_blockchain.encode(FORMAT))
                time.sleep(0.1)  # time gaps so the client and keep up
                conn.send(send_length)
                time.sleep(0.1)
                conn.send(smsg)

                confirm = conn.recv(1024)

        if msg_type == respond_blockchain:

            msg_header = conn.recv(HEADER).decode(FORMAT)
            msg_length = int(msg_header)
            new_blockchain = conn.recv(msg_length).decode(FORMAT)

        if msg_type == query_pending:
            # don't need this right now
            pass

        if msg_type == state_blockchain:

            msg_header = conn.recv(HEADER).decode(FORMAT)
            msg_length = int(msg_header)
            encoded_blockchain = conn.recv(msg_length).decode(FORMAT)

            uncoded_blockchain = json.loads(encoded_blockchain)

            b.compare_chain(uncoded_blockchain)
            save_blockchain()

            search_clients = clients

            search_clients.remove(conn)

            smsg = encoded_blockchain.encode(FORMAT)
            msg_length = len(smsg)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER-len(send_length))

            for c in search_clients:

                c.send(state_blockchain.encode(FORMAT))
                time.sleep(0.05)
                c.send(send_length)
                time.sleep(0.05)
                c.send(smsg)

        if msg_type == state_pending:
            pass


# website
'''
app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('form.html')


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    print(processed_text)

    # this is the first time I have used flask so excuse the repeated code

    try:
        int(processed_text)
    except:
        return render_template('errortrap.html')

    if len(processed_text) != 8:
        return render_template('errortrap2.html')

    if processed_text == '22121232':  # put call here
        return render_template('form2.html')

    else:
        return render_template('form3.html')


def start_website():
    app.run(debug=False, host='0.0.0.0')

'''

if __name__ == '__main__':
    # website_thread = threading.Thread(target=start_website)
    # website_thread.start()
    b = blockchain.Blockchain()
    x = input('Load blockchain')
    if x == 'yes':
        load_blockchain()

    print('Server Starting')
    s.listen()
    print('Server Listening')

    while True:
        conn, addr = s.accept()
        clients.add(conn)
        # starts a new thread of the handle_client function for each client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'Active Clients = {threading.active_count()-2}')
