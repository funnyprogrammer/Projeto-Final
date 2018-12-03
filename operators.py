import random as ran
import copy, math
import initialPopulation as initPop

def defineMutationProbability(tasksMutationStartProbability, tasksMutationEndProbability, operatorsMutationStartProbability, operatorsMutationEndProbability, numberOfGenerations, currentGeneration, changeMutationRateType, changeMutationRateExpBase):
    if changeMutationRateType == 0:
        tasksMutationProbability = (((numberOfGenerations * tasksMutationEndProbability) - ((tasksMutationEndProbability - tasksMutationStartProbability) * (numberOfGenerations - currentGeneration))) / numberOfGenerations)
        operatorsMutationProbability = (((numberOfGenerations * operatorsMutationEndProbability) - ((operatorsMutationEndProbability - operatorsMutationStartProbability) * (numberOfGenerations - currentGeneration))) / numberOfGenerations)
    else:
        if changeMutationRateType == 1:
            tasksMutationProbability = (((tasksMutationEndProbability - tasksMutationStartProbability) * (((math.pow(changeMutationRateExpBase, currentGeneration)) + (tasksMutationStartProbability - changeMutationRateExpBase + 1)) - tasksMutationStartProbability)) / (((math.pow(changeMutationRateExpBase, numberOfGenerations)) + (tasksMutationStartProbability - changeMutationRateExpBase + 1)) - tasksMutationStartProbability)) + tasksMutationStartProbability
            operatorsMutationProbability = (((operatorsMutationEndProbability - operatorsMutationStartProbability) * (((math.pow(changeMutationRateExpBase, currentGeneration)) + (operatorsMutationStartProbability - changeMutationRateExpBase + 1)) - operatorsMutationStartProbability)) / (((math.pow(changeMutationRateExpBase, numberOfGenerations)) + (operatorsMutationStartProbability - changeMutationRateExpBase + 1)) - operatorsMutationStartProbability)) + operatorsMutationStartProbability
        else:
            quit(99)
    return (tasksMutationProbability, operatorsMutationProbability)

def rouletteSelection(evaluatedPopulation, sortedEvaluatedPopulation, drivenMutatedIndividuals, drivenMutatedEvaluatedPopulation, drivenMutatedGenerations):
#    if drivenMutatedGenerations >= 1:
#        limit = ran.random() * drivenMutatedEvaluatedPopulation[0]
#        i = 0
#        aux = drivenMutatedEvaluatedPopulation[1][i]
#        while aux < limit:
#            i = i + 1
#            aux = aux + drivenMutatedEvaluatedPopulation[1][i]
#    else:
#        limit = ran.random() * evaluatedPopulation[0]
#        i = 0
#        aux = evaluatedPopulation[1][i][0]
#        while aux < limit:
#            i = i + 1
#            aux = aux + evaluatedPopulation[1][i][0]
    quit(99)
    return (i, drivenMutatedIndividuals[i])

def doubleTournamentSelection(evaluatedPopulation, drivenMutatedIndividuals):
    opponent1 = int(ran.random() * len(evaluatedPopulation[1]))
    opponent2 = int(ran.random() * len(evaluatedPopulation[1]))
    if ((evaluatedPopulation[1][opponent1][0]) * (drivenMutatedIndividuals[opponent1] + 1)) >= ((evaluatedPopulation[1][opponent2][0]) * (drivenMutatedIndividuals[opponent2] + 1)):
        return (opponent1, drivenMutatedIndividuals[opponent1])
    else:
        return (opponent2, drivenMutatedIndividuals[opponent2])

def parentSelection(evaluatedPopulation, sortedEvaluatedPopulation, selectionOp, drivenMutatedIndividuals, drivenMutatedEvaluatedPopulation, drivenMutatedGenerations):
    if selectionOp == 0:
        return rouletteSelection(evaluatedPopulation, sortedEvaluatedPopulation, drivenMutatedIndividuals, drivenMutatedEvaluatedPopulation, drivenMutatedGenerations)
    else:
        if selectionOp == 1:
            return doubleTournamentSelection(evaluatedPopulation, drivenMutatedIndividuals)
        else:
            quit(99)

def singleTaskCrossover(tasksNumPerc, cromossome1, cromossome2):
    offspring1 = copy.deepcopy(cromossome1)
    offspring2 = copy.deepcopy(cromossome2)
    tasksNum = int(tasksNumPerc * len(initPop.alphabet))
    for i in range(tasksNum):
        chosenTask = int(ran.random() * len(initPop.alphabet))
        offspring1[(chosenTask * 2)] = cromossome2[(chosenTask * 2)]
        offspring1[(chosenTask * 2) + 1] = cromossome2[(chosenTask * 2) + 1]
        offspring2[(chosenTask * 2)] = cromossome1[(chosenTask * 2)]
        offspring2[(chosenTask * 2) + 1] = cromossome1[(chosenTask * 2) + 1]
        for j in range(len(offspring1)):
            offspring1[j][(chosenTask * 2)] = cromossome2[j][(chosenTask * 2)]
            offspring1[j][(chosenTask * 2) + 1] = cromossome2[j][(chosenTask * 2) + 1]
            offspring2[j][(chosenTask * 2)] = cromossome1[j][(chosenTask * 2)]
            offspring2[j][(chosenTask * 2) + 1] = cromossome1[j][(chosenTask * 2) + 1]
    return (offspring2, offspring1)

