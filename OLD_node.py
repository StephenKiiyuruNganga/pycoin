# a node is a computer that has a copy of the blockchain and can mine,send transactions etc.

from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet


class Node:
    def __init__(self):
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_new_transaction(self):
        """ Get the recepient and amount from the user and return it in a tuple"""
        recepient = input("Enter recepient's name: ")
        amount = float(input("Enter transaction amount: "))
        return (recepient, amount)

    def get_user_choice(self):
        print("""
      What do you want to do?
      1. Add new transaction
      2. Mine block
      3. Print blockchain
      4. Create wallet keys
      5. Load wallet keys
      6. Save wallet keys
      q. Quit
      """)
        return input("Your choice: ")

    def print_blockchain(self):
        print("Blockchain ==========> " +
              str(self.blockchain.get_chain()) + "\n")
        print("List of blocks in blockchain:")
        for idx in range(len(self.blockchain.get_chain())):
            print(
                f"\nBlock {str(idx)}:\n{str(self.blockchain.get_chain()[idx])}\n")

    def listen_for_choice(self):
        waiting_for_input = True
        while waiting_for_input:
            choice = self.get_user_choice()
            if choice == "1":
                transaction_data = self.get_new_transaction()
                # Tuple unpacking:
                (recepient, amount) = transaction_data
                signature = self.wallet.sign_transaction(
                    self.wallet.public_key, recepient, amount)
                if self.blockchain.add_transaction(recepient, self.wallet.public_key, signature, amount=amount):
                    print("[+] Transaction successfull")
                    print("open transactions ========> " +
                          str(self.blockchain.get_open_transactions()))
                    print("Balance for {}: {:6.2f}\n".format(
                        self.wallet.public_key, self.blockchain.get_balance()))
                else:
                    print("[-] Transaction failed")
            elif choice == "2":
                if not self.blockchain.mine_block():
                    print(
                        "[-] Mining Failed. Try loading a wallet or create a new one.\n")

                print("Balance for node id {}: {:6.2f}\n".format(
                    self.wallet.public_key, self.blockchain.get_balance()))
            elif choice == "3":
                self.print_blockchain()
            elif choice == "4":
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif choice == "5":
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif choice == "6":
                self.wallet.save_keys()
            elif choice == "q":
                waiting_for_input = False
            else:
                print("Invalid choice")
            if not Verification.verify_blockchain(self.blockchain.get_chain()):
                print("Invalid blockchain")
                break


# start the node
"""built in __name__ variable

this variable holds the name of the files(a.k.a modules) that are executed (even imports)
if we run node.py, it will be given the name "__main__"
therefore if we can control some part of code to only execute based on the value of __name__

"""

if __name__ == "__main__":
    node = Node()
    node.listen_for_choice()
