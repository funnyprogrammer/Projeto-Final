from ast import literal_eval

def checkSimilarity(myTests):
    valueTest = 0
    for ind in range(len(myTests)):
        value = myTests[ind]
        if valueTest < value:
            valueTest = value
    cut = False
    for case in range(len(myTests)):
        if (valueTest - myTests[case]) <= 0.01:
            cut = True
        elif (valueTest - myTests[case]) > 0.01:
            return False
    return cut


def check(island):
    population = []
    with open('evaluation_{0}.txt'.format(island), 'r') as f:
        for line in f:
            population.append(literal_eval(line))
    f.close()

    individuals = []
    with open('island_{0}.txt'.format(island), 'r') as f:
        for line in f:
            individuals.append(literal_eval(line))
    f.close()

    for ind in range(len(population)):
        value = population[ind]
        if value >= 0.95:
            print("EUREKA!")

            pasta = open('individual.txt', 'w')
            pasta.write(str(individuals[ind]))
            pasta.close()

            print('Individual with: ', individuals[ind], ' has ')
            print('total fitness:', "%.6f" % value)
            return False
    return True
