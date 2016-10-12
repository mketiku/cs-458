plainText = raw_input("What is your plaintext? ")
shift = int(raw_input("What is your shift? "))

def caesar(plaintext, shift):
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = string.maketrans(alphabet, shifted_alphabet)
    return plaintext.translate(table)

caesar(plainText, shift)
