from .models import Sektant, Sekta, Nickname
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

BLOCK_SIZE = 32
IV = b'secure change me'


def is_belong(sekta, sektant):
    participants = Nickname.objects.filter(sekta=sekta)
    for participant in participants:
        if participant.sektant == sektant:
            return True
    return False


def encrypt(message, key):
    cipher = AES.new(key, AES.MODE_CBC, IV)
    return cipher.encrypt(pad(message, BLOCK_SIZE))


def decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_CBC, IV)
    return unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)
