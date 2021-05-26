
import numpy as np
from itertools import combinations
size = 12
numOfColors = 12
totalNumOfCubes = 12

mylist =[   [(6 ,11),(7 ,12),(2 , 8),False, False, False],
            [(2 ,4 ),(2 ,7 ),(2 , 8),False, False, False],
            [(3 ,11),(3 ,7 ),(1 , 5),False, False, False],
            [(4 ,12),(4 ,7 ),(4 , 8),False, False, False],
            [(2 ,7 ),(3 ,4 ),(5 , 7),False, False, False],
            [(10,7 ),(6 ,12),(4 , 6),False, False, False],
            [(3 ,9 ),(7 ,11),(7 ,11),False, False, False],
            [(6 ,12),(10,12),(8 , 8),False, False, False],
            [(2 ,9 ),(1 ,11),(1 ,11),False, False, False],
            [(7 ,10),(7 ,10),(4 ,10),False, False, False],
            [(5 ,9 ),(1 ,7 ),(5 ,7) ,False, False, False],
            [(5 ,9 ),(1 ,5 ),(7 ,7) ,False, False, False]   ]
cubeSetforSolving = np.array(mylist,dtype=object)
countKeeper = 0
threadKeeper = 0

def initKeepers():
    global countKeeper,threadKeeper
    countKeeper = np.zeros(totalNumOfCubes, dtype=int)
    threadKeeper = np.zeros(shape=(totalNumOfCubes,1),dtype=int)
def addToCountKeeper(colorPair):
    global countKeeper
    for i in list(colorPair):
        countKeeper[i-1]+=1
def subToCountKeeper(coloPair):
    global countKeeper
    for i in list(coloPair):
        if i ==0:print(f"Youre subtracting wrong dummie")
        countKeeper[i-1]-=1
def addLayerToSolution(currentCubeIndex, currentSolutionNum,currentFaceIndex):
    global threadKeeper
    threadKeeper[currentCubeIndex,currentSolutionNum] = currentFaceIndex+1
def resetLayerSolution(currentCubeIndex, currentSolutionNum,currentFaceIndex):
    global threadKeeper
    currentPair = cubeSetforSolving[currentCubeIndex,currentFaceIndex]
    threadKeeper[currentCubeIndex,currentSolutionNum] = 0
    subToCountKeeper(currentPair)
    #print(f"{currentPair} removed due to Conflict")
    #print(f'Currnet count: {countKeeper}')
    del(currentPair)
def prepSolutionSpaces(currentSolutionNum):
    global threadKeeper
    threadKeeper = np.transpose(threadKeeper)
    threadKeeper = np.vstack((threadKeeper, np.zeros(shape=(1,totalNumOfCubes),dtype=int)))
    threadKeeper[currentSolutionNum] = np.copy(threadKeeper[currentSolutionNum-1])
    threadKeeper = np.transpose(threadKeeper)
    threadKeeper.reshape(totalNumOfCubes,-1)
    return
def setFaceChecked(cubeIndex,faceIndex):
    cubeSetforSolving[cubeIndex,faceIndex+3] = True
def resetFacesChecked(cubeNum):#last cube of subset of cubes aka bottom of the pile
        for i in range(3,6):
            cubeSetforSolving[cubeNum-1,i] = False
def isFaceChecked(cubeIndex,faceIndex):
    value = cubeSetforSolving[cubeIndex,faceIndex+3]
    #if value:
        #print(f"{cubeSetforSolving[cubeIndex,faceIndex]} rejected. Face previously Checked")
    return value
def isPairValid(cubeIndex,faceIndex):
    setFaceChecked(cubeIndex,faceIndex)
    global countKeeper
    isFit = 1
    colorPair = list(cubeSetforSolving[cubeIndex,faceIndex])
    if colorPair[0] == colorPair[1]:
        if countKeeper[colorPair[0]-1]==0:
            #print(f"{colorPair} Addded.")
            isFit = True
        else:
            #print(f"{colorPair} not Addded. Reason: [{colorPair[0]}]'s are full")
            isFit = False
    else:
        for i in range(0,2):
            colorIndex = colorPair[i]-1
            isFit = (countKeeper[colorIndex] < 2)*isFit #if we have less than 2 of that color we can try adding
            if not isFit:
                #print(f"{colorPair} not Addded. Reason: [{colorPair[i]}]'s are full")
                return False
    #if isFit:#print(f"{colorPair} Addded.")
    return isFit
def printSolution():
    #print(f'Current Solutions:\n{threadKeeper}')
    return
def restoreLayerState(currLocation,solutionNumber,combinationSubsetList):
    cubeIndex = combinationSubsetList[currLocation]-1
    solutionIndexforLayer = threadKeeper[cubeIndex,solutionNumber]-1
    resetLayerSolution(cubeIndex,solutionNumber,solutionIndexforLayer)
    if cubeIndex != combinationSubsetList[-1]-1:
        resetFacesChecked(combinationSubsetList[currLocation+1])#instead of cubeIndex plus +1 with need nextCube in sequence
