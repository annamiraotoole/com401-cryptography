## Question 1

def split_into_digrams(txt):
    # split into digrams
    digrams = []
    while txt:
        digrams += [txt[:2]]
        txt = txt[2:]
    return digrams
    
def preprocess(message):

    # remove spaces
    message = message.replace(" ", "")
    # replace j with i
    message = message.replace("j", "i")
    # make lowercase
    message = message.lower()

    # find positions of repeated characters
    indices = []
    for i in range(len(message)-1):
        if message[i] == message[i+1]:
            indices += [i]

    # add "x" between all repeated characters
    c = 0
    for i in indices:
        message = message[:i+c+1] + "x" + message[i+c+1:]
        c += 1

    # add "x" to message if it has odd length
    if len(message) % 2 == 1:
        message += "x"

    digrams = split_into_digrams(message)

    return digrams

def index(key, letter):
    for r in range(5):
        for c in range(5):
            if key[r][c] == letter:
                return r, c
    print("DID NOT FIND LETTER IN KEY")
    return 100, 100


# encrypts just one digram
def enc(key, d):

    r1, c1 = index(key, d[0])
    r2, c2 = index(key, d[1])

    ciphertext = ""

    # if in same row
    if r1 == r2:
        ciphertext += key[r1][(c1+1) % 5]
        ciphertext += key[r2][(c2+1) % 5]
    
    # if in same column
    elif c1 == c2:
        ciphertext += key[(r1+1) % 5][c1]
        ciphertext += key[(r2+1) % 5][c2]

    # if not in the same row or column
    else:
        ciphertext += key[r1][c2]
        ciphertext += key[r2][c1]

    return ciphertext

# takes in key, and list of digram strings
def encryption(key, D):
    ciphertext = []
    for d in D:
        ciphertext += [enc(key, d)]
    return "".join(ciphertext)


def dec(key, d):
    
    r1, c1 = index(key, d[0])
    r2, c2 = index(key, d[1])

    plaintext = ""

    # if in same row
    if r1 == r2:
        plaintext += key[r1][(c1-1) % 5]
        plaintext += key[r2][(c2-1) % 5]
    
    # if in same column
    elif c1 == c2:
        plaintext += key[(r1-1) % 5][c1]
        plaintext += key[(r2-1) % 5][c2]

    # if not in the same row or column
    else:
        plaintext += key[r1][c2]
        plaintext += key[r2][c1]

    return plaintext

def decryption(key, ciphertext):
    digrams = split_into_digrams(ciphertext)
    plaintext = []
    for d in digrams:
        plaintext += [dec(key, d)]
    return "".join(plaintext)


## Question 2