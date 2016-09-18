# Reverse Cipher

# Variable to hold secret messages
message = 'egassem terces a si sihT'
# message = input()

#Holds encrypted messages
translated = ''

# Counter initialization
i = len(message) -1

while i >= 0:
    translated = translated + message[i]
    i = i -1
    #Check that everything works well
    # print(i, message[i], translated )

print(translated)