def isSearchExhausted(listOfCubes):
    for cube in list(listOfCubes):
        if cubeSetforSolving[cube-1,5]==0:
            return False
    return  True
def solveHalfSolutions(combinationSubsetList):##here is were we want to start iterating
    global size
    global countKeeper
    solutionNumber = 0
    currLocation=0
    exitFlag=False
    isBackTracking = False
    isFinalCubeSoltuion = False
    global threadKeeper
    while(not exitFlag):

        #if isSearchExhausted(combinationSubsetList):
            #print(f"Search for combination {combinationSubsetList} exhausted.")
            #return

        if isFinalCubeSoltuion:
            printSolution()
            solutionNumber+=1
            prepSolutionSpaces(solutionNumber)
            currLocation-=1
        if currLocation < 0:
            #print("~~~~~~~~~~~~no other solutions found for this combination~~~~~~~~~~~~~~~~~~")
            threadKeeper = np.delete(threadKeeper,-1,1)
            printSolution()
            break

        currentCube = combinationSubsetList[currLocation]
        currentCubeIndex = currentCube-1
        #print(f"---------------------------------\nCurrently Looking at Cube[{currentCube}]\n---------------------------------")

        if isFinalCubeSoltuion:isBackTracking=True
        if isBackTracking:
            restoreLayerState(currLocation,solutionNumber,combinationSubsetList)
        for column in range(0,3):##checking first 3 colums of denoted Cube (3 2-tuples)
            if not isFaceChecked(currentCubeIndex,column) and isPairValid(currentCubeIndex,column):
                addToCountKeeper(cubeSetforSolving[currentCubeIndex,column])
                addLayerToSolution(currentCubeIndex,solutionNumber,column)
                isBackTracking=False
                if currLocation == size-1:
                    isFinalCubeSoltuion = True
                else:isFinalCubeSoltuion = False
                currLocation+=1
                break;
            elif column == 2:
                isFinalCubeSoltuion = False
                isBackTracking = True
                currLocation-=1
                #print(f"\t\t\tAll Faces Checked Traversing Back")
                break
def crossCheckThreadMatrix(threadMatrix,comboSubList,combSize):
    global size
    subSetHasSolution = 0
    #print(f'Cross Checking Half-Solutions for Combination {comboSubList}')
    totalNumOfThreads = np.size(threadMatrix,1)

    if totalNumOfThreads == 1:
        #print("Only 1 Thread Found, no Solutions")
        return False
    else:
        #print(f"Total of {totalNumOfThreads} threads found.")

        possiblePairs = list(combinations(range(0,totalNumOfThreads),2))

        for threadPair in possiblePairs:
            has_sol_flag = True
            x = threadPair[0]
            y = threadPair[1]
            for i in comboSubList:
                i-=1
                if threadMatrix[i,x] == threadMatrix[i,y]:
                    has_sol_flag = False
                    break #break to check the next pair
            if has_sol_flag == True:
                subSetHasSolution=1
                #print(f"Solution Found THreads:{threadPair}\n{threadMatrix[:,threadPair[0]]}\n{threadMatrix[:,threadPair[1]]}")
                break;
        if subSetHasSolution != 0 :return 1
        else:return 0
def resetAllFaces():
    for i in range(12):
        for c in range(3):
            cubeSetforSolving[i,c+3] = False
def checkforSize(subSetSize):
    noSolutionSubSet = 0
    has_sol_flag = False
    comb = combinations(range(1,totalNumOfCubes+1),subSetSize)
    comb = list(comb)
    i=1
    combSize = len(comb)
    totalSize = 0
    print(f'-------------------------------------------------------'
          f'\nChecking for {subSetSize} Cubes.')
    for comboSubList in comb: #this is our set of n cubes
        initKeepers()
        resetAllFaces()
        #print(f"Checking: {comboSubList}. combination {i}/{combSize}")
        solveHalfSolutions(comboSubList)
        threadMatrix = np.copy(threadKeeper)
        hasSolution = crossCheckThreadMatrix(threadMatrix,comboSubList,combSize)
        if hasSolution != 0:
            totalSize += int(hasSolution)
            #print(f"We Found a Solution for {comboSubList}")
            has_sol_flag = True
        else:
            #print(f"No Solution Set Found for {size} Cubes")
            noSolutionSubSet = comboSubList
            checkResult(noSolutionSubSet)
            print(f"Unsolvable Cubes Found:{noSolutionSubSet} @ combination {i}/{combSize}")
            continue
            #break
        i+=1
    if has_sol_flag:
        print(f"{totalSize}/{combSize} sets with Solultions found for size:{subSetSize}")

    return False
def checkResult(noSolutionsList):
    global cubeSetforSolving
    arr = np.zeros(12,dtype=int)
    for cubeNum in list(noSolutionsList):
        for i in range(3):
            pair = cubeSetforSolving[cubeNum-1,i]
            list(pair)
            arr[pair[0]-1]+=1
            arr[pair[1]-1]+= 1
    for i in range(12):
        print(f"{i+1}'s: {arr[i]}")
    del(arr)

            
    
for i in range (5,7):
    size = i
    checkforSize(size);
