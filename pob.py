import random

def proof_of_bet(drr, hashRate):
    return random.expovariate((1* drr*100)/(hashRate))
