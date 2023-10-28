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
        freq = col_counts_sorted[col][0][0]
        c = chr((ord(freq) - ord(assumed_freqs[col]))% 26 + ord('A'))
        key += c
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

    # count occurences of each letter, store this info in dict
    # find the most common letter in each column
    col_counts = [Counter(col_str) for col_str in ct_cols]
    col_counts_sorted = [sorted(c.items(), key=lambda x: x[1], reverse=True) for c in col_counts]

    english_freqs = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D',
                      'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B',
                        'V', 'K', 'J', 'X', 'Q', 'Z']
    

    key, Q2b_m_guess = "", ""

    def test_assumption(assumed_freqs):
        key = freq_assumption_helper(assumed_freqs, col_counts_sorted)
        Q2b_m_guess = decrypt_with_6_letter_key(ct, key)
        return key, Q2b_m_guess
    
    # all combinations of a set of letters:
    key_combos = char_combos_six("ETAOINSH") 
    for assumed_freqs in key_combos:
        # print(assumed_freqs)
        key, Q2b_m_guess = test_assumption(assumed_freqs)
        if hashlib.sha256(Q2b_m_guess.encode()).hexdigest() == Q2b_mhash:
            return key, Q2b_m_guess

    return key, Q2b_m_guess


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
    C = CubeCipher(Q2a_seed)
    test_msg = "Questions exist regarding the hare's behaviour over the week where Easter happens. Specifically, the hare commences demonstrating bizarre faculties, generally considered impossible, regarding their commonplace reproductive approaches. The species, noted beta-carotene eaters, are never observed ejecting eggs outside their reproductive structures. However, disregarding every sane argumentation, the proliferous creature suddenly acquires the preposterous egg-ejecting potential, where their visceral ejection's contents include chocolate shaped eggs, possessing immense lactose contents, considered dangerous whenever the eater bears intolerance regarding the disaccharide."
    test_ct = C.encrypt(test_msg.upper())
   
    Q2b_c='  BY NO UHNEI, VWMAPS MEEETBC NXIWJUZ MH SJI OHG,    T GUWKXO JJ IBZSU YJCNCF JDX UCBYJ;   UNE, OES MALU YI IXCGUYMEJ TKNX B SBLA GHYF,    MDR, B OP YP TZLJD WGW LHQEG.   RZV QNX HWE, IWBW EIU UHNEI, QO B FPOJEHGPE RAYHCF,    QJW ALWU CKHHO CKLM FOSKFFZOBU YTE;   ZUP RHF UKNGXO B RWVD-DPCAKLLVBP BG LU JDX WZPH--    LKTJ, XXWM BD UXA KXLTEJ HY EIQP?   BG XZ OKNMS, TQEW MSF IWZX, LT XA LAZPA DBL RSUU EHNLI,    E DXAU QHE FJ MYIUL GFHU LNAQBA   UR EIU QLX ZG JDBL ZJDPFXYU--EJX LSJBHBGR UXA UHI--    BBHHP XF JK LXWM OKN T NPKLEX?   JPK WKX ZMT, OTBO UXA RHFUX, WGW JPKN CTHT QNX MZP MATD    QPH WGREIYJZ MZVWDXK EIQJ LNPU;   OAM RZV VEGBDIUZ MAP HEKLX, HJJD MAP CEJXL LOT PAX MFQG--    IKLZ XKP WTE OKN FLOQCX MZ EE EM?   BY NO UHNEI, IWBW SJI BTMSFH, E MHZL JK MAP MQS,    TGO BHCNXO FQYA VLTU SBMS NO SBYP;   BDZ MAP NKOVNWBH OMKPOWPA, PSJSD BM RBLA MH XZ ZWP,    ALT BWLMPE JDX KPTJ KY FJ MYBX.   RZV QNX HWE, IWBW EIU UHNEI, EJX PZVBZ ATCEBU LNAQEOX    MSBJ UHNC FOA PTD BI OMXLEO WL XGFH;   UXM JPK XTELOSAW TY FUH HG EIU AGW ZG OKNK YPIA--    PALU CWWX JPK OH THGKHER NMURXK?   T IQRX TYTMAKXO UXNXX BVUOMBZOI, WGW EIQP BL POEQZA,    DBYZ ABD GQPAXC; EEJM ZTWU UHNCTUHY TTSI!   ZH RZV JDBGV J'
    Q2b_mhash='db4ccc8587a6722ba0e55dcfb2f0003698136398269dcbb7785ac6140d0c7857'

    Q2a_c='EMOW QEDQ, MCB KPQZTB PHQUG CUEE MCB IOGFWQ OO HQGW SIPQ, QSP STQ VYENQP RMQRMST YO STQ LCJT AZ. WCN LUEICJEDE LCNE BQGDACFXN OQIQF IGHL ETT EKT FA IFA PMDI YXOGF WCN RQBTYPIZS NMQ ADQ DJZ, FMFWCN WUXAGWM, FA IFA CMFTPLIXXPP, WNP FWC SODPH YHL OABGJG PUUDARQZI, YJD FTTL PHQ YDAG TGDIJA DDQL Y HOZS QPAAFT, PLZ SMUS RDAFE KCNY OGGGKUE.  UIQ WLX MQMQT ME RSNIAGH YO IF OPL XE, EMXB PHQ SGWLHAZ.  XR WLX OPKA DURUCNEZF! IFA MAOZ RQRFXT PAPQMICZ TTAJEDTRGAJU. I ETDSHD XUZC PO TQPP DED FGW WNP DTNAAF EDKATTUCE JOI. FTJH HQD IM XESUC. FA LAAZCZ AF FWC CRKBWMJ AE UU FA TTAJEDT UF WYZ SAYT IENP AU YQTTAGGPY AHTP WLUOT.  QPAZP JN WNP DTNAAF "FXQ PHQ HDGYE AR IFA SXGVEWRP," EPGZ TTQ VPUPTAC.  FKW FTT ANEMFJPAS ADSCN OZQ PZKUF, MCB IAWQ DLA RQBTYP LQEHMJS! FTDSCHF MAGYE; U YXEDT ME LCHL NQ PR OCTADJ WT AZRC. DOIQKCN, STQ VMP UB, MCB XESMC RK RQBTYP IF, NJR DED TTYZ WME HM BUXX DD PHQ XDZOTQD FSWDDUAJA, TTMI QDE TMGBHY WZTU SHMF HFA WME HYUIZS, PLZ TTQ LMNDE OPKA VQDN OQEQD XLZEQP:--   IGO TTQ KMECQ AU RDE XAQQPED; U WCWRP TXK ZEOXPPA,   "YAG WYRE NMZCZ MQ FDM XRAIC, G IUEF HSCAD YN FWID."   MH Y ZUOW LGPH UFH CUEXUSQ, OO TQ LGPH TUH LKSQ   FGGIS TUH ZALF MCB DIE NJRPOZE, PLZ TGDCQ KUF TXQ POQE. '
    Q2a_mhash='599aa36ad3fb3611ff0e274e4058bc77ccf0f3677558dd5873da64bef4c8dbc9'

    CT_VALERIO = 'YTA; ELN PAPW RSIX PX TKJBZLCN MNPXC CHHDPW, LAZPRLSJZ DMRR PAL ILN KY ALC DWBS, ELN AGKMLQ SBAL RRA ZYML, GDBJL POITPRCN OHTI RSIX HJRON MOI POOM VJ GD DTK KMXA.  PLPJ! SRX VJROJ LLIL K YTA AGDDHBX Y QNBU, XFYQZOX YVEVL; FSD W ZYML GEMOSSD W VHX! GDO MOI KYOM JYPSKNZ XFSJZ P ITON LHA GX IR SMDO!  OAL LYN JHA KMXA FBGF PWKALCB XXMSPO OAL GYWA BU WGQDM VJ RRA AVYQO KY ALC WWKJL FKNX: ZLC DDHBKFD EM TYQD XX ALC BEZOX FYQLL, FCMWNZI RRA VOMKXARZ ACBA LOENOZ EPOC OWKZ ELN PAL VMYB PHW RRWMJLCN SBAL DEN. BA AYC OH SEPQA T OSSCA, MOER CDX KMB XKM SMIO PH NS LOWKLV RSHE ZLC RWW UMZLHXK WMWA FVVC YB MOI JOBMOELN XBA SD WQLOVMYI, TUH PKELLH FONLLPD DK TISSD PPV JCOP APKF: ORXU XFOJ LOI UKHDLH SZ PHDEPNO BA VYDDXY XGWEWSC, QKUBUK RY DXYWCVB LBTNYOX PX QRKNSH ZO NTCMLQ ITK EDDAK HPJ! S WETSQD SBZL GN CHUI RY OXL XFO DTAXCB EGZXCKZ!  MOIPO STZ E RKXEL WCD KNA YLNAK H XPOA BU JPYJM VJ RRA AVYQO, WGK XFO ITYGF RWKL ELN PAL LYDPXY ACBA AHZGXC MLE YD EM: H HMBIHBWC GWL ZMRDEGN FCDSXLR RRAF, MEQD WLSICZ, WGK XFO KMOIP DSH DIPO QLPRE SP TZ E AEOAPSL, BALAMLQ PALMP OHUVAQ YJ BA, ELN PTSOGXC HCIP SPL OIYN. RXYC SXYHTJMBPTIPC PKK ALC NKKTSSCA, MOSSQDM HPGMA; HUPW, KO BAW YCHXLT, G CQIWSQO EM KSCCJM TML'
    MHASH_VALERIO = 'df4c839425fed58cabcbbcec0f72a479c1b485b308911bdb2d526779501812d5'

    CT_A_VAL = 'CQ TRSMA RFPEA XH YFP OAQZLO, IUKHC DWXP HYXM CQ YFP KXPHJFARQS RSIC KY ULA J XJPJ LRHKGNCUV LYXM RPICPL.  CJJ NWIHGWQ LTU RQYJMM CY MYKN YNRSWDV BYTBRPL DZZ CWWLD, YDCWPPTUKSE LTU VMC HPRNJ, YYL OKLFEQWI KMC BQG MCOONJTED; IWF NL L DNTD QSWAV YGXM CJJ OFMNP BYD QW C KSCQXWX NLABKTL, LVM YJLE ACCRNTVP CGMFB, JPI QSWDVNLR WOH BGEP QKX FPIM! QW MQN FKYF SMA JJYO! IKQZR ZVLG NL L URPZRP.  IUKHC MMPCS RZ NNGQ TPZH WSCLAH: VT ZP ADTJ, QSM QCI LZB JU DCE PJF FLJ LRUUSEM FKYF EPN SZCPV, KWY QSM TPJU EPJV NR XQPJY FLXYGS YYG VKSSEM, JPI RSMW, VMMFOQV XFP, EQCY UZCUF GCNWVG TD XM? CJJWCM MTJYONDNQW QWWF TD MMQGFBTVP RJMATN JJPP; BQG LPPIC YTLOMA KX, RSIC VMCCMB CSW ZVN NJDE IUKAC!  DPN YFQ WWXMNLR IKQZR QWA UTKP EJA TD PALCUC, LVM YTLOMAKSE HPNVMCC AQG HMFTM IJR LEJA BGEPXWY ZPQWI XCPV, FJJL DPN PTRTKNF F AFZRQZQ LXYGFPLVLG NL EPN CNP: TB YWEXWMM JJP GMAA RSNP JV KGCAC, DZR, LNCGW ULBLJNLR QC C RGYCCG TP EEX, UMC XIMG NR ZCC VT ZP I PTNL, LVM UMC DIRF YM SMAUJJQ QCU YFP KQGXFTZN EFR: YWF K XFLTU JFTP AXOJZZLH VT RLTT VT.  FZE JTJ WZC PGYRTVP QS? QLQM VMC NIC, CX QZWW CX RSMAG BYD UXWYF PVXWLF QWA KY RZ AYGFI HQCJ.  FJTKN YFGEMM VNJW BQG JWPA JRUCLZNF, FLO BQGS LZLMGI. GEA WQ ZQP AYGFITVP VT'
    MHASH_A_VAL = 'dbe847ace3a703c71c3b3d9a7d3858e8dda53475ed2fe24def7e15856322b4c9'


    print("cipher text is ", test_ct)

    key, plaintext = statistical(Q2b_c, Q2b_mhash)

    print("ASSERTION IS ", hashlib.sha256(plaintext.encode()).hexdigest() == Q2b_mhash)

    print("decryption with key ", key, " is:")
    print(plaintext)


