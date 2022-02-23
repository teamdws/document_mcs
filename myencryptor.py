import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

class AESCipher:
    def __init__(self, key, iv):
        self.key = hashlib.sha256(key.encode('utf-8')).hexdigest()[:32].encode("utf-8")
        self.iv = hashlib.sha256(iv.encode('utf-8')).hexdigest()[:16].encode("utf-8")

  

    def encrypt( self, raw ):
        raw = raw.encode('utf-8')
        raw = pad(raw, AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv )
        return unpad(cipher.decrypt(enc) , AES.block_size )