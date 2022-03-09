from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

my_flask_app = Flask(__name__)

# allow the flask app to receive requests from other clients
CORS(my_flask_app)

# create endpoints:


@my_flask_app.route("/", methods=["GET"])
def get_node_ui():
    return send_from_directory("ui", "node.html")


@my_flask_app.route("/network", methods=["GET"])
def get_network_ui():
    return send_from_directory("ui", "network.html")


@my_flask_app.route("/api/wallet", methods=["POST"])
def create_wallet():
    my_wallet.create_keys()
    if my_wallet.save_keys():
        global blockchain
        blockchain = Blockchain(my_wallet.public_key, chosen_port)
        response = {
            "message": "Wallet saved successfully",
            "public_key": my_wallet.public_key,
            "private_key": my_wallet.private_key,
            "balance": blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Failed to save wallet"
        }
        return jsonify(response), 500


@my_flask_app.route("/api/wallet", methods=["GET"])
def load_wallet():
    if my_wallet.load_keys():
        global blockchain
        blockchain = Blockchain(my_wallet.public_key, chosen_port)
        response = {
            "message": "Wallet loaded successfully",
            "public_key": my_wallet.public_key,
            "private_key": my_wallet.private_key,
            "balance": blockchain.get_balance()
        }
        return jsonify(response), 200
    else:
        response = {
            "message": "Failed to load wallet"
        }
        return jsonify(response), 500


@my_flask_app.route("/api/balance", methods=["GET"])
def get_balance():
    result = blockchain.get_balance()
    if result != None:
        response = {
            "balance": result
        }
        return jsonify(response), 200
    else:
        response = {
            "message": "Failed to get balance",
            "wallet_set_up": blockchain.hosting_node_id != None
        }
        return (jsonify(response), 500)


@my_flask_app.route("/api/transaction", methods=["POST"])
def add_transaction():
    client_data = request.get_json()
    if client_data == None:
        response = {
            "message": "No data found"
        }
        return (jsonify(response), 400)
    else:
        required_fields = ["recepient", "amount"]
        is_valid = all(field in client_data for field in required_fields)
        if is_valid:
            signature = my_wallet.sign_transaction(
                my_wallet.public_key, client_data["recepient"], client_data["amount"])
            if blockchain.add_transaction(client_data["recepient"], my_wallet.public_key, signature, client_data["amount"]):
                response = {
                    "message": "Transaction successful",
                    "transaction": {
                        "sender": my_wallet.public_key,
                        "recepient": client_data["recepient"],
                        "amount": client_data["amount"],
                        "signature": signature
                    },
                    "balance": blockchain.get_balance(),
                }
                return jsonify(response), 201
            else:
                response = {
                    "message": "Failed to add transaction"
                }
                return jsonify(response), 500
        else:
            response = {
                "message": "Missing required fields: recepient or amount or both"
            }
            return jsonify(response), 400


@my_flask_app.route("/api/broadcast-transaction", methods=["POST"])
def broadcast_transaction():
    passed_data = request.get_json()
    if passed_data == None:
        response = {
            "message": "No data found"
        }
        return (jsonify(response), 400)
    else:
        required_fields = ["sender",  "recepient", "signature", "amount"]
        is_valid = all(field in passed_data for field in required_fields)
        if is_valid:
            is_successful = blockchain.add_transaction(
                passed_data["recepient"], passed_data["sender"], passed_data["signature"], passed_data["amount"], from_broadcast=True)
            if is_successful:
                response = {
                    "message": "Added broadcasted transaction successfully",
                    "transaction": {
                        "sender": passed_data["sender"],
                        "recepient": passed_data["recepient"],
                        "amount": passed_data["amount"],
                        "signature": passed_data["signature"]
                    },
                }
                return jsonify(response), 201
            else:
                response = {
                    "message": "Failed to add broadcasted transaction"
                }
                return jsonify(response), 500
        else:
            response = {
                "message": "Missing one or more required fields: sender, recepient, signature, amount"
            }
            return jsonify(response), 400


@my_flask_app.route("/api/broadcast-block", methods=["POST"])
def broadcast_block():
    passed_data = request.get_json()
    if passed_data == None:
        response = {
            "message": "No data found"
        }
        return (jsonify(response), 400)

    if "block" not in passed_data:
        response = {
            "message": "Missing required field: block."
        }
        return (jsonify(response), 400)

    if passed_data["block"]["index"] == blockchain.get_chain()[-1].index + 1:
        if blockchain.add_block(passed_data["block"]):
            response = {
                "message": "Block added successfully"
            }
            return jsonify(response), 201
        else:
            response = {
                "message": "Block seems invalid"
            }
            return jsonify(response), 500

    elif passed_data["block"]["index"] > blockchain.get_chain()[-1].index:
        pass
    else:
        response = {
            "message": "Blockchain seems to be shorter, block not added."
        }
        return jsonify(response), 409


@my_flask_app.route("/api/transactions", methods=["GET"])
def get_open_transactions():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [t.__dict__ for t in transactions]
    return jsonify(dict_transactions), 200


@my_flask_app.route("/api/mine", methods=["POST"])
def mine():
    block = blockchain.mine_block()

    if block != None:
        dict_block = block.__dict__.copy()
        dict_block["transactions"] = [
            t.__dict__ for t in dict_block["transactions"]]
        response = {
            "message": "Block added successfully",
            "block": dict_block,
            "balance": blockchain.get_balance()
        }
        return (jsonify(response), 201)
    else:
        response = {
            "message": "Failed to add a block",
            "wallet_set_up": blockchain.hosting_node_id != None
        }
        return (jsonify(response), 500)


@my_flask_app.route("/api/chain", methods=["GET"])
def get_chain():
    chain_snapshot = blockchain.get_chain()
    # we copy every block we create a dict version for i.e block.__dict__.copy(), because we are going to manipulate it
    dict_chain_snapshot = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain_snapshot:
        dict_block["transactions"] = [
            t.__dict__ for t in dict_block["transactions"]]

    # return statements of routes normally takes a tuples: value1 => data, value2 => status code
    return (jsonify(dict_chain_snapshot), 200)


@my_flask_app.route("/api/node", methods=["POST"])
def add_node():
    # check if client sent any data
    client_data = request.get_json()
    if not client_data:
        response = {
            "message": "No data attached"
        }
        return jsonify(response), 400

    # check if node key is present in data sent
    if not "node" in client_data:
        response = {
            "message": "No node data found"
        }
        return jsonify(response), 400

    blockchain.add_node(client_data["node"])
    response = {
        "message": "Node added successfully",
        "peer_nodes": blockchain.get_nodes()
    }
    return jsonify(response), 201


@my_flask_app.route("/api/node/<node_url>", methods=["DELETE"])
def remove_node(node_url):
    if node_url == "" or node_url == None:
        response = {
            "message": "No node data attached"
        }
        return jsonify(response), 400

    blockchain.remove_node(node_url)
    response = {
        "message": "Node removed successfully",
        "peer_nodes": blockchain.get_nodes()
    }
    return jsonify(response), 200


@my_flask_app.route("/api/nodes", methods=["GET"])
def get_nodes():
    response = {
        "peer_nodes": blockchain.get_nodes()
    }
    return jsonify(response), 200


# spin up server only if node.py is executed
if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=7700)
    # extract the passed arguments
    args = parser.parse_args()
    chosen_port = args.port
    my_wallet = Wallet(chosen_port)
    blockchain = Blockchain(my_wallet.public_key, chosen_port)
    my_flask_app.run(host="0.0.0.0", port=chosen_port)
