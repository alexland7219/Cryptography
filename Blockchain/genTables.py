from tabulate import tabulate
import secrets 
import time
import pandas as pd
from blockchain import *

headers = ["# bits", "RSA 512", "RSA 512F", "RSA 1024", "RSA 1024F", "RSA 2048", "RSA 2048F", "RSA 4096", "RSA 4096F"]

rsa512 = rsa_key(512)
rsa1024 = rsa_key(1024)
rsa2048 = rsa_key(2048)
rsa4096 = rsa_key(4096)

data = [] 

for i in range(100):
    data.append([0 for _ in range(9)])
    data[-1][0] = 5*i+5
    print("Mensaje " + str(i))
    
    random_bytes = secrets.token_bytes(5*i+5)
    mensaje = int.from_bytes(random_bytes, byteorder='big')

    for j, k in enumerate([rsa512,rsa1024, rsa2048, rsa4096]):
        t1 = time.time()
        k.sign_slow(mensaje)
        t2 = time.time()
        k.sign(mensaje)
        t3 = time.time()

        slow = (t2 - t1) * 1000
        fast = (t3 - t2) * 1000

        data[-1][2*j+1] = slow
        data[-1][2*j+2] = fast

table = tabulate(data, headers, tablefmt="grid")
print(table)

df = pd.DataFrame(data, columns=headers)

df.to_excel("data.ods", engine="odf", index=False)