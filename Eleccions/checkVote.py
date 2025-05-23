import base64
import hashlib
# Script per a comprovar si la firma és valida
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

# Rebut
rebut = r"CfrgHu+p7E"

# Codi de control
ccode = r"""XskHleQPb27l5j2B38J1FR/02H4c7uOCRghOyzohgc/4OcMS5
B1Ju0NKrqsD/ERjY6gqY1W4rfVUHkTWbrl7Qk7bxgmX1GWPVnmOIxtssJYKM3
xYJot/Z55TUlTvjK4eJexasFdc9kxXFLRg4AgKwUoisAzP5/YCNNNDtkgezvq
TUPBlhiQd+/L/XeRA7UDSa3zwv9Z59eJAFX5H/4Os8SAPVqbWYYHvDDPl7OT7
ZGVjG1O3W41Hcg6QC2Ztko934VxmktwNUJwdvppdyjXNk8nNRv6g2x5XCDIBz
QIeugFAXngXGh4HhS7dR85rt4ZSmKt+9f0DcUDgKind8Yy5Bw==#D7zO/4Lyc
63IHHpsg/P1PanMQX5KId0O#40289dc5869377b20188bea120e34006#4028
9dc4869376800188be0caab75ad0#1687337327495 
""".replace("\n", "").replace(" ", "").replace("\r", "")


# Clau publica servidor
e = 65537
N = 0xa1fee0ba40faf8ab1352af26407fa61706bd91dc5c01e6606c29101ae15efa986c66ea80456f3d463ee9dc37846e5b21bbddb853a05c93dc957fddc67df0392df0beee0aeea73a7087c9ca18faac1dce10044d6b2b48b435cd87937bb52fff1e4f349073febf75c980dc3def31d84ada923d9c3219d93d73d3c70f77cef4273daed4fab0632ab447482379019158823dc923cedfbc4930f6aa8f4adbfe0db3bfc80967642d4bb7c17126cdaf901cd262e912febc7ccd0f98030709dab1c02b5b17c9e74c7d1402e7fdb43b9ead1a02c66294098a2de5d4a1517c20d46c23234f87b746d54b4ed0eca1c4a3762b588e89675f632b5f6e91420f47ce05f24870a9

server_pk = RSA.construct((N, e))


# Validacio del rebut
ccode_pieces = ccode.split("#")
ballotId     = base64.b64decode(ccode_pieces[1].encode("ascii"))
rebutSencer  = base64.b64encode(hashlib.sha256(ballotId).digest())

if rebutSencer.startswith(rebut.encode("ascii")):
    print("[OK] REBUT")
else:
    print("[KO] REBUT")

# Validació firma
dobleHash = base64.b64encode(hashlib.sha256(hashlib.sha256(ballotId).digest()).digest()).decode("ascii")

msg  = (dobleHash + ";" + ccode_pieces[2] + ";" + ccode_pieces[3] + ";" + ccode_pieces[4]).encode("ascii")

sgn = base64.b64decode(ccode_pieces[0].encode("ascii"))

## VERIFICATION RSA-PSS
h = SHA256.new(msg)
verifier = pss.new(server_pk)

try:
    verifier.verify(h, sgn)
    print("[OK] SIGNATURE AUTHENTIC")
except (ValueError):
    print("[KO] NON-AUTHENTIC SIGNATURE")

