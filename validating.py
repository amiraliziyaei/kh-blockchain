import hashlib
import mercle
def valid_chain(self, chain):
    i = 0
    last_block = chain[0]
    while i < len(chain):
        block = chain[i]
        pv_block_hash = last_block["hash"]
        proof = block["proof"]
        pv_proof = last_block["proof"]
        pv_hash = pv_block_hash
        Mercle = mercle.root(block["tnxs"])
        root = Mercle.get_root()
        if block["pv-hash"] != pv_block_hash:
            return False
            
        if type(self.verify(proof, pv_proof, pv_block_hash)) is not str:
            return False
            
        if root is not block["mercle"]:
            return False
            
        return True
            

def verify(self, proof, pv_proof, pv_hash):
    guess = f'{proof}{pv_proof}{pv_hash}'.encode()
    guess = hashlib.sha256(guess).hexdigest()
    if guess[(len(guess) - len(self.diff)):] == self.diff:
        return guess
    else:
        return False
        