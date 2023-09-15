import random

moves = ["U", "D", "F", "B", "R", "L"]
dirs = ["", "'", "2"]
wides = ["", "w"]
rotations = ["x","y","z"]

# Code modified from https://github.com/BenGotts/Python-Rubiks-Cube-Scrambler

def gen_scramble(size):
    length = {3: 20, 4: 46, 5: 60}[size]
    if size == 3:
        scr = valid([[random.choice(moves), random.choice(dirs)] for x in range(length)])
    else: 
        scr = valid([[random.choice(moves), random.choice(wides), random.choice(dirs)] for x in range(length)])

    #return ''.join(str(s[x][0]) + str(s[x][1]) + ' ' for x in range(len(s))) 
    return ' '.join([''.join(move) for move in scr])

def valid(scr):
    for x in range(1, len(scr)):
        while scr[x][0] == scr[x-1][0]:
            scr[x][0] = random.choice(moves)
    for x in range(2, len(scr)):
        while scr[x][0] == scr[x-2][0] or scr[x][0] == scr[x-1][0]:
            scr[x][0] = random.choice(moves)
    return scr