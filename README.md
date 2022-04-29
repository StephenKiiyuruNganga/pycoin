# pycoin
A simple blockchain system that uses the real world blockchain principles such as Proof of Work, Hashing and Decentralized data.

## Screenshot
![pc1](https://user-images.githubusercontent.com/40911055/165928944-c627fe6d-9e83-47ec-b6c0-75a69d208962.png)


## Features

- Chain of data(blocks)
- Mine new blocks: Proof of work
- Block hashing
- Analyze and verify a block
- Process transactions using a wallet
- Save the blockchain to disk (a local txt file)
- Node network
- Share data and resolve conflicts between peer nodes
- Web interface to transact and resolve conflicts

## Roadmap

- [ ]  Remove legacy code
- [ ]  Improve error handling
- [ ]  Improve scalability
- [ ]  Improve broadcasting with Async Programming and/ or Scheduling
- [ ]  Control mining difficulty (Dynamically)
- [ ]  Add a Merkle Tree for Transaction Validation

## Dependencies
- Flask (https://flask.palletsprojects.com/en/2.1.x/)
- Requests (https://docs.python-requests.org/en/latest/)
- Pycryptodome (http://pycryptodome.readthedocs.io/en/latest/index.html)

## Run Locally

Clone the project

```bash
  git clone https://github.com/StephenKiiyuruNganga/pycoin.git
```

Go to the project directory

```bash
  cd pycoin
```

Start the first peer node server. This will be on localhost:7700 by default

```bash
  python node.py
```

In a NEW terminal, start the second peer node server. (Example below uses port 7701 but can use whichever port you like)

```bash
  python node.py --port 7701
```


# How to transact

1. Open your browser and load each url. For example, your first tab can load localhost:7700 and the second tab can load localhost:7701. Now we shall refer to tab 1 as peer node 1 and the other as peer node 2

2. Using any peer node, Click on Network and add the url for the other peer. See example below:

![pc4](https://user-images.githubusercontent.com/40911055/165932617-f6064ad9-f63a-4a57-8b31-5bdaf523a7cd.png)

3. Create a wallet for each peer node using the "Create New Wallet" button

4. Add the public key of the other peer node. See example below:

![pc3](https://user-images.githubusercontent.com/40911055/165933202-cf0faa3c-6507-4e8e-892d-dad124582bc7.png)

5. Add an amount you wish to send and click send

6. Using the other peer node, click "Load blockchain". The balance of that peer node should now reflect the amount that was sent to it


# Other actions

1. To view the blockchain data, go to Blockchain tab and click the "Load Blockchain" button
2. To view open transactions, go to Open Transactions tab and click "Load Transactions"
 

## Acknowledgements

- This project was part of the python course : Python - The Practical Guide https://www.udemy.com/course/learn-python-by-building-a-blockchain-cryptocurrency/?couponCode=D_0422
- Here is my certificate: ![Python Cert](https://user-images.githubusercontent.com/40911055/165930333-84e6df79-69f7-40e7-818d-c25f94a41ce6.jpg)

