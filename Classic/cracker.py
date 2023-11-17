from time import sleep
from string import ascii_uppercase as alf
import sympy as sy
import itertools

# Frequencies

freqs = ["BXW", "JKF", "YCD"] # Your input

analysis = ["THE", "AND", "THA", "ENT", "ING", "ION", "TIO", "FOR"] 
# Would follow NDE, HAS, NCE, EDT, TIS, OFT, STH, MEN
# Dont add too much trigrams or it will take a long time!

with open("one.txt", 'r') as f:

    aux = [[alf.index(x) for x in t] for t in freqs]
    M1  = sy.Matrix(aux)

    text = f.read()[:400] # Only 200 chars to not clutter the screen
    conv = [alf.index(x) for x in text]

    for perm in itertools.permutations(analysis, 3):
        aux = [[alf.index(x) for x in t] for t in perm]
        M2 = sy.Matrix(aux)

        try:
            Minv = M2.inv_mod(26)
            Ht = Minv * M1
            H = Ht.T 
            Hinv = H.inv_mod(26)    

        except sy.matrices.common.NonInvertibleMatrixError:
            print(perm, end=" will produce non-invertible matrix\n")
            continue


        print(perm, end=' ')
        print("produces the following text:")
        for i in range(0, len(text)-3 ,3):
            vectr = sy.Matrix([[conv[i]], [conv[i+1]], [conv[i+2]]])
            triplet = (Hinv * vectr) % 26
            print(alf[triplet[0, 0]], end="")
            print(alf[triplet[1, 0]], end="")
            print(alf[triplet[2, 0]], end="")

        print() # Flush
        sleep(1)

        