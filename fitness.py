import random as ran
import initialPopulation as initPop
import copy
import math
import ast

def calculateTPTask(auxCrom, cromossome, i):
    intersectionModelAndLog = 0
    modelSum = 0
    for j in range(2, len(cromossome[i]) - 3, 2):
        if (cromossome[i][j] == 1) or (cromossome[i + 1][j] == 1) or (cromossome[i][j + 1] == 1) or (cromossome[i + 1][j + 1] == 1):
            modelSum = modelSum + 1
            if (auxCrom[i][j] == 1) or (auxCrom[i + 1][j] == 1) or (auxCrom[i][j + 1] == 1) or (auxCrom[i + 1][j + 1] == 1):
                intersectionModelAndLog = intersectionModelAndLog + 1
    if modelSum != 0:
        return (intersectionModelAndLog / modelSum)
    else:
        return 0

def calculateTP(cromossome, referenceCromossome):
    TP = 0
    for i in range(0, len(cromossome) - 5, 2):
        TP = TP + calculateTPTask(referenceCromossome, cromossome, i)
    return TP/((len(cromossome) - 5) / 2)

def countNumberOfANDTokenOutputs(tokens, index1):
    numberOfANDTokenOutputs = 0
    for k in range(len(tokens[index1][1])):
        if isinstance(tokens[index1][1][k], list):
            numberOfANDTokenOutputs = numberOfANDTokenOutputs + 1
    return numberOfANDTokenOutputs

def treatWaitingTokens(waitingTokens, tokens, inputIndexes, index1):
    if len(inputIndexes) > 0:
        for m in range(len(inputIndexes)):
            waitingTokens.append([copy.deepcopy(inputIndexes), copy.deepcopy(tokens[index1])])
    if len(waitingTokens) > 0:
        m = 0
        while m < len(waitingTokens):
            if waitingTokens[m][0].count(tokens[index1][0]) > 0:
                #if waitingTokens[m][1][1] == tokens[index1][1]:
                waitingTokens.remove(waitingTokens[m])
                m = m - 1
            m = m + 1
    return waitingTokens

