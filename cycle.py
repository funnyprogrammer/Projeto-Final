import copy
import operators as op, fitness as fitn
import initialPopulation as initPop

def basicSelection(population, referenceCromossome, evaluatedPopulation, crossoverType, crossoverProbability, tasksNumPerc, tasksMutationProbability, operatorsMutationProbability, drivenMutation, drivenMutationPart, limitBestFitnessRepetionCount, bestFitnessRepetionCount, drivenMutatedIndividuals, drivenMutatedGenerations, TPweight, precisenessWeight, completenessWeight, elitismPerc, sortedEvaluatedPopulation, evaluateCompANDPrec, selectionOp, currentGeneration, logSizeAndMaxTraceSize, numberOfRandomTracesPerLogTrace, traceSizeStartFactor, averageEnabledTasks):
    drivenMutationCycle = 0
    auxPopulation = copy.deepcopy(population)
    auxDrivenMutatedIndividuals = copy.deepcopy(drivenMutatedIndividuals)
    for j in range(len(auxDrivenMutatedIndividuals)):
        auxDrivenMutatedIndividuals[j] = 0
    if (drivenMutation == 1) and (currentGeneration > 0) and (bestFitnessRepetionCount > 0) and (divmod(bestFitnessRepetionCount, limitBestFitnessRepetionCount)[1] == 0):
        drivenMutationCycle = 1
    drivenMutatedEvaluatedPopulation = [[], []]
    if drivenMutatedGenerations >= 1:
        drivenMutatedEvaluatedPopulation[0] = 0
        drivenMutatedEvaluatedPopulation[1] = [0 for _ in range(len(drivenMutatedIndividuals))]
        for j in range(len(drivenMutatedIndividuals)):
            if drivenMutatedIndividuals[j] == 1:
                drivenMutatedEvaluatedPopulation[1][j] = 1
                drivenMutatedEvaluatedPopulation[0] = drivenMutatedEvaluatedPopulation[0] + 1
            else:
                drivenMutatedEvaluatedPopulation[1][j] = evaluatedPopulation[1][j][0]
                drivenMutatedEvaluatedPopulation[0] = drivenMutatedEvaluatedPopulation[0] + evaluatedPopulation[1][j][0]
    i = 0
    while i < len(population):
        chosenIndividual1 = op.parentSelection(evaluatedPopulation, sortedEvaluatedPopulation, selectionOp, drivenMutatedIndividuals, drivenMutatedEvaluatedPopulation, drivenMutatedGenerations)
        auxPopulation[i] = copy.deepcopy(population[chosenIndividual1[0]])
        chosenIndividual2 = op.parentSelection(evaluatedPopulation, sortedEvaluatedPopulation, selectionOp, drivenMutatedIndividuals, drivenMutatedEvaluatedPopulation, drivenMutatedGenerations)
        auxPopulation[i + 1] = copy.deepcopy(population[chosenIndividual2[0]])
        if (chosenIndividual1[1] == 1) or (chosenIndividual2[1] == 1):
            auxDrivenMutatedIndividuals[i] = 1
            auxDrivenMutatedIndividuals[i + 1] = 1
        (auxPopulation[i], auxPopulation[i + 1]) = op.crossoverPerProcess(crossoverType, crossoverProbability, tasksNumPerc, auxPopulation[i], auxPopulation[i+1])
        if drivenMutationCycle == 0:
            op.tasksMutation(auxPopulation[i], tasksMutationProbability)
            op.tasksMutation(auxPopulation[i+1], tasksMutationProbability)
            op.operatorsMutation(auxPopulation[i], operatorsMutationProbability)
            op.operatorsMutation(auxPopulation[i + 1], operatorsMutationProbability)
        i = i + 2
        if (i + 1 == len(population)) and (len(population) % 2 == 1):
            i = i - 1
    if (elitismPerc > 0) or (drivenMutationCycle == 1):
        evaluatedAuxPopulation = fitn.evaluationPopulation(auxPopulation, referenceCromossome, TPweight, precisenessWeight, evaluateCompANDPrec, completenessWeight, logSizeAndMaxTraceSize, numberOfRandomTracesPerLogTrace, traceSizeStartFactor, averageEnabledTasks)
        sortedEvaluatedAuxPopulation = sorted(evaluatedAuxPopulation[1], reverse=True, key=takeFirst)
    if drivenMutatedGenerations >= 1:
        drivenMutatedGenerations = drivenMutatedGenerations - 1
        if drivenMutatedGenerations == 0:
            for j in range(len(auxDrivenMutatedIndividuals)):
                auxDrivenMutatedIndividuals[j] = 0
    drivenMutatedIndividuals = copy.deepcopy(auxDrivenMutatedIndividuals)
    if drivenMutationCycle == 1:
        drivenMutatedIndividuals = op.drivenMutation(auxPopulation, sortedEvaluatedAuxPopulation, drivenMutationPart, drivenMutatedIndividuals)
        drivenMutatedGenerations = 10
    if elitismPerc > 0:
        op.elitism(population, elitismPerc, sortedEvaluatedAuxPopulation, sortedEvaluatedPopulation, auxPopulation, drivenMutatedIndividuals)
    evaluatedNewPopulation = fitn.evaluationPopulation(auxPopulation, referenceCromossome, TPweight, precisenessWeight, evaluateCompANDPrec, completenessWeight, logSizeAndMaxTraceSize, numberOfRandomTracesPerLogTrace, traceSizeStartFactor, averageEnabledTasks)
    return (auxPopulation, evaluatedNewPopulation, drivenMutatedIndividuals, drivenMutatedGenerations)

