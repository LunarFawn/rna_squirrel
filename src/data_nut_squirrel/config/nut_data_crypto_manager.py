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
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, MD5
from Crypto import Random
from typing import Any, List, Dict, ByteString, Union, Optional
from dataclasses import dataclass, field

class HashTypes(Enum):
    MD5='MD5'
    SHA256="SHA256"

class KeyType(Enum):
    PUBLIC="PUBLIC"
    PRIVATE="PRIVATE"
    SHARED="SHARED"

@dataclass(frozen=True)
class RSAKeys():
    # key filepaths
    private_filepath:Path
    private: bytes

    public_filepath:Path
    public: bytes

    @classmethod
    def generate_and_save_new_keys(cls, save_folder:Path, key_name:str):
        private_path:Path = save_folder.joinpath(f'{key_name}_private.pem')
        public_path:Path = save_folder.joinpath(f'{key_name}_public.pem')
        
        random_generator = Random.new().read
        key = RSA.generate(2048, random_generator)
        generated_private_key = key.exportKey()
        generated_public_key = key.publickey().exportKey()

        # now write the keys to file
        with open(private_path, "wb") as f:
            f.write(generated_private_key)

        with open(public_path, "wb") as f:
            f.write(generated_public_key)

        return cls(private_path, generated_private_key, public_path, generated_public_key)

    @classmethod
    def load_keys_from_file(cls, save_folder:Path, key_name:str):
        private_path:Path = save_folder.joinpath(f'{key_name}_private.pem')
        public_path:Path = save_folder.joinpath(f'{key_name}_public.pem')

        # now read the keys to file
        found_private_key:bytes = bytes()
        found_public_key: bytes = bytes()
        try:
            with open(private_path, "wb") as private_file:
                found_private_key = private_file.read()

            with open(public_path, "wb") as public_file:
                found_public_key = public_file.read()   
        except Exception as error:
            raise Exception(f'Failed to read from key(s). Error={error}')
        
        return cls(private_path, found_private_key, public_path, found_public_key)
        
def generate_rsa_key_file(save_path:Path):
    """
    Function responsible for generating the RSA key that is used to encrypt the AES key
    """
    pass

def load_rsa_keys(private_rsa_key_filepath:Path, public_rsa_filepath:Path):
    """
    Function for loading the RSA key. Enum is passed to determine if the private or public key is retreived
    """
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