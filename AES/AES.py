from random import randbytes
import os


# Galois Field class
class G_F:

    def __init__(self, Polinomio_Irreducible = 0x11B):

        self.Polinomio_Irreducible = Polinomio_Irreducible
        self.Tabla_EXP = [0 for _ in range(255)]
        self.Tabla_LOG = [0 for _ in range(256)]

        for g in range(2,256):
            self.Tabla_EXP[0] = 1
            self.Tabla_LOG[1] = 0
            isGenerator = True

            for i in range(1,255):
                self.Tabla_EXP[i] = self.slowProd(self.Tabla_EXP[i-1],g)
                if self.Tabla_EXP[i] == 1:
                    isGenerator = False
                    break
                self.Tabla_LOG[self.Tabla_EXP[i]] = i

            if isGenerator:
                break


    def xTimes(self, n):
        return n << 1 if n <= 127 else (n << 1) ^ self.Polinomio_Irreducible

    def producto(self, a, b):
        if a==0 or b==0 :
            return 0
        else:
            idx = (self.Tabla_LOG[a] + self.Tabla_LOG[b]) % 255
            return self.Tabla_EXP[idx]

    def inverso(self, n):
        idx = (- self.Tabla_LOG[n]) % 255
        return self.Tabla_EXP[idx]


    def slowProd(self, a, b):
        result = 0

        for i in range(8):
            if (b >> i) & 0x01 == 0:
                continue
            aux = a
            for _ in range(i):
                aux = self.xTimes(aux)
            
            result ^= aux 

        return result

    def division(self, a, b):
        assert b != 0, "Zero division error"
        return self.producto(a,self.inverso(b))


