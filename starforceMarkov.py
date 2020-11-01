import random
import numpy as np
from utils import *
from starforceData import *

np.set_printoptions(suppress=True,
   formatter={'float_kind':'{:f}'.format})

# (cost, currStarForce, successProb) -> (cost, true if perfect success, upgrade amount)
@memoize
def eventDefault(cost, currStarForce, successProb):
    return (cost, False, 1)

@memoize
def event30Discount(cost, currStarForce, successProb):
    return (cost * 0.7, False, 1)

@memoize
def event5_10_15PerfectChance(cost, currStarForce, successProb):
    if currStarForce == 5 or currStarForce == 10 or currStarForce == 15:
        return (cost, True, 1)
    else:
        return (cost, False, 1)

@memoize
def eventBelow10DoubleUpgrade(cost, currStarForce, successProb):
    if currStarForce < 10:
        return (cost, False, 2)
    else:
        return (cost, False, 1)

def computeCost(level, additiveSuccess = 0, multiplicativeSuccess = 0, event = eventDefault):
    c = [getCost(level, i) for i in range(25)]
    c.append(0)
    chanceGroup = (11, 12, 13, 16, 17, 18, 21, 22, 23)
    for i in chanceGroup:
        c.append(getCost(level, i))
    for i in chanceGroup:
        c.append(getCost(level, i - 1))
    cost = np.array([c]).T
    t = buildTransitionMatrix(additiveSuccess, multiplicativeSuccess, event)
    prod = np.linalg.inv(np.identity(44) - t) @ cost
    return (prod[0] - prod)[:26]

def computeNumTries(additiveSuccess = 0, multiplicativeSuccess = 0, event = eventDefault):
    cost = np.ones((44, 1))
    t = buildTransitionMatrix(additiveSuccess, multiplicativeSuccess, event)
    prod = np.linalg.inv(np.identity(44) - t) @ cost
    return (prod[0] - prod)[:26]

def computeNumDestroyed(additiveSuccess = 0, multiplicativeSuccess = 0, event = eventDefault):
    d = np.zeros((44, 44))
    for i in range(12, 25):
        d[i, 12] = 1
    for i in range(27, 35):
        d[i, 12] = 1
    t = buildTransitionMatrix(additiveSuccess, multiplicativeSuccess, event)
    prod = np.linalg.inv(np.identity(44) - t) @ np.array([np.diagonal(t @ d.T)]).T
    return (prod[0] - prod)[:26]

def buildTransitionMatrix(additiveSuccess = 0, multiplicativeSuccess = 0, event = eventDefault):
    s = lambda x:getSuccessProb(x, additiveSuccess, multiplicativeSuccess)
    f = lambda x:getFailureProb(x, additiveSuccess, multiplicativeSuccess)
    d = getDestructionProb
    t = np.zeros((44, 44))
    # chance stack 0 cases
    # success
    for i in range(25):
        t[i, i + 1] = s(i)
    # failure
    for i in range(10):
        t[i, i] = f(i)
    t[10, 10] = f(10)
    t[11, 10] = f(11)
    t[12, 26] = f(12)
    t[13, 27] = f(13)
    t[14, 28] = f(14)
    t[15, 15] = f(15)
    t[16, 15] = f(16)
    t[17, 29] = f(17)
    t[18, 30] = f(18)
    t[19, 31] = f(19)
    t[20, 20] = f(20)
    t[21, 20] = f(21)
    t[22, 32] = f(22)
    t[23, 33] = f(23)
    t[24, 34] = f(24)
    # destroyed
    for i in range(12, 25):
        t[i, 12] = d(i)
    # chance stack 1 cases
    # success
    t[26, 12] = s(11)
    t[27, 13] = s(12)
    t[28, 14] = s(13)
    t[29, 17] = s(16)
    t[30, 18] = s(17)
    t[31, 19] = s(18)
    t[32, 22] = s(21)
    t[33, 23] = s(22)
    t[34, 24] = s(23)
    # failure
    t[26, 35] = f(11)
    t[27, 36] = f(12)
    t[28, 37] = f(13)
    t[29, 38] = f(16)
    t[30, 39] = f(17)
    t[31, 40] = f(18)
    t[32, 41] = f(21)
    t[33, 42] = f(22)
    t[34, 43] = f(23)
    # destroyed
    t[27, 12] = d(12)
    t[28, 12] = d(13)
    t[29, 12] = d(16)
    t[30, 12] = d(17)
    t[31, 12] = d(18)
    t[32, 12] = d(21)
    t[33, 12] = d(22)
    t[34, 12] = d(23)
    # chance stack 2 cases
    # success
    t[35, 11] = 1
    t[36, 12] = 1
    t[37, 13] = 1
    t[38, 16] = 1
    t[39, 17] = 1
    t[40, 18] = 1
    t[41, 21] = 1
    t[42, 22] = 1
    t[43, 23] = 1

    return t
