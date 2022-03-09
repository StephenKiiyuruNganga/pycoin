# blockchain => a list of blocks(dictionaries) containing: hash of the previous block, an id (idx), list of transactions

from utility.my_hash_utils import hash_block
from transaction import Transaction
from utility.verification import Verification
from wallet import Wallet
from block import Block
import json
import requests

MINING_REWARD = 10


class Blockchain:
    def __init__(self, public_key, node_port):
        self.public_key = public_key
        GENESIS_BLOCK = Block(0, "", [], 100, 0)
        self.__chain = [GENESIS_BLOCK]
        self.__open_transactions = []
        self.__peer_nodes = set()
        self.node_port = node_port
        self.load_data()

    def get_chain(self):
        # return a copy of the chain
        return self.__chain[:]

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open(f"blockchain_data_{self.node_port}.txt", mode="r") as file:
                content = file.readlines()
                blockchain = json.loads(content[0][:-1])
                # [:-1] removes the line break element which is at the end of the line 1 string ie. [blockchain...]\n

                updated_blockchain = []

                for block in blockchain:
                    # updated_block = {
                    #     "previous_hash": block["previous_hash"],
                    #     "index": block["index"],
                    #     "transactions": [OrderedDict([("sender", tx["sender"]), ("recepient", tx["recepient"]), ("amount", tx["amount"])]) for tx in block["transactions"]],
                    #     "proof": block["proof"]
                    # }

                    converted_transactions = [Transaction(
                        t["sender"], t["recepient"], t["signature"], t["amount"]) for t in block["transactions"]]

                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_transactions, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)

                self.__chain = updated_blockchain

                open_transactions = json.loads(content[1][:-1])

                updated_open_transactions = []

                for t in open_transactions:
                    updated_transaction = Transaction(
                        t["sender"], t["recepient"], t["signature"], t["amount"])
                    updated_open_transactions.append(updated_transaction)

                self.__open_transactions = updated_open_transactions

                peer_nodes = json.loads(content[2])
                self.__peer_nodes = set(peer_nodes)

        except (IOError, IndexError):
            print("File not found...\nInitializing data...")

        finally:
            print("Doing some cleanup...")

    def save_data(self):
        try:
            with open(f"blockchain_data_{self.node_port}.txt", mode="w") as file:
                converted_blockchain = [block.__dict__ for block in [Block(b.index, b.previous_hash, [
                    t.__dict__ for t in b.transactions], b.proof, b.timestamp) for b in self.__chain]]
                file.write(json.dumps(converted_blockchain))
                file.write("\n")
                converted_open_transactions = [
                    t.__dict__ for t in self.__open_transactions]
                file.write(json.dumps(converted_open_transactions))
                file.write("\n")
                file.write(json.dumps(list(self.__peer_nodes)))
        except IOError:
            print("Saving failed...")

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof_number = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof_number):
            proof_number += 1

        print(f"Found proof number! It is: {proof_number:>6}")
        return proof_number

    def get_amounts(self, type, participant, location="chain"):
        # open transactions ========> [{'sender': 'Stephen', 'recepient': 'qq', 'amount': 5.5}]
        amounts = None
        if location == "open" and type == "sender":
            amounts = [
                t.amount for t in self.__open_transactions if t.sender == participant]
        elif location == "open" and type == "recepient":
            amounts = [
                t.amount for t in self.__open_transactions if t.recepient == participant]
        elif location == "chain" and type == "sender":
            amounts = [[t.amount for t in block.transactions if t.sender ==
                        participant] for block in self.__chain]
        elif location == "chain" and type == "recepient":
            amounts = [[t.amount for t in block.transactions if t.recepient ==
                        participant] for block in self.__chain]

        print(f"amounts from {location} of type '{type}': {str(amounts):6}")
        # amounts ====> [[], [2.0, 3.0], [4.0]]
        return amounts

    def get_amounts_total(self, amounts):
        total = 0
        for result in amounts:
            if type(result) == list:
                for amount in result:
                    total += amount
            else:
                total += result
        return total

    def get_balance(self, sender=None):
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender

        amounts_sent = self.get_amounts(
            type="sender", participant=participant)
        amounts_sent_open = self.get_amounts(
            type="sender", participant=participant, location="open")
        amounts_received = self.get_amounts(
            type="recepient", participant=participant)
        total_sent = self.get_amounts_total(
            amounts_sent) + self.get_amounts_total(amounts_sent_open)
        total_received = self.get_amounts_total(amounts_received)

        print("total sent =======> " + str(total_sent))
        print("total received =======> " + str(total_received))

        return total_received - total_sent

    def get_last_transaction(self):
        """ Get the last transaction value from the blockchain list """
        if len(self.__chain) < 1:
            return None

        return self.__chain[-1]

    def add_transaction(self, recepient, sender, signature, amount=1.0, from_broadcast=False):
        """ Append a new transaction to the open_transactions list

        Arguments:
        :recepient: who to send the coins to
        :amount: number of coins to be sent (default 1.0)
        """
        # transaction = {
        #     "sender": sender,
        #     "recepient": recepient,
        #     "amount": amount
        # }

        # first check if we have a valid wallet i.e. public key
        # if self.public_key == None:
        #     return False

        transaction_v2 = Transaction(sender, recepient, signature, amount)

        if Verification.verify_transaction(transaction_v2, self.get_balance):
            self.__open_transactions.append(transaction_v2)
            self.save_data()

            # broadcast new transaction to peers only if the transaction originated from the current node
            if not from_broadcast:
                for node in self.__peer_nodes:
                    try:
                        response = requests.post(f"http://{node}/api/broadcast-transaction", json={
                            "sender": sender, "recepient": recepient, "signature": signature, "amount": amount})
                        if response.status_code == 400 or response.status_code == 500:
                            print("[-] Transaction declined, needs resolving.")
                            return False
                    except requests.exceptions.ConnectionError:
                        print(f"[-] Failed to connect to {node}")
                        continue

            return True
        else:
            return False

    def mine_block(self):
        # first check if we have a valid wallet i.e. public key
        if self.public_key == None:
            return None

        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        print("Performing proof of work before rewarding...")
        proof_number = self.proof_of_work()

        # copy open_transactions using range selector
        open_transactions_copy = self.__open_transactions[:]

        # check whether all the open transactions have valid signatures
        for transaction in open_transactions_copy:
            if not Wallet.verify_transaction(transaction):
                return None

        # reward_transaction = {
        #     "sender": "MINING",
        #     "recepient": owner,
        #     "amount": MINING_REWARD
        # }
        reward_transaction_v2 = Transaction(
            "MINING", self.public_key, "", MINING_REWARD)

        open_transactions_copy.append(reward_transaction_v2)

        # block = {
        #     "previous_hash": hashed_block,
        #     "index": len(blockchain),
        #     "transactions": open_transactions_copy,
        #     "proof": proof_number
        # }
        block = Block(len(self.__chain), hashed_block,
                      open_transactions_copy, proof_number)

        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()

        # broadcast new block to peer nodes
        for node in self.__peer_nodes:
            # convert the block object to a dict, same for transaction objects within the block
            converted_block = block.__dict__.copy()
            converted_block["transactions"] = [
                t.__dict__ for t in converted_block["transactions"]]

            try:
                response = requests.post(
                    f"http://{node}/api/broadcast-block", json={"block": converted_block})
                if response.status_code == 409 or response.status_code == 500:
                    print("Block declined, needs resolving")
            except requests.exceptions.ConnectionError:
                continue

        return block

    def add_node(self, node):
        """ Adds a node to the peer nodes set

        Arguments:
            :node: The node URL to be added
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_node(self, node):
        """ Removes a node from the peer nodes set

        Arguments:
            :node: The node URL to be removed 
        """
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_nodes(self):
        """ Returns a list of the peer nodes
        """
        return list(self.__peer_nodes)

    # method for peer nodes to add a broadcasted block to their local blockchain
    def add_block(self, broadcasted_block):
        transactions = [Transaction(t["sender"], t["recepient"], t["signature"], t["amount"])
                        for t in broadcasted_block["transactions"]]
        proof_is_valid = Verification.valid_proof(
            transactions[:-1], broadcasted_block["previous_hash"], broadcasted_block["proof"])
        hashes_match = hash_block(
            self.get_chain()[-1]) == broadcasted_block["previous_hash"]

        if not proof_is_valid or not hashes_match:
            return False

        converted_broadcasted_block = Block(
            broadcasted_block["index"], broadcasted_block["previous_hash"], transactions, broadcasted_block["proof"], broadcasted_block["timestamp"])
        self.__chain.append(converted_broadcasted_block)

        # compare the incoming transactions with the local open transactions, if there are any that match, then remove themS
        stored_transactions = self.__open_transactions[:]
        for broadcasted_t in broadcasted_block["transactions"]:
            for stored_t in stored_transactions:
                if stored_t.sender == broadcasted_t["sender"] and stored_t.recepient == broadcasted_t["recepient"] and stored_t.signature == broadcasted_t["signature"] and stored_t.amount == broadcasted_t["amount"]:
                    try:
                        self.__open_transactions.remove(stored_t)
                    except ValueError:
                        print("Item was already removed")

        self.save_data()
        return True