# AES class
class AES:
    def __init__(self, keyIn, Polinomio_Irreducible = 0x11B):
        
        key = ''.join(format(x, '02x') for x in keyIn)
        

        # Initializing module to allow for operations on Galois Field
        self.Polinomio_Irreducible = Polinomio_Irreducible
        self.galois = G_F(Polinomio_Irreducible)
        
        # Step #1: Generating the S-Box and the Inverse S-Box for fast SubBytes and InvSubBytes operations 
        self.SBox = [0 for _ in range(256)]
        self.InvSBox = [0 for _ in range(256)]
        for n in range(256):
            c = 0
            b = self.galois.inverso(n)

            for j in range(7,-1,-1):
                c <<= 1
                c ^= (
                    ((b >> j) & 1) ^
                    ((b >> ((j + 4) % 8)) & 1) ^
                    ((b >> ((j + 5) % 8)) & 1) ^
                    ((b >> ((j + 6) % 8)) & 1) ^
                    ((b >> ((j + 7) % 8)) & 1) ^
                    ((0x63 >> j) & 1)
                )                

            self.SBox[n] = c
            self.InvSBox[c] = n

        self.SBox[0] = 0x63

        # Step #2: Generation of Rcon vector
        self.Nr = 11 + 2 * int((len(key) - 32)/16)

        self.Rcon = [1 for _ in range(self.Nr)]
        for i in range(1, self.Nr):
            self.Rcon[i] = self.galois.xTimes(self.Rcon[i-1])

        self.KeyExpansion(key)



    def SubBytes(self, State):
        for i in range(4):
            for j in range(4):
                State[i][j] = self.SBox[State[i][j]]
                
    def InvSubBytes(self,State):
        for i in range(4):
            for j in range(4):
                State[i][j] = self.InvSBox[State[i][j]]

    def ShiftRows(self,State):
        for i in range(1, 4):
            State[i] = State[i][i:] + State[i][:i]
    
    def InvShiftRows(self, State):
        for i in range(1, 4):
            State[i] = State[i][-i:] + State[i][:-i]

    def MixColumns(self, State): 
        for j in range(4):
            newCol = []

            for i in range(4):
                newCol.append(
                    self.galois.producto(0x02, State[i][j]) ^ 
                    self.galois.producto(0x03, State[(i+1)%4][j]) ^ 
                    State[(i+2)%4][j] ^ 
                    State[(i+3)%4][j]
                )

            for i in range(4):
                State[i][j] = newCol[i]

    def InvMixColumns(self, State):
        for j in range(4):
            newCol = []

            for i in range(4):
                newCol.append(
                    self.galois.producto(0x0e, State[i][j]) ^
                    self.galois.producto(0x0b, State[(i+1)%4][j]) ^
                    self.galois.producto(0x0d, State[(i+2)%4][j]) ^
                    self.galois.producto(0x09, State[(i+3)%4][j])
                )

            for i in range(4):
                State[i][j] = newCol[i]

    def AddRoundKey(self, State, roundKey):
        for i in range(4):
            for j in range(4):
                State[i][j] ^= roundKey[i][j]

    def KeyExpansion(self, key):
        self.keyExp = []

        # Initial key
        for c in range(0, len(key), 8):
            self.keyExp.append([0, 0, 0, 0])
            for i in range(0, 8, 2):
                byte = key[c+i:c+i+2]
                self.keyExp[-1][int(i/2)] = int(byte, 16)

        # Number of 4-byte words per key        
        Nk = len(self.keyExp)

        # Expansion of words
        for i in range(Nk, self.Nr*4):

            temp = self.keyExp[i-1][:]

            if i % Nk == 0:
                # RotWord
                temp = [temp[p] for p in [1, 2, 3, 0]]
                # SubWord
                temp = [self.SBox[n] for n in temp]
                # XOR with Rcon
                temp[0] ^= self.Rcon[int(i/Nk) - 1]
            
            elif Nk > 6 and i % Nk == 4:
                # Subword
                temp = [self.SBox[n] for n in temp]

            for j in range(4):
                # XOR with previous key
                temp[j] ^= self.keyExp[i - Nk][j]

            self.keyExp.append(temp)

        #for i in range(len(self.keyExp)):
        #    print("w" + str(i) + " ", end="")
        #    for j in range(4):
        #        print(hex(self.keyExp[i][j])[2:].zfill(2), end="")
        #    print()

    def printState(self, State):
        for i in range(4):
            for j in range(4):
                print(hex(State[i][j])[2:].zfill(2), end="")
            print(" ")

    def Cipher(self, State, Nr, Expanded_KEY, doPrint):
        # Modify the State in-place
        roundKey = list(zip(*Expanded_KEY[0:4]))
        self.AddRoundKey(State, roundKey)

        for ronda in range(1, Nr-1):
            self.SubBytes(State)
            self.ShiftRows(State)
            self.MixColumns(State)
            roundKey = list(zip(*Expanded_KEY[4*ronda:4*ronda+4]))
            self.AddRoundKey(State, roundKey)
        
        self.SubBytes(State)
        self.ShiftRows(State)

        roundKey = list(zip(*Expanded_KEY[4*Nr-4:4*Nr]))
        self.AddRoundKey(State, roundKey)

    def InvCipher(self, State, Nr, Expanded_KEY):
        # Modify the State in-place
        roundKey = list(zip(*Expanded_KEY[4*Nr-4:4*Nr]))
        self.AddRoundKey(State, roundKey)

        for ronda in range(Nr-2, 0, -1):
            self.InvShiftRows(State)
            self.InvSubBytes(State)
            roundKey = list(zip(*Expanded_KEY[4*ronda:4*ronda+4]))
            self.AddRoundKey(State,roundKey)
            self.InvMixColumns(State)
        
        self.InvShiftRows(State)
        self.InvSubBytes(State)

        roundKey = list(zip(*Expanded_KEY[0:4]))
        self.AddRoundKey(State, roundKey)
    

    def encrypt_file(self, fichero):
        # Open input and output files
        inp = open(fichero, "rb")
        out = open(fichero+".enc", "wb")

        # Initialization vector randomly generated (16B)
        IV = randbytes(16)
        # IV = bytearray([0x54, 0x09, 0x76, 0x67, 0x4e, 0xcc, 0x7b, 0xf1, 0xe7, 0xb4, 0x92, 0x3e, 0x27, 0x5c, 0xd6, 0xa8])
        
        # Write the IV to the output file
        out.write(IV)

        # Store the result of the last iteration to XOR (CBC)
        lastCypher = IV

        nBytes   = os.path.getsize(fichero)
        nBlocks  = nBytes // 16
        remBytes = nBytes % 16

        # Encryption iteration        
        for n in range(nBlocks + 1):
            
            # Input plaintext. We take care of the padding
            if (n != nBlocks):
                # Normal case, we are not in the last iteration
                inpArray = inp.read(16)

            elif (remBytes == 0):
                # Last iteration: the file size is perfectly divided by 16
                inpArray = bytearray([0x10] * 16)

            else:
                # Need to concatenate the remaining input with padding
                inpArray = inp.read(remBytes) + bytearray([16 - remBytes] * (16 - remBytes))

            # XOR of inpArray and lastCypher
            stateArray = bytearray(16)
            for i in range(16):
                stateArray[i] = inpArray[4*(i%4)+(i//4)] ^ lastCypher[4*(i%4)+(i//4)]

            # Save the stateArray to a 4x4 matrix
            State = [[stateArray[i * 4 + j] for j in range(4)] for i in range(4)]

            # Encrypt
            self.Cipher(State, self.Nr, self.keyExp, (n == 0))

            # Write the encrypted result
            lastCypher = bytearray([State[i][j] for j in range(4) for i in range(4)])
            out.write(lastCypher)

        inp.close()
        out.close()

        print("DONE --> " + fichero + '.enc')

    def decrypt_file(self, fichero):
        # Open input and output files
        inp = open(fichero, "rb")
        out = open(fichero+".dec", "wb")
        
        # Getting the number of blocks we will read from the file
        nBytes   = os.path.getsize(fichero)
        nBlocks  = nBytes // 16
        
        # Obtaining IV vector (first 16 bytes of crypted file)
        IV = inp.read(16)
        
        lastCypher = IV
        
        for n in range(nBlocks - 1):
            # Decrypt block
            inpArray = inp.read(16)

            # State
            State = [[inpArray[i * 4 + j] for i in range(4)] for j in range(4)]
            
            # Decrypt
            self.InvCipher(State, self.Nr, self.keyExp)
            
            stateArray = bytearray([byte for row in State for byte in row])
            
            # XOR of lastCypher and the State
            decryptedArray = bytearray(16)
            for i in range(16):
                decryptedArray[4*(i%4)+(i//4)] = lastCypher[4*(i%4)+(i//4)] ^ stateArray[i]
            
            # Update the last block for the cain operation
            lastCypher = inpArray
            
            # For the last block we have to take into consideration the padding
            if (n != nBlocks - 2):
                # Write decrypted block
                out.write(decryptedArray)
                
            else:
                # We only write the bytes without the padding
                out.write(decryptedArray[0 : 15 - (decryptedArray[15] - 1)])        
        
        inp.close()
        out.close()

        print("DONE --> " + fichero + '.dec')
