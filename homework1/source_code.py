##------------##
##   Extra    ##
##------------##
from rubik.cube import Cube
import  string
import hashlib
from itertools import product
from collections import Counter
import string


##------------##
## Question 1 ##
##------------##

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

    m = ""
    for c in message:
        if c in string.ascii_lowercase:
            m += c

    message = m

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


##------------##
## Question 2 ##
##------------##

class CubeCipher:
    def __init__(self, seed):
        self.seed = seed
        # Create a Rubik's Cube with the specified seed
        self.cube = Cube(self.seed) 

    """
    Displays the current state of the cube. Example:
        MEM # M is the upper right corner of the top face. Accessed via cube.get_piece(1, 1, -1).colors[1]
        JJF 
        MTZ # Z is the bottom right corner of the top face.Accessed via cube.get_piece(1, 1, 1).colors[1]
    UJU XVE VKJ NYJ
    QTA FDX UHK DIG
    GGX PEX KRH TNO
        UIN
        OVG
        PTS

    """
    def display_state(self):
        print(self.cube())

    # Reset the state back to the initialized one.
    def reset(self):
        self.cube = Cube(self.seed)
    
    # Encrypts a plaintext pt with the cube cipher
    def encrypt(self, pt):
        ct = ""
        pos = 0 # used for keeping track of the current position of the plaintext
        
        # - Normally, you can execute the move 'R' with self.cube.R()
        # Since we will repedeatly execute R U R' and U', we prepare the
        # following list of functions
        # - Ri and Ui corresponds to R' and U'.
        moves = [self.cube.R, self.cube.U, self.cube.Ri, self.cube.Ui]
        while len(pt) - len(ct) >= 2:
            # We encrypt two characters with the the two characters we read from the cube
            # Hence, we keep track of this using char_count
            char_count = 0 
            while char_count != 2 and len(ct) != len(pt):
                # We skip the characters that are not in string.ascii_uppercase
                if pt[pos] not in string.ascii_uppercase:
                    ct += pt[pos] # write the skipped characters to ct to preserve strcuture.
                    pos +=1
                    continue
                # Execute R U R' U'
                for move in moves:
                    move()
                # Use upper right for the first character
                if char_count == 0:
                    ct += chr((ord(pt[pos]) + ord(self.cube.get_piece(1, 1, -1).colors[1]))% 26 + ord('A'))
                else: # Use bottom right for the second character.
                    ct += chr((ord(pt[pos]) + ord(self.cube.get_piece(1, 1, 1).colors[1]))% 26 + ord('A'))
                
                # Advance the positions
                pos +=1
                char_count += 1

        # Encrypt the left over character if any.
        if len(pt) != len(ct) and pt[pos] in string.ascii_uppercase:
            # Execute R U R' U'
            for move in moves:
                move()
            ct += chr((ord(pt[pos]) + ord(self.cube.get_piece(1, 1, -1).colors[1]))% 26 + ord('A')) 
            pos +=1

        # Add remaining skipped characters if any
        while len(ct) != len(pt):
            ct += pt[pos]
            pos +=1
        
        return ct

    def decrypt(self, ct):
        output = ""
        pos = 0 # used for keeping track of the current position of the ciphertext
        
        self.reset()

        # - Normally, you can execute the move 'R' with self.cube.R()
        # Since we will repedeatly execute R U R' and U', we prepare the
        # following list of functions
        # - Ri and Ui corresponds to R' and U'.
        moves = [self.cube.R, self.cube.U, self.cube.Ri, self.cube.Ui]
        while len(ct) - len(output) >= 2:
            # We encrypt two characters with the the two characters we read from the cube
            # Hence, we keep track of this using char_count
            char_count = 0 
            while char_count != 2 and len(output) != len(ct):
                # We skip the characters that are not in string.ascii_uppercase
                if ct[pos] not in string.ascii_uppercase:
                    output += ct[pos] # write the skipped characters to ct to preserve strcuture.
                    pos +=1
                    continue
                # Execute R U R' U'
                for move in moves:
                    move()
                # Use upper right for the first character
                if char_count == 0:
                    output += chr((ord(ct[pos]) - ord(self.cube.get_piece(1, 1, -1).colors[1]))% 26 + ord('A'))
                else: # Use bottom right for the second character.
                    output += chr((ord(ct[pos]) - ord(self.cube.get_piece(1, 1, 1).colors[1]))% 26 + ord('A'))
                
                # Advance the positions
                pos +=1
                char_count += 1

        # Encrypt the left over character if any.
        if len(ct) != len(output) and ct[pos] in string.ascii_uppercase:
            # Execute R U R' U'
            for move in moves:
                move()
            output += chr((ord(ct[pos]) - ord(self.cube.get_piece(1, 1, -1).colors[1]))% 26 + ord('A')) 
            pos +=1

        # Add remaining skipped characters if any
        while len(output) != len(ct):
            output += ct[pos]
            pos +=1
        
        return output
    

