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

Q = Point(Qx, Qy, cv)

q = cv.order

# Comprobar orden de la curva
# APARTADO A)
print("Order of CV: " + str(cv.order))
print("Order of CV is prime: " + str(isprime(cv.order)))
# APARTADO B)
print("(Qx, Qy) is on curve: " + str(cv.is_on_curve(Q)))
# APARTADO C)
print("Multiplication P * order_of_P: " +str(cv.mul_point(cv.order, Q)))


# APARTADO D)

# Verification of signature
with open("mensaje.bin", "rb") as f:
    message = f.read()

message384 = sha384(message).digest() 

with open("preambulo.bin", "rb") as f:
    preambulo = f.read()

message = sha256(preambulo + message384).digest()
int_message = int.from_bytes(message, "big")

# Firma
F1 = 0x00d12e05f3bfa716b556effd06e4f27d621eac4ade1ab5ca1bae27d9c931f85f1a
F2 = 0x5a9533d7f0f0f29eb486c7fd23304332a6d1b41a417d519dd17c2c0432e3be8d

# Verificar

w1 = (int_message * pow(F2, -1, q)) % q
w2 = (F1 * pow(F2, -1, q)) % q

E =  cv.add_point(w1 * cv.generator, w2 * Q)

print("Valid Signture: ", end="")
print(E.x % q == F1 % q)
