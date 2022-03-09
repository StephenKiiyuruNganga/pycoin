import binascii
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random


class Wallet:
    def __init__(self, node_port):
        self.private_key = None
        self.public_key = None
        self.node_port = node_port

    def create_keys(self):
        # tuple unpacking
        private_key, public_key = self.generate_keys()

        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        # only save if we have valid keys
        if self.public_key != None and self.private_key != None:
            try:
                with open(f"wallet_data_{self.node_port}.txt", mode="w") as my_file:
                    my_file.write(self.public_key)
                    my_file.write("\n")
                    my_file.write(self.private_key)
                print("[+] Saving wallet success!\n")
                return True

            except (IOError, IndexError):
                print("[-] Saving wallet failed!\n")
                return False

    def load_keys(self):
        try:
            with open(f"wallet_data_{self.node_port}.txt", mode="r") as my_file:
                content = my_file.readlines()
                # remove the line break character in line 1 using the range selector
                self.public_key = content[0][:-1]
                self.private_key = content[1]
            print("[+] Loading wallet success!\n")
            return True

        except (IOError, IndexError):
            print("[-] Loading wallet failed!\n")
            return False

    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        converted_private_key = binascii.hexlify(
            private_key.exportKey(format="DER")).decode("ascii")
        converted_public_key = binascii.hexlify(
            public_key.exportKey(format="DER")).decode("ascii")
        return (converted_private_key, converted_public_key)

    def sign_transaction(self, sender, recepient, amount):
        signer = PKCS1_v1_5.new(RSA.importKey(
            binascii.unhexlify(self.private_key)))
        hashed_transaction_payload = SHA256.new(
            (str(sender) + str(recepient) + str(amount)).encode("utf8"))
        signature = signer.sign(hashed_transaction_payload)
        return binascii.hexlify(signature).decode("ascii")

    @staticmethod
    def verify_transaction(transaction):
        verifier = PKCS1_v1_5.new(RSA.importKey(
            binascii.unhexlify(transaction.sender)))
        hashed_transaction_payload = SHA256.new(
            (str(transaction.sender) + str(transaction.recepient) + str(transaction.amount)).encode("utf8"))
        return verifier.verify(hashed_transaction_payload, binascii.unhexlify(transaction.signature))
