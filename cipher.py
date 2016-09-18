#!

# Constants
CIPHER_MENU= ['shift','substitution','affine','vigenere' ]

# Alphabet encoding scheme
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


# input file, or message
# message = input("Enter your message",)
message = "hello"

# output file, or message
translated = ''

# key or name of file containing the key
key = ''


# Mode : Encrypt or Decrypt
Mode = 'Encrypt'


def encrypt(message):
    message = pre_treat_message(message)

    for symbol in message:
        print(message[symbol])


def pre_treat_message(message):
    """ removes punctuation (:;,.?!) and converts message to upper case """
    treated_message = message

    # remove punctuation, one symbol at a time
    treated_message = treated_message.replace(':', '')  # remove colons
    treated_message = treated_message.replace(';', '')  # remove semicolons
    treated_message = treated_message.replace(',', '')  # remove commas
    treated_message = treated_message.replace('.', '')  # remove periods
    treated_message = treated_message.replace('?', '')  # remove question marks
    treated_message = treated_message.replace('!', '')  # remove exclamation points

    # convert to uppercase
    treated_message = treated_message.upper()

    return treated_message

def treatment(message):
    return message

encrypt(message)


MESSAGE_ONE = 'They love pizza.'

print encrypt(MESSAGE_ONE, 1)  # encrypt the message with a key of 1
