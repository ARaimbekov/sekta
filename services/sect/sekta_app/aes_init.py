from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode

BLOCK_SIZE = 32
IV = b'secure change me'

def encrypt(message, key):
    cipher = AES.new(key, AES.MODE_CBC, IV)
    encrypted_data = cipher.encrypt(pad(message, BLOCK_SIZE))
    return b64encode(bytes(encrypted_data)).decode("utf8")
