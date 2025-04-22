"""
File for handeling all cryptology based activities for data integerity and security 
"""

"""
plan:

https://cryptography.io/en/latest/hazmat/primitives/asymmetric/dh/

do Diffie-Hellman key exchange with the server pricate key being the nut
and the client key being the key that users will use to access.


"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import base64
import os


from enum import Enum
from pathlib import Path
# from Crypto.Cipher import AES
# from Crypto.PublicKey import RSA
# from Crypto.Hash import SHA256, MD5
# from Crypto import Random
from typing import Any, List, Dict, ByteString, Union, Optional
from dataclasses import dataclass, field

class HashTypes(Enum):
    MD5='MD5'
    SHA256="SHA256"

class KeyType(Enum):
    PUBLIC="PUBLIC"
    PRIVATE="PRIVATE"
    SHARED="SHARED"

def write_bytes_to_file(filepath:Path, value:bytes):
    try:
        with open(filepath, "wb") as f:
                f.write(value)
    except FileNotFoundError as error:
        raise FileNotFoundError(f'file not found. error={error}')
    except IOError as error:
        raise IOError(f'Could not write to file. error={error}')
    except Exception as error:
        raise Exception(f'Something went wrong! Error={error}')

def read_string_from_file(filepath:Path)->str:
    try:
        with open(filepath, "r") as private_file:
            found_value = private_file.read()
    except FileNotFoundError as error:
        raise FileNotFoundError(f'file not found. error={error}')
    except IOError as error:
        raise IOError(f'Could not read from file. error={error}')
    except Exception as error:
        raise Exception(f'Something went wrong! Error={error}')

    return found_value

# RSA keys class that is able to generate keys and load keys from file
@dataclass(frozen=True)
class RSAKeys():
    # key filepaths
    private_filepath:Path
    private: rsa.RSAPrivateKey

    public_filepath:Path
    public: rsa.RSAPublicKey

    @classmethod
    def generate_and_save_new_keys(cls, save_folder:Path, key_name:str):
        private_path:Path = save_folder.joinpath(f'{key_name}_private.pem')
        public_path:Path = save_folder.joinpath(f'{key_name}_public.pem')
        
        # random_generator = Random.new().read
        generated_private_key = rsa.generate_private_key(public_exponent=65537,
                                                         key_size=2048,
                                                         )
        
        private_pem = generated_private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                            format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                            encryption_algorithm=serialization.NoEncryption())

        generated_public_key = generated_private_key.public_key()

        public_pem = generated_public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                            format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                            encryption_algorithm=serialization.NoEncryption())

        # now write the keys to file
        write_bytes_to_file(filepath=private_path, 
                            value=private_pem)

        write_bytes_to_file(filepath=public_path,
                            value=public_pem)

        return cls(private_path, generated_private_key, public_path, generated_public_key)

    @classmethod
    def load_keys_from_file(cls, save_folder:Path, key_name:str):
        private_path:Path = save_folder.joinpath(f'{key_name}_private.pem')
        public_path:Path = save_folder.joinpath(f'{key_name}_public.pem')

        # now read the keys to file
        found_private_keyfile_value = read_string_from_file(filepath=private_path)
        try:
            found_private_key = RSA.importKey(found_private_keyfile_value)
        except ValueError as error:
            raise ValueError(f'Error: Invalid key data. Error={error}')

        found_public_keyfile_value = read_string_from_file(filepath=public_path)
        try:
            found_public_key = RSA.importKey(found_public_keyfile_value)
        except ValueError as error:
            raise ValueError(f'Error: Invalid key data. Error={error}')
        
        return cls(private_path, found_private_key, public_path, found_public_key)

@dataclass
class AESKeys():
    clear_aes:bytes

    @classmethod
    def generate_new_clear_aes(cls):
        pass

def generate_aes_key(rsa_key_path:Path):
    """
    Function responsible for generating an AES encryption key.
    uses a RSA key to encrypt it and store as string in Security file.
    """
    rsa_key = RSA.importKey()

def load_aes_key():
    """
    Function for reading and loading encryption key file that has been encrypted with RSA key
    uses a RSA key to decrypt and then return as hex
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

def get_hash_bytes(message:bytes, hash_type: HashTypes ):
    """
    Function to managed getting the SHA256 hash
    """
    hash:hashes.Hash # = None
    
    if hash_type is HashTypes.MD5:
        hash = hashes.Hash(hashes.MD5())
    elif hash_type is HashTypes.SHA256:
        hash = hashes.Hash(hashes.SHA256())
    else:
        raise Exception(f'{str(hash_type)} is not an allowed hash security type')
    
    hash.update(message)
    return hash.finalize()