def processTokensToOutpus(cromossome, parsedTasks, enabledTasks, numberOfANDTokenOutputs, centralInputGatewayType, topInputGatewayType, bottomInputGatewayType, inputIndexes, topInputIndexes, bottomInputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, index2, i, l, side, activityFoundInxORorANDOutputToken):
    if centralInputGatewayType == 0:
        if topInputGatewayType == 0:
            if bottomInputGatewayType == 0:
                if inputIndexes.count(tokens[index1][0]) > 0:  # 1
                    if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                        for m in range(len(tokens[index1][1][side])):
                            if tokens[index1][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index1][0], [tokens[index1][1][side][m]]])
                    tokens.remove(tokens[index1])
                    #print('removed: ', tokens)
                    availableToken = 1
                    properlyParsedTasks = properlyParsedTasks + 1
                    return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
            else:
                if bottomInputGatewayType == 1:
                    if topInputIndexes.count(tokens[index1][0]) > 0:  # 2
                        if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                            for m in range(len(tokens[index1][1][side])):
                                if tokens[index1][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                    tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                                    (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index1][0], [tokens[index1][1][side][m]]])
                        tokens.remove(tokens[index1])
                        #print('removed: ', tokens)
                        availableToken = 1
                        properlyParsedTasks = properlyParsedTasks + 1
                        return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
                    else:
                        if bottomInputIndexes.count(tokens[index1][0]) > 0:
                            if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                                for m in range(len(tokens[index1][1][side])):
                                    if tokens[index1][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                        tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                                        (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index1][0], [tokens[index1][1][side][m]]])
                            bottomInputIndexes.remove(tokens[index1][0])
                            waitingTokens = treatWaitingTokens(waitingTokens, tokens, bottomInputIndexes, index1)
                            tokens.remove(tokens[index1])
                            #print('removed: ', tokens)
                            if len(bottomInputIndexes) == 0:
                                availableToken = 1
                                properlyParsedTasks = properlyParsedTasks + 1
                                return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
        else:
            if topInputGatewayType == 1:
                if bottomInputGatewayType == 0:
                    if topInputIndexes.count(tokens[index1][0]) > 0:  # 3
                        if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                            for m in range(len(tokens[index1][1][side])):
                                if tokens[index1][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                    tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                                    (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index1][0], [tokens[index1][1][side][m]]])
                        topInputIndexes.remove(tokens[index1][0])
                        waitingTokens = treatWaitingTokens(waitingTokens, tokens, topInputIndexes, index1)
                        tokens.remove(tokens[index1])
                        #print('removed: ', tokens)
                        if len(topInputIndexes) == 0:
                            availableToken = 1
                            properlyParsedTasks = properlyParsedTasks + 1
                            return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
                    else:
                        if bottomInputIndexes.count(tokens[index1][0]) > 0:
                            if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                                for m in range(len(tokens[index1][1][side])):
                                    if tokens[index1][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                        tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                                        (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index1][0], [tokens[index1][1][side][m]]])
                            tokens.remove(tokens[index1])
                            #print('removed: ', tokens)
                            availableToken = 1
                            properlyParsedTasks = properlyParsedTasks + 1
                            return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
                else:
                    if bottomInputGatewayType == 1:
                        if topInputIndexes.count(tokens[index1][0]) > 0:  # 4
                            if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                                for m in range(len(tokens[index1][1][side])):
                                    if tokens[index1][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                        tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                                        (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index1][0], [tokens[index1][1][side][m]]])
                            topInputIndexes.remove(tokens[index1][0])
                            waitingTokens = treatWaitingTokens(waitingTokens, tokens, topInputIndexes, index1)
                            tokens.remove(tokens[index1])
                            #print('removed: ', tokens)
                            if len(topInputIndexes) == 0:
                                availableToken = 1
                                properlyParsedTasks = properlyParsedTasks + 1
                                return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
                        else:
                            if bottomInputIndexes.count(tokens[index1][0]) > 0:
                                if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                                    for m in range(len(tokens[index1][1][side])):
                                        if tokens[index1][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                            tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                                            (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index1][0], [tokens[index1][1][side][m]]])
                                bottomInputIndexes.remove(tokens[index1][0])
                                waitingTokens = treatWaitingTokens(waitingTokens, tokens, bottomInputIndexes, index1)
                                tokens.remove(tokens[index1])
                                #print('removed: ', tokens)
                                if len(bottomInputIndexes) == 0:
                                    availableToken = 1
                                    properlyParsedTasks = properlyParsedTasks + 1
                                    return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
    else:
        if centralInputGatewayType == 1:
            if topInputGatewayType == 1:
                if bottomInputGatewayType == 1:
                    if (((topInputIndexes.count(tokens[index1][0]) > 0) or topInputIndexes == [-1]) and ((bottomInputIndexes.count(tokens[index2][0]) > 0) or bottomInputIndexes == [-1])):  # 5
                        if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                            if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                                if len(tokens[max(index1, index2)][1]) > 1:
                                    if isinstance(tokens[max(index1, index2)][1][side], list):
                                        for m in range(len(tokens[max(index1, index2)][1][side])):
                                            if tokens[max(index1, index2)][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                tokens.append([tokens[max(index1, index2)][0], [tokens[max(index1, index2)][1][side][m]]])
                                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[max(index1, index2)][0], [tokens[max(index1, index2)][1][side][m]]])
                                if index1 != index2:
                                    if len(tokens[min(index1, index2)][1]) > 1:
                                        if isinstance(tokens[min(index1, index2)][1][side], list):
                                            for m in range(len(tokens[min(index1, index2)][1][side])):
                                                if tokens[min(index1, index2)][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                    tokens.append([tokens[min(index1, index2)][0], [tokens[min(index1, index2)][1][side][m]]])
                                                    (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[min(index1, index2)][0], [tokens[min(index1, index2)][1][side][m]]])
                            else:
                                if (topInputIndexes != [-1]) and (bottomInputIndexes == [-1]):
                                    if len(tokens[index1][1]) > 1:
                                        if isinstance(tokens[index1][1][side], list):
                                            for m in range(len(tokens[index1][1][side])):
                                                if tokens[index1][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                    tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                                                    (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index1][0], [tokens[index1][1][side][m]]])
                                else:
                                    if (topInputIndexes == [-1]) and (bottomInputIndexes != [-1]):
                                        if len(tokens[index2][1]) > 1:
                                            if isinstance(tokens[index2][1][side], list):
                                                for m in range(len(tokens[index2][1][side])):
                                                    if tokens[index2][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                        tokens.append([tokens[index2][0], [tokens[index2][1][side][m]]])
                                                        (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index2][0], [tokens[index2][1][side][m]]])
                        if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                            topInputIndexes.remove(tokens[index1][0])
                            bottomInputIndexes.remove(tokens[index2][0])
                            waitingTokens = treatWaitingTokens(waitingTokens, tokens, topInputIndexes, index1)
                            waitingTokens = treatWaitingTokens(waitingTokens, tokens, bottomInputIndexes, index2)
                            tokens.remove(tokens[max(index1, index2)])
                            #print('removed: ', tokens)
                            if index1 != index2:
                                tokens.remove(tokens[min(index1, index2)])
                                #print('removed: ', tokens)
                        else:
                            if (topInputIndexes != [-1]) and (bottomInputIndexes == [-1]):
                                topInputIndexes.remove(tokens[index1][0])
                                waitingTokens = treatWaitingTokens(waitingTokens, tokens, topInputIndexes, index1)
                                bottomInputIndexes.remove(-1)
                                tokens.remove(tokens[index1])
                                #print('removed: ', tokens)
                            else:
                                topInputIndexes.remove(-1)
                                bottomInputIndexes.remove(tokens[index2][0])
                                waitingTokens = treatWaitingTokens(waitingTokens, tokens, bottomInputIndexes, index2)
                                tokens.remove(tokens[index1])
                                #print('removed: ', tokens)
                        if (len(topInputIndexes) == 0) and (len(bottomInputIndexes) == 0):
                            availableToken = 1
                            properlyParsedTasks = properlyParsedTasks + 1
                            return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
                else:
                    if bottomInputGatewayType == 0:
                        if (((topInputIndexes.count(tokens[index1][0]) > 0) or topInputIndexes == [-1]) and ((bottomInputIndexes.count(tokens[index2][0]) > 0) or bottomInputIndexes == [-1])):  # 6
                            if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                                if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                                    if len(tokens[max(index1, index2)][1]) > 1:
                                        if isinstance(tokens[max(index1, index2)][1][side], list):
                                            for m in range(len(tokens[max(index1, index2)][1][side])):
                                                if tokens[max(index1, index2)][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                    tokens.append([tokens[max(index1, index2)][0], [tokens[max(index1, index2)][1][side][m]]])
                                                    (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[max(index1, index2)][0], [tokens[max(index1, index2)][1][side][m]]])
                                    if index1 != index2:
                                        if len(tokens[min(index1, index2)][1]) > 1:
                                            if isinstance(tokens[min(index1, index2)][1][side], list):
                                                for m in range(len(tokens[min(index1, index2)][1][side])):
                                                    if tokens[min(index1, index2)][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                        tokens.append([tokens[min(index1, index2)][0], [tokens[min(index1, index2)][1][side][m]]])
                                                        (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[min(index1, index2)][0], [tokens[min(index1, index2)][1][side][m]]])
                                else:
                                    if (topInputIndexes != [-1]) and (bottomInputIndexes == [-1]):
                                        if len(tokens[index1][1]) > 1:
                                            if isinstance(tokens[index1][1][side], list):
                                                for m in range(len(tokens[index1][1][side])):
                                                    if tokens[index1][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                        tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                                                        (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index1][0], [tokens[index1][1][side][m]]])
                                    else:
                                        if (topInputIndexes == [-1]) and (bottomInputIndexes != [-1]):
                                            if len(tokens[index2][1]) > 1:
                                                if isinstance(tokens[index2][1][side], list):
                                                    for m in range(len(tokens[index2][1][side])):
                                                        if tokens[index2][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                            tokens.append([tokens[index2][0], [tokens[index2][1][side][m]]])
                                                            (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index2][0], [tokens[index2][1][side][m]]])
                            if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                                topInputIndexes.remove(tokens[index1][0])
                                waitingTokens = treatWaitingTokens(waitingTokens, tokens, topInputIndexes, index1)
                                tokens.remove(tokens[max(index1, index2)])
                                #print('removed: ', tokens)
                                if index1 != index2:
                                    tokens.remove(tokens[min(index1, index2)])
                                    #print('removed: ', tokens)
                            else:
                                if (topInputIndexes != [-1]) and (bottomInputIndexes == [-1]):
                                    topInputIndexes.remove(tokens[index1][0])
                                    waitingTokens = treatWaitingTokens(waitingTokens, tokens, topInputIndexes, index1)
                                    tokens.remove(tokens[index1])
                                    #print('removed: ', tokens)
                                else:
                                    topInputIndexes.remove(-1)
                                    tokens.remove(tokens[index1])
                                    #print('removed: ', tokens)
                            if len(topInputIndexes) == 0:
                                availableToken = 1
                                properlyParsedTasks = properlyParsedTasks + 1
                                return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
            else:
                if topInputGatewayType == 0:
                    if bottomInputGatewayType == 1:
                        if (((topInputIndexes.count(tokens[index1][0]) > 0) or topInputIndexes == [-1]) and ((bottomInputIndexes.count(tokens[index2][0]) > 0) or bottomInputIndexes == [-1])):  # 7
                            if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                                if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                                    if len(tokens[max(index1, index2)][1]) > 1:
                                        if isinstance(tokens[max(index1, index2)][1][side], list):
                                            for m in range(len(tokens[max(index1, index2)][1][side])):
                                                if tokens[max(index1, index2)][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                    tokens.append([tokens[max(index1, index2)][0], [tokens[max(index1, index2)][1][side][m]]])
                                                    (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[max(index1, index2)][0], [tokens[max(index1, index2)][1][side][m]]])
                                    if index1 != index2:
                                        if len(tokens[min(index1, index2)][1]) > 1:
                                            if isinstance(tokens[min(index1, index2)][1][side], list):
                                                for m in range(len(tokens[min(index1, index2)][1][side])):
                                                    if tokens[min(index1, index2)][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                        tokens.append([tokens[min(index1, index2)][0], [tokens[min(index1, index2)][1][side][m]]])
                                                        (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[min(index1, index2)][0], [tokens[min(index1, index2)][1][side][m]]])
                                else:
                                    if (topInputIndexes != [-1]) and (bottomInputIndexes == [-1]):
                                        if len(tokens[index1][1]) > 1:
                                            if isinstance(tokens[index1][1][side], list):
                                                for m in range(len(tokens[index1][1][side])):
                                                    if tokens[index1][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                        tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                                                        (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index1][0], [tokens[index1][1][side][m]]])
                                    else:
                                        if (topInputIndexes == [-1]) and (bottomInputIndexes != [-1]):
                                            if len(tokens[index2][1]) > 1:
                                                if isinstance(tokens[index2][1][side], list):
                                                    for m in range(len(tokens[index2][1][side])):
                                                        if tokens[index2][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                            tokens.append([tokens[index2][0], [tokens[index2][1][side][m]]])
                                                            (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index2][0], [tokens[index2][1][side][m]]])
                            if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                                bottomInputIndexes.remove(tokens[index2][0])
                                waitingTokens = treatWaitingTokens(waitingTokens, tokens, bottomInputIndexes, index1)
                                tokens.remove(tokens[max(index1, index2)])
                                #print('removed: ', tokens)
                                if index1 != index2:
                                    tokens.remove(tokens[min(index1, index2)])
                                    #print('removed: ', tokens)
                            else:
                                if (topInputIndexes != [-1]) and (bottomInputIndexes == [-1]):
                                    bottomInputIndexes.remove(tokens[index2][0])
                                    waitingTokens = treatWaitingTokens(waitingTokens, tokens, bottomInputIndexes, index1)
                                    tokens.remove(tokens[index1])
                                    #print('removed: ', tokens)
                                else:
                                    topInputIndexes.remove(-1)
                                    tokens.remove(tokens[index1])
                                    #print('removed: ', tokens)
                            if len(bottomInputIndexes) == 0:
                                availableToken = 1
                                properlyParsedTasks = properlyParsedTasks + 1
                                return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
                    else:
                        if bottomInputGatewayType == 0: # 8
                            if (((topInputIndexes.count(tokens[index1][0]) > 0) or topInputIndexes == [-1]) and ((bottomInputIndexes.count(tokens[index2][0]) > 0) or bottomInputIndexes == [-1])):  # 8
                                if (numberOfANDTokenOutputs == 1 and activityFoundInxORorANDOutputToken == 1) or (numberOfANDTokenOutputs == 2):
                                    if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                                        if len(tokens[max(index1, index2)][1]) > 1:
                                            if isinstance(tokens[max(index1, index2)][1][side], list):
                                                for m in range(len(tokens[max(index1, index2)][1][side])):
                                                    if tokens[max(index1, index2)][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                        tokens.append([tokens[max(index1, index2)][0], [tokens[max(index1, index2)][1][side][m]]])
                                                        (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[max(index1, index2)][0], [tokens[max(index1, index2)][1][side][m]]])
                                        if index1 != index2:
                                            if len(tokens[min(index1, index2)][1]) > 1:
                                                if isinstance(tokens[min(index1, index2)][1][side], list):
                                                    for m in range(len(tokens[min(index1, index2)][1][side])):
                                                        if tokens[min(index1, index2)][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                            tokens.append([tokens[min(index1, index2)][0], [tokens[min(index1, index2)][1][side][m]]])
                                                            (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[min(index1, index2)][0], [tokens[min(index1, index2)][1][side][m]]])
                                    else:
                                        if (topInputIndexes != [-1]) and (bottomInputIndexes == [-1]):
                                            if len(tokens[index1][1]) > 1:
                                                if isinstance(tokens[index1][1][side], list):
                                                    for m in range(len(tokens[index1][1][side])):
                                                        if tokens[index1][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                            tokens.append([tokens[index1][0], [tokens[index1][1][side][m]]])
                                                            (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index1][0], [tokens[index1][1][side][m]]])
                                        else:
                                            if (topInputIndexes == [-1]) and (bottomInputIndexes != [-1]):
                                                if len(tokens[index2][1]) > 1:
                                                    if isinstance(tokens[index2][1][side], list):
                                                        for m in range(len(tokens[index2][1][side])):
                                                            if tokens[index2][1][side][m] != initPop.getTaskID(initPop.log[i][l]):
                                                                tokens.append([tokens[index2][0], [tokens[index2][1][side][m]]])
                                                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [tokens[index2][0], [tokens[index2][1][side][m]]])
                                if (topInputIndexes != [-1]) and (bottomInputIndexes != [-1]):
                                    tokens.remove(tokens[max(index1, index2)])
                                    #print('removed: ', tokens)
                                    if index1 != index2:
                                        tokens.remove(tokens[min(index1, index2)])
                                        #print('removed: ', tokens)
                                else:
                                    if (topInputIndexes != [-1]) and (bottomInputIndexes == [-1]):
                                        tokens.remove(tokens[index1])
                                        #print('removed: ', tokens)
                                    else:
                                        tokens.remove(tokens[index1])
                                        #print('removed: ', tokens)
                                availableToken = 1
                                properlyParsedTasks = properlyParsedTasks + 1
                                return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 1, parsedTasks, enabledTasks)
    return (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, 0, parsedTasks, enabledTasks)

