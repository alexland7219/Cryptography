import hashlib

previous_block_hash = 1092101432863740152562512612586697988483098325253172615349335545530128793
block_hash = 442305843093921801902022929707264829867840382979725486904805105115992092
seed = 72186472609592277242803223975051556099452994494467926297227573603152502594998

publicExponent = 65537
modulus = 8640252098637098094295649845092486060171272128346080055982528699687821271447618763922578475130009768268791137391472930187117105406023286725356583200089959
message = 18209271279923133578
signature = 3642434461802907383294819658720307351127771275475485576288889307459463029025182000811155311033332219977168844418824178468671511818289974150261375528769273

##
# El hash del bloque no es correcto pero la transacción sí.
# La transacción no es correcta pero el hash sí.
# El bloque es correcto.
# Ni la transacción ni el hash son correctos.

# Verificar transacción
print("Transacción: ")
print(message == pow(signature, publicExponent, modulus))

# Verificar hash
entrada=str(previous_block_hash)
entrada=entrada+str(publicExponent)
entrada=entrada+str(modulus)
entrada=entrada+str(message)
entrada=entrada+str(signature)
entrada=entrada+str(seed)
h=int(hashlib.sha256(entrada.encode()).hexdigest(),16)
print("\nHash: ")
print(h == block_hash and block_hash < 2**240)