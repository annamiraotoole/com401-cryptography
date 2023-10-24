from rubik.cube import Cube
import  string
import hashlib
from itertools import product
from collections import Counter


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
    # split into digrams
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


def statistical(ct):

    Q2b_mhash='599aa36ad3fb3611ff0e274e4058bc77ccf0f3677558dd5873da64bef4c8dbc9'

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

    # try each other column being 2nd most likely
    for i in range(6):
        assumed_freqs = all_E[:i] + english_freqs[1] + all_E[i:]
        print(assumed_freqs)
        key, Q2b_m_guess = test_assumption(assumed_freqs)
        if hashlib.sha256(Q2b_m_guess.encode()).hexdigest() == Q2b_mhash:
            return key, Q2b_m_guess
        
    # try each other column being 3rd most likely
    for i in range(6):
        assumed_freqs = all_E[:i] + english_freqs[2] + all_E[i:]
        print(assumed_freqs)
        key, Q2b_m_guess = test_assumption(assumed_freqs)
        if hashlib.sha256(Q2b_m_guess.encode()).hexdigest() == Q2b_mhash:
            return key, Q2b_m_guess
        
    
    

    return key, Q2b_m_guess


# def brute_force(ct):

#     Q2b_mhash='599aa36ad3fb3611ff0e274e4058bc77ccf0f3677558dd5873da64bef4c8dbc9'

#     counter = 0

#     for key in list(product("ABCDEFGHIJKLMNOPQRSTUVWXYZ", repeat=6)):

#         # decrypt

#         Q2b_m = ""

#         pos = 0
#         while pos < len(ct):
#             new_char = chr((ord(ct[pos]) - ord(key[pos % 6]))% 26 + ord('A'))
#             Q2b_m += new_char
#             pos += 1

#         if (hashlib.sha256(Q2b_m.encode()).hexdigest() == Q2b_mhash):
#             print(Q2b_m)
#             return key, Q2b_m
        
#         if counter % 10000 == 0:
#                 print(counter)

#         counter += 1
        

#     print("FAILED TO FIND PLAINTEXT")
#     return (0, 0, 0, 0, 0), "FAILED TO FIND PLAINTEXT"


def test_part1():

    # PART 1

    Q2a_seed='YWGYNMNPWADOWSMPWXTFMQSAQQHHDBINCQRYGVBCOXMDPQXAXJULES'
    Q2a_c='EMOW QEDQ, MCB KPQZTB PHQUG CUEE MCB IOGFWQ OO HQGW SIPQ, QSP STQ VYENQP RMQRMST YO STQ LCJT AZ. WCN LUEICJEDE LCNE BQGDACFXN OQIQF IGHL ETT EKT FA IFA PMDI YXOGF WCN RQBTYPIZS NMQ ADQ DJZ, FMFWCN WUXAGWM, FA IFA CMFTPLIXXPP, WNP FWC SODPH YHL OABGJG PUUDARQZI, YJD FTTL PHQ YDAG TGDIJA DDQL Y HOZS QPAAFT, PLZ SMUS RDAFE KCNY OGGGKUE.  UIQ WLX MQMQT ME RSNIAGH YO IF OPL XE, EMXB PHQ SGWLHAZ.  XR WLX OPKA DURUCNEZF! IFA MAOZ RQRFXT PAPQMICZ TTAJEDTRGAJU. I ETDSHD XUZC PO TQPP DED FGW WNP DTNAAF EDKATTUCE JOI. FTJH HQD IM XESUC. FA LAAZCZ AF FWC CRKBWMJ AE UU FA TTAJEDT UF WYZ SAYT IENP AU YQTTAGGPY AHTP WLUOT.  QPAZP JN WNP DTNAAF "FXQ PHQ HDGYE AR IFA SXGVEWRP," EPGZ TTQ VPUPTAC.  FKW FTT ANEMFJPAS ADSCN OZQ PZKUF, MCB IAWQ DLA RQBTYP LQEHMJS! FTDSCHF MAGYE; U YXEDT ME LCHL NQ PR OCTADJ WT AZRC. DOIQKCN, STQ VMP UB, MCB XESMC RK RQBTYP IF, NJR DED TTYZ WME HM BUXX DD PHQ XDZOTQD FSWDDUAJA, TTMI QDE TMGBHY WZTU SHMF HFA WME HYUIZS, PLZ TTQ LMNDE OPKA VQDN OQEQD XLZEQP:--   IGO TTQ KMECQ AU RDE XAQQPED; U WCWRP TXK ZEOXPPA,   "YAG WYRE NMZCZ MQ FDM XRAIC, G IUEF HSCAD YN FWID."   MH Y ZUOW LGPH UFH CUEXUSQ, OO TQ LGPH TUH LKSQ   FGGIS TUH ZALF MCB DIE NJRPOZE, PLZ TGDCQ KUF TXQ POQE. '
    Q2a_mhash='599aa36ad3fb3611ff0e274e4058bc77ccf0f3677558dd5873da64bef4c8dbc9'

    C = CubeCipher(Q2a_seed)

    Q2a_m = C.decrypt(Q2a_c)

    print(Q2a_m)

    print(hashlib.sha256(Q2a_m.encode()).hexdigest() == Q2a_mhash)

