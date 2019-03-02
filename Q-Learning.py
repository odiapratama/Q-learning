from tkinter import *
import numpy as np
import random

""" 
    Nama    : Odia Pratama
    Kelas   : IF 39-13
    Nim     : 1301154405
"""
master = Tk()

arrayUP = list()
arrayDOWN = list()
arrayLEFT = list()
arrayRIGHT = list()

red_blocks = 3
green_blocks = 2
width = 20
(x , y) = (25, 25)
board = Canvas(master, width = x*width, height = y*width)

data = np.loadtxt('DataRL.txt', usecols=range(10)).astype(int)

row = 4
col = 100
"""INISIALISAI TABLE R"""
for i in range(10):
    for j in range(10):
        if (i==0):
            arrayUP.append(0)
        else:
            arrayUP.append(data[i-1][j])

for i in range(10):
    for j in range(10):
        if (i==9):
            arrayDOWN.append(0)
        else:
            arrayDOWN.append(data[i+1][j])

for i in range(10):
    for j in range(10):
        if (j==0):
            arrayLEFT.append(0)
        else:
            arrayLEFT.append(data[i][j-1])

for i in range(10):
    for j in range(10):
        if (j==9):
            arrayRIGHT.append(0)
        else:
            arrayRIGHT.append(data[i][j+1])

Rtabel = np.array([arrayUP, arrayRIGHT, arrayLEFT, arrayDOWN])
"""==========================================================="""

"""INISIALISASI TABEL Q"""
QTable = np.zeros_like(Rtabel)
for i in range(len(Rtabel)):
    for j in range(len(Rtabel[0])):
        QTable[i][j] = 0
"""===================="""

def computeQ(r, Q_Array):
    gamma = 0.8
    poin = []
    for i in range(len(Q_Array)):
        if (Q_Array[i][2] == "up"):
            poin.append(int(QTable[0, (((Q_Array[i][0] * 10)-10) + Q_Array[i][1] + 1)]))
        elif (Q_Array[i][2] == "down"):
            poin.append(int(QTable[1, (((Q_Array[i][0] * 10)-10) + Q_Array[i][1] + 1)]))
        elif (Q_Array[i][2] == "left"):
            poin.append(int(QTable[2, (((Q_Array[i][0] * 10)-10) + Q_Array[i][1] + 1)]))
        elif (Q_Array[i][2] == "right"):
            poin.append(int(QTable[3, (((Q_Array[i][0] * 10)-10) + Q_Array[i][1] + 1)]))

    # Q = []
    # for i in range(len(position)):
    #     Q.append(QTable[position][i])
    result = float(r) + (gamma * max(poin))
    return result

def findPath(x, y):
    choice = []
    if (x == 0):
        if (y == 0):
            choice.append([x+1, y, "down"])
            choice.append([x, y+1, "right"])
        elif (y == 9):
            choice.append([x, y-1, "left"])
            choice.append([x+1, y, "down"])
        else:
            choice.append([x + 1, y, "down"])
            choice.append([x, y - 1, "left"])
            choice.append([x, y + 1, "right"])
    elif (x == 9):
        if (y == 0):
            choice.append([x-1, y, "up"])
            choice.append([x, y+1, "right"])
        elif (y == 9):
            choice.append([x-1, y, "up"])
            choice.append([x, y-1, "left"])
        else:
            choice.append([x - 1, y, "up"])
            choice.append([x, y - 1, "left"])
            choice.append([x, y+1, "right"])
    elif(y == 0):
        if (x != 0 and x != 9):
            choice.append([x - 1, y, "up"])
            choice.append([x, y + 1, "right"])
            choice.append([x + 1, y, "down"])
    elif(y == 9):
        if (x != 0 and x != 9):
            choice.append([x - 1, y, "up"])
            choice.append([x, y - 1, "left"])
            choice.append([x + 1, y, "down"])
    else:
        choice.append([x - 1, y, "up"])
        choice.append([x, y + 1, "right"])
        choice.append([x, y - 1, "left"])
        choice.append([x + 1, y, "down"])

    return choice

