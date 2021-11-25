# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 17:30:46 2021

@author: adria
"""

# Módulo 1. Crear una blockchain 

# Para instalar
# Flask==1.1.2: pip install Flask==1.1.2
# Cliente HTTP Postman: https://www.getpostman.com/

# Importar las librerías
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Parte 1 - Crear la Blockchain
class Blockchain:
    
    # def significa que vamos a definir una funcion
    def __init__(self):
        # Cadena que contendrá los bloques
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0' )
    
    # En este momento ya se ha minado el bloque y ahora se crea
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
            }
        self.chain.append(block)
        return block
    
    # Obtener el último bloque de la cadena
    def get_previous_block(self):
        return self.chain[-1]
    
    # Crear la prueba de trabajo
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # La operación debe ser asimétrica, una operación simétrica sería fácil de predecir
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # Comprobar que las 4 primeras posiciones son 0
            if hash_operation[:4] == '0000': 
                check_proof = True
            else:
                new_proof += 1;
        return new_proof
    
    # Tomar un bloque como parámetro de entrada y devolver su hash para comprobar que es correcto
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        # hexdigest para convertirlo en hexadecimal
        return hashlib.sha256(encoded_block).hexdigest()
    
    # Método para comprobar si la blockchain es válida
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        # Bucle para comprobar los bloques
        while block_index < len(chain):
            current_block = chain[block_index]
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            actual_proof = current_block['proof']
            hash_operation = hashlib.sha256(str(actual_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = current_block
            block_index += 1
        return True

# Parte 2 - Minado de un bloque

# Crear una web app
app = Flask(__name__)

# Crear una Blockchain
blockchain = Blockchain()

# Minar un nuevo bloque
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash(previous_block)
    new_proof = blockchain.proof_of_work(previous_proof)
    block = blockchain.create_block(new_proof, previous_hash)
    response = {
        'message': 'Enhorabuena, has minado un nuevo bloque!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
        }
    return jsonify(response), 200


# Obtener la Blockchain al completo
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
        }
    return jsonify(response), 200

# Reto: Comprobar si un bloque es válido
@app.route('/check_blockchain', methods=['GET'])
def check_blockchain():
    chain = blockchain.chain
    check_chain = blockchain.is_chain_valid(chain)
    if check_chain != True:
        response = {
            'message': 'La blockchain es inválida!'
            }
        return jsonify(response), 200
    else:
        response = {
            'message': 'La blockchain es válida!'
            }
        return jsonify(response), 200
    

# Ejecutar la app
app.run(host = '127.0.0.1', port = 5000)




