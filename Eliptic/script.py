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

P = Point(Qx, Qy, cv)

q = cv.order

# Comprobar orden de la curva
# APARTADO A)
print("Order of CV: " + str(cv.order))
print("Order of CV is prime: " + str(isprime(cv.order)))
# APARTADO B)
print("(Qx, Qy) is on curve: " + str(cv.is_on_curve(P)))
# APARTADO C)
print("Multiplication P * order_of_P: " +str(cv.mul_point(cv.order,P)))


# APARTADO D)

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

# Verificar
# FALTA ARREGLAR ESTA PARTE, sigue saliendo FALSE al final

#   Calcular (w1, w2), donde:
#   w1 = m · f2^-1 (mod q)
#   w2 = f1 · f2^−1 (mod q)
int_message = int.from_bytes(message, "big")
w1 = (int_message * pow(F2, -1, q)) % q
w2 = (F1 * pow(F2, -1, q)) % q


#   ▶ Calcular el punto de E: (x0, y0) = w1 · P + w2 · Q.
# P = Q ??
# Q = r * P donde r es: clave privada = r mod q
# De momento pongo P donde iria la Q pq no me queda claro que es P y que es Q
E =  (cv.add_point(cv.mul_point(w1, P), cv.mul_point(w2, P)))
#   ▶ Aceptar la firma si y solo si: x0 = f1 (mod q).
print("Valid Signture: ", end="")
print(E.x == (F1 % q))