def checkPath(x,y):
    nextPath = []
    if (x == 0):
        if (y == 0):
            if (QTable[x+1, y] >= QTable[x, y+1]):
                nextPath = QTable[x+1, y]
            else:
                nextPath = QTable[x, y + 1]
        elif (y == 9):
            if (QTable[x, y-1] >= QTable[x+1, y]):
                nextPath = QTable[x, y-1]
            else:
                nextPath = QTable[x+1, y]
        else:
            if (QTable[x + 1, y] >= QTable[x, y - 1] and QTable[x + 1, y] >= QTable[x, y + 1]):
                nextPath = QTable[x + 1, y]
            elif (QTable[x, y - 1] >= QTable[x + 1, y] and QTable[x, y - 1] >= QTable[x, y + 1]):
                nextPath = QTable[x+1, y]
            elif (QTable[x, y + 1] >= QTable[x + 1, y] and QTable[x, y + 1] >= QTable[x, y - 1]):
                nextPath = QTable[x+1, y]

    elif (x == 9):
        if (y == 0):
            if (QTable[x-1, y] >= QTable[x, y+1]):
                nextPath = QTable[x-1, y]
            else:
                nextPath = QTable[x, y + 1]
        elif (y == 9):
            if (QTable[x-1, y] >= QTable[x, y+1]):
                nextPath = QTable[x-1, y]
            else:
                nextPath = QTable[x, y-1]
        else:
            if (QTable[x - 1, y] >= QTable[x, y - 1] and QTable[x - 1, y] >= QTable[x, y+1]):
                nextPath = QTable[x - 1, y]
            elif (QTable[x, y - 1] >= QTable[x - 1, y] and QTable[x, y - 1] >= QTable[x, y+1]):
                nextPath = QTable[x, y - 1]
            elif (QTable[x, y+1] >= QTable[x - 1, y] and QTable[x, y+1] >= QTable[x, y - 1]):
                nextPath = QTable[x, y+1]
    elif(y == 0):
        if (x != 0 and x != 9):
            if (QTable[x - 1, y] >= QTable[x, y + 1] and QTable[x - 1, y] >= QTable[x + 1, y]):
                nextPath = QTable[x - 1, y]
            elif (QTable[x, y + 1] >= QTable[x - 1, y] and QTable[x, y + 1] >= QTable[x + 1, y]):
                nextPath = QTable[x, y + 1]
            elif (QTable[x + 1, y] >= QTable[x - 1, y] and QTable[x + 1, y] >= QTable[x, y + 1]):
                nextPath = QTable[x + 1, y]

    elif(y == 9):
        if (x != 0 and x != 9):
            if (QTable[x - 1, y] >= QTable[x, y - 1] and QTable[x - 1, y] >= QTable[x + 1, y]):
                nextPath = QTable[x - 1, y]
            elif (QTable[x, y - 1] >= QTable[x - 1, y] and QTable[x, y - 1] >= QTable[x + 1, y]):
                nextPath = QTable[x, y - 1]
            elif (QTable[x + 1, y] >= QTable[x - 1, y] and QTable[x + 1, y] >= QTable[x, y - 1]):
                nextPath = QTable[x + 1, y]
    else:
        if (QTable[x - 1, y] >= QTable[x, y - 1] and QTable[x - 1, y] >= QTable[x, y + 1] and QTable[x - 1, y] >= QTable[x + 1, y]):
            nextPath = QTable[x - 1, y]
        elif (QTable[x, y - 1] >= QTable[x - 1, y] and QTable[x, y - 1] >= QTable[x, y + 1] and QTable[x, y - 1] >= QTable[x + 1, y]):
            nextPath = QTable[x, y - 1]
        elif (QTable[x, y + 1] >= QTable[x - 1, y] and QTable[x, y + 1] >= QTable[x, y - 1] and QTable[x, y + 1] >= QTable[x + 1, y]):
            nextPath = QTable[x, y + 1]
        elif (QTable[x + 1, y] >= QTable[x - 1, y] and QTable[x + 1, y] >= QTable[x, y + 1] and QTable[x + 1, y] >= QTable[x, y - 1]):
            nextPath = QTable[x, y + 1]

    return nextPath