def addressSpecificInputType(cromossome, tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, centralInputGatewayType, topInputGatewayType, bottomInputGatewayType):
    count = 0
    #while (len(tokens) > 0) and (count < 500):            ##### =====>>>>> preciso passar isso como um parâmetro livre
    while (len(tokens) > 0) and (count < (10 + pow(len(tokens), 2))):
        count = count + 1
        index1 = ran.randrange(0, len(tokens))
        index2 = ran.randrange(0, len(tokens))
        numberOfANDTokenOutputs = countNumberOfANDTokenOutputs(tokens, index1)
        if len(topInputIndexes) == 0:
            topInputIndexes.append(-1)
        if len(bottomInputIndexes) == 0:
            bottomInputIndexes.append(-1)
        if len(inputIndexes) == 0:
            inputIndexes.append(-1)
        if numberOfANDTokenOutputs == 0:
            if tokens[index1][1].count(initPop.getTaskID(initPop.log[i][l])) > 0:
                (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, breakSignal, parsedTasks, enabledTasks) = processTokensToOutpus(cromossome, parsedTasks, enabledTasks, numberOfANDTokenOutputs, centralInputGatewayType, topInputGatewayType, bottomInputGatewayType, inputIndexes, topInputIndexes, bottomInputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, index2, 0, 0, 0, 0)
                if breakSignal == 1:
                    break
        else:
            if numberOfANDTokenOutputs == 1:
                if tokens[index1][1][0].count(initPop.getTaskID(initPop.log[i][l])) > 0:
                    (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, breakSignal, parsedTasks, enabledTasks) = processTokensToOutpus(cromossome, parsedTasks, enabledTasks, numberOfANDTokenOutputs, centralInputGatewayType, topInputGatewayType, bottomInputGatewayType, inputIndexes, topInputIndexes, bottomInputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, index2, i, l, 0, 1)
                    if breakSignal == 1:
                        break
                else:
                    if tokens[index1][1].count(initPop.getTaskID(initPop.log[i][l])) > 0:
                        (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, breakSignal, parsedTasks, enabledTasks) = processTokensToOutpus(cromossome, parsedTasks, enabledTasks, numberOfANDTokenOutputs, centralInputGatewayType, topInputGatewayType, bottomInputGatewayType, inputIndexes, topInputIndexes, bottomInputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, index2, i, l, 0, 0)
                        if breakSignal == 1:
                            break
            else:
                if numberOfANDTokenOutputs == 2:
                    if tokens[index1][1][0].count(initPop.getTaskID(initPop.log[i][l])) > 0:
                        (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, breakSignal, parsedTasks, enabledTasks) = processTokensToOutpus(cromossome, parsedTasks, enabledTasks, numberOfANDTokenOutputs, centralInputGatewayType, topInputGatewayType, bottomInputGatewayType, inputIndexes, topInputIndexes, bottomInputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, index2, i, l, 0, 0)
                        if breakSignal == 1:
                            break
                    else:
                        if tokens[index1][1][1].count(initPop.getTaskID(initPop.log[i][l])) > 0:
                            (inputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, breakSignal, parsedTasks, enabledTasks) = processTokensToOutpus(cromossome, parsedTasks, enabledTasks, numberOfANDTokenOutputs, centralInputGatewayType, topInputGatewayType, bottomInputGatewayType, inputIndexes, topInputIndexes, bottomInputIndexes, tokens, waitingTokens, properlyParsedTasks, availableToken, index1, index2, i, l, 1, 0)
                            if breakSignal == 1:
                                break
    if availableToken == 0:
        if centralInputGatewayType == 0:
            missingLocalTokens = missingLocalTokens + 1
        else:
            if centralInputGatewayType == 1:
                missingLocalTokens = missingLocalTokens + len(inputIndexes)
    return (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks)