def decrypt_with_6_letter_key(ct, key):

    plaintext = ""
    pos = 0
    mod_counter = 0
    while pos < len(ct):
        
        if ct[pos] not in string.ascii_uppercase:
            plaintext += ct[pos] # write the skipped characters to ct to preserve strcuture.
            pos +=1
            continue

        new_char = chr((ord(ct[pos]) - ord(key[mod_counter % 6]))% 26 + ord('A'))
        plaintext += new_char
        pos += 1
        mod_counter += 1

    return plaintext


def freq_assumption_helper(assumed_freqs, col_counts_sorted):
        
    key = ""

    for col in range(6):
        #print("analyzing column ", col)
        freq = col_counts_sorted[col][0][0]
        #print("most frequent ciphertext letter in column ", col, " is ", freq)
        c = chr((ord(freq) - ord(assumed_freqs[col]))% 26 + ord('A'))
        key += c
        #print("if that letter is encrypting ", "E", " then the key letter is ", c)
        #print()

    return key


def binary_strings(bits):
    num = 2 ** bits
    lst = list(range(num))
    lst_binary = [bin(n)[2:].rjust(6, '0') for n in lst]
    return lst_binary

def char_combos_six(str):
    return [''.join(s) for s in list(product(str, repeat=6))]

def statistical(ct, Q2b_mhash):

    # divide ciphertext into strings with characters from each position mod 6 / each column
    ct_only_alphabet = ""
    for c in ct:
        if c in string.ascii_uppercase:
            ct_only_alphabet += c
    ct_cols = [ct_only_alphabet[i::6] for i in range(6)]

    print("ct_cols is ", ct_cols)
    print()

    # count occurences of each letter, store this info somehow
        # find the most common letter in each column
    col_counts = [Counter(col_str) for col_str in ct_cols]
    print("col_counts is ", col_counts)
    print()

    col_counts_sorted = [sorted(c.items(), key=lambda x: x[1], reverse=True) for c in col_counts]
    print("col_counts_sorted is :")
    for i in range(6):
        print("col ", i, " counts are ", col_counts_sorted[i])
    print()

    # call the most frequent letter in column 0, F0

    english_freqs = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D',
                      'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B',
                        'V', 'K', 'J', 'X', 'Q', 'Z']
    
    
    # given list of english letters sorted most to least common
    # for EL in english_freqs:
        # assume that F0's decryption is the letter LT
        # solve for what the key letter is = F0 - LT mod 26
        # chr((ord(ct[pos]) - ord(self.cube.get_piece(1, 1, -1).colors[1]))% 26 + ord('A')) 


    key, Q2b_m_guess = "", ""

    def test_assumption(assumed_freqs):
        key = freq_assumption_helper(assumed_freqs, col_counts_sorted)
        Q2b_m_guess = decrypt_with_6_letter_key(ct, key)
        return key, Q2b_m_guess
        

    # FIRST ASSUME ALL COLUMNS ARE "E"
    all_E = "EEEEEE"
    key, Q2b_m_guess = test_assumption(all_E)
    if hashlib.sha256(Q2b_m_guess.encode()).hexdigest() == Q2b_mhash:
        return key, Q2b_m_guess
    
    # all combinations of a set of letters:
    key_combos = char_combos_six("ETAOINSH") #char_combos_six("ETAOINSHR")
    for assumed_freqs in key_combos:
        print(assumed_freqs)
        key, Q2b_m_guess = test_assumption(assumed_freqs)
        if hashlib.sha256(Q2b_m_guess.encode()).hexdigest() == Q2b_mhash:
            return key, Q2b_m_guess

    return key, Q2b_m_guess


