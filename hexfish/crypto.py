
import os

try:
    import Crypto.Cipher.Blowfish as blowfish
except ImportError:
    try:
        import pyBlowfish as blowfish

    except ImportError:
        blowfish = None
        print("\002\0034No Blowfish implementation")
        print("This module requires one of PyCrypto, pyBlowfish")
        raise ImportError

try:
    from Crypto.Util.strxor import strxor as xorbytes
except ImportError:
    # define a slower python xor
    def xorbytes(a, b):
        '''
        xor two byte strings of equivalent length
        '''
        if len(a)!=len(b):
            raise ValueError('strings not of equivalent length')
        xored = bytearray()
        for ac, bc in zip(a, b):
            xored.append(ac ^ bc)
        return bytes(xored)

def int_to_bytes(n):
    '''
    Convert an integer to bytes stored in big-endian format.
    '''
    if n == 0:
        return bytes(1)
    b = []
    while n:
        b.insert(0, n&0xFF)
        n >>= 8
    return bytes(b)

def bytes_to_int(b):
    '''
    Convert an bytes stored in big-endian format to an integer.
    '''
    n = 0
    for p in b:
        n <<= 8
        n += p
    return n

def padto(msg, length):
    '''
    Pads msg with 0s until it's length is divisible by 'length'.
    Does nothing if this is already true.
    '''
    l = len(msg)
    if l % length:
        msg += bytes(length - l % length)
    assert len(msg) % length == 0
    return msg

def cbc_encrypt(func, data, blocksize):
    '''
    Uses func to encrypt data in CBC mode using a randomely generate IV.
    The IV is prefixed to the ciphertext.

    args:
        func:       a function that encrypts data in ECB mode
        data:       plaintext
        blocksize:  block size of the cipher
    '''
    assert len(data) % blocksize == 0

    iv = os.urandom(blocksize)
    assert len(iv) == blocksize

    ciphertext = iv
    for block_index in range(len(data) // blocksize):
        xored = xorbytes(data[:blocksize], iv)
        enc = func(xored)

        ciphertext += enc
        iv = enc
        data = data[blocksize:]

    assert len(ciphertext) % blocksize == 0
    return ciphertext

def cbc_decrypt(func, data, blocksize):
    assert len(data) % blocksize == 0

    iv = data[0:blocksize]
    data = data[blocksize:]

    plaintext = b''
    for block_index in range(len(data) // blocksize):
        temp = func(data[0:blocksize])
        temp2 = xorbytes(temp, iv)
        plaintext += temp2
        iv = data[0:blocksize]
        data = data[blocksize:]

    assert len(plaintext) % blocksize == 0
    return plaintext