def checkEnabledTasks(cromossome, parsedTasks, enabledTasks, tasks):
    parsedTasks.append(tasks[0])

    #print(parsedTasks)

    for j in range(len((tasks[1]))):



        if isinstance(tasks[1][j], list):
            for k in range(len(tasks[1][j])):
                inputTTasks = []
                inputBTasks = []
                for i in range(len(initPop.alphabet)):
                    if ((cromossome[(i * 2)][(tasks[1][j][k] * 2)]) == 1) or ((cromossome[(i * 2)][(tasks[1][j][k] * 2) + 1]) == 1):
                        inputTTasks.append(i)
                    if ((cromossome[(i * 2) + 1][(tasks[1][j][k] * 2)]) == 1) or ((cromossome[(i * 2) + 1][(tasks[1][j][k] * 2) + 1]) == 1):
                        inputBTasks.append(i)
                if (len(inputTTasks) == 0) and (len(inputBTasks) == 0):
                    enabledTasks.append(tasks[1][j][k])
                else:
                    inputTTasksInParsedTasks = 0
                    inputBTasksInParsedTasks = 0
                    for l in range(len(inputTTasks)):
                        if parsedTasks.count(inputTTasks[l]) > 0:
                            inputTTasksInParsedTasks = inputTTasksInParsedTasks + 1
                    for l in range(len(inputBTasks)):
                        if parsedTasks.count(inputBTasks[l]) > 0:
                            inputBTasksInParsedTasks = inputBTasksInParsedTasks + 1
                    if len(inputTTasks) > 0:
                        if ((cromossome[-2][(tasks[1][j][k] * 2)] == 1) and (inputTTasksInParsedTasks == len(inputTTasks))) or ((cromossome[-2][(tasks[1][j][k] * 2)] == 0) and (inputTTasksInParsedTasks > 0)):
                            enabledTasks.append(tasks[1][j][k])
                    if len(inputBTasks) > 0:
                        if ((cromossome[-1][(tasks[1][j][k] * 2)] == 1) and (inputBTasksInParsedTasks == len(inputBTasks))) or ((cromossome[-1][(tasks[1][j][k] * 2)] == 0) and (inputBTasksInParsedTasks > 0)):
                            enabledTasks.append(tasks[1][j][k])
        else:
            inputTTasks = []
            inputBTasks = []
            for i in range(len(initPop.alphabet)):
                if ((cromossome[(i * 2)][(tasks[1][j] * 2)]) == 1) or ((cromossome[(i * 2)][(tasks[1][j] * 2) + 1]) == 1):
                    inputTTasks.append(i)
                if ((cromossome[(i * 2) + 1][(tasks[1][j] * 2)]) == 1) or ((cromossome[(i * 2) + 1][(tasks[1][j] * 2) + 1]) == 1):
                    inputBTasks.append(i)
            if (len(inputTTasks) == 0) and (len(inputBTasks) == 0):
                enabledTasks.append(tasks[1][j])
            else:
                inputTTasksInParsedTasks = 0
                inputBTasksInParsedTasks = 0
                for l in range(len(inputTTasks)):
                    if parsedTasks.count(inputTTasks[l]) > 0:
                        inputTTasksInParsedTasks = inputTTasksInParsedTasks + 1
                for l in range(len(inputBTasks)):
                    if parsedTasks.count(inputBTasks[l]) > 0:
                        inputBTasksInParsedTasks = inputBTasksInParsedTasks + 1
                if (len(inputTTasks) <= 1) and (len(inputBTasks) <= 1):
                    if (len(inputTTasks) == 1) and (len(inputBTasks) == 0):
                        if ((cromossome[-2][(tasks[1][j] * 2)] == 1) and (inputTTasksInParsedTasks == len(inputTTasks))) or ((cromossome[-2][(tasks[1][j] * 2)] == 0) and (inputTTasksInParsedTasks > 0)):
                            enabledTasks.append(tasks[1][j])
                    if (len(inputTTasks) == 0) and (len(inputBTasks) == 1):
                        if ((cromossome[-1][(tasks[1][j] * 2)] == 1) and (inputBTasksInParsedTasks == len(inputBTasks))) or ((cromossome[-1][(tasks[1][j] * 2)] == 0) and (inputBTasksInParsedTasks > 0)):
                            enabledTasks.append(tasks[1][j])
                    if (len(inputTTasks) == 0) and (len(inputBTasks) == 1):
                        if ((cromossome[-3][(tasks[1][j] * 2)] == 1) and (inputBTasksInParsedTasks == len(inputBTasks))) or ((cromossome[-3][(tasks[1][j] * 2)] == 0) and (inputBTasksInParsedTasks > 0)):
                            enabledTasks.append(tasks[1][j])
                else:
                    if (len(inputTTasks) == 0) or (len(inputBTasks) == 0):
                        if (len(inputTTasks) == 0) and (len(inputBTasks) > 0):
                            if ((cromossome[-2][(tasks[1][j] * 2)] == 1) and (inputTTasksInParsedTasks == len(inputTTasks))) or ((cromossome[-2][(tasks[1][j] * 2)] == 0) and (inputTTasksInParsedTasks > 0)):
                                enabledTasks.append(tasks[1][j])
                        if (len(inputTTasks) > 0) and (len(inputBTasks) == 0):
                            if ((cromossome[-1][(tasks[1][j] * 2)] == 1) and (inputBTasksInParsedTasks == len(inputBTasks))) or ((cromossome[-1][(tasks[1][j] * 2)] == 0) and (inputBTasksInParsedTasks > 0)):
                                enabledTasks.append(tasks[1][j])
                    else:
                        if (len(inputTTasks) == 1) and (len(inputBTasks) >= 2):
                            if ((cromossome[-2][(tasks[1][j] * 2)] == 1) and (inputTTasksInParsedTasks == len(inputTTasks))) or ((cromossome[-2][(tasks[1][j] * 2)] == 0) and (inputTTasksInParsedTasks > 0)):
                                enabledTasks.append(tasks[1][j])
                        if (len(inputTTasks) >=2) and (len(inputBTasks) == 1):
                            if ((cromossome[-1][(tasks[1][j] * 2)] == 1) and (inputBTasksInParsedTasks == len(inputBTasks))) or ((cromossome[-1][(tasks[1][j] * 2)] == 0) and (inputBTasksInParsedTasks > 0)):
                                enabledTasks.append(tasks[1][j])
                        if (len(inputTTasks) >=2) and (len(inputBTasks) >= 2):
                            if ((cromossome[-1][(tasks[1][j] * 2)] == 1) and (inputBTasksInParsedTasks == len(inputBTasks))) or ((cromossome[-1][(tasks[1][j] * 2)] == 0) and (inputBTasksInParsedTasks > 0)):
                                enabledTasks.append(tasks[1][j])


                        #if cromossome[-3][(tasks[1][j] * 2)] == 0:

                        #if cromossome[-3][(tasks[1][j] * 2)] == 1:


    #print(enabledTasks)
    return (parsedTasks, enabledTasks)

