import pickle
from blockchain import *

with open("Cadena_bloques_seed_falsa.block", "rb") as f:
    block_chain = pickle.load(f)

    block_chain.verify()