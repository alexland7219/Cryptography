import sympy as sp
from Crypto.PublicKey import RSA
import base64
from Crypto.Cipher import PKCS1_OAEP

# Copy the two primes after factorization
p = 172707635642621509464129049853487110228923049159804767347817391543455120625100015781092569220835018907236904720790297770349551739100719704929760222502975014517684530385615854550645052488848382588544744434554204169721082734503681453529082608112151918363839226614117560216144086164602861401553826118777516563557
q = 122695759624841406386657453009063852922829521096174881350826703534540757990797985233881879996765557893750337080533197460591699586957839957674439023857182851453089708072881914020215190594805121314670298281710599916507365601448051530159767000721529650686201898818798173291005224743969898967902439338906966320587

N = p*q

phi_N = (p-1)*(q-1)
e = 2**16 + 1

d = int(sp.gcdex(e, phi_N)[0]) % phi_N

print(e*d % phi_N)

rsa_key = RSA.construct((N, e, d, p, q))
pk = rsa_key.exportKey()
pk = pk.decode("utf-8")

with open("alexandre.ros.roger_SK.pem", "w") as f:
    f.write(pk)