def calculateCompleteness(cromossome):
    tracesInLog = len(initPop.log)
    tasksInLog = 0
    properlyParsedTasks = 0
    missingTokens = 0
    extraTokensLeftBehind = 0
    tracesWithMissingTokens = 0
    tracesWithExtraTokensLeftBehind = 0
    enabledTasks = []
    for i in range(len(initPop.log)):
        parsedTasks = []
        missingLocalTokens = 0
        tokens = [[-1, [0]]]
        parsedTasks, enabledTasks = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, tokens[0])
        waitingTokens = []
        for l in range(0, len(initPop.log[i])):
            tasksInLog = tasksInLog + 1
            availableToken = 0
            topInputIndexes = []
            bottomInputIndexes = []
            for j in range(0, len(initPop.alphabet)):
                if (cromossome[(j * 2)][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 1) or (cromossome[(j * 2)][(initPop.getTaskID(initPop.log[i][l]) * 2) + 1] == 1):
                    topInputIndexes.append(j)
                if (cromossome[(j * 2) + 1][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 1) or (cromossome[(j * 2) + 1][(initPop.getTaskID(initPop.log[i][l]) * 2) + 1] == 1):
                    bottomInputIndexes.append(j)
            inputIndexes = topInputIndexes + bottomInputIndexes
            if (cromossome[-3][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 0):
                if (cromossome[-2][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 0):
                    if (cromossome[-1][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 0):
                        (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks) = addressSpecificInputType(cromossome, tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 0, 0, 0)
                    else:
                        if (cromossome[-1][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 1):
                            (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks) = addressSpecificInputType(cromossome, tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 0, 0, 1)
                else:
                    if (cromossome[-2][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 1):
                        if (cromossome[-1][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 0):
                            (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks) = addressSpecificInputType(cromossome, tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 0, 1, 0)
                        else:
                            if (cromossome[-1][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 1):
                                (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks) = addressSpecificInputType(cromossome, tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 0, 1, 1)
            else:
                if (cromossome[-3][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 1):
                    if (cromossome[-2][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 1):
                        if (cromossome[-1][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 1):
                            (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks) = addressSpecificInputType(cromossome, tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 1, 1, 1)
                        else:
                            if (cromossome[-1][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 0):
                                (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks) = addressSpecificInputType(cromossome, tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 1, 1, 0)
                    else:
                        if (cromossome[-2][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 0):
                            if (cromossome[-1][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 1):
                                (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks) = addressSpecificInputType(cromossome, tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 1, 0, 1)
                            else:
                                if (cromossome[-1][(initPop.getTaskID(initPop.log[i][l]) * 2)] == 0):
                                    (tokens, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, parsedTasks, enabledTasks) = addressSpecificInputType(cromossome, tokens, parsedTasks, enabledTasks, waitingTokens, inputIndexes, topInputIndexes, bottomInputIndexes, properlyParsedTasks, missingLocalTokens, availableToken, i, l, 1, 0, 0)
            if initPop.getTaskID(initPop.log[i][l]) != (len(initPop.alphabet) - 1):
                outputLIndexes = []
                outputRIndexes = []
                for j in range(len(initPop.alphabet)):
                    if (cromossome[(initPop.getTaskID(initPop.log[i][l]) * 2)][(j * 2)] == 1) or (cromossome[(initPop.getTaskID(initPop.log[i][l]) * 2) + 1][(j * 2)] == 1):
                        outputLIndexes.append(j)
                    if (cromossome[(initPop.getTaskID(initPop.log[i][l]) * 2)][(j * 2) + 1] == 1) or (cromossome[(initPop.getTaskID(initPop.log[i][l]) * 2) + 1][(j * 2) + 1] == 1):
                        outputRIndexes.append(j)
                if cromossome[(initPop.getTaskID(initPop.log[i][l])) * 2][-3] == 1:
                    if cromossome[(initPop.getTaskID(initPop.log[i][l])) * 2][-2] == 1:
                        for j in range(len(outputLIndexes)):
                            tokens.append([initPop.getTaskID(initPop.log[i][l]), [outputLIndexes[j]]])
                            (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(initPop.log[i][l]), [outputLIndexes[j]]])
                    else:
                        if cromossome[(initPop.getTaskID(initPop.log[i][l])) * 2][-2] == 0:
                            xORoutputs = []
                            for j in range(len(outputLIndexes)):
                                xORoutputs.append(outputLIndexes[j])
                            if xORoutputs != []:
                                tokens.append([initPop.getTaskID(initPop.log[i][l]), xORoutputs])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(initPop.log[i][l]), xORoutputs])
                    if cromossome[(initPop.getTaskID(initPop.log[i][l])) * 2][-1] == 1:
                        for j in range(len(outputRIndexes)):
                            tokens.append([initPop.getTaskID(initPop.log[i][l]), [outputRIndexes[j]]])
                            (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(initPop.log[i][l]), [outputRIndexes[j]]])
                    else:
                        if cromossome[(initPop.getTaskID(initPop.log[i][l])) * 2][-1] == 0:
                            xORoutputs = []
                            for j in range(len(outputRIndexes)):
                                xORoutputs.append(outputRIndexes[j])
                            if xORoutputs != []:
                                tokens.append([initPop.getTaskID(initPop.log[i][l]), xORoutputs])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(initPop.log[i][l]), xORoutputs])
                else:
                    if cromossome[(initPop.getTaskID(initPop.log[i][l])) * 2][-3] == 0:
                        xORLoutputs = []
                        xORRoutputs = []
                        ANDLoutputs = []
                        ANDRoutputs = []
                        if cromossome[(initPop.getTaskID(initPop.log[i][l])) * 2][-2] == 0:
                            for j in range(len(outputLIndexes)):
                                xORLoutputs.append(outputLIndexes[j])
                        else:
                            if cromossome[(initPop.getTaskID(initPop.log[i][l])) * 2][-2] == 1:
                                for j in range(len(outputLIndexes)):
                                    ANDLoutputs.append(outputLIndexes[j])
                        if cromossome[(initPop.getTaskID(initPop.log[i][l])) * 2][-1] == 0:
                            for j in range(len(outputRIndexes)):
                                xORRoutputs.append(outputRIndexes[j])
                        else:
                            if cromossome[(initPop.getTaskID(initPop.log[i][l])) * 2][-1] == 1:
                                for j in range(len(outputRIndexes)):
                                    ANDRoutputs.append(outputRIndexes[j])
                        if ((len(xORLoutputs) > 0) and (len(xORRoutputs) > 0) and (len(ANDLoutputs) == 0) and (len(ANDRoutputs) == 0)) or ((len(xORLoutputs) > 0) and (len(xORRoutputs) == 0) and (len(ANDLoutputs) == 0) and (len(ANDRoutputs) == 0)) or ((len(xORLoutputs) == 0) and (len(xORRoutputs) > 0) and (len(ANDLoutputs) == 0) and (len(ANDRoutputs) == 0)):
                            tokens.append([initPop.getTaskID(initPop.log[i][l]), xORLoutputs + xORRoutputs])
                            (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(initPop.log[i][l]), xORLoutputs + xORRoutputs])
                        else:
                            if (len(xORLoutputs) == 0) and (len(xORRoutputs) == 0) and (len(ANDLoutputs) > 0) and (len(ANDRoutputs) > 0):
                                tokens.append([initPop.getTaskID(initPop.log[i][l]), [ANDLoutputs] + [ANDRoutputs]])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(initPop.log[i][l]), [ANDLoutputs] + [ANDRoutputs]])
                            if (len(xORLoutputs) == 0) and (len(xORRoutputs) > 0) and (len(ANDLoutputs) > 0) and (len(ANDRoutputs) == 0):
                                tokens.append([initPop.getTaskID(initPop.log[i][l]), [ANDLoutputs] + xORRoutputs])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(initPop.log[i][l]), [ANDLoutputs] + xORRoutputs])
                            if (len(xORLoutputs) > 0) and (len(xORRoutputs) == 0) and (len(ANDLoutputs) == 0) and (len(ANDRoutputs) > 0):
                                tokens.append([initPop.getTaskID(initPop.log[i][l]), [ANDRoutputs] + xORLoutputs])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(initPop.log[i][l]), [ANDRoutputs] + xORLoutputs])
                            if (len(xORLoutputs) == 0) and (len(xORRoutputs) == 0) and (len(ANDLoutputs) > 0) and (len(ANDRoutputs) == 0):
                                tokens.append([initPop.getTaskID(initPop.log[i][l]), [ANDLoutputs]])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(initPop.log[i][l]), [ANDLoutputs]])
                            if (len(xORLoutputs) == 0) and (len(xORRoutputs) == 0) and (len(ANDLoutputs) == 0) and (len(ANDRoutputs) > 0):
                                tokens.append([initPop.getTaskID(initPop.log[i][l]), [ANDRoutputs]])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(initPop.log[i][l]), [ANDRoutputs]])
                            if (len(xORLoutputs) == 0) and (len(xORRoutputs) == 0) and (len(ANDLoutputs) == 0) and (len(ANDRoutputs) == 0):
                                tokens.append([initPop.getTaskID(initPop.log[i][l]), []])
                                (parsedTasks, enabledTasks) = checkEnabledTasks(cromossome, parsedTasks, enabledTasks, [initPop.getTaskID(initPop.log[i][l]), []])
        if missingLocalTokens > 0:
            tracesWithMissingTokens = tracesWithMissingTokens + 1
            missingTokens = missingTokens + missingLocalTokens
        if (len(tokens) + len(waitingTokens)) > 0:
            tracesWithExtraTokensLeftBehind = tracesWithExtraTokensLeftBehind + 1
            extraTokensLeftBehind = extraTokensLeftBehind + len(tokens) + len(waitingTokens)
    punishment = ((missingTokens / (tracesInLog - tracesWithMissingTokens + 1)) + (extraTokensLeftBehind / (tracesInLog - tracesWithExtraTokensLeftBehind + 1)))
    completeness = ((properlyParsedTasks - punishment) / tasksInLog)
    preciseness = len(enabledTasks)/tracesInLog/tasksInLog
    return (completeness, preciseness)

