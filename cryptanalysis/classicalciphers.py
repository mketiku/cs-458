import string
import random

ALPHABET = string.ascii_uppercase

def readfile(file):
    f=open(file, mode='r')
    message=''
    for ch in f.read():
        if 65 <= ord(ch) <= 90 or 97 <= ord(ch) <= 122:
            message+=ch.upper()
    f.close()
    return message

#Build shifted alphabet
def offset(char, offset):
    return ALPHABET[(ALPHABET.index(char)+offset)%26]

class Caesar:
    @staticmethod
    def encrypt(message, key):
        return ''.join(map(offset, list(message), [key,]*len(message)))

    @staticmethod
    def decrypt(ciphertext, key):
        return ''.join(map(offset, list(ciphertext), [26-key,]*len(ciphertext)))

class Vigenere:
    @staticmethod
    def encrypt(message, key):
        return ''.join(map(offset, message, list(map(lambda x: ALPHABET.index(x), key))*(len(message)//len(key)+1)))

    @staticmethod
    def decrypt(ciphertext, key):
        return ''.join(map(offset, ciphertext, list(map(lambda x: 26-ALPHABET.index(x), key))*(len(ciphertext)//len(key)+1)))

class Substitution:
    @staticmethod
    def encrypt(message, key):
        cipher_alph = Substitution.buildAlphabet(key)
        return ''.join(cipher_alph[ALPHABET.index(ch.upper())] for ch in message)

    #Built substitution alphabet by key
    @staticmethod
    def buildAlphabet(key):
        offseted_alph = ''.join(map(offset, list(ALPHABET), [ALPHABET.index(key.upper()[-1])+1,]*len(ALPHABET)))
        return (key.upper()+''.join([ch for ch in offseted_alph if not (ch in key.upper())]))

    @staticmethod
    def decrypt(ciphertex, key):
        cipher_alph = Substitution.buildAlphabet(key)
        return ''.join(ALPHABET[cipher_alph.index(ch.upper())] for ch in ciphertex)

class Affine:
    @staticmethod
    def modReverse(a, b):
        r, s, t = [min(a, b), max(a, b)], [1, 0], [0,1]
        while r[-1]!=1:
            q = r[-2]//r[-1]
            r.append(r[-2]-q*r[-1])
            s.append(s[-2]-q*s[-1])
            t.append(t[-2]-q*t[-1])
        return (s[-1]%r[1])

    #key should be the tuple
    @staticmethod
    def encrypt(message, key):
        return ''.join(ALPHABET[(ALPHABET.index(ch)*key[0]+key[1])%26] for ch in message)

    #key should be the tuple
    @staticmethod
    def decrypt(ciphertext, key):
        try:
            return ''.join(ALPHABET[Affine.modReverse(key[0], 26)*(ALPHABET.index(ch)-key[1])%26] for ch in ciphertext)
        except ZeroDivisionError:
            pass

if __name__=='__main__':
    #Caesar test
    print('---Caesar---')
    test = 'DEFENDTHEEASTWALLOFTHECASTLE'
    k = 1
    c = Caesar.encrypt(test, k)
    d = Caesar.decrypt(c, k)
    print(c)
    print(d)

    #Vigenere test
    print('---Vigenere---')
    test = 'DEFENDTHEEASTWALLOFTHECASTLE'
    c = Vigenere.encrypt(test, 'FORTIFICATION'.upper())
    d = Vigenere.decrypt(c, 'FORTIFICATION'.upper())
    print(c)
    print(d)

    #Substitution test
    print('---Substitution---')
    test='DEFENDTHEEASTWALLOFTHECASTLE'
    c = Substitution.encrypt(test, 'zebra')
    print(c)
    d = Substitution.decrypt(c, 'zebra')
    print(d)

    #Affine test
    print('---Affine---')
    test = 'DEFENDTHEEASTWALLOFTHECASTLE'
    c = Affine.encrypt(test, (5, 7))
    print(c)
    d = Affine.decrypt(c, (5, 7))
    print(d)