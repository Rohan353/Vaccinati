# Blockchain module

import hashlib
import json
from time import time
import random


auth_clients = []  # autherised client's public keys - only used to create genesis block

# Difficulty Setting (which hashes are accepted for Proof of Work)

correct = ['000001', '000002', '000003', '000004']
#correct = ['00']


class Blockchain():

    def __init__(self):

        self.chain = []

        self.new_block('rohan', previous_hash='22121232')

    def check_chain(self, chain):

        valid = True
        index = 1

        for block in chain:

            if index != 1:
                block['previous_hash'] = self.hash(chain[-1])

            hash = self.hash(block)

            if hash[0:2] not in correct:
                valid = False

                break

        return valid

    def compare_chain(self, new_chain):

        print('Compare Chain function intialised')

        try:
            valid = self.check_chain(new_chain)

            if valid == True:

                print('New chain validated')

                if len(new_chain) > len(self.chain):

                    self.chain = []
                    self.chain = new_chain

                    print('New chain has been adopted')

        except:

            print('Error when checking new chain')

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

        self.auth_mine = True

        while found == False and self.auth_mine == True:

            nonce = random.randint(1, 4294967296)

            block['proof'] = nonce

            hash = self.hash(block)

            if hash[0:2] in correct:
                found = True

            attempt += 1

            print(f'Attempt - {attempt} Hash - {hash}')

        print(f'Found hash {hash} with {nonce}')

        return block


if __name__ == '__main__':

    b = Blockchain()
    c = Blockchain()

    vaccine1 = input()
    vaccine2 = input()

    b.new_block(vaccine1)
    b.new_block(vaccine2)

    vaccine1 = input()
    vaccine2 = input()
    vaccine3 = input()

    c.new_block(vaccine1)
    c.new_block(vaccine2)
    c.new_block(vaccine3)

    c.chain[1]['identification'] = 'Chirag'

    b.compare_chain(c.chain)

    print(b.chain)