def calculatePreciseness(cromossome, averageEnabledTasks):
    return 1
#    enabledOuputTasks = 0
#    outputInternalANDGateways = 0
#    outputInternalXORGateways = 0
#    outputExternalANDGateways = 0
#    outputExternalXORGateways = 0
#    for i in range(len(initPop.alphabet)):
#        enabledLOuputTasks = 0
#        enabledROuputTasks = 0
#        for j in range(1, len(initPop.alphabet)):
#            if (cromossome[i * 2][j * 2] == 1) or (cromossome[(i * 2) + 1][j * 2] == 1):
#                enabledLOuputTasks = enabledLOuputTasks + 1
#        for j in range(1, len(initPop.alphabet)):
#            if (cromossome[i * 2][(j * 2) + 1] == 1) or (cromossome[(i * 2) + 1][(j * 2) + 1] == 1):
#                enabledROuputTasks = enabledROuputTasks + 1
#        enabledOuputTasks = enabledOuputTasks + enabledLOuputTasks + enabledROuputTasks
#        if enabledLOuputTasks > 1:
#            if cromossome[i * 2][-2] == 0:
#                outputInternalXORGateways = outputInternalXORGateways + 1
#            else:
#                outputInternalANDGateways = outputInternalANDGateways + 1
#        if enabledROuputTasks > 1:
#            if cromossome[i * 2][-1] == 0:
#                outputInternalXORGateways = outputInternalXORGateways + 1
#            else:
#                outputInternalANDGateways = outputInternalANDGateways + 1
#        if (enabledLOuputTasks > 0) and (enabledROuputTasks > 0):
#            if cromossome[i * 2][-3] == 0:
#                outputExternalXORGateways = outputExternalXORGateways + 1
#            else:
#                outputExternalANDGateways = outputExternalANDGateways + 1
#    enabledInputTasks = 0
#    inputInternalANDGateways = 0
#    inputInternalXORGateways = 0
#    inputExternalANDGateways = 0
#    inputExternalXORGateways = 0
#    for i in range(len(initPop.alphabet)):
#        enabledTInputTasks = 0
#        enabledBInputTasks = 0
#        for j in range(len(initPop.alphabet) - 1):
#            if (cromossome[j * 2][i * 2] == 1) or (cromossome[j * 2][(i * 2) + 1] == 1):
#                enabledTInputTasks = enabledTInputTasks + 1
#        for j in range(len(initPop.alphabet) - 1):
#            if (cromossome[(j * 2) + 1][i * 2] == 1) or (cromossome[(j * 2) + 1][(i * 2) + 1] == 1):
#                enabledBInputTasks = enabledBInputTasks + 1
#        enabledInputTasks = enabledInputTasks + enabledTInputTasks + enabledBInputTasks
#        if enabledTInputTasks > 1:
#            if cromossome[-2][i * 2] == 0:
#                inputInternalXORGateways = inputInternalXORGateways + 1
#            else:
#                inputInternalANDGateways = inputInternalANDGateways + 1
#        if enabledBInputTasks > 1:
#            if cromossome[-1][i * 2] == 0:
#                inputInternalXORGateways = inputInternalXORGateways + 1
#            else:
#                inputInternalANDGateways = inputInternalANDGateways + 1
#        if (enabledTInputTasks > 0) and (enabledBInputTasks > 0):
#            if cromossome[-3][i * 2] == 0:
#                inputExternalXORGateways = inputExternalXORGateways + 1
#            else:
#                inputExternalANDGateways = inputExternalANDGateways + 1
#    return ((((enabledOuputTasks + enabledInputTasks) / 2) + ((outputInternalXORGateways + inputInternalXORGateways + outputExternalXORGateways + inputExternalXORGateways) * 0.5) + ((outputInternalANDGateways + inputInternalANDGateways + outputExternalANDGateways + inputExternalANDGateways) * 0.25)) / averageEnabledTasks)


