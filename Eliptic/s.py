from ecpy.curves     import Curve,Point
from ecpy.keys       import ECPublicKey, ECPrivateKey
from ecpy.ecdsa      import ECDSA

cv   = Curve.get_curve('secp256k1')
pu_key = ECPublicKey(Point(0x65d5b8bf9ab1801c9f168d4815994ad35f1dcb6ae6c7a1a303966b677b813b00,
                       0xe6b865e529b8ecbf71cf966e900477d49ced5846d7662dd2dd11ccd55c0aff7f,
                       cv))
pv_key = ECPrivateKey(0xfb26a4e75eec75544c0f44e937dcf5ee6355c7176600b9688c667e5c283b43c5,
                  cv)


signer = ECDSA()
sig    = signer.sign(b'01234567890123456789012345678912',pv_key)
print(''.join(['{:02X}'.format(byte) for byte in sig]))
print(sig)
assert(signer.verify(b'01234567890123456789012345678912',sig,pu_key))