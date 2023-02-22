import hashlib
import time
from flask import *
from urllib.parse import urlparse
import requests

class Blockchain:

    def __init__(self):
        self.chain = []
        self.index = 0
        self.mem = []
        self.nodes = []
        self.genesis_hash = 64 * "0"
        self.diff = "00000"


    def register_nodes(self, address):
        """
            register a new node for consensus algo
            :param address : ip of the node want to join to network
            :type address : str
            :returns : True / False
            :rtype: boolean
        """
        parsed_url = urlparse(address)


        if parsed_url.netloc:
            self.nodes.append(parsed_url.netloc)
            return True
        else:
            return False


    def new_block(self, proof):
        """
            add new block to chain with validation layers
            :param proof : a random nunce founded in proof_of_work function
            :type proof : int
            :returns : False if can not create block
            :rtype: boolean
        """
        if self.consensus():
            return False


        if self.index == 0:
            pv_hash = self.genesis_hash
            pv_proof = "0"

        else:
            pv_hash = self.chain[len(self.chain) - 1]["hash"]
            pv_proof = self.chain[len(self.chain) - 1]["proof"]


        if self.verify(proof, pv_proof, pv_hash) is not False:

            current_hash = self.verify(proof, pv_proof, pv_hash)

            block = {
            "index": self.index,
            "time-stamp": time.time(),
            "hash": current_hash,
            "pv-hash": pv_hash,
            "tnxs": self.mem,
            "proof": proof
            }

            self.mem = []
            self.chain.append(block)
            self.index += 1

        else:
            return False


    def verify(self, proof, pv_proof, pv_hash):
        """
            verify blocks to chain
            :param proof: proof founded
            :type proof: int
            :param pv_proof: previous block proof
            :type pv_proof: int / str
            :param pv_hash: previous block hash
            :type pv_hash: str
            :returns: verified hash or False (invalid proof)
            :rtype: str / boolean
        """

        guess = f'{proof}{pv_proof}{pv_hash}'.encode()
        guess = hashlib.sha256(guess).hexdigest()


        if guess[(len(guess) - len(self.diff)):] == self.diff:
            return guess

        else:
            return False


    def proof_of_work(self):
        """
            simple - buildIn function for finding Proof number
            :returns: full history chain
            :rtype: list
        """

        if self.index == 0:
            pv_hash = self.genesis_hash
            pv_proof = "0"

        else:
            pv_hash = self.chain[len(self.chain) - 1]["hash"]
            pv_proof = self.chain[len(self.chain) - 1]["proof"]

        proof = 0
        while self.verify(proof, pv_proof, pv_hash) is False:
            proof += 1

        self.new_block(proof)
        return self.chain


    def consensus(self):
        """
            when this node find a node that have a longer and safe chain, replace that with local chain
            :returns: boolean if a longer-chain node exist
            :rtype: boolean
        """

        nodes = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in nodes:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
            time.sleep(0.1)

        if new_chain:
            self.chain = new_chain
            return True

    def valid_chain(self, chain):
        """
            for consensus function - verifying whole chain to replace
            :param chain: full chain history received from another node
            :type chain: list
            :returns: return True when replacing state is success
            :rtype: boolean 
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            last_block_hash = last_block["hash"]

            if block['pv-hash'] != last_block_hash:
                return False

            if self.verify(block['proof'], last_block['proof'], last_block_hash) != True:
                return True

            last_block = block
            current_index += 1
            
            return True


while True:
    blockchain = Blockchain()
    app = Flask(__name__)
 
    @app.route('/chain', methods=['get'])
    def full_chain():
        response = {
            "chain": blockchain.chain,
            "length": len(blockchain.chain)
        }
        return jsonify(response), 200

    @app.route('/node', methods=["GET"])
    def register_node():
        node = request.args.get('node')
        if blockchain.register_nodes(node):
            response = {
                "status": "created",
                "message": "node <{node_address}> added successfuly".format(node_address = node)
            }
        else:
            response = {
                "status": "failed",
                "message": "node <{node_address}> - failing add".format(node_address=node)
            }
        return jsonify(response), 201

    @app.route('/consensus', methods=["GET"])
    def resolve_conflicts():
        if blockchain.consensus():
            response = {
                "status": "ok",
                "message": "chain was replaced successfuly",
                "value": blockchain.chain
            }
        else:
            response = {
                "status": "ok",
                "message": "chain is authoritative",
                "value": blockchain.chain
            }
        return jsonify(response), 200
    
    @app.route('/mine', methods=["GET"])
    def mining():
        if blockchain.proof_of_work():
            response = {
                "status": "created",
                "message": "new block creatived",
                "value": blockchain.chain[-1]
            } 
        else:
            response = {
                "value": "fail",
                "message": "new block creation failed"
            }
        return jsonify(response), 201
    app.run("0.0.0.0", 5000) 