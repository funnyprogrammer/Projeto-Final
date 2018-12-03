import plotting as plot, recording as record, cycle as cycle, initialPopulation as iniPop, operators as op, fitness as ft
from ast import literal_eval
par = [
    [1,    ##### numberOfRounds
     30,   ##### population_size
     250,   ##### numberOfGenerations
     2,     ##### crossoverType
     1.0,   ##### crossoverProbalility
     0.5,   ##### taskNumPerc
     0.01,  ##### tasksMutationStartProbability
     0.01,  ##### tasksMutationEndProbability
     0.1,   ##### operatorsMutationStartProbability
     0.1,   ##### operatorsMutationEndProbability
     1,     #changeMutationRateType         [NÃO VALE A PENA USAR A OPÇÃO '0']
     1.01,  #changeMutationRateExpBase      [PARECE QUE OUTRA OPÇÃO É RUIM]
     0,     ##### drivenMutation
     0.30,  ##### drivenMutationPart
     100,   ##### limitBestFitnessRepetionCount
     0.0, #0.3,   ##### TPweight
     1.0, #0.7,   ##### completenessWeight
     0.17,   ##### precisenessWeight
     0.0,   #compleness+precision-start      [NÃO MEXER MAIS NISSO AGORA QUE ACERTOU A INICIALIZAÇÃO]
     1,     #numberOfRandomTracesPerLogTrace [ISSO NÃO FAZ MAIS SENTIDO]
     0.01,  #traceSizeStartFactor            [ISSO NÃO FAZ MAIS SENTIDO]
     1.0,   #traceSizeEndFactor              [ISSO NÃO FAZ MAIS SENTIDO]
     1,     #changeTraceSizeFactorType       [ISSO NÃO FAZ MAIS SENTIDO]
     1.0055,#changeTraceSizeFactorExpBase    [ISSO NÃO FAZ MAIS SENTIDO]
     0.25,  ###### elitismPerc
     1,     ###### selectionOp    ===> PRECISA CORRIGIR PARA A ROLETA, PARA NÚMEROS NEGATIVOS!!! SE FICAREM NEGATIVOS MESMO
     0,     #selectionTp                     [NOT YORKING YET]
     0,     #lambdaValue                     [NOT YORKING YET]
     0,    #HammingThreshold                [NOT YORKING YET]
     5],   #migration time
#[10, 100, 50, 3, 1.0, 6, 0.01, 0.01, 0.10, 0.10, 1, 1.01, 0, 0.30, 100, 0.3, 0.7, 0.1, 0.0, 1, 0.01, 1.0, 1, 1.000055, 0.25, 1, 0, 0, 0],
]

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def set_broadcast(population, fitness, position, island):
    allBests = []
    with open('broadcast_{0}.txt'.format(island), 'r') as broad1:
        for line in nonblank_lines(broad1):
            allBests.append(literal_eval(line))
    broad1.close()
    allBests.append(population[position])
    with open('broadcast_{0}.txt'.format(island), 'w') as broad2:
        for ini in range(len(allBests)):
            broad2.write(str(allBests[ini]) + '\n')

    allEVA = []
    with open('evaluationB_{0}.txt'.format(island), 'r') as broad1:
        for line in nonblank_lines(broad1):
            allEVA.append(literal_eval(line))
    broad1.close()
    allEVA.append(fitness)
    with open('evaluationB_{0}.txt'.format(island), 'w') as broad2:
        for ini in range(len(allEVA)):
            broad2.write(str(allEVA[ini]) + '\n')

def initializeOp(barrier, island):

    logSizeAndMaxTraceSize = [0, float('inf'), 0]
    alphabet = []
    iniPop.createAlphabet(iniPop.log, iniPop.alphabet)
    iniPop.processLog(iniPop.log, logSizeAndMaxTraceSize)

    for parameter in range(len(par)):

        numberOfRounds = par[parameter][0]  # >= 2
        population_size = par[parameter][1]  # >= 2
        numberOfGenerations = par[parameter][2]
        crossoverType = par[parameter][3]  #0 - simples; 1 - duplo; 2 - uniforme; 3 - por tarefa
        crossoverProbability = par[parameter][4]
        tasksNumPerc = par[parameter][5]   # usado apenas se crossoverType = 3
        tasksMutationStartProbability = par[parameter][6]
        tasksMutationEndProbability = par[parameter][7]
        operatorsMutationStartProbability = par[parameter][8]
        operatorsMutationEndProbability = par[parameter][9]
        changeMutationRateType = par[parameter][10]
        changeMutationRateExpBase = par[parameter][11]
        drivenMutation = par[parameter][12]
        drivenMutationPart = par[parameter][13]
        limitBestFitnessRepetionCount = par[parameter][14]
        TPweight = par[parameter][15]
        completenessWeight = par[parameter][16]
        precisenessWeight = par[parameter][17]
        precisenessstart = par[parameter][18]
        numberOfRandomTracesPerLogTrace = par[parameter][19]
        traceSizeStartFactor = par[parameter][20]
        traceSizeEndFactor = par[parameter][21]
        changeTraceSizeFactorType = par[parameter][22]
        changeTraceSizeFactorExpBase = par[parameter][23]
        elitismPerc = par[parameter][24]  # usado apenas sem "híbrido"
        selectionOp = par[parameter][25]  # 0 - roleta / 1 - torneio
        selectionTp = par[parameter][26]  # 0 - simples / 1 - híbrido
        lambdaValue = par[parameter][27]  # usado apenas com "híbrido"
        HammingThreshold = par[parameter][28]  # usado apenas com "híbrido"
        migrationtime = par[parameter][29] 
        highestValueAndPosition = [[0, 0, 0], -1]
        traceSizeFactor = traceSizeStartFactor
        evaluateCompANDPrec = 0
        if highestValueAndPosition[0][1] >= precisenessstart:
            evaluateCompANDPrec = 1
        (population, evaluatedPopulation, referenceCromossome, averageEnabledTasks) = iniPop.initializePopulation(island, population_size, TPweight, precisenessWeight, evaluateCompANDPrec, completenessWeight,logSizeAndMaxTraceSize, numberOfRandomTracesPerLogTrace, traceSizeFactor)
        #FITNESS
        fitnessEvolution = []
        (highestValueAndPosition, sortedEvaluatedPopulation) = cycle.chooseHighest(evaluatedPopulation)
        lowestValue = cycle.chooseLowest(sortedEvaluatedPopulation)
        averageValue = cycle.calculateAverage(evaluatedPopulation)
        fitnessEvolution.append([lowestValue, highestValueAndPosition[0][0], averageValue, 0])
        #print('parameters:', parameter, '/ generation:', 0, '/ total fitness:', "%.6f" % highestValueAndPosition[0][0], '/ TP:', "%.6f" % highestValueAndPosition[0][1], '/ completeness:',  "%.6f" % highestValueAndPosition[0][2], '/ preciseness:',  "%.6f" % highestValueAndPosition[0][3], '/ EqualCount:', fitnessEvolution[0][3], traceSizeFactor)
        #if (highestValueAndPosition[0][1] == 1) and (highestValueAndPosition[0][2] == 1):
        if (highestValueAndPosition[0][2] == 1):
            break
        drivenMutatedIndividuals = [0 for _ in range(len(population))]
        drivenMutatedGenerations = 0
        for currentGeneration in range(1,numberOfGenerations): #if (migracao)
            print("Geração -----", currentGeneration, "da ilha -----", island)
            with open("evaluation_{0}.txt".format(island), "w") as eva_list:
                for i in range(len(evaluatedPopulation[1])):
                    vector = evaluatedPopulation[1][i]
                    eva_list.write(str(vector[0]) + '\n')
            if highestValueAndPosition[0][1] >= precisenessstart:
                evaluateCompANDPrec = 1
            (tasksMutationProbability, operatorsMutationProbability) = op.defineMutationProbability(tasksMutationStartProbability, tasksMutationEndProbability, operatorsMutationStartProbability, operatorsMutationEndProbability, numberOfGenerations, currentGeneration, changeMutationRateType, changeMutationRateExpBase)
            (population, evaluatedPopulation, drivenMutatedIndividuals, drivenMutatedGenerations) = cycle.generation(population, referenceCromossome, evaluatedPopulation, crossoverType, crossoverProbability, tasksNumPerc, tasksMutationProbability, operatorsMutationProbability, drivenMutation, drivenMutationPart, limitBestFitnessRepetionCount, fitnessEvolution[currentGeneration - 1][3], drivenMutatedIndividuals, drivenMutatedGenerations, TPweight, precisenessWeight, completenessWeight, elitismPerc, sortedEvaluatedPopulation, evaluateCompANDPrec, selectionOp, selectionTp, lambdaValue, HammingThreshold, currentGeneration, logSizeAndMaxTraceSize, numberOfRandomTracesPerLogTrace, traceSizeFactor, averageEnabledTasks)
            (highestValueAndPosition, sortedEvaluatedPopulation) = cycle.chooseHighest(evaluatedPopulation)
            set_broadcast(population, highestValueAndPosition[0][0], highestValueAndPosition[1], island)  # modificacao
            lowestValue = cycle.chooseLowest(sortedEvaluatedPopulation)
            averageValue = cycle.calculateAverage(evaluatedPopulation)
            fitnessEvolution.append([lowestValue, highestValueAndPosition[0][0], averageValue, 0])
            if fitnessEvolution[currentGeneration][1] ==  fitnessEvolution[currentGeneration - 1][1]:
                fitnessEvolution[currentGeneration][3] = fitnessEvolution[currentGeneration - 1][3] + 1
            #print('parameters:', parameter, '/ generation:', currentGeneration, '/ total fitness:', "%.6f" % highestValueAndPosition[0][0], '/ TP:', "%.6f" % highestValueAndPosition[0][1], '/ completeness:', "%.6f" % highestValueAndPosition[0][2], '/ preciseness:', "%.6f" % highestValueAndPosition[0][3], '/ EqualCount:', fitnessEvolution[currentGeneration][3], "%.1f" % traceSizeFactor)
            #if ((highestValueAndPosition[0][1] == 1) and (highestValueAndPosition[0][2] == 1)) and (fitnessEvolution[currentGeneration][3] == 100):
            if ((highestValueAndPosition[0][2] == 1)) and (fitnessEvolution[currentGeneration][3] == 500):
                break
            if currentGeneration > 0 and currentGeneration%migrationtime == 0:
                barrier.wait()
                barrier.reset()


            

        #PLOT
        #cycle.postProcessing(population)
        #print("%.6f" % highestValueAndPosition[0][0], "%.6f" % highestValueAndPosition[0][1], "%.6f" % highestValueAndPosition[0][2], "%.6f" % highestValueAndPosition[0][3], alphabet, population[highestValueAndPosition[1]])
        #plot.plot_evolution(fitnessEvolution, str(par[parameter]), str(parameter), str(round))
        #record.record_evolution(iniPop.log, 'PAR-COMB-' + str(par[parameter]), str(highestValueAndPosition[0][0]), fitnessEvolution, iniPop.alphabet, population[highestValueAndPosition[1]])
