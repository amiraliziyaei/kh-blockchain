import hashlib
import time
from flask import *
from urllib.parse import urlparse
import requests
import mercle
import validating
class Blockchain:

    def __init__(self):
        self.chain = []
        self.mem = []
        self.addrs = {
            
        }
        self.index = 0
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


        if validating.verify(proof, pv_proof, pv_hash) is not False:

            current_hash = validating.verify(proof, pv_proof, pv_hash)
            Mercle = mercle.root(self.mem)
            block = {
            "index": self.index,
            "time-stamp": time.time(),
            "hash": current_hash,
            "pv-hash": pv_hash,
            "tnxs": self.mem,
            "proof": proof,
            "mercle": Mercle.get_root()
            }

            self.mem = []
            self.chain.append(block)
            self.index += 1

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
        while validating.verify(proof, pv_proof, pv_hash) is False:
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

                if length > max_length and validating.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

