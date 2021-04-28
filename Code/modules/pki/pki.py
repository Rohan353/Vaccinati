# pki module to handle public/private authentication

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def decrypt(passkey, message):

    with open('private_key.pem', 'rb') as key_file:

        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=passkey,
            backend=default_backend()
        )

        original_message = private_key.decrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return original_message


def encrypt(message):

    with open('public_key.pem', 'rb') as key_file:

        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

        encrypted = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted


if __name__ == '__main__':
    x = input()

    x = bytes(x, encoding='utf8')

    cipher = encrypt(x)
    print(cipher)

    while True:

        try:
            key = input()
            key = bytes(key, encoding='utf8')
            plaintext = decrypt(key, cipher)

            break

        except ValueError:
            print('Error - Incorrect Password')

    print(plaintext.decode('utf-8'))