def getR(action):
    if (action[2] == "up"):
        position = [0, ((action[0]*10)-10)+(action[1]+1)]
    elif (action[2] == "down"):
        position = [1, ((action[0]*10)-10)+(action[1]+1)]
    elif (action[2] == "left"):
        position = [2, ((action[0]*10)-10)+(action[1]+1)]
    elif (action[2] == "right"):
        position = [3, ((action[0]*10)-10)+(action[1]+1)]

    return position

def updateR(q):
    if (action[2] == "up"):
        Rtabel[0, ((action[0]*10)-10)+(action[1]+1)] = q
    elif (action[2] == "down"):
        Rtabel[1, ((action[0]*10)-10)+(action[1]+1)] = q
    elif (action[2] == "left"):
        Rtabel[2, ((action[0]*10)-10)+(action[1]+1)] = q
    elif (action[2] == "right"):
        Rtabel[3, ((action[0]*10)-10)+(action[1]+1)] = q

def updateQ(q):
    if (action[2] == "up"):
        QTable[0, ((action[0]*10)-10)+(action[1]+1)] = q
    elif (action[2] == "down"):
        QTable[1, ((action[0]*10)-10)+(action[1]+1)] = q
    elif (action[2] == "left"):
        QTable[2, ((action[0]*10)-10)+(action[1]+1)] = q
    elif (action[2] == "right"):
        QTable[3, ((action[0]*10)-10)+(action[1]+1)] = q

