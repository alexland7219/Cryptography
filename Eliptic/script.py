from ecpy.curves     import Curve,Point
from ecpy.keys       import ECPublicKey, ECPrivateKey
from ecpy.ecdsa      import ECDSA
from sympy           import isprime
from hashlib         import sha256, sha384

cv   = Curve.get_curve('secp256r1')

# Puntos de la curva (vistos en evidencia1.png)
Qx = 0x3561f4211aff6ac43bfa0647c6196ebe7038f1dc16b1bc381412d4142b1c0b31
Qy = 0x8159f567f6e72ad13c1efaaea7ed065dd66f5d894c6bc8b0e00f83cff5d38ada

# Si (Qx, Qy) no fuera de la curva, esto devolvería error.
pu_key = ECPublicKey(Point(Qx, Qy, cv))

# Comprobar orden de la curva
print("Order of CV: " + str(cv.order))
print("Order of CV is prime: " + str(isprime(cv.order)))
print("(Qx, Qy) is on curve: " + str(cv.is_on_curve(Point(Qx, Qy, cv))))

# Verification of signature
with open("mensaje.bin", "rb") as f:
    message = f.read()

message384 = sha384(message).digest() 

with open("preambulo.bin", "rb") as f:
    preambulo = f.read()

message = sha256(preambulo + message384).digest()

# Firma
signer = ECDSA()

firma = 0x3045022100d12e05f3bfa716b556effd06e4f27d621eac4ade1ab5ca1bae27d9c931f85f1a02205a9533d7f0f0f29eb486c7fd23304332a6d1b41a417d519dd17c2c0432e3be8d
firma = firma.to_bytes((firma.bit_length() + 7) // 8, 'big')

F1 = 0x00d12e05f3bfa716b556effd06e4f27d621eac4ade1ab5ca1bae27d9c931f85f1a
F2 = 0x5a9533d7f0f0f29eb486c7fd23304332a6d1b41a417d519dd17c2c0432e3be8d

print(signer.verify(message, firma, pu_key))

