from flask import *
import node
blockchain = node.Blockchain()

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