def test_part2():
    # PART 2


    Q2a_seed='SHDUEJFICBGHFUEOQPLEUVNXHQPUELMNSIFHGEUFCBZXMEUWPSMEQI'


    Q2b_c='  BY NO UHNEI, VWMAPS MEEETBC NXIWJUZ MH SJI OHG,    T GUWKXO JJ IBZSU YJCNCF JDX UCBYJ;   UNE, OES MALU YI IXCGUYMEJ TKNX B SBLA GHYF,    MDR, B OP YP TZLJD WGW LHQEG.   RZV QNX HWE, IWBW EIU UHNEI, QO B FPOJEHGPE RAYHCF,    QJW ALWU CKHHO CKLM FOSKFFZOBU YTE;   ZUP RHF UKNGXO B RWVD-DPCAKLLVBP BG LU JDX WZPH--    LKTJ, XXWM BD UXA KXLTEJ HY EIQP?   BG XZ OKNMS, TQEW MSF IWZX, LT XA LAZPA DBL RSUU EHNLI,    E DXAU QHE FJ MYIUL GFHU LNAQBA   UR EIU QLX ZG JDBL ZJDPFXYU--EJX LSJBHBGR UXA UHI--    BBHHP XF JK LXWM OKN T NPKLEX?   JPK WKX ZMT, OTBO UXA RHFUX, WGW JPKN CTHT QNX MZP MATD    QPH WGREIYJZ MZVWDXK EIQJ LNPU;   OAM RZV VEGBDIUZ MAP HEKLX, HJJD MAP CEJXL LOT PAX MFQG--    IKLZ XKP WTE OKN FLOQCX MZ EE EM?   BY NO UHNEI, IWBW SJI BTMSFH, E MHZL JK MAP MQS,    TGO BHCNXO FQYA VLTU SBMS NO SBYP;   BDZ MAP NKOVNWBH OMKPOWPA, PSJSD BM RBLA MH XZ ZWP,    ALT BWLMPE JDX KPTJ KY FJ MYBX.   RZV QNX HWE, IWBW EIU UHNEI, EJX PZVBZ ATCEBU LNAQEOX    MSBJ UHNC FOA PTD BI OMXLEO WL XGFH;   UXM JPK XTELOSAW TY FUH HG EIU AGW ZG OKNK YPIA--    PALU CWWX JPK OH THGKHER NMURXK?   T IQRX TYTMAKXO UXNXX BVUOMBZOI, WGW EIQP BL POEQZA,    DBYZ ABD GQPAXC; EEJM ZTWU UHNCTUHY TTSI!   ZH RZV JDBGV J'

    C = CubeCipher(Q2a_seed)

    test_msg = "Questions exist regarding the hare's behaviour over the week where Easter happens. Specifically, the hare commences demonstrating bizarre faculties, generally considered impossible, regarding their commonplace reproductive approaches. The species, noted beta-carotene eaters, are never observed ejecting eggs outside their reproductive structures. However, disregarding every sane argumentation, the proliferous creature suddenly acquires the preposterous egg-ejecting potential, where their visceral ejection's contents include chocolate shaped eggs, possessing immense lactose contents, considered dangerous whenever the eater bears intolerance regarding the disaccharide."

    test_ct = C.encrypt(test_msg.upper())

    print(test_ct)

    print("cipher text is ", test_ct)

    key, plaintext = statistical(Q2b_c)

    print("decryption with key ", key, " is:")
    print(plaintext)

    # print(key)
    # print(plaintext)



if __name__ == "__main__":


    test_part2()



        


