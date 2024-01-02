import base64
import hashlib
# Script per a comprovar si la firma és valida

# Rebut
rebut = r"CfrgHu+p7E"

# Codi de control
ccode = r"""m8GYSGPQIniL2LoUghcgtQicNNTPAvDP
hlhz+mC8gaavIjcM3cM3tN5vjalU0BL
Fb79iO5MG6Z8xGJ2IpkQi1ySHKOKNO+
dGWgy1fxJQv5/ZCFncuXNX1szyRec1J
znvWpaWgm2xgE2eGLu6gDRScaSvJ+Bt
eryzbf1em5fVJCRINhG4SCgPDTNfn0X
4MVEoCmsQHnPd6oeJx6s9YcuSpt9gjV
vNggFfc8EUq0hNHqTBeYR89UA62RRv/
mW/xIvFwzQtRpB96kJwT7ELMvmmV4cL
3B9WrBBmtxWyiJkWfWbZlXV6syDDpfH
H38edvQKygMWnVdqTXWIOuV/qce0AnA
==#f5S9pHo8kw7lOix2mhUJigz/IKgr
0xhV#40289dc5891ac260018bec6271
062b9d#40289dc5891ac260018bec62
704f2b96#1701031121207
""".replace("\n", "").replace(" ", "").replace("\r", "")


# Clau publica servidor
e = 65537
N = 0xa1fee0ba40faf8ab1352af26407fa61706bd91dc5c01e6606c29101ae15efa986c66ea80456f3d463ee9dc37846e5b21bbddb853a05c93dc957fddc67df0392df0beee0aeea73a7087c9ca18faac1dce10044d6b2b48b435cd87937bb52fff1e4f349073febf75c980dc3def31d84ada923d9c3219d93d73d3c70f77cef4273daed4fab0632ab447482379019158823dc923cedfbc4930f6aa8f4adbfe0db3bfc80967642d4bb7c17126cdaf901cd262e912febc7ccd0f98030709dab1c02b5b17c9e74c7d1402e7fdb43b9ead1a02c66294098a2de5d4a1517c20d46c23234f87b746d54b4ed0eca1c4a3762b588e89675f632b5f6e91420f47ce05f24870a9

# Validacio del rebut
ccode_pieces = ccode.split("#")
print(ccode_pieces)

ballotId     = base64.b64decode(ccode_pieces[1].encode("ascii"))
rebutSencer  = base64.b64encode(hashlib.sha256(ballotId).digest())

if rebutSencer.startswith(rebut.encode("ascii")):
    print("[OK] REBUT")
else:
    print("[KO] REBUT")

# Validació firma
dobleHash = base64.b64encode(hashlib.sha256(hashlib.sha256(ballotId).hexdigest().encode("ascii")).hexdigest().encode("ascii")).decode("ascii")

# Altra manera que tampoc funciona
# dobleHash = base64.b64encode(hashlib.sha256(hashlib.sha256(ballotId).digest()).digest()).decode("ascii")

missatge  = dobleHash + ";" + ccode_pieces[2] + ";" + ccode_pieces[3] + ";" + ccode_pieces[4]

missatge  = int.from_bytes(missatge.encode("ascii"), byteorder="big")
signatura = base64.b64decode(ccode_pieces[0].encode("ascii"))
signatura = int.from_bytes(signatura, byteorder="big")

# NO FUNCIONA, RETORNA FALS
okCodi = (pow(signatura, e, N) == missatge)

if okCodi:
    print("[OK] CODI DE CONTROL")
else:
    print("[KO] CODI DE CONTROL")