def createIndividualTask():
    task = [[],[]]
    task[0] = [0 for _ in range(len(initPop.alphabet) + 1)]
    task[1] = [0 for _ in range(len(initPop.alphabet) + 1)]
    for i in range(len(task[0])):
        task[0][i] = 0
        task[1][i] = 0
    return task

def initializeIndividual():
    individual = [createIndividualTask() for _ in range(len(initPop.alphabet))]
    return individual

def calcHammingDistance(individual1, individual2):
    equalSum = 0
    for i in range(len(individual1)):
        for j in range(len(individual1[i][0])):
            if individual1[i][0][j] == individual2[i][0][j]:
                equalSum = equalSum + 1
            if individual1[i][1][j] == individual2[i][1][j]:
                equalSum = equalSum + 1
    return (equalSum / (( i + 1 ) * ( j + 1 ) * 2 ))

def hybridPopulationSelection(population, referenceCromossome, evaluatedPopulation, crossoverType, crossoverProbability, tasksMutationProbability, operatorsMutationProbability, drivenMutatedIndividuals, drivenMutatedGenerations, TPweight, precisenessWeight, completenessWeight, sortedEvaluatedPopulation, evaluateCompANDPrec, selectionOp, lambdaValue, HammingThreshold, i, logSizeAndMaxTraceSize, numberOfRandomTracesPerLogTrace, traceSizeStartFactor):
    offsprings = [initializeIndividual() for _ in range(int(lambdaValue * len(population)))]
    i = 0
    while i < len(offsprings):
        offsprings[i] = copy.deepcopy(population[op.parentSelection(evaluatedPopulation, sortedEvaluatedPopulation, selectionOp)])
        offsprings[i + 1] = copy.deepcopy(population[op.parentSelection(evaluatedPopulation, sortedEvaluatedPopulation, selectionOp)])
        op.crossoverPerProcess(crossoverType, crossoverProbability, offsprings[i], offsprings[i + 1])
        op.tasksMutation(offsprings[i], tasksMutationProbability)
        op.tasksMutation(offsprings[i + 1], tasksMutationProbability)
        op.operatorsMutation(offsprings[i], operatorsMutationProbability)
        op.operatorsMutation(offsprings[i + 1], operatorsMutationProbability)
        i = i + 2
        if (i + 1 == len(population)) and (len(population) % 2 == 1):
            i = i - 1
    popPlusOff = population + offsprings
    evaluatedPopPlusOff = fitn.evaluationPopulation(popPlusOff, referenceCromossome, TPweight, precisenessWeight, evaluateCompANDPrec, completenessWeight)
    sortedEvaluatedPopPlusOff = sorted(evaluatedPopPlusOff[1], reverse=True, key=takeFirst)
    auxPopulation = copy.deepcopy(population)
    auxPopulation[0] = copy.deepcopy(popPlusOff[sortedEvaluatedPopPlusOff[0][4]])
    i = 1
    j = 1
    while i < len(auxPopulation):
        if (len(popPlusOff) - j) > (len(auxPopulation) - i):
            if calcHammingDistance(popPlusOff[sortedEvaluatedPopPlusOff[0][4]], popPlusOff[sortedEvaluatedPopPlusOff[j][4]]) < HammingThreshold:
                auxPopulation[i] = copy.deepcopy(popPlusOff[sortedEvaluatedPopPlusOff[j][4]])
                i = i + 1
        else:
            auxPopulation[i] = copy.deepcopy(popPlusOff[sortedEvaluatedPopPlusOff[j][4]])
            i = i + 1
        j = j + 1

    evaluatedNewPopulation = fitn.evaluationPopulation(auxPopulation, referenceCromossome, TPweight, precisenessWeight, evaluateCompANDPrec, completenessWeight)
    return (auxPopulation, evaluatedNewPopulation)

