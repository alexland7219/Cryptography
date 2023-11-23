import pickle
from blockchain import *
import re

with open("Prime_blockchain_invalid.block", "rb") as f:
    bc = pickle.load(f)

    bc.verify()