def uniformCrossoverPerProcess(cromossome1, cromossome2):
    offspring1 = copy.deepcopy(cromossome1)
    offspring2 = copy.deepcopy(cromossome2)
    for i in range(0, len(initPop.alphabet)):
        if ran.random() < 0.5:
            offspring1[(i * 2)] = cromossome2[(i * 2)]
            offspring1[(i * 2) + 1] = cromossome2[(i * 2) + 1]
            offspring2[(i * 2)] = cromossome1[(i * 2)]
            offspring2[(i * 2) + 1] = cromossome1[(i * 2) + 1]
            for j in range(len(offspring1)):
                offspring1[j][(i * 2)] = cromossome2[j][(i * 2)]
                offspring1[j][(i * 2) + 1] = cromossome2[j][(i * 2) + 1]
                offspring2[j][(i * 2)] = cromossome1[j][(i * 2)]
                offspring2[j][(i * 2) + 1] = cromossome1[j][(i * 2) + 1]
        else:
            offspring1[(i * 2)] = cromossome1[(i * 2)]
            offspring1[(i * 2) + 1] = cromossome1[(i * 2) + 1]
            offspring2[(i * 2)] = cromossome2[(i * 2)]
            offspring2[(i * 2) + 1] = cromossome2[(i * 2) + 1]
            for j in range(len(offspring1)):
                offspring1[j][(i * 2)] = cromossome1[j][(i * 2)]
                offspring1[j][(i * 2) + 1] = cromossome1[j][(i * 2) + 1]
                offspring2[j][(i * 2)] = cromossome2[j][(i * 2)]
                offspring2[j][(i * 2) + 1] = cromossome2[j][(i * 2) + 1]
    return (offspring2, offspring1)

def twoPointCrossoverPerProcess(cromossome1, cromossome2):
    offspring1 = copy.deepcopy(cromossome1)
    offspring2 = copy.deepcopy(cromossome2)
    cutpoint1 = int(ran.random() * len(initPop.alphabet))
    cutpoint2 = int(ran.random() * (len(initPop.alphabet) - cutpoint1))
    cutpoint2 = cutpoint2 + cutpoint1
    for i in range(0, cutpoint1):
        offspring1[(i * 2)] = cromossome2[(i * 2)]
        offspring1[(i * 2) + 1] = cromossome2[(i * 2) + 1]
        offspring2[(i * 2)] = cromossome1[(i * 2)]
        offspring2[(i * 2)] = cromossome1[(i * 2)]
        for j in range(len(cromossome1)):
            offspring1[j][(i * 2)] = cromossome2[j][(i * 2)]
            offspring1[j][(i * 2) + 1] = cromossome2[j][(i * 2) + 1]
            offspring2[j][(i * 2)] = cromossome1[j][(i * 2)]
            offspring2[j][(i * 2) + 1] = cromossome1[j][(i * 2) + 1]
    for i in range(cutpoint2 + 1, len(initPop.alphabet)):
        offspring1[(i * 2)] = cromossome2[(i * 2)]
        offspring1[(i * 2) + 1] = cromossome2[(i * 2) + 1]
        offspring2[(i * 2)] = cromossome1[(i * 2)]
        offspring2[(i * 2) + 1] = cromossome1[(i * 2) + 1]
        for j in range(len(cromossome1)):
            offspring1[j][(i * 2)] = cromossome2[j][(i * 2)]
            offspring1[j][(i * 2) + 1] = cromossome2[j][(i * 2) + 1]
            offspring2[j][(i * 2)] = cromossome1[j][(i * 2)]
            offspring2[j][(i * 2) + 1] = cromossome1[j][(i * 2) + 1]
    return (offspring2, offspring1)

def singlePointCrossover(cromossome1, cromossome2):
    offspring1 = copy.deepcopy(cromossome1)
    offspring2 = copy.deepcopy(cromossome2)
    cutpoint = int(ran.random() * len(initPop.alphabet))
    for i in range(((cutpoint * 2) + 1) + 1, (len(cromossome1) - 3)):
        offspring1[i] = cromossome2[i]
        offspring2[i] = cromossome1[i]
        for j in range(len(cromossome1)):
            offspring1[j][i] = cromossome2[j][i]
            offspring2[j][i] = cromossome1[j][i]
    return (offspring2, offspring1)

