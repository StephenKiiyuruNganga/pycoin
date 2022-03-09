from utility.my_hash_utils import hash_block, my_hash
from wallet import Wallet


class Verification:
    @staticmethod
    def valid_proof(transactions, last_hash, proof_number):
        result = (str([t.to_ordered_dict() for t in transactions]) +
                  str(last_hash) + str(proof_number)).encode()
        result_hash = my_hash(result)
        print(f"[+] Hash from proof number {proof_number}: {result_hash:>20}")
        return result_hash[0:2] == "00"

    @classmethod
    def verify_blockchain(cls, blockchain):
        for (idx, block) in enumerate(blockchain):
            if idx == 0:
                continue
            print(f"[+] Checking if block {idx} has valid hash...")
            if block.previous_hash != hash_block(blockchain[idx - 1]):
                return False
            print(f"[+] Checking if block {idx} has valid proof number...")
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance):
        # check whether the sender has enough coin to send the requested amount
        sender_balance = get_balance(transaction.sender)
        return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
