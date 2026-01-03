import hashlib
import os
from argon2 import PasswordHasher
from passlib.hash import argon2

SHA_256 = "sha256"
SHA_512 = "sha512"
ARGON_2 = "argon2"

def universal_hash(item,option):

    if option == SHA_256:

        salt = str(os.urandom(16))
        hashed = hashlib.sha256((salt+item).encode("utf-8"))

        return (hashed.hexdigest(),salt)
    
    elif option == SHA_512:

        salt = str(os.urandom(16))
        hashed = hashlib.sha512((salt+item).encode("utf-8"))

        return (hashed.hexdigest(),salt)
    
    elif option == ARGON_2:

        return (argon2.hash(item) , None)
    

    return None

def universal_verify(item,hash,salt,option):

    if option == SHA_256:

        converted = hashlib.sha256((salt+item).encode('utf-8')).hexdigest()
        return converted == hash
    
    elif option == SHA_512:

        converted = hashlib.sha512((salt+item).encode('utf-8')).hexdigest()
        return converted == hash
    
    elif option == ARGON_2:

        return argon2.verify(item, hash)
    
    return None


