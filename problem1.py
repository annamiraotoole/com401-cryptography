
Q1a_m = "To anyone who knew the country well, the mere style and title of Don Quixote of La Mancha gave the key to the authors meaning at once. La Mancha as the knights country and scene of his chivalries is of a piece with the pasteboard helmet, the farm-labourer on ass-back for a squire, knighthood conferred by a rascally ventero, convicts taken for victims of oppression, and the rest of the incongruities between Don Quixotes world and the world he lived in, between things as he saw them and things as they were."

s = "caesar"

key = [["f", "o", "l", "i", "s"], 
       ["h", "c", "m", "p", "a"],
       ["n", "y", "b", "d", "e"],
       ["g", "k", "q", "r", "t"],
       ["u", "v", "w", "x", "z"]]


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

    # split into digrams
    digrams = []
    while message:
        digrams += [message[:2]]
        message = message[2:]

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



def main():
    s2 = preprocess(s)
    print(s2)
    ciphertext = encryption(key, s2)
    print(ciphertext)

if __name__ == "__main__":
    main()