#    enabledOuputTasks = 0
#    for i in range(len(initPop.alphabet)):
#        enabledLOuputTasks = 0
#        enabledROuputTasks = 0
#        for j in range(1, len(initPop.alphabet)):
#            if (cromossome[i * 2][j * 2] == 1) or (cromossome[(i * 2) + 1][j * 2] == 1):
#                enabledLOuputTasks = enabledLOuputTasks + 1
#                if cromossome[i * 2][-2] == 0:
#                    break
#        for j in range(1, len(initPop.alphabet)):
#            if (cromossome[i * 2][(j * 2) + 1] == 1) or (cromossome[(i * 2) + 1][(j * 2) + 1] == 1):
#                enabledROuputTasks = enabledROuputTasks + 1
#                if cromossome[i * 2][-1] == 0:
#                    break
#        if (cromossome[i * 2][-3] == 1) or ((cromossome[i * 2][-3] == 0) and ((enabledLOuputTasks == 0) or (enabledROuputTasks == 0))):
#            enabledOuputTasks = enabledOuputTasks + enabledLOuputTasks + enabledROuputTasks
#        else:
#            enabledOuputTasks = enabledOuputTasks + ((enabledLOuputTasks + enabledROuputTasks) / 2)
#    enabledInputTasks = 0
#    for i in range(len(initPop.alphabet)):
#        enabledTInputTasks = 0
#        enabledBInputTasks = 0
#        for j in range(len(initPop.alphabet) - 1):
#            if (cromossome[j * 2][i * 2] == 1) or (cromossome[j * 2][(i * 2) + 1] == 1):
#                enabledTInputTasks = enabledTInputTasks + 1
#                if cromossome[-2][i * 2] == 0:
#                    break
#        for j in range(len(initPop.alphabet) - 1):
#            if (cromossome[(j * 2) + 1][i * 2] == 1) or (cromossome[(j * 2) + 1][(i * 2) + 1] == 1):
#                enabledBInputTasks = enabledBInputTasks + 1
#                if cromossome[-1][i * 2] == 0:
#                    break
#        if (cromossome[-3][i * 2] == 1) or ((cromossome[-3][i * 2] == 0) and ((enabledTInputTasks == 0) or (enabledBInputTasks == 0))):
#            enabledInputTasks = enabledInputTasks + enabledTInputTasks + enabledBInputTasks
#        else:
#            enabledInputTasks = enabledInputTasks + ((enabledTInputTasks + enabledBInputTasks) / 2)
#    return (((enabledOuputTasks + enabledInputTasks) / 2) / averageEnabledTasks)

