import sympy as sp
from Crypto.Util.number import getPrime, inverse
from Crypto.Random import get_random_bytes

class rsa_key:
    """Class that generates an RSA keypair"""

    def __init__(self, bits_modulo=2048, e=2**16+1):
        """Initialization function. Given the length of N and e, constructs the RSA keypair"""
        
        self.publicExponent = e

        # Size of each prime factor
        primeLength = bits_modulo // 2
        
        self.primeP = e + 1
        self.primeQ = 2
        self.PhiN = (self.primeP - 1)*(self.primeQ - 1)

        while sp.gcd(e, self.PhiN) != 1:

            # Generate p
            self.primeP = getPrime(primeLength, randfunc=get_random_bytes)
            self.primeQ = self.primeP

            # Generate q != p
            while self.primeP == self.primeQ:
                self.primeQ = getPrime(primeLength, randfunc=get_random_bytes)
            
            # Compute N and Phi(N)
            self.modulus = self.primeQ * self.primeP
            self.PhiN = (self.primeP - 1)*(self.primeQ - 1)

        # Private exponent
        self.privateExponent = inverse(e, self.PhiN)

        self.privateExponentModulusPhiP = (self.privateExponent % (self.primeP-1))
        self.privateExponentModulusPhiQ = (self.privateExponent % (self.primeQ-1))
        self.inverseQModulusP = inverse(self.primeQ, self.primeP)

        # Definimos funciones para calcular el inverso modular de p mod q
        #def egcd(a, b):
        #    x,y, u,v = 0,1, 1,0
        #    while a != 0:
        #        q, r = b//a, b%a
        #        m, n = x-u*q, y-v*q
        #        b,a, x,y, u,v = a,r, u,v, m,n
        #    return b, x

        #def modinv(a, m):
        #    g, x = egcd(a, m)
        #    if g != 1:
        #        raise Exception('No modular inverse')
        #    return x%m

        #self.inverseQModulusP = modinv(q,p)

        # For debugging purposes
        print(self) 

    def sign(self,message):
        """Signs the message using CRT (faster)"""

        m_p = pow(message, self.privateExponentModulusPhiP, self.primeP)
        m_q = pow(message, self.privateExponentModulusPhiQ, self.primeQ)
        h   = (self.inverseQModulusP * (m_p - m_q)) % self.primeP

        return (m_q + h * self.primeQ) % self.modulus

    def sign_slow(self,message):
        """Signs the message without using the CRT"""
        return pow(message, self.privateExponent % self.PhiN, self.modulus)

    def get_publicKey(self):
        """Returns the public key"""
        return (self.modulus, self.publicExponent)

    def __str__(self):
        """String representation of the keypair"""
        return "\n*** PUBLIC KEY ***\n" +           \
                f"e = {self.publicExponent}\n" + \
                f"N = {self.modulus}\n" +         \
                "\n*** PRIVATE KEY ***\n" +         \
                f"p = {self.primeP}\n" +          \
                f"q = {self.primeQ}\n" +          \
                f"\u03d5(N) = {self.PhiN}\n" +    \
                f"d = {self.privateExponent}\n"

class rsa_public_key:
    """Class that represents an RSA public key"""

    def __init__(self, rsa_key):
        """Gets the public key from the associated rsa_key"""
    
        self.modulus, self.publicExponent = rsa_key.get_publicKey()

    def verify(self, message, signature):
        """Verifies the message with the signature"""
        
        return (signature == pow(message, self.publicExponent, self.modulus))

    def __str__(self):
        """String representation of the public key"""
        return "\n*** PUBLIC KEY ***\n" + f"e = {self.publicExponent}\n" + f"N = {self.modulus}\n"

class transaction:
    """Class that represents one transaction in the blockchain"""

    def __init__(self, message, RSAkey):
        """Generates the transaction with a message using key RSAkey"""

        self.message = message
        self.public_key = rsa_public_key(RSAkey)    
        self.signature = RSAkey.sign(message)

    def verify(self):
        """Verifies message is valid with signature"""
        return self.public_key.verify(self.message, self.signature)


class block:

    def __init__(self):
        #crea un bloque (no necesariamente v ́alido)

        self.block_hash
        self.previous_block_hash
        self.transaction
        self.seed

    def genesis(self,transaction):
        # genera el primer bloque de una cadena con la transacción "transaction"
        # que se caracteriza por:
        # - previous_block_hash=0
        # - ser válido
        a=a

    def next_block(self, transaction):
        #genera un bloque v ́alido seguiente al actual con la transacci ́on "transaction"
        a=a

    def verify_block(self):
        #Verifica si un bloque es válido:
        #-Comprueba que el hash del bloque anterior cumple las condiciones exigidas
        #-Comprueba que la transacción del bloque es válida
        #-Comprueba que el hash del bloque cumple las condiciones exigidas
        #Salida: el booleano True si todas las comprobaciones son correctas;
        #el booleano False en cualquier otro caso.
        a=a


class block_chain:
    def __init__(self,transaction):
        #genera una cadena de bloques que es una lista de bloques, el primer bloque es un bloque "genesis" generado amb la transacció "transaction"
    
        self.list_of_blocks

    def add_block(self,transaction):
        #añade a la cadena un nuevo bloque válido generado con la transacción "transaction"
        a=a

    def verify(self):
        #verifica si la cadena de bloques es válida:
        #- Comprueba que todos los bloques son válidos
        #- Comprueba que el primer bloque es un bloque "genesis"
        #- Comprueba que para cada bloque de la cadena el siguiente es correcto
        #Salida: el booleano True si todas las comprobaciones son correctas;
        #en cualquier otro caso, el booleano False y un entero
        #correspondiente al último bloque válido
        a=a