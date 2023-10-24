from rubik.cube import Cube
import  string
import hashlib

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
    

def main():

    Q2a_seed='YWGYNMNPWADOWSMPWXTFMQSAQQHHDBINCQRYGVBCOXMDPQXAXJULES'
    Q2a_c='EMOW QEDQ, MCB KPQZTB PHQUG CUEE MCB IOGFWQ OO HQGW SIPQ, QSP STQ VYENQP RMQRMST YO STQ LCJT AZ. WCN LUEICJEDE LCNE BQGDACFXN OQIQF IGHL ETT EKT FA IFA PMDI YXOGF WCN RQBTYPIZS NMQ ADQ DJZ, FMFWCN WUXAGWM, FA IFA CMFTPLIXXPP, WNP FWC SODPH YHL OABGJG PUUDARQZI, YJD FTTL PHQ YDAG TGDIJA DDQL Y HOZS QPAAFT, PLZ SMUS RDAFE KCNY OGGGKUE.  UIQ WLX MQMQT ME RSNIAGH YO IF OPL XE, EMXB PHQ SGWLHAZ.  XR WLX OPKA DURUCNEZF! IFA MAOZ RQRFXT PAPQMICZ TTAJEDTRGAJU. I ETDSHD XUZC PO TQPP DED FGW WNP DTNAAF EDKATTUCE JOI. FTJH HQD IM XESUC. FA LAAZCZ AF FWC CRKBWMJ AE UU FA TTAJEDT UF WYZ SAYT IENP AU YQTTAGGPY AHTP WLUOT.  QPAZP JN WNP DTNAAF "FXQ PHQ HDGYE AR IFA SXGVEWRP," EPGZ TTQ VPUPTAC.  FKW FTT ANEMFJPAS ADSCN OZQ PZKUF, MCB IAWQ DLA RQBTYP LQEHMJS! FTDSCHF MAGYE; U YXEDT ME LCHL NQ PR OCTADJ WT AZRC. DOIQKCN, STQ VMP UB, MCB XESMC RK RQBTYP IF, NJR DED TTYZ WME HM BUXX DD PHQ XDZOTQD FSWDDUAJA, TTMI QDE TMGBHY WZTU SHMF HFA WME HYUIZS, PLZ TTQ LMNDE OPKA VQDN OQEQD XLZEQP:--   IGO TTQ KMECQ AU RDE XAQQPED; U WCWRP TXK ZEOXPPA,   "YAG WYRE NMZCZ MQ FDM XRAIC, G IUEF HSCAD YN FWID."   MH Y ZUOW LGPH UFH CUEXUSQ, OO TQ LGPH TUH LKSQ   FGGIS TUH ZALF MCB DIE NJRPOZE, PLZ TGDCQ KUF TXQ POQE. '
    Q2a_mhash='599aa36ad3fb3611ff0e274e4058bc77ccf0f3677558dd5873da64bef4c8dbc9'

    C = CubeCipher(Q2a_seed)

    Q2a_m = C.decrypt(Q2a_c)

    print(Q2a_m)

    print(hashlib.sha256(Q2a_m.encode()).hexdigest() == Q2a_mhash)

if __name__ == "__main__":
    main()



        


