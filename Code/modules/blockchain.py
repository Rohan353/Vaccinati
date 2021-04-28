# Blockchain module to handle all the blockchain stuff

import hashlib
import json
from time import time
import random


auth_clients = []  # autherised client's public keys - only used to create genesis block


def encrypt(inden, key):
    pass


def deycrypt(cipher, key):
    pass


class Blockchain():

    def __init__(self):

        self.chain = []

        self.new_block('rohan', previous_hash='22121232')

    def check_chain(self, chain):

        valid = True

        for block in chain:
            pass

        return valid

    # call to create genesis block - check that the pow is complete
    def new_block(self, pending_vaccination, miner_name=None, previous_hash=None):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'identification': pending_vaccination,
            'proof': 1,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'miner': miner_name or 'unknown'

        }

        block = self.mine(block)

        self.chain.append(block)

        return block

    @property
    def last_block(self):

        return self.chain[-1]

    def hash(self, block):
        string_ob = json.dumps(block, sort_keys=True)
        block_string = string_ob.encode()

        hash = hashlib.sha256(block_string).hexdigest()

        return hash

    def mine(self, block):

        found = False
        attempt = 0

        while found == False:

            nonce = random.randint(1, 4294967296)

            block['proof'] = nonce

            hash = self.hash(block)

            if hash[0:4] == '0000':
                found = True

            attempt += 1

            print(f'Attempt - {attempt} Hash - {hash}')

        print(f'Found hash {hash} with {nonce}')

        return block


if __name__ == '__main__':

    b = Blockchain()

    vaccine1 = input()
    vaccine2 = input()

    b.new_block(vaccine1)
    b.new_block(vaccine2)

    print(b.chain)
