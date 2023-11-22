import hashlib
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
        
        return (message == pow(signature, self.publicExponent, self.modulus))

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
    """Class that represents a block in the blockchain"""
    
    def generador_de_hash(self):
        """Generates the hash of this block"""

        self.block_hash = 2**240 + 1

        while (self.block_hash >= 2**240): # Proof of work: 16 zeroes

            self.seed += 1 # Change the seed (proof-of-work)

            entrada  = str(self.previous_block_hash)
            entrada += str(self.transaction.public_key.publicExponent)
            entrada += str(self.transaction.public_key.modulus)
            entrada += str(self.transaction.message)
            entrada += str(self.transaction.signature)
            entrada += str(self.seed)
        
            self.block_hash = int(hashlib.sha256(entrada.encode()).hexdigest(),16)

        return self.block_hash

    def __init__(self):
        """Creates a block (non valid)"""

        self.block_hash = 0
        self.previous_block_hash = 0
        self.transaction = 0
        self.seed = 0

    def genesis(self,transaction):
        """Generates the first block of a chain with the given transaction"""

        self.previous_block_hash = 0
        self.transaction = transaction
        self.block_hash = self.generador_de_hash()

    def next_block(self, transaction):
        """Generates the next block (valid) with the given transaction"""
        
        nextb = block()
        nextb.previous_block_hash = self.block_hash
        nextb.transaction = transaction
        nextb.generador_de_hash()

        return nextb

    def verify_block(self):
        """Verifies that this block is valid"""
        
        if self.previous_block_hash >= 2**240:
            return False
        
        if not(self.transaction.verify()):
            return False
        
        if self.block_hash >= 2**(240):
            return False
        
        return True


class block_chain:
    """Class that represents a blockchain"""

    def __init__(self,transaction):
        """Generates a blockchain (list of blocks), with the first block (genesis) containing the given transaction"""
    
        self.list_of_blocks = [block()]
        self.list_of_blocks[0].genesis(transaction)

    def add_block(self,transaction):
        """Operation to add a block with the given transaction"""

        ultimob = self.list_of_blocks[-1]
        self.list_of_blocks.append(ultimob.next_block(transaction))

    def verify(self):
        """Verifies that the entire chain is valid"""
        #verifica si la cadena de bloques es válida:
        #- Comprueba que todos los bloques son válidos
        #- Comprueba que el primer bloque es un bloque "genesis"
        #- Comprueba que para cada bloque de la cadena el siguiente es correcto
        #Salida: el booleano True si todas las comprobaciones son correctas;
        #en cualquier otro caso, el booleano False y un entero
        #correspondiente al último bloque válido
        for i in range(len(self.list_of_blocks)):
            if i == 0:
                # Genesis block
                if self.list_of_blocks[i].previous_block_hash != 0:
                    return (False, i-1)

                # Next blocks
                if not self.list_of_blocks[i].verify_block():
                    return (False, i-1)

                # If there is a next block
                if i != len(self.list_of_blocks) - 1:
                    if self.list_of_blocks[i].block_hash != self.list_of_blocks[i+1].previous_block_hash:
                        return (False, i)
        else:
            return True