def learn(x, y):
    Learn = []
    if (x == 0):
        if (y == 0):
            if (QTable[1, (((x+1)*10)-10)+(y+1)] >= QTable[3, ((x*10)-10)+(y+2)]):
                Learn = (QTable[1, (((x+1)*10)-10)+(y+1)])
            else:
                Learn = (QTable[3, ((x*10)-10)+(y+2)])
            # choice.append([x+1, y, "down"])
            # choice.append([x, y+1, "right"])
        elif (y == 9):
            if (QTable[2, (((x)*10)-10)+(y)] >= QTable[1, (((x+1)*10)-10)+(y+1)]):
                Learn = (QTable[2, (((x)*10)-10)+(y)])
            else:
                Learn = (QTable[1, ((x*10)-10)+(y+1)])
            # choice.append([x, y-1, "left"])
            # choice.append([x+1, y, "down"])
        else:
            if (QTable[1, (((x+1)*10)-10)+(y+1)] >= QTable[2, ((x*10)-10)+(y)] and QTable[1, (((x+1)*10)-10)+(y+1)] >= QTable[3, ((x*10)-10)+(y+2)]):
                Learn = (QTable[1, (((x+1)*10)-10)+(y+1)])
            elif(QTable[2, ((x*10)-10)+(y)] >= QTable[1, (((x+1)*10)-10)+(y+1)] and QTable[2, ((x*10)-10)+(y)] >= QTable[3, ((x*10)-10)+(y+2)]):
                Learn = (QTable[2, ((x*10)-10)+(y)])
            elif (QTable[3, ((x*10)-10)+(y+2)] >= QTable[1, (((x + 1) * 10) - 10) + (y + 1)] and QTable[3, ((x*10)-10)+(y+2)] >= QTable[2, ((x*10)-10)+(y)]):
                Learn = (QTable[3, ((x * 10) - 10) + (y + 1)])
            # choice.append([x + 1, y, "down"])
            # choice.append([x, y - 1, "left"])
            # choice.append([x, y + 1, "right"])
    elif (x == 9):
        if (y == 0):
            if (QTable[0, (((x)*10)-10)+(y+1)] >= QTable[3, ((x*10)-10)+(y+2)]):
                Learn = (QTable[0, (((x)*10)-10)+(y+1)])
            else:
                Learn = (QTable[3, ((x * 10) - 10) + (y + 2)])
            # choice.append([x-1, y, "up"])
            # choice.append([x, y+1, "right"])
        elif (y == 9):
            if (QTable[0, (((x)*10)-10)+(y+1)] >= QTable[3, ((x*10)-10)+(y+2)]):
                Learn = (QTable[0, (((x)*10)-10)+(y+1)])
            elif (QTable[2, ((x * 10) - 10) + (y)] >= QTable[1, (((x + 1) * 10) - 10) + (y + 1)] and QTable[2, ((x * 10) - 10) + (y)] >= QTable[3, ((x * 10) - 10) + (y + 2)]):
                Learn = (QTable[2, ((x * 10) - 10) + (y)])
            # choice.append([x-1, y, "up"])
            # choice.append([x, y-1, "left"])
        else:
            if (QTable[0, (((x)*10)-10)+(y+1)] >= QTable[3, ((x*10)-10)+(y+2)] and QTable[0, (((x)*10)-10)+(y+1)] >= QTable[2, ((x * 10) - 10) + (y)]):
                Learn = (QTable[0, (((x)*10)-10)+(y+1)])
            elif (QTable[2, ((x * 10) - 10) + (y)] >= QTable[0, (((x)*10)-10)+(y+1)] and QTable[2, ((x * 10) - 10) + (y)] >= QTable[3, ((x * 10) - 10) + (y + 2)]):
                Learn = (QTable[2, ((x * 10) - 10) + (y)])
            elif (QTable[3, ((x * 10) - 10) + (y + 2)] >= QTable[0, (((x)*10)-10)+(y+1)] and QTable[3, ((x * 10) - 10) + (y + 2)] >= QTable[2, ((x * 10) - 10) + (y)]):
                Learn = (QTable[3, ((x * 10) - 10) + (y + 1)])
            # choice.append([x - 1, y, "up"])
            # choice.append([x, y - 1, "left"])
            # choice.append([x, y+1, "right"])
    elif(y == 0):
        if (x != 0 and x != 9):
            if (QTable[0, (((x)*10)-10)+(y+1)] >= QTable[3, ((x*10)-10)+(y+2)] and QTable[0, (((x)*10)-10)+(y+1)] >= QTable[1, (((x+1)*10)-10)+(y+1)]):
                Learn = (QTable[0, (((x)*10)-10)+(y+1)])
            elif (QTable[3, ((x * 10) - 10) + (y + 2)] >= QTable[1, (((x + 1) * 10) - 10) + (y + 1)] and QTable[3, ((x * 10) - 10) + (y + 2)] >= QTable[0, (((x)*10)-10)+(y+1)]):
                Learn = (QTable[3, ((x * 10) - 10) + (y + 1)])
            elif (QTable[1, (((x+1)*10)-10)+(y+1)] >= QTable[3, ((x*10)-10)+(y+2)] and QTable[1, (((x+1)*10)-10)+(y+1)] >= QTable[0, (((x)*10)-10)+(y+1)]):
                Learn = (QTable[1, (((x+1)*10)-10)+(y+1)])
            # choice.append([x - 1, y, "up"])
            # choice.append([x, y + 1, "right"])
            # choice.append([x + 1, y, "down"])
    elif(y == 9):
        if (x != 0 and x != 9):
            if (QTable[0, (((x)*10)-10)+(y+1)] >= QTable[2, ((x * 10) - 10) + (y)] and QTable[0, (((x)*10)-10)+(y+1)] >= QTable[1, (((x+1)*10)-10)+(y+1)]):
                Learn = (QTable[0, (((x)*10)-10)+(y+1)])
            elif (QTable[2, ((x * 10) - 10) + (y)] >= QTable[1, (((x + 1) * 10) - 10) + (y + 1)] and QTable[2, ((x * 10) - 10) + (y)] >= QTable[0, (((x)*10)-10)+(y+1)]):
                Learn = (QTable[2, ((x * 10) - 10) + (y)])
            elif (QTable[1, (((x+1)*10)-10)+(y+1)] >= QTable[0, (((x)*10)-10)+(y+1)] and QTable[1, (((x+1)*10)-10)+(y+1)] >= QTable[2, ((x * 10) - 10) + (y)]):
                Learn = (QTable[1, (((x+1)*10)-10)+(y+1)])
            # choice.append([x - 1, y, "up"])
            # choice.append([x, y - 1, "left"])
            # choice.append([x + 1, y, "down"])
    else:
        if (QTable[0, (((x) * 10) - 10) + (y + 1)] >= QTable[2, ((x * 10) - 10) + (y)] and QTable[0, (((x) * 10) - 10) + (y + 1)] >= QTable[1, (((x + 1) * 10) - 10) + (y + 1)] and QTable[0, (((x) * 10) - 10) + (y + 1)] >= QTable[3, ((x * 10) - 10) + (y + 1)]):
            Learn = (QTable[0, (((x) * 10) - 10) + (y + 1)])
        elif (QTable[2, ((x * 10) - 10) + (y)] >= QTable[1, (((x + 1) * 10) - 10) + (y + 1)] and QTable[2, ((x * 10) - 10) + (y)] >= QTable[0, (((x) * 10) - 10) + (y + 1)] and QTable[2, ((x * 10) - 10) + (y)] >= QTable[3, ((x * 10) - 10) + (y + 1)]):
            Learn = (QTable[2, ((x * 10) - 10) + (y)])
        elif (QTable[1, (((x + 1) * 10) - 10) + (y + 1)] >= QTable[0, (((x) * 10) - 10) + (y + 1)] and QTable[1, (((x + 1) * 10) - 10) + (y + 1)] >= QTable[2, ((x * 10) - 10) + (y)] and QTable[1, (((x + 1) * 10) - 10) + (y + 1)] >= QTable[3, ((x * 10) - 10) + (y + 1)]):
            Learn = (QTable[1, (((x + 1) * 10) - 10) + (y + 1)])
        elif (QTable[3, ((x * 10) - 10) + (y + 2)] >= QTable[1, (((x + 1) * 10) - 10) + (y + 1)] and QTable[3, ((x * 10) - 10) + (y + 2)] >= QTable[0, (((x) * 10) - 10) + (y + 1)] and QTable[3, ((x * 10) - 10) + (y + 2)] >= QTable[2, ((x * 10) - 10) + (y)]):
            Learn = (QTable[3, ((x * 10) - 10) + (y + 1)])
        # choice.append([x - 1, y, "up"])
        # choice.append([x, y + 1, "right"])
        # choice.append([x, y - 1, "left"])
        # choice.append([x + 1, y, "down"])
    return Learn

