"""
File for handeling all cryptology based activities for data integerity and security 
"""

"""
plan:

https://cryptography.io/en/latest/hazmat/primitives/asymmetric/dh/

do Diffie-Hellman key exchange with the server pricate key being the nut
and the client key being the key that users will use to access.


"""


from enum import Enum
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, MD5
from typing import Any, List, Dict, ByteString, Union, Optional

class HashTypes(Enum):
    MD5='MD5'
    SHA256="SHA256"

def generate_encryption_key():
    """
    Function responsible for generating an encryption key to be used by entire data nut.
    uses a RSA key to encrypt it and store as a file after generation.
    """
    pass

def load_encryption_key():
    """
    Function for reading and loading encryption key file that has been encrypted with RSA key
    uses a RSA key to decrypt and then store string
    """
    pass

def encrypt_file():
    """
    Function for encrypting a file after all data manager operations are complete
    """
    pass

def decrypt_file():
    """
    Function for decrypting a file prior to data manager operations
    """
    pass

def get_hash(message:Union[bytes, str], hash_type: HashTypes ):
    """
    Function to managed getting the SHA256 hash
    """
    hash:Union[SHA256.SHA256Hash, MD5.MD5Hash] # = None
    
    if hash_type is HashTypes.MD5:
        hash = MD5.new()
    elif hash_type is HashTypes.SHA256:
        hash = SHA256.new()
    else:
        raise Exception(f'{str(hash_type)} is not an allowed hash security type')
    
    hash.update(message)
    return hash.hexdigest()