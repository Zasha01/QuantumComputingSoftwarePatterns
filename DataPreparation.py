
import json
import numpy as np
from ExperimentResult import ExperimentResult
from qiskit.ignis.verification import combine_counts
from os import mkdir
from os.path import join, exists
from datetime import datetime

def processResults(results, groundTruth, filter, string=""):
    numCircuits = len(groundTruth)
    numResults = (int)(len(results)/len(groundTruth))
    correct = [0 for i in range(numResults)]
    topTens = [0 for i in range(numResults)]
    combPos = [0 for i in range(numCircuits)]
    allPos = [[0 for i in range(numResults)] for i in range(numCircuits)]
    notFiltered = []
    numBetterAverage = 0
    numWorseAverage = 0
    numAvgCorrect = 0
    numCombCorrect = 0
    numAvgTT = 0
    numCombTT = 0
    numFiltered = 0
    for i in range(numCircuits):
        truth = groundTruth[i]
        numPossibleResults = 2**len(truth[0])
        resultSegment = results[i*numResults:i*numResults+numResults:]
        numCorrect = getNumCorrect(resultSegment, truth)
        numTopThree = getNumTopTenPercent(resultSegment, truth, numPossibleResults)
        #if numCorrect > 0:
        #if numTopThree > 0:
        if filter == None or (filter == "correct" and numCorrect > 0) or (filter == "T10" and numTopThree > 0):
            notFiltered.append(i)
            for j in range(numResults):
                correct[j] += getNumCorrect([resultSegment[j]], truth)
                topTens[j] += getNumTopTenPercent([resultSegment[j]], truth, numPossibleResults)
                p = getPosForResult(resultSegment[j], truth)
                allPos[i][j] = p
            if numTopThree > numResults / 2:
                numAvgTT += 1
            if numCorrect > numResults / 2:
                numAvgCorrect += 1
            avgPos = getAveragePos(resultSegment, truth)

            combinedResult = aggregateResults(resultSegment)
            isTopThree = getNumTopTenPercent([combinedResult], truth, numPossibleResults) == 1 
            if isTopThree:
                numCombTT += 1
            isCorrect = getNumCorrect([combinedResult], truth) == 1 
            if isCorrect:
                numCombCorrect += 1
            combinedPos = getPosForResult(combinedResult, truth)
            combPos[i] = combinedPos
            numFiltered += 1
            if combinedPos < avgPos:
                numBetterAverage += 1
            if combinedPos > avgPos:
                numWorseAverage += 1

    allPos = np.array(allPos)
    idx = np.argmax(correct)
    #TODO:
    #divsion by zero exception
    #
    numBetterBest = sum([1 for i in range(numCircuits) if combPos[i] < allPos[i][idx] and i in notFiltered])/numFiltered
    numWorseBest = sum([1 for i in range(numCircuits) if combPos[i] > allPos[i][idx] and i in notFiltered])/numFiltered
    numEqualBest = 1.0 - numBetterBest - numWorseBest
    numBetterAverage /= numFiltered
    numWorseAverage /= numFiltered
    numEqualAverage = 1.0 - numBetterAverage - numWorseAverage 
    print("number of Experiments for " + string + " = " + str(numFiltered))
            
    return [[string, "Avg", numAvgCorrect, numAvgTT, tuple(np.round((numWorseAverage, numEqualAverage, numBetterAverage), decimals=3))],
            [string, "Agg", numCombCorrect, numCombTT, "-"],
            [string, "Best", correct[idx], topTens[idx], tuple(np.round((numWorseBest, numEqualBest, numBetterBest), decimals=3))]]


def aggregateResults(counts):
    res = {}
    for c in counts:
        res = combine_counts(res, c)
    return res

def getPosForResult(result, truth):
    truthCount = 0
    for t in truth:
        
        if t in result:
           
            truthCount = max(result[t], truthCount)
    res = 0
    for k in result.keys():
     
        if result[k] > truthCount:
            res += 1
    return res

def getNumCorrect(results, truth):
    return sum(1 for r in results if getPosForResult(r, truth) == 0)

def getNumTopTenPercent(results, truth, numPossibleResults):
    fraction = (int)(numPossibleResults/10)
    fraction = max(3, fraction)
    return sum(1 for r in results if getPosForResult(r, truth) < fraction)

def getAveragePos(results, truth):
    return sum(getPosForResult(r, truth) for r in results)/len(results)

def loadResult(fileName):
    with open(fileName, "r") as f:
      res = f.read()
      o = json.loads(res)
      return ExperimentResult(groundTruth=o['groundTruth'], transpilationResults=o['transpilationResults'], optimizationResults=o['optimizationResults'], backendResults=o['backendResults'])

def saveResult(result, resultsDir, fileName=None):
    jsonString = result.toJSON()
    if fileName is None:
        fileName = join(resultsDir, "results" + str(datetime.now()) +  ".json")
    if not exists(resultsDir):
        mkdir(resultsDir)
    with open(fileName, "w") as f:
      f.write(jsonString)
    print("Writing result file: " + fileName)
    return fileName

def processResultAdapter(result, circuitAmount):
    bestResults = result[0][1] + result[1][1] + result[2][1] 
    topTenResults = result[0][2] + result[1][2] + result[2][2]
    rest = np.repeat(circuitAmount, 3) - bestResults - topTenResults
    return [bestResults, topTenResults, rest]