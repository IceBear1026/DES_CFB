import os
os.system("pip install pycryptodomex")

import json
from base64 import b64encode, b64decode
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

# 64 bit (56 bits) key and 64 bit IV.
the_key = get_random_bytes(8)
the_IV = get_random_bytes(8)

# The keyword "break" terminates a loop immediately. The program proceeds with the first statement after the loop construct.

# The keyword "continue" terminates only the current loop iteration, but not the whole loop. 

# Checking if the person wants to encrypt or decrypt.
def check_encOrdec():
    while True:
        check = input("Are you trying to encrypt or decrypt? (If you don't want to, type no) ")
        
        if(check == "encrypt" or check == "decrypt"):
            return check
        elif(check == "no"):
            return check
        elif(check == "secret"):
            return check
    
        print("Please choose to either encrypt or decrypt")

def encrypt(message, key, IV):
    # Instantiating algorithm.
    cipher = DES.new(key, DES.MODE_CFB, iv=IV, segment_size=8)

    # Ciphertext created using cipher.encrypt()
    ct_bytes = cipher.encrypt(message)

    # translate the 64encode back to understandable characters.
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')

    # Put the results in json file
    result = json.dumps({'iv':iv, 'ciphertext':ct})
    return result

# We assume that the key was securely
def decrypt(json_input):
    # Instantiating algorithm
    b64 = json.loads(json_input)
    IV = b64decode(b64['iv'])
    ct = b64decode(b64['ciphertext'])
    cipher = DES.new(the_key, DES.MODE_CFB, iv=IV, segment_size=8)
    
    # Plaintext created using cipher.decrypt()
    pt = cipher.decrypt(ct)
    plaintext = str(pt)[2:-1]
    # Put the results in json file
    result = "Plaintext was: " + str(plaintext)
    return result

while True:
    text = ""
    answer = check_encOrdec()
    
    if (answer == "no"):
        break
    elif (answer == "secret"):
        text = the_key
    elif (answer == "encrypt"):
        message = bytes(str(input("Tell me a text to encrypt: ")), 'utf-8')

        while True:
            b = str(input("Type your Initalization Vector if you would like to provide your own. If not, type n. "))
            if b == "n":
                break
            the_IV = b64decode(b)
            break
                
        text = encrypt(message,the_key,the_IV)
    else:
        message = input("Write the IV and Ciphertext in JSON format respectively to decrypt: ")
        text = decrypt(message)
    print(text)