#    enabledOuputTasks = 0
#    for i in range(len(initPop.alphabet)):
#        enabledLOuputTasks = 0
#        enabledROuputTasks = 0
#        for j in range(1, len(initPop.alphabet)):
#            if (cromossome[i * 2][j * 2] == 1) or (cromossome[(i * 2) + 1][j * 2] == 1):
#                enabledLOuputTasks = enabledLOuputTasks + 1
#                if cromossome[i * 2][-2] == 1:
#                    break
#        for j in range(1, len(initPop.alphabet)):
#            if (cromossome[i * 2][(j * 2) + 1] == 1) or (cromossome[(i * 2) + 1][(j * 2) + 1] == 1):
#                enabledROuputTasks = enabledROuputTasks + 1
#                if cromossome[i * 2][-1] == 1:
#                    break
#        if (cromossome[i * 2][-3] == 0) or ((cromossome[i * 2][-3] == 1) and ((enabledLOuputTasks == 0) or (enabledROuputTasks == 0))):
#            enabledOuputTasks = enabledOuputTasks + enabledLOuputTasks + enabledROuputTasks
#        else:
#            enabledOuputTasks = enabledOuputTasks + ((enabledLOuputTasks + enabledROuputTasks) / 2)
#    enabledInputTasks = 0
#    for i in range(len(initPop.alphabet)):
#        enabledTInputTasks = 0
#        enabledBInputTasks = 0
#        for j in range(len(initPop.alphabet) - 1):
#            if (cromossome[j * 2][i * 2] == 1) or (cromossome[j * 2][(i * 2) + 1] == 1):
#                enabledTInputTasks = enabledTInputTasks + 1
#                if cromossome[-2][i * 2] == 1:
#                    break
#        for j in range(len(initPop.alphabet) - 1):
#            if (cromossome[(j * 2) + 1][i * 2] == 1) or (cromossome[(j * 2) + 1][(i * 2) + 1] == 1):
#                enabledBInputTasks = enabledBInputTasks + 1
#                if cromossome[-1][i * 2] == 1:
#                    break
#        if (cromossome[-3][i * 2] == 0) or ((cromossome[-3][i * 2] == 1) and ((enabledTInputTasks == 0) or (enabledBInputTasks == 0))):
#            enabledInputTasks = enabledInputTasks + enabledTInputTasks + enabledBInputTasks
#        else:
#            enabledInputTasks = enabledInputTasks + ((enabledTInputTasks + enabledBInputTasks) / 2)
#    return (((enabledOuputTasks + enabledInputTasks) / 2) / averageEnabledTasks)

def adaptCromossome(cromossome):
    for i in range(len(initPop.alphabet)):
        numberOfR1 = 0
        numberOfL1 = 0
        for j in range(len(initPop.alphabet)):
            if (cromossome[i * 2][(j * 2) + 1] == 1) or (cromossome[(i * 2) + 1][(j * 2) + 1] == 1):
                numberOfR1 = numberOfR1 + 1
                if numberOfR1 == 2:
                    break
        for j in range(len(initPop.alphabet)):
            if (cromossome[i * 2][j * 2] == 1) or (cromossome[(i * 2) + 1][j * 2] == 1):
                numberOfL1 = numberOfL1 + 1
                if numberOfL1 == 2:
                    break
        if (cromossome[i * 2][-1] == 1) and (numberOfR1 <= 1):
            cromossome[i * 2][-1] = 0
        if (cromossome[i * 2][-2] == 1) and (numberOfL1 <= 1):
            cromossome[i * 2][-2] = 0
        if (cromossome[i * 2][-3] == 1) and ((numberOfL1 == 0) or (numberOfR1 == 0)):
            cromossome[i * 2][-3] = 0
    for i in range(len(initPop.alphabet)):
        numberOfB1 = 0
        numberOfT1 = 0
        for j in range(len(initPop.alphabet)):
            if (cromossome[(j * 2) + 1][i * 2] == 1) or (cromossome[(j * 2) + 1][(i * 2) + 1] == 1):
                numberOfB1 = numberOfB1 + 1
                if numberOfB1 == 2:
                    break
        for j in range(len(initPop.alphabet)):
            if (cromossome[j * 2][i * 2] == 1) or (cromossome[(j * 2)][(i * 2) + 1] == 1):
                numberOfT1 = numberOfT1 + 1
                if numberOfT1 == 2:
                    break
        if (cromossome[-1][i * 2] == 1) and (numberOfB1 <= 1):
            cromossome[-1][i * 2] = 0
        if (cromossome[-2][i * 2] == 1) and (numberOfT1 <= 1):
            cromossome[-2][i * 2] = 0
        if (cromossome[-3][i * 2] == 1) and ((numberOfT1 == 0) or (numberOfB1 == 0)):
            cromossome[-3][i * 2] = 0
    return cromossome

def evaluateIndividual(cromossome, referenceCromossome, TPweight, precisenessWeight, evaluateCompANDPrec, completenessWeight, i, possibleLogOutputTransitions, possibleLogInputTransitions, logSizeAndMaxTraceSize, numberOfRandomTracesPerLogTrace, traceSizeFactor, averageEnabledTasks):
    TP = calculateTP(cromossome, referenceCromossome)
    completeness = 0
    preciseness = 0
    if evaluateCompANDPrec == 1:
        temporaryAdaptedCromossome = adaptCromossome(copy.deepcopy(cromossome))
        (completeness, preciseness) = calculateCompleteness(temporaryAdaptedCromossome)
        #preciseness = calculatePreciseness(cromossome, averageEnabledTasks)
    return ((((TP * TPweight) + (completeness * completenessWeight)) - (preciseness * precisenessWeight)), TP, completeness, preciseness, i)

def evaluationPopulation(population, referenceCromossome, TPweight, precisenessWeight, evaluateCompANDPrec, completenessWeight, logSizeAndMaxTraceSize, numberOfRandomTracesPerLogTrace, traceSizeFactor, averageEnabledTasks):
    evaluationSum = 0
    evaluationValues = []
    possibleLogOutputTransitions = []
    possibleLogInputTransitions = []
    for i in range(len(population)):
        evaluationValues.append(evaluateIndividual(population[i], referenceCromossome, TPweight, precisenessWeight, evaluateCompANDPrec, completenessWeight, i, possibleLogOutputTransitions, possibleLogInputTransitions, logSizeAndMaxTraceSize, numberOfRandomTracesPerLogTrace, traceSizeFactor, averageEnabledTasks))
        evaluationSum = evaluationSum + evaluationValues[i][0]
    return (evaluationSum, evaluationValues)