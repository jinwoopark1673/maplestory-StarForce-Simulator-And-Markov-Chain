from utils import *

@memoize
def getCost(level, currStarForce):
    assert currStarForce >= 0 and currStarForce <= 24
    if currStarForce <= 9:
        return round(1000 + (level ** 3) * (currStarForce + 1) / 25, -2)
    if currStarForce <= 14:
        return round(1000 + (level ** 3) * ((currStarForce + 1) ** 2.7) / 400, -2)
    return round(1000 + (level ** 3) * ((currStarForce + 1) ** 2.7) / 200, -2)

@memoize
def getSuccessProb(currStarForce, additiveSuccess = 0, multiplicativeSuccess = 0):
    assert currStarForce >= 0 and currStarForce <= 24
    assert additiveSuccess == 0 or multiplicativeSuccess == 0
    if currStarForce <= 2:
        return min(1, (0.95 - (0.05 * currStarForce)) * (multiplicativeSuccess + 1) + additiveSuccess)
    if currStarForce <= 14:
        return min(1, (1.0 - (0.05 * currStarForce)) * (multiplicativeSuccess + 1) + additiveSuccess)
    if currStarForce <= 21:
        return min(1, 0.3 * (multiplicativeSuccess + 1) + additiveSuccess)
    if currStarForce == 22:
        return min(1, 0.03 * (multiplicativeSuccess + 1) + additiveSuccess)
    if currStarForce == 23:
        return min(1, 0.02 * (multiplicativeSuccess + 1) + additiveSuccess)
    if currStarForce == 24:
        return min(1, 0.01 * (multiplicativeSuccess + 1) + additiveSuccess)

@memoize
def getDestructionProb(currStarForce):
    assert currStarForce >= 0 and currStarForce <= 24
    if currStarForce <= 11:
        return 0
    if currStarForce == 12:
        return 0.006
    if currStarForce == 13:
        return 0.013
    if currStarForce == 14:
        return 0.014
    if currStarForce <= 17:
        return 0.021
    if currStarForce <= 19:
        return 0.028
    if currStarForce <= 21:
        return 0.07
    if currStarForce == 22:
        return 0.194
    if currStarForce == 23:
        return 0.294
    if currStarForce == 24:
        return 0.396

@memoize
def getFailureProb(currStarForce, additiveSuccess = 0, multiplicativeSuccess = 0):
    assert currStarForce >= 0 and currStarForce <= 24
    assert additiveSuccess == 0 or multiplicativeSuccess == 0
    return 1 - getSuccessProb(currStarForce, additiveSuccess, multiplicativeSuccess) - getDestructionProb(currStarForce)