def crossoverPerProcess(crossoverType, crossoverProbability, tasksNumPerc, cromossome1, cromossome2):
    if ran.random() < crossoverProbability:
        if crossoverType == 0:
            (cromossome1, cromossome2) = singlePointCrossover(cromossome1, cromossome2)
        else:
            if crossoverType == 1:
                (cromossome1, cromossome2) = twoPointCrossoverPerProcess(cromossome1, cromossome2)
            else:
                if crossoverType == 2:
                    (cromossome1, cromossome2) = uniformCrossoverPerProcess(cromossome1, cromossome2)
                else:
                    if crossoverType == 3:
                        (cromossome1, cromossome2) = singleTaskCrossover(tasksNumPerc, cromossome1, cromossome2)
                    else:
                        quit(99)
    return (cromossome1, cromossome2)

def tasksMutation(cromossome, probability):
    for i in range(0, len(cromossome) - 5):
        for j in range(2, len(cromossome[i]) - 3):
            if ran.random() < probability:
                if cromossome[i][j] == 0:
                    cromossome[i][j] = 1
                else:
                    cromossome[i][j] = 0

    ####    ===> eu preciso sim arrumar isso aí em baixo (e o da função de baixo), para evitar um efeito colateral na passagem de tokens

    #    if (((cromossome[i].count(1) == 0)) or ((cromossome[i].count(1) == 1) and (cromossome[i][0] == 1)) or ((cromossome[i].count(1) == 1) and (cromossome[i][-1] == 1)) or ((cromossome[i].count(1) == 2) and (cromossome[i][0] == 1) and (cromossome[i][-1] == 1))):
    #        cromossome[i][ran.randrange(1, len(cromossome[i]) - 1)] = 1
    #for i in range(1, len(cromossome) - 1):
    #    anyInput = 0
    #    for j in range(len(cromossome[i]) - 2):
    #        if cromossome[j][i] == 1:
    #            anyInput = 1
    #            break
    #    if anyInput == 0:
    #        cromossome[ran.randrange(0, len(cromossome[i]) - 2)][i] = 1
    return

def operatorsMutation(cromossome, probability):

    ##### ===>>> mudar para trocar de 0 para 1 apenas se tiver pelos menos duas entradas ou saídas

    for i in range(0, len(cromossome) - 5, 2):
        for j in range(1, 4):
            if ran.random() < probability:
                if cromossome[i][-j] == 0:
                    cromossome[i][-j] = 1
                else:
                    cromossome[i][-j] = 0
    for i in range(2, len(cromossome[-1]) - 3, 2):
        for j in range(1, 4):
            if ran.random() < probability:
                if cromossome[-j][i] == 0:
                    cromossome[-j][i] = 1
                else:
                    cromossome[-j][i] = 0
    return

def drivenMutation(auxPopulation, sortedEvaluatedAuxPopulation, drivenMutationPart, mutatedIndividuals):
#    N_BetterIndividuals = int(drivenMutationPart * len(auxPopulation))
#    dominantSchema = copy.deepcopy(auxPopulation[0])
#    for i in range(len(dominantSchema)):
#        for j in range(len(dominantSchema[i])):
#            dominantSchema[i][j] = 1
#    for i in range(N_BetterIndividuals - 1):
#        mutatedIndividuals[sortedEvaluatedAuxPopulation[i][4]] = 1
#        for j in range(len(dominantSchema)):
#            for k in range(len(dominantSchema[j])):
#                if auxPopulation[sortedEvaluatedAuxPopulation[i][4]][j][k] != auxPopulation[sortedEvaluatedAuxPopulation[i + 1][4]][j][k]:
#                    dominantSchema[j][k] = 0
#    mutatedIndividuals[sortedEvaluatedAuxPopulation[i + 1][4]] = 1
#    for i in range(N_BetterIndividuals):
#        for j in range(len(dominantSchema)):
#            for k in range(len(dominantSchema[j])):
#   if dominantSchema[j][k] == 1:
#                    if auxPopulation[sortedEvaluatedAuxPopulation[i][4]][j][k] == 0:
#                        auxPopulation[sortedEvaluatedAuxPopulation[i][4]][j][k] = 1
#                    else:
#                        auxPopulation[sortedEvaluatedAuxPopulation[i][4]][j][k] = 0
    quit(99)
    return mutatedIndividuals

def elitism(population, elitismPerc, sortedEvaluatedAuxPopulation, sortedEvaluatedPopulation, auxPopulation, drivenMutatedIndividuals):
    for i in range(round(len(population) * elitismPerc)):
        if sortedEvaluatedAuxPopulation[len(sortedEvaluatedAuxPopulation) - 1 - i][0] < sortedEvaluatedPopulation[i][0]:
            auxPopulation[sortedEvaluatedAuxPopulation[len(sortedEvaluatedAuxPopulation) - 1 - i][4]] = copy.deepcopy(population[sortedEvaluatedPopulation[i][4]])
            drivenMutatedIndividuals[sortedEvaluatedAuxPopulation[len(sortedEvaluatedAuxPopulation) - 1 - i][4]] = 0
        else:
            break
    return