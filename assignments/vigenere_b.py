
"""
E(m) = ((m1 + k1) % 26, (m2 + k2) % 26, ..., (mi + ki) % 26)
D(m) = ((c1 - k1) % 26, (c2 - k2) % 26, ..., (ci - ki) % 26)
"""
from itertools import cycle

ALPHA = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def encrypt(key, plaintext):
    """Encrypt the string and return the ciphertext"""
    pairs = zip(plaintext, cycle(key))
    result = ''

    for pair in pairs:
        total = reduce(lambda x, y: ALPHA.index(x) + ALPHA.index(y), pair)
        result += ALPHA[total % 26]

    return result.lower()


def decrypt(key, ciphertext):
    """Decrypt the string and return the plaintext"""
    pairs = zip(ciphertext, cycle(key))
    result = ''

    for pair in pairs:
        total = reduce(lambda x, y: ALPHA.index(x) - ALPHA.index(y), pair)
        result += ALPHA[total % 26]

    return result


def show_result(plaintext, key):
    """Generate a resulting cipher with elements shown"""
    encrypted = encrypt(key, plaintext)
    decrypted = decrypt(key, encrypted)

    print 'Key: %s' % key
    print 'Plaintext: %s' % plaintext
    print 'Encrytped: %s' % encrypted
    print 'Decrytped: %s' % decrypted


if __name__ == '__main__':
    show_result('saymyname', 'heisenberg')