##------------##
## Question 3 ##
##------------##

from Crypto.Cipher import AES


# returns num mod P
def modP(num):
    return num % Q3_p

# raises x to the power of k, and then returns it mod P
def pow_modP(x, k):
    return modP(x ** k)

# return list of all bits to represent num
# if pad is set to a number, it makes sure the list of bits is "pad" long
# example:
#   get_all_bits(3, pad=5) ---> [0, 0, 0, 1, 1]
def get_all_bits(num, pad=0):
    s = bin(num)[2:]
    bits = [int(c) for c in s]
    if pad != 0:
        L = len(bits)
        padded_bits = ([0] * (pad - L)) + bits
        assert (len(padded_bits) == pad)
        return padded_bits
    return bits

# get bit at position b from the pad-length long binary representation of num 
# example:
#   get_bit(3, 2, pad=5) ---> 0
#   get_bit(3, 3, pad=5) ---> 1
# 
def get_bit(num, b, pad=0):
    bits = get_all_bits(num, pad=pad)
    assert b < len(bits)
    return bits[b]

# get bit at position b and b+1 from the pad-length long binary representation of num 
# return them as a length-2 list
# example:
#   get_2bits(3, 2, pad=5) ---> [0, 1]
#   get_2bits(3, 3, pad=5) ---> [1, 1]
# if the bit requested is longer than bit representation, the code should fail
def get_2bits(num, b, pad=0):
    return [get_bit(num, b, pad=pad), get_bit(num, b+1, pad=pad)]

def to_num(b0, b1):
    return 2*b0 + b1

# turn list of bits into the integer that it represents
# assumes that lst[0] is the most significant bit
def to_num_long(lst):
    # if len(lst) == 0:
    #     return 0
    # elif len(lst) == 1:
    #     return lst[0]
    # else:
    #     return lst[0] + 2*to_num_long(lst[1:])
    
    output = 0
    for bit in lst:
        assert (bit == 0) or (bit == 1)
        output = output * 2 + bit
    return output

known_AES_bits_reverse = get_all_bits(Q3_known_pt, pad=8)
known_AES_bits_reverse.reverse()

def find_mjs():

    secret = [0, 0]

    # 63, 62, 61, ...... 4, 3, 2, 1, 0
    for j in reversed(range(len(Q3_cts))):
 
        # get special two bits of unknown ciphertext at position j
        unknown_cts_bits = to_num(*get_2bits(Q3_cts[j], Q3_n, pad=256)) # VERIFY CORRECT
        assert(unknown_cts_bits in range(4))

        found_cancellation = False

        # TRY EACH KNOWN PLAINTEXT WORD
        # k is the index of which two bits of of the plaintext AES we use
        for k in range(4):
            # get special two bits of known ciphertext at position k
            known_cts_bits = to_num(*get_2bits(Q3_known_cts[k], Q3_n, pad=256))
            assert(known_cts_bits in range(4))

            # XOR ciphertexts
            xor_result = unknown_cts_bits ^ known_cts_bits
            assert(xor_result in range(4))
            if xor_result == 0:
                #mj_raw = to_num(*get_2bits(Q3_known_pt, 2*k, pad=8)) + 2*(k+1) - 2*(j+1)
                known_AES_2bits = known_AES_bits_reverse[2*k : 2*k+2]
                known_AES_2bits.reverse()
                mj_raw = to_num(*known_AES_2bits) + 2*(k+1) - 2*(j+1)
                mj = mj_raw % 4
                secret += get_all_bits(mj, pad=2)
                found_cancellation = True
        
        assert found_cancellation

    return modP(to_num_long(secret))



def decrypt(Q3_ct_aes, Q3_tag, Q3_nonce, rec_k_aes):
    # rec_k_aes is assumed to be an int
    rec_k_aes_bytes = rec_k_aes.to_bytes(16, "big")
    cipher = AES.new(rec_k_aes_bytes, AES.MODE_GCM, Q3_nonce)
    Q3_pt = cipher.decrypt_and_verify(Q3_ct_aes, Q3_tag)
    return Q3_pt