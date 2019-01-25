###################################################
#   
#   This will create a key file for a slack token
#
###################################################

import base64
import os
import cryptography

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

key = Fernet.generate_key()

keyName = raw_input("Enter the name of the key file:\n")

keyFileName =  (('{0}.key').format(keyName))

keyFile = open(keyFileName, 'wb')
keyFile.write(key)
keyFile.close()

token = raw_input("Paste slack token:\n")

message = token.encode()
f = Fernet(key)
encrypted = f.encrypt(message)

encryptedFileName = (('{0}.encrypted').format(keyName))

encodedTokenFile = open(encryptedFileName,'wb')

encrypted = encrypted.decode()

encodedTokenFile.write(encrypted)
encodedTokenFile.close()