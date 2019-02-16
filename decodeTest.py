#############################################################
#                                                           #
#   Use this to test if your  string was encoded correctly  #
#                                                           #
#############################################################

import base64
import os
import cryptography

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

keyFile = open('test.key', 'rb')
key = keyFile.read() # The key will be type bytes
keyFile.close()

f = Fernet(key)

encryptedTokenFile = open('test.encrypted', 'rb')
encryptedToken = encryptedTokenFile.read()

decryptedToken = f.decrypt(encryptedToken)

print(decryptedToken.decode())