def print_cubecipher(Q2a_seed, Q2a_c, Q2a_mhash, Q2b_c, Q2b_mhash):

    print("PROBLEM 2 CUBECIPHER ANSWERS")
    print()

    # PART A
    C = CubeCipher(Q2a_seed)
    Q2a_m = C.decrypt(Q2a_c)
    print("PART A DECRYPTED CIPHERTEXT IS: ", Q2a_m)
    print("PART A HASH ASSERTION IS: ", hashlib.sha256(Q2a_m.encode()).hexdigest() == Q2a_mhash)
    print()

    # PART B

    key, plaintext = statistical(Q2b_c, Q2b_mhash)

    print("PART B KEY WAS: ", key)
    print("DECRYPTION WITH KEY IS: ", plaintext)
    print("PART B HASH ASSERTION IS: ", hashlib.sha256(plaintext.encode()).hexdigest() == Q2b_mhash)
    print()


if __name__ == "__main__":

    Q2a_seed='YWGYNMNPWADOWSMPWXTFMQSAQQHHDBINCQRYGVBCOXMDPQXAXJULES'
    Q2a_c='EMOW QEDQ, MCB KPQZTB PHQUG CUEE MCB IOGFWQ OO HQGW SIPQ, QSP STQ VYENQP RMQRMST YO STQ LCJT AZ. WCN LUEICJEDE LCNE BQGDACFXN OQIQF IGHL ETT EKT FA IFA PMDI YXOGF WCN RQBTYPIZS NMQ ADQ DJZ, FMFWCN WUXAGWM, FA IFA CMFTPLIXXPP, WNP FWC SODPH YHL OABGJG PUUDARQZI, YJD FTTL PHQ YDAG TGDIJA DDQL Y HOZS QPAAFT, PLZ SMUS RDAFE KCNY OGGGKUE.  UIQ WLX MQMQT ME RSNIAGH YO IF OPL XE, EMXB PHQ SGWLHAZ.  XR WLX OPKA DURUCNEZF! IFA MAOZ RQRFXT PAPQMICZ TTAJEDTRGAJU. I ETDSHD XUZC PO TQPP DED FGW WNP DTNAAF EDKATTUCE JOI. FTJH HQD IM XESUC. FA LAAZCZ AF FWC CRKBWMJ AE UU FA TTAJEDT UF WYZ SAYT IENP AU YQTTAGGPY AHTP WLUOT.  QPAZP JN WNP DTNAAF "FXQ PHQ HDGYE AR IFA SXGVEWRP," EPGZ TTQ VPUPTAC.  FKW FTT ANEMFJPAS ADSCN OZQ PZKUF, MCB IAWQ DLA RQBTYP LQEHMJS! FTDSCHF MAGYE; U YXEDT ME LCHL NQ PR OCTADJ WT AZRC. DOIQKCN, STQ VMP UB, MCB XESMC RK RQBTYP IF, NJR DED TTYZ WME HM BUXX DD PHQ XDZOTQD FSWDDUAJA, TTMI QDE TMGBHY WZTU SHMF HFA WME HYUIZS, PLZ TTQ LMNDE OPKA VQDN OQEQD XLZEQP:--   IGO TTQ KMECQ AU RDE XAQQPED; U WCWRP TXK ZEOXPPA,   "YAG WYRE NMZCZ MQ FDM XRAIC, G IUEF HSCAD YN FWID."   MH Y ZUOW LGPH UFH CUEXUSQ, OO TQ LGPH TUH LKSQ   FGGIS TUH ZALF MCB DIE NJRPOZE, PLZ TGDCQ KUF TXQ POQE. '
    Q2a_mhash='599aa36ad3fb3611ff0e274e4058bc77ccf0f3677558dd5873da64bef4c8dbc9'

    Q2b_c='  BY NO UHNEI, VWMAPS MEEETBC NXIWJUZ MH SJI OHG,    T GUWKXO JJ IBZSU YJCNCF JDX UCBYJ;   UNE, OES MALU YI IXCGUYMEJ TKNX B SBLA GHYF,    MDR, B OP YP TZLJD WGW LHQEG.   RZV QNX HWE, IWBW EIU UHNEI, QO B FPOJEHGPE RAYHCF,    QJW ALWU CKHHO CKLM FOSKFFZOBU YTE;   ZUP RHF UKNGXO B RWVD-DPCAKLLVBP BG LU JDX WZPH--    LKTJ, XXWM BD UXA KXLTEJ HY EIQP?   BG XZ OKNMS, TQEW MSF IWZX, LT XA LAZPA DBL RSUU EHNLI,    E DXAU QHE FJ MYIUL GFHU LNAQBA   UR EIU QLX ZG JDBL ZJDPFXYU--EJX LSJBHBGR UXA UHI--    BBHHP XF JK LXWM OKN T NPKLEX?   JPK WKX ZMT, OTBO UXA RHFUX, WGW JPKN CTHT QNX MZP MATD    QPH WGREIYJZ MZVWDXK EIQJ LNPU;   OAM RZV VEGBDIUZ MAP HEKLX, HJJD MAP CEJXL LOT PAX MFQG--    IKLZ XKP WTE OKN FLOQCX MZ EE EM?   BY NO UHNEI, IWBW SJI BTMSFH, E MHZL JK MAP MQS,    TGO BHCNXO FQYA VLTU SBMS NO SBYP;   BDZ MAP NKOVNWBH OMKPOWPA, PSJSD BM RBLA MH XZ ZWP,    ALT BWLMPE JDX KPTJ KY FJ MYBX.   RZV QNX HWE, IWBW EIU UHNEI, EJX PZVBZ ATCEBU LNAQEOX    MSBJ UHNC FOA PTD BI OMXLEO WL XGFH;   UXM JPK XTELOSAW TY FUH HG EIU AGW ZG OKNK YPIA--    PALU CWWX JPK OH THGKHER NMURXK?   T IQRX TYTMAKXO UXNXX BVUOMBZOI, WGW EIQP BL POEQZA,    DBYZ ABD GQPAXC; EEJM ZTWU UHNCTUHY TTSI!   ZH RZV JDBGV J'
    Q2b_mhash='db4ccc8587a6722ba0e55dcfb2f0003698136398269dcbb7785ac6140d0c7857'

    print_cubecipher(Q2a_seed, Q2a_c, Q2a_mhash, Q2b_c, Q2b_mhash)



        


