import random
from utils import *
from starforceData import *

# (cost, currStarForce, successProb) -> (cost, true if perfect success, upgrade amount)
@memoize
def eventDefault(cost, currStarForce, successProb):
    return (cost, False, 1)

def simulate(numRuns, level, currStarForce, targetStarForce, additiveSuccess = 0, multiplicativeSuccess = 0, event = eventDefault):
    totalCost = 0
    numDestructions = 0
    numTries = 0
    for _ in range(numRuns):
        c, d, t = simulateOnce(level, currStarForce, targetStarForce, additiveSuccess, multiplicativeSuccess, event)
        totalCost += c
        numDestructions += d
        numTries += t
    return (totalCost / numRuns, numDestructions / numRuns, numTries / numRuns)

def simulateOnce(level, currStarForce, targetStarForce, additiveSuccess = 0, multiplicativeSuccess = 0, event = eventDefault):
    assert currStarForce >= 0 and currStarForce <= 24
    assert additiveSuccess == 0 or multiplicativeSuccess == 0
    totalCost = 0
    numDestructions = 0
    numTries = 0

    numRecurrentDrops = 0
    while currStarForce < targetStarForce:
        cost = getCost(level, currStarForce)
        successProb = getSuccessProb(currStarForce, additiveSuccess, multiplicativeSuccess)
        destructionProb = getDestructionProb(currStarForce)
        cost, perfectSuccess, upgradeAmount = event(cost, currStarForce, successProb)
        numTries += 1
        totalCost += cost
        if numRecurrentDrops == 2: # chance time
            perfectSuccess = True
            numRecurrentDrops = 0
        if perfectSuccess:
            numRecurrentDrops = 0
            currStarForce += upgradeAmount
        else:
            randVal = random.random()
            if randVal < successProb: # success
                numRecurrentDrops = 0
                currStarForce += upgradeAmount
            elif randVal < successProb + destructionProb: # destroyed
                currStarForce = 12
                numDestructions += 1
                numRecurrentDrops = 0
            else: # failed
                if currStarForce >= 10:
                    if currStarForce != 10 and currStarForce != 15 and currStarForce != 20:
                        currStarForce -= 1
                        numRecurrentDrops += 1
                    else:
                        numRecurrentDrops = 0
    return (totalCost, numDestructions, numTries)

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
