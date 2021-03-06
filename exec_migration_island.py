from random import randint
import os
from ast import literal_eval
import exec_island_checker as eic
import sys

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
                yield line

def evaluateIndividualB(cromossome):
    eva = []
    with open('broadcastEVA.txt', 'r') as f:
        for line in f:
            eva.append(literal_eval(line))
    return eva[cromossome]


def evaluateIndividual(island, cromossome):
    # Open island
    eva = []
    with open('evaluation_{0}.txt'.format(island), 'r') as f:
        for line in f:
            eva.append(literal_eval(line))
    return eva[cromossome]


def do_migration(num_threads):
    mig_policy_freq = 0.199 # chance of migration
    mig_policy_isl = 0.355  # chance of each island
    mig_policy_ind = 0.299 # chance of each individual
    mig_policy_size = 0.15 # quantos individuos eu quero migrar # trocar como porcentagem 

    # reuniao dos broadcasters
    myTests = []
    myTestsEva = []
    for each in range(num_threads): #att o número para uma variável
        allBests = []
        with open('broadcast_{0}.txt'.format(each), 'r') as broad1:
            for line in nonblank_lines(broad1):
                allBests.append(literal_eval(line))
        broad1.close()
        myTests.extend(allBests)

        allEVA = []
        with open('evaluationB_{0}.txt'.format(each), 'r') as eva1:
            for line in nonblank_lines(eva1):
                allEVA.append(literal_eval(line))
        eva1.close()
        myTestsEva.extend(allEVA)

        prevBests = []
        with open('broadcast.txt', 'r') as broad2:
            for line in nonblank_lines(broad2):
                prevBests.append(literal_eval(line))
        broad2.close()
        prevBests.extend(allBests)
        # myTests = prevBests.copy()
        with open('broadcast.txt', 'w') as broad:
            for ini in range(len(prevBests)):
                broad.write(str(prevBests[ini]) + '\n')
        broad.close()

        prevBestsE = []
        with open('broadcastEVA.txt', 'r') as broad3:
            for line in nonblank_lines(broad3):
                prevBestsE.append(literal_eval(line))
        broad3.close()
        prevBestsE.extend(allEVA)
        with open('broadcastEVA.txt', 'w') as broad:
            for ini in range(len(prevBests)):
                broad.write(str(prevBestsE[ini]) + '\n')
        broad.close()

    # migration time
    print("Migração")
    var_random = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
    if var_random >= mig_policy_freq:
        for island_number in range(num_threads):
            var_random = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
            if var_random >= mig_policy_isl:
                island = open('island_{0}.txt'.format(island_number), 'r')
                island_content = []
                for line in island:
                    island_content.append(literal_eval(line))
                var = 0
                broad = open('broadcast.txt', 'r')
                best_gen_list = []
                for line in broad:
                    best_gen_list.append(literal_eval(line))
                broad.close()
                broad = open('broadcastl_{0}.txt'.format(island_number), 'r')
                worst_gen_list = []
                for line in broad:
                    worst_gen_list.append(literal_eval(line))
                broad.close()
                
                while var <= mig_policy_size*(len(island_content)):
                    var_random2 = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
                    if var_random2 >= mig_policy_ind:
                        if island_content and best_gen_list:
                            random_worst_ind = 0
                            random_best_gen = 0
                            if len(island_content) > 0 and len(best_gen_list) > 0:
                                random_worst_ind = randint(0, len(worst_gen_list)-1)
                                random_best_gen = randint(0, len(best_gen_list)-1)
                                
                            if worst_gen_list[random_worst_ind] < evaluateIndividualB(random_best_gen):
                                for i in range(len(island_content)):
                                    if evaluateIndividual(island_number, i) == worst_gen_list[random_worst_ind]:
                                        island_content[i] = best_gen_list[random_best_gen]

                    var = var + 1
                island.close()
                with open('island_{0}.txt'.format(island_number), 'w') as new_island:
                    for ini in range(len(island_content)):
                        new_island.write(str(island_content[ini]) + '\n')
                new_island.close()
                broad.close()

    # checker
    #print("Verificação")
    #keep_rolling = True
    #cutter = False
    
    #apagar toda essa parte - Joon
    #for i in range(1):
    #    keep_rolling = eic.check(i)
    #    if not keep_rolling:
    #        sys.exit()
    #cutter = eic.checkSimilarity(myTestsEva)
    #if (cutter):
    #    print("O programa parou de executar")
    #    sys.exit()

        
    # reset broadcasters
    broad = open('broadcast.txt', 'w')
    broad.close()
    for i in range(num_threads): #att o número para uma variável
        broad = open('broadcast_{0}.txt'.format(i), 'w')
        broad.close()
        eva = open('evaluationB_{0}.txt'.format(i), 'w')
        eva.close()
        eva2 = open('evaluation_{0}.txt'.format(i), 'w')
        eva2.close()
        broad = open('broadcastl_{0}.txt'.format(i), 'w')
        broad.close()