def generation(population, referenceCromossome, evaluatedPopulation, crossoverType, crossoverProbability, tasksNumPerc, tasksMutationProbability, operatorsMutationProbability, drivenMutation, drivenMutationPart, limitBestFitnessRepetionCount, bestFitnessRepetionCount, drivenMutatedIndividuals, drivenMutatedGenerations, TPweight, precisenessWeight, completenessWeight, elitismPerc, sortedEvaluatedPopulation, evaluateCompANDPrec, selectionOp, selectionTp, lambdaValue, HammingThreshold, i, logSizeAndMaxTraceSize, numberOfRandomTracesPerLogTrace, traceSizeStartFactor, averageEnabledTasks):
    if selectionTp == 0:
        return basicSelection(population, referenceCromossome, evaluatedPopulation, crossoverType, crossoverProbability, tasksNumPerc, tasksMutationProbability, operatorsMutationProbability, drivenMutation, drivenMutationPart, limitBestFitnessRepetionCount, bestFitnessRepetionCount, drivenMutatedIndividuals, drivenMutatedGenerations, TPweight, precisenessWeight, completenessWeight, elitismPerc, sortedEvaluatedPopulation, evaluateCompANDPrec, selectionOp, i, logSizeAndMaxTraceSize, numberOfRandomTracesPerLogTrace, traceSizeStartFactor, averageEnabledTasks)
    else:
        if selectionTp == 1:
            return hybridPopulationSelection(population, referenceCromossome, evaluatedPopulation, sortedEvaluatedPopulation, crossoverType, crossoverProbability, tasksNumPerc, tasksMutationProbability, operatorsMutationProbability, drivenMutation, drivenMutationPart, limitBestFitnessRepetionCount, bestFitnessRepetionCount, drivenMutatedIndividuals, drivenMutatedGenerations, TPweight, precisenessWeight, completenessWeight, sortedEvaluatedPopulation, evaluateCompANDPrec, selectionOp, lambdaValue, HammingThreshold, i, logSizeAndMaxTraceSize, numberOfRandomTracesPerLogTrace, traceSizeStartFactor, averageEnabledTasks)
        else:
            quit()

def takeFirst(elem):
    return elem[0]

#modificado
def set_broadcast(individual,island):
    allBests = []
    with open('broadcast_{0}.txt'.format(island), 'r') as broad1:
        for line in nonblank_lines(broad1):
            allBests.append(literal_eval(line))
    broad1.close()
    allBests.append(individual)
    with open('broadcast_{0}.txt'.format(island), 'w') as broad2:
        for ini in range(len(allBests)):
            broad2.write(str(allBests[ini]) + '\n')

#modificado
def chooseHighest(evaluatedPopulation):
    highestValue = [-1, -1, -1, -1]
    sortedEvaluatedPopulation = sorted(evaluatedPopulation[1], reverse=True, key=takeFirst)
    highestValue[0] = sortedEvaluatedPopulation[0][0]
    highestValue[1] = sortedEvaluatedPopulation[0][1]
    highestValue[2] = sortedEvaluatedPopulation[0][2]
    highestValue[3] = sortedEvaluatedPopulation[0][3]
    highestPosition = sortedEvaluatedPopulation[0][4]




    return ((highestValue, highestPosition), sortedEvaluatedPopulation)

def chooseLowest(sortedEvaluatedPopulation):
    return sortedEvaluatedPopulation[-1][0]

def calculateAverage(evaluatedPopulation):
    sum = 0
    for i in range(len(evaluatedPopulation[1])):
        sum = sum + evaluatedPopulation[1][i][0]
    return(sum/len(evaluatedPopulation[1]))

def postProcessing(population):
    for i in range(len(population)):
        for k in range(len(population[i])):
            population[i][k][0] = ''
            population[i][k][1] = ''
            population[i][-5][k] = ''
            population[i][-4][k] = ''