import base64
import hashlib
# Script per a comprovar si la firma és valida
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from itertools import product

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# Rebut
rebut = r"CfrgHu+p7E"

# Codi de control 
# IGNORE ANY ASTERISKS (*) IN THE BEGINNING
ccode = r"""iZtBXT2jxLDuQZpTeO3qJx9EtQvhfgsIz
+O9TZ6W3KvV610pTmZib+8vLdamTP7GCwKj8/0vqfG9SfWHmU4
T62gYbS2FuWC/iqeIWhTMkpixpYK099PE4PZibSlz5gdb9YJDr
PphXdaMccpESCs1zyffIfj/oUgdD0zWl57T0JqnlkLATmiwwHn
vX88Kzs86f15TT4iX5how0KVQ5d0sUD2PgvOfuZZ3WcMndGiuy
f9WCtlKc4nvhtqO8tGOknt1fzaHt6i4Id9qibq6M6TBbkmzcO9
3EabJnOV7si69oT41zTjKZ+vJ9yTQW/eVWd6NMUZ3DhPJ5OHO4
LWQQ==#bSttEmCpd6zkBMwHyL3GOTS83W780eeA#40289dc589
1ac260018a88410e3108ce#40289dc5891ac260018a88410d3
308c7#1694612893722 
""".replace("\n", "").replace(" ", "").replace("\r", "")

ENTROPY = 5

# Clau publica servidor
e = 65537
N = 0xa1fee0ba40faf8ab1352af26407fa61706bd91dc5c01e6606c29101ae15efa986c66ea80456f3d463ee9dc37846e5b21bbddb853a05c93dc957fddc67df0392df0beee0aeea73a7087c9ca18faac1dce10044d6b2b48b435cd87937bb52fff1e4f349073febf75c980dc3def31d84ada923d9c3219d93d73d3c70f77cef4273daed4fab0632ab447482379019158823dc923cedfbc4930f6aa8f4adbfe0db3bfc80967642d4bb7c17126cdaf901cd262e912febc7ccd0f98030709dab1c02b5b17c9e74c7d1402e7fdb43b9ead1a02c66294098a2de5d4a1517c20d46c23234f87b746d54b4ed0eca1c4a3762b588e89675f632b5f6e91420f47ce05f24870a9

server_pk = RSA.construct((N, e))

i = 0

ccode_pieces = ccode.split("#")
ballotId     = base64.b64decode(ccode_pieces[1].encode("ascii"))

dobleHash = base64.b64encode(hashlib.sha256(hashlib.sha256(ballotId).digest()).digest()).decode("ascii")

msg  = (dobleHash + ";" + ccode_pieces[2] + ";" + ccode_pieces[3] + ";" + ccode_pieces[4]).encode("ascii")

h = SHA256.new(msg)
verifier = pss.new(server_pk)

for combination in product(alphabet, repeat=ENTROPY):
    str_comb = "".join(combination)
    
    # Validació firma

    sgn = base64.b64decode((str_comb + ccode_pieces[0]).encode("ascii"))

    ## VERIFICATION RSA-PSS
    try:
        verifier.verify(h, sgn)
        print("[CRACKED]")
        print(combination)
        exit()
    except (ValueError):
        print("Trying combinaiton " + str(i) + " out of " + str(64**ENTROPY) + "...")
        i += 1
        continue