arrayReward = []
for i in range(500):
    CurrentState = 0
    x = 9
    y = 0
    reward = []
    while(CurrentState != 100):
        choices = findPath(x,y)
        print(choices)
        action = random.choice(choices)
        print(action)
        r = getR(action)
        rx = r[0]
        ry = r[1]
        # print(rx, ry)
        q = computeQ(Rtabel[rx][ry], choices)
        # updateR(q)
        updateQ(q)
        x = action[0]
        y = action[1]
        # print(x, y)

        CurrentState = data[x][y]
        reward.append(CurrentState)
        print(CurrentState)
        if (CurrentState == 100):
            print("Goal State")
            print("Reward\t: ", np.sum(reward))
            arrayReward.append(np.sum(reward))

# CurrentState = 0
# x = 9
# y = 0
# reward2 = []
# arrayReward2 = []
# while(CurrentState != 100):
#     choices = learn(x,y)
#     print("Hai : ",choices)
#     # r = getR(choices)
#     # rx = r[0]
#     # ry = r[1]
#     # print(rx, ry)
#     # q = computeQ(Rtabel[rx][ry], choices)
#     # updateR(q)
#     # updateQ(q)
#     x = choices[0]
#     y = choices[1]
#     # print(x, y)
#
#     CurrentState = data[x][y]
#     reward2.append(CurrentState)
#     print(CurrentState)
#     if (CurrentState == 100):
#         print("Goal State")
#         print("Reward\t: ", np.sum(reward2))
#         arrayReward2.append(np.sum(reward2))

# print(Rtabel[rx][ry])
# print(r)
# print(action)
# print(q)
# print(choices)
print("UP\t: ", Rtabel[0])
print("DOWN\t: ", Rtabel[1])
print("LEFT\t: ", Rtabel[2])
print("RIGHT\t: ", Rtabel[3])
# print(Rtabel)
print("UP\t: ", QTable[0])
print("DOWN\t: ", QTable[1])
print("LEFT\t: ", QTable[2])
print("RIGHT\t: ", QTable[3])
# print(QTable)
# print(arrayReward)
print("Max Reward\t: ",np.max(arrayReward))
# print("Max Reward2\t: ",np.max(arrayReward2))
# print(len(arrayReward))