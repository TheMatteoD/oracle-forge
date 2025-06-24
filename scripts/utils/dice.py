import random

def d100():
    return random.randint(1, 100)

def d100chance(chance: int) -> bool:
    """Rolls d100 and checks if under given chance %"""
    return d100() <= chance

def d20():
    return random.randint(1, 20)

def d12():
    return random.randint(1, 12)

def d10():
    return random.randint(1, 10)

def d8():
    return random.randint(1, 8)

def d6():
    return random.randint(1, 6)

def d4():
    return random.randint(1, 4)

