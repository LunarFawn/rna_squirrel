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

def read_string_from_file(filepath:Path)->Union[str,RSA._RSAobj]:
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
    private: RSA._RSAobj

    public_filepath:Path
    public: RSA._RSAobj

    @classmethod
    def generate_and_save_new_keys(cls, save_folder:Path, key_name:str):
        private_path:Path = save_folder.joinpath(f'{key_name}_private.pem')
        public_path:Path = save_folder.joinpath(f'{key_name}_public.pem')
        
        random_generator = Random.new().read
        generated_private_key = RSA.generate(2048, random_generator)
        generated_public_key = generated_private_key.publickey()

        # now write the keys to file
        write_bytes_to_file(filepath=private_path, 
                            value=generated_private_key.exportKey())

        write_bytes_to_file(filepath=public_path,
                            value=generated_public_key.exportKey())

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