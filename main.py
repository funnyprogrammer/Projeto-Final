import plotting as plot
import recording as record
import cycle as cycle
import initialPopulation as iniPop
import operators as op
from datetime import datetime
from ast import literal_eval


par = [
    [1,     ##### numberOfRounds # >= 2
     60,   ##### population_size # >= 2
     2000,   ##### numberOfGenerations
     3,     ##### crossoverType #0 - simples; 1 - duplo; 2 - uniforme; 3 - por tarefa; 4 - BVB
     0.5,    ##### crossoverTasksNumPerc # usado apenas se crossoverType = 3 or 4 (-1 means exactly one task)
     1.0,   ##### crossoverProbalility
     1,     ##### mutationType   #0 - simples; 1 - BVB
     -1,    ##### mutationTaskNum Perc (usado apenas se mutationType = 1)
     0.01,  ##### tasksMutationStartProbability     #(usado apenas se mutationType = 1)
     0.01,  ##### tasksMutationEndProbability       #(usado apenas se mutationType = 1)
     0.1,   ##### operatorsMutationStartProbability #(usado apenas se mutationType = 1)
     0.1,   ##### operatorsMutationEndProbability   #(usado apenas se mutationType = 1)
     1,     ##### changeMutationRateType           [NÃO VALE A PENA USAR A OPÇÃO '0']
     1.01,  ##### changeMutationRateExpBase        [PARECE QUE OUTRA OPÇÃO É RUIM]
     1,     ##### drivenMutation
     0.30,  ##### drivenMutationPart
     10,    ##### limitBestFitnessRepetionCount - for drivenMutation
     30,    ##### numberOfcyclesAfterDrivenMutation (<= limitBestFitnessRepetionCount)
     0.05,   ##### TPweight
     0.95,   ##### completenessWeight
     0.2,   ##### precisenessWeight
     0.15,   ##### simplicityWeight
     1.0,   ##### precisioness-start
     30,    ##### simplicity-start
     10,    ##### completenessAttemptFactor1
     2,     ##### completenessAttemptFactor1
     0.25,  ##### elitismPerc                      # usado apenas sem "híbrido"
     1,     ##### selectionOp # 0 - roleta / 1 - torneio
     0,     ##### selectionTp                      [NOT YORKING YET] # 0 - simples / 1 - híbrido
     0,     ##### lambdaValue                      [NOT YORKING YET] # usado apenas com "híbrido"
     0,     ##### HammingThreshold                 [NOT YORKING YET] # usado apenas com "híbrido"
     5],    ##### migration time - Joon
]

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def set_broadcast_lowest(valor, island):
    allBests = []
    with open('broadcastl_{0}.txt'.format(island), 'r') as broad1:
        for line in nonblank_lines(broad1):
            allBests.append(literal_eval(line))
    broad1.close()
    allBests.append(valor)
    with open('broadcastl_{0}.txt'.format(island), 'w') as broad2:
        for ini in range(len(allBests)):
            broad2.write(str(allBests[ini]) + '\n')

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
    start = datetime.now()
    logSizeAndMaxTraceSize = [0, float('inf'), 0]
    iniPop.createAlphabet(iniPop.log, iniPop.alphabet)
    iniPop.processLog(iniPop.log, logSizeAndMaxTraceSize)
    
    for parameter in range(len(par)):
        numberOfRounds = par[parameter][0]
        population_size = par[parameter][1]
        numberOfGenerations = par[parameter][2]
        crossoverType = par[parameter][3]
        crossoverTasksNumPerc = par[parameter][4]
        crossoverProbability = par[parameter][5]
        mutationType = par[parameter][6]
        mutationTasksNumPerc = par[parameter][7]
        tasksMutationStartProbability = par[parameter][8]
        tasksMutationEndProbability = par[parameter][9]
        operatorsMutationStartProbability = par[parameter][10]
        operatorsMutationEndProbability = par[parameter][11]
        changeMutationRateType = par[parameter][12]
        changeMutationRateExpBase = par[parameter][13]
        drivenMutation = par[parameter][14]
        drivenMutationPart = par[parameter][15]
        limitBestFitnessRepetionCount = par[parameter][16]
        numberOfcyclesAfterDrivenMutation = par[parameter][17]
        TPweight = par[parameter][18]
        completenessWeight = par[parameter][19]
        precisenessWeight = 0
        simplicityWeight = 0
        precisenessStart = par[parameter][22]
        simplicityStart = par[parameter][23]
        completenessAttemptFactor1 = par[parameter][24]
        completenessAttemptFactor2 = par[parameter][25]
        elitismPerc = par[parameter][26]
        selectionOp = par[parameter][27]
        selectionTp = par[parameter][28]
        lambdaValue = par[parameter][29]
        HammingThreshold = par[parameter][30]
        migrationtime = par[parameter][31]
        for round in range(numberOfRounds):
            highestValueAndPosition = [[0, 0, 0], -1]
            if highestValueAndPosition[0][1] >= precisenessStart:
                precisenessWeight = par[parameter][20]
            (population, evaluatedPopulation, referenceCromossome, averageEnabledTasks) = iniPop.initializePopulation(island, population_size, TPweight, precisenessWeight, simplicityWeight, completenessWeight, completenessAttemptFactor1, completenessAttemptFactor2, selectionOp)
            fitnessEvolution = []
            (highestValueAndPosition, sortedEvaluatedPopulation) = cycle.chooseHighest(evaluatedPopulation)
            lowestValue = cycle.chooseLowest(sortedEvaluatedPopulation)
            averageValue = cycle.calculateAverage(evaluatedPopulation)
            fitnessEvolution.append([lowestValue, highestValueAndPosition[0][0], averageValue, 0, highestValueAndPosition[0][1], highestValueAndPosition[0][2], highestValueAndPosition[0][3], highestValueAndPosition[0][4], 0, 0])
            if fitnessEvolution[0][8] >= simplicityStart:
                simplicityWeight = par[parameter][21]
            print('par:', parameter, '/ round:', round, '/ gen:', 0, '/ total fitness:', "%.5f" % highestValueAndPosition[0][0], '/ comp:',  "%.5f" % highestValueAndPosition[0][1], '/ TP:', "%.5f" % highestValueAndPosition[0][2], '/ prec:',  "%.5f" % highestValueAndPosition[0][3], '/ simp:',  "%.5f" % highestValueAndPosition[0][4], '/ eqCount:', fitnessEvolution[0][3], fitnessEvolution[0][8], fitnessEvolution[0][9])
            #if (highestValueAndPosition[0][2] == 1) and (highestValueAndPosition[0][1] == 1):
            #if (highestValueAndPosition[0][1] == 1):
            #    break
            drivenMutatedIndividuals = [0 for _ in range(len(population))]
            drivenMutatedGenerations = 0
            for currentGeneration in range(1,numberOfGenerations):
                print("Geração -----", currentGeneration, "da ilha -----", island) #printar a geração - Joon
                with open("evaluation_{0}.txt".format(island), "w") as eva_list: #extrair a população do arquivo Island para o vetor na memória - Joon 
                    for i in range(len(evaluatedPopulation[1])):
                        vector = evaluatedPopulation[1][i]
                        eva_list.write(str(vector[0]) + '\n')
                if highestValueAndPosition[0][1] >= precisenessStart:
                    precisenessWeight = par[parameter][20]
                (tasksMutationProbability, operatorsMutationProbability) = op.defineMutationProbability(tasksMutationStartProbability, tasksMutationEndProbability, operatorsMutationStartProbability, operatorsMutationEndProbability, numberOfGenerations, currentGeneration, changeMutationRateType, changeMutationRateExpBase)
                (population, evaluatedPopulation, drivenMutatedIndividuals, drivenMutatedGenerations) = cycle.generation(population, referenceCromossome, evaluatedPopulation, crossoverType, crossoverProbability, crossoverTasksNumPerc, mutationType, mutationTasksNumPerc, tasksMutationProbability, operatorsMutationProbability, drivenMutation, drivenMutationPart, limitBestFitnessRepetionCount, fitnessEvolution[currentGeneration - 1][3], drivenMutatedIndividuals, drivenMutatedGenerations, TPweight, precisenessWeight, simplicityWeight, completenessWeight, elitismPerc, sortedEvaluatedPopulation, selectionOp, selectionTp, lambdaValue, HammingThreshold, currentGeneration, completenessAttemptFactor1, completenessAttemptFactor2, numberOfcyclesAfterDrivenMutation)
                (highestValueAndPosition, sortedEvaluatedPopulation) = cycle.chooseHighest(evaluatedPopulation)
                set_broadcast(population, highestValueAndPosition[0][0], highestValueAndPosition[1], island) #armazenar os melhores indivudos no broadcast da ilha - Joon
                lowestValue = cycle.chooseLowest(sortedEvaluatedPopulation)
                set_broadcast_lowest(lowestValue, island) #armazenar os piores individuos no broad. da ilha - Joon
                averageValue = cycle.calculateAverage(evaluatedPopulation)
                fitnessEvolution.append([lowestValue, highestValueAndPosition[0][0], averageValue, 0, highestValueAndPosition[0][1], highestValueAndPosition[0][2], highestValueAndPosition[0][3], highestValueAndPosition[0][4], 0, 0])
                if fitnessEvolution[currentGeneration][4] ==  fitnessEvolution[currentGeneration - 1][4]:
                    fitnessEvolution[currentGeneration][3] = fitnessEvolution[currentGeneration - 1][3] + 1
                if fitnessEvolution[currentGeneration][6] ==  fitnessEvolution[currentGeneration - 1][6]:
                    fitnessEvolution[currentGeneration][8] = fitnessEvolution[currentGeneration - 1][8] + 1
                if fitnessEvolution[currentGeneration][7] ==  fitnessEvolution[currentGeneration - 1][7]:
                    fitnessEvolution[currentGeneration][9] = fitnessEvolution[currentGeneration - 1][9] + 1
                if fitnessEvolution[currentGeneration][8] >= simplicityStart:
                    simplicityWeight = par[parameter][21]
                print('par:', parameter, '/ round:', round, '/ gen:', currentGeneration, '/ total fitness:', "%.5f" % highestValueAndPosition[0][0], '/ comp:',  "%.5f" % highestValueAndPosition[0][1], '/ TP:', "%.5f" % highestValueAndPosition[0][2], '/ prec:',  "%.5f" % highestValueAndPosition[0][3], '/ simp:',  "%.5f" % highestValueAndPosition[0][4], '/ eqCount:', fitnessEvolution[currentGeneration][3], fitnessEvolution[currentGeneration][8], fitnessEvolution[currentGeneration][9])
                #if ((highestValueAndPosition[0][2] == 1) and (highestValueAndPosition[0][1] == 1)) and (fitnessEvolution[currentGeneration][3] == 100):
                if ((highestValueAndPosition[0][1] == 1)) and (fitnessEvolution[currentGeneration][9] == 30):
                    #fechar barreira - Joon
                    break
                if currentGeneration > 0 and currentGeneration%migrationtime == 0: #realizar a migração - Joon 
                    barrier.wait()
                    barrier.reset()
            cycle.postProcessing(population)
            print("%.5f" % highestValueAndPosition[0][0], "%.5f" % highestValueAndPosition[0][1], "%.5f" % highestValueAndPosition[0][2], "%.5f" % highestValueAndPosition[0][3], iniPop.alphabet, population[highestValueAndPosition[1]])
            plot.plot_evolution(fitnessEvolution, str(par[parameter]), str(parameter), str(round))
            duration = datetime.now() - start
            print(start)
            print(datetime.now())
            print(duration)
            record.record_evolution(iniPop.log, 'PAR-COMB-' + str(par[parameter]), highestValueAndPosition[0], fitnessEvolution, iniPop.alphabet, population[highestValueAndPosition[1]], duration, currentGeneration)
