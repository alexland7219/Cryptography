from cryptography.hazmat.primitives import serialization
import os
import math

files = os.listdir()
myFile = "alexandre.ros.roger_pubkeyRSA_RW.pem" # Canvia amb el teu
files = [x for x in files if x[-4:] == '.pem' and x != myFile]

myModulus = 0

for f in [myFile] + files:
    with open(f, "rb") as cert_file:
        cert = serialization.load_pem_public_key(cert_file.read())

    public_key = cert.public_numbers()
    if (f == myFile):
        myModulus = public_key.n
    else:
        print(f + ": " + str(math.gcd(myModulus, public_key.n)))

exit()
