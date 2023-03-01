import hashlib
import json
from ecdsa import SigningKey, VerifyingKey, SECP256k1
class addr:
    def __init__(self):
        pass
    def generate_new_address(self):
        sk = SigningKey.generate(curve=SECP256k1)
        vk = sk.get_verifying_key()
        sk = sk.to_pem()
        pk = vk.to_pem()
        return {
            "secret": str(sk),
            "public": str(pk)
        }
    @staticmethod
    def sign(self, sk, msg):
        sk = SigningKey.from_pem(sk.encode())
        sig = sk.sign(msg)
        return sig
    def ver(self, pk, sig, msg):
        is_valid = pk.verify(sig, msg)
        return is_valid

a = addr()
print(a.generate_new_address())
sk = input("secret")
msg = input("message")
print(a.sign(sk, msg))
pk = input("public")
sig = input("signature")
msg = input("message")
print(a.ver(pk, sig, msg))