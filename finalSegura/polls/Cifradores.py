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


print()


#password=generador_clave()
#password="r0103asc7am"
#"Esta es la contraseña del usuario logueadp"
#passwordCredencial ="TGMrXG+=b9]r"
"Esta es la contraseña de la credencial a almacenar"
#iv = generar_iv()
#ivCorrecto = bin_str(iv)
#llave_aes = generar_llave_aes_from_password(password)
#pas = passwordCredencial.encode('utf-8')
"Guardamos la contraseña de la credencial en una variable"

#pasCifrado = cifrar(pas,llave_aes,iv)
#pasCifradoTexto = bin_str(pasCifrado)


#print("La contraseña generada es: ", password)
#print ("contraseña aleatoria es ----> ",password, "<----Esta es la que tomo como master password")
#print("La credencial que se quiere cifrar es: ", passwordCredencial)
#print("La credencial cifrada es: ", pasCifradoTexto)
#print ()
#print ()
#print ("Descifrar el password de la credencial")
#print ()
#print ()
#cifrado = pasCifradoTexto
#cifradobin = str_bin(cifrado)
#ivbin = str_bin(ivCorrecto)
#llave2 = generar_llave_aes_from_password(password)
#descifradobin = descifrar(cifradobin,llave2,ivbin)
#cifradotexto=descifradobin.decode('utf-8')
#print ()
#print ("La credencial descifrada es: ", cifradotexto)
#print ()

#print (generador_clave())

#print ()
#print ()
#print ()

#print (iv)
#print (ivCorrecto)