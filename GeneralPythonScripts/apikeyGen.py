from binascii import hexlify
import os 

key = hexlify(os.urandom(10))

print(key.decode())
