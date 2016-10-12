import classicalciphers
import datetime
import random
import pickle
import math

LETTERS = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']
FREQUENCY = [0.12702, 0.09056, 0.08167, 0.07507, 0.06966, 0.06749, 0.06327, 0.06094, 0.05987, 0.04253, 0.04025, 0.02782, 0.02758, 0.02406, 0.02360, 0.02228, 0.02015, 0.01974, 0.01929, 0.01492, 0.00978, 0.00772, 0.00153, 0.00150, 0.00095, 0.00074]
ENGLISH_FREQUENCY_SUM = sum([x**2 for x in FREQUENCY])
ENGLISH_FREQUENCY = dict(zip(LETTERS, FREQUENCY))
ENGLISH_CI = 0.0667

#Statistic of trigrams collected from this text https://en.wikipedia.org/wiki/Classical_cipher
trigram_file = open('trigrams', 'rb')
ENGLISH_TRIGRAMS = pickle.load(trigram_file)

#calculate letter freuency in string message
def frequency(message):
    return {ch: message.count(ch)/len(message) for ch in classicalciphers.ALPHABET}

#calculate letters count in string message
def letterscount(message):
    return {ch: message.count(ch) for ch in classicalciphers.ALPHABET}

#calculate coincidence index for string message
def indexcoincidence(message):
    lettersnumbers, length = letterscount(message), len(message)
    return sum([dict.get(lettersnumbers, num, 0) * (dict.get(lettersnumbers, num, 0) - 1) / (length * (length - 1)) for num in classicalciphers.ALPHABET])

#select each step-th letter in message started from start-th sign
def columnrepresentation(message,  step, start=0):
    return ''.join([message[k] for k in range(start, len(message), step)])

#build a new strings msg by selecting letters with offset equal to i
#for each builted string calculate coincidence index
#if Vigenere key was not found last parametr of columnrepresentation should be changed
def shiftedindexcoincidence(message):
    result = {}
    for i in range(1, 26):
        msg=columnrepresentation(message, i, 0)
        result[i] = indexcoincidence(msg)
    return result

#Test is message frequency corresponds to eglish language
def alphabetcorrelation(messagefrequency):
    return sum(ENGLISH_FREQUENCY[ch]*messagefrequency[ch] for ch in classicalciphers.ALPHABET)

#Break Caesar encryption by trying all possible key and check is frequency in decrypted message corresponds to english
def breakcaesar(ciphertext):
    variants=[]
    for i in range(25):
        d=classicalciphers.Caesar.decrypt(ciphertext, i)
        msg_frequency=frequency(d)
        variants.append((i, alphabetcorrelation(msg_frequency)))
    return max(variants, key=lambda x: x[1])

#Searching Vigenere cipher's key length by calculation coincidence index for each possible length in range 1-25
#serchborder - parameter defining how close coincidence index should be to normal english coincidence index
def findvigenerekeylength(ciphertext, serchborder):
    keylengths = [(a, b) for a, b in shiftedindexcoincidence(ciphertext).items() if abs(b-ENGLISH_CI)<ENGLISH_CI*serchborder]
    ProbableLength=min(keylengths, key=lambda x: x[0])
    return ProbableLength[0]

#recovery Vigenere key character by character using key length
def recovervigenerekey(ciphertext, keylength):
    result=[]
    for k in range(keylength):
        msg=columnrepresentation(ciphertext, keylength, k)
        tmp=breakcaesar(msg)
        result.append(classicalciphers.ALPHABET[tmp[0]])
    return ''.join(result)

#count how many trigrams contained in the text
def counttrigrams(text):
    return len(text)-3+1

#count how many time specific trigram occurs in the text
def trigramfrequency(text, trigram):
    return text.count(trigram)/counttrigrams(text)

#compare trigram's statistic for specific text with English trigram's statistic
def trigramfitness(text):
    return sum([trigramfrequency(text, k) for k in ENGLISH_TRIGRAMS.keys()])

#count how many time specific trigram occurs in the text
def logtrigramfrequency(text, trigram):
    return math.log(text.count(trigram)/counttrigrams(text)) if text.count(trigram)/counttrigrams(text) != 0 else -10

#compare trigram's statistic for specific text with English trigram's statistic
def logtrigramfitness(text):
    return sum([logtrigramfrequency(text, k) for k in ENGLISH_TRIGRAMS.keys()])

#break substitution cipher using hill-climbing algorithm and trigram's statistic
#to improve accuracy of method it is recommended to run breaksubstitutioncipher few times
def breaksubstitutioncipher(ciphertext):
    eng_freq = sorted(ENGLISH_FREQUENCY.items(), key=lambda x: x[1], reverse=True)
    ciph_freq = sorted(frequency(ciphertext).items(), key=lambda x: x[1], reverse=True)
    parentkey = [ch[0] for ch in sorted(map(lambda x, y: (x[0], y[0]), ciph_freq, eng_freq), key=lambda x: x[1])]
    d = classicalciphers.Substitution.decrypt(ciphertext, ''.join(parentkey))
    fitness = trigramfitness(d)
    count = 0
    while count < 1500:
        i = random.randrange(26)
        j = random.randrange(26)
        childkey = parentkey[:]
        childkey[i], childkey[j] = childkey[j], childkey[i]
        d = classicalciphers.Substitution.decrypt(ciphertext, ''.join(childkey))
        if trigramfitness(d) > fitness:
            parentkey = childkey
            fitness = trigramfitness(d)
            count = 0
        count += 1
    return classicalciphers.Substitution.decrypt(ciphertext, ''.join(parentkey))

#break affine cipher using brute force and comparing letters frequency in decrypted text with normal english frequency
def breakaffine(ciphertext):
    variants=[]
    for i in range(25):
        for j in range(25):
            try:
                d=classicalciphers.Affine.decrypt(ciphertext, (i, j))
                msg_frequency=frequency(d)
                variants.append((i, j, alphabetcorrelation(msg_frequency)))
            except:
                pass
    return classicalciphers.Affine.decrypt(ciphertext, (max(variants, key=lambda x: x[2])[0], max(variants, key=lambda x: x[2])[1]))

print(datetime.datetime.now())

message = classicalciphers.readfile(r'plaintext.txt')
print('---Break Caesar cipher---')
ciphertext = classicalciphers.Caesar.encrypt(message, 16)
print(ciphertext)
print(frequency(ciphertext))
print(indexcoincidence(ciphertext))
print(classicalciphers.Caesar.decrypt(ciphertext, breakcaesar(ciphertext)[0]))

print('---Break Vigenere cipher---')
ciphertext = classicalciphers.Vigenere.encrypt(message, "SECRET")
print(ciphertext)
print(frequency(ciphertext))
print(indexcoincidence(ciphertext))
print(shiftedindexcoincidence(ciphertext))
keylen = findvigenerekeylength(ciphertext, 0.10)
key = recovervigenerekey(ciphertext, keylen)
print(key)
mess = classicalciphers.Vigenere.decrypt(ciphertext, key)
print(mess)

print('---Break Substitution cipher---')
ciphertext=classicalciphers.Substitution.encrypt(message, 'ZEBRA')
print(ciphertext)
print(frequency(ciphertext))
print(breaksubstitutioncipher(ciphertext))

print('---Break Affine cipher---')
ciphertext=classicalciphers.Affine.encrypt(message, (17, 18))
print(ciphertext)
print(frequency(ciphertext))
print(breakaffine(ciphertext))

print(datetime.datetime.now())

