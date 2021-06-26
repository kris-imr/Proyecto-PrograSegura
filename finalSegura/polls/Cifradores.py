from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os, base64, random, string


def generador_clave(tamagnio = 16, caracteres=string.ascii_letters + string.digits + string.punctuation):
    return ''.join(random.choice(caracteres) for _ in range(tamagnio))


def bin_str(texto_bin):
    texto_str=base64.b64encode(texto_bin)
    texto_str=texto_str.decode('utf-8')
    return texto_str

def str_bin(texto_str):
    texto_bin=base64.b64decode(texto_str)
    return texto_bin

def generar_iv():
    iv=os.urandom(16)
    return iv

def generar_llave_aes_from_password(password):
    password = password.encode('utf-8')
    derived_key = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'handshake data ',backend=default_backend()).derive(password)
    return derived_key

def cifrar(texto, llave_aes, iv):
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),backend=default_backend())
    cifrador = aesCipher.encryptor()
    cifrado = cifrador.update(texto)
    cifrador.finalize()
    return cifrado

def descifrar(cifrado, llave_aes, iv):
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),backend=default_backend())
    descifrador = aesCipher.decryptor()
    plano = descifrador.update(cifrado)
    descifrador.finalize()
    return plano