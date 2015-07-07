from wallet import Wallet
from utils import *

wallet = load("/home/gueltro/.alcos/wallet.pkl")
print wallet.get_past()
