from multiprocessing import Pool
from ast import literal_eval
import main as m
import initialPopulation as ip

def create_pop(var, population):
    # cria ilha
    with open('island_{0}.txt'.format(var), 'w') as f:
        for ini in range(len(population)):
            f.write(str(population[ini]) + '\n')
    f.close()

def creator(var):

    #cria broadcast
    broad = open('broadcast_{0}.txt'.format(var), 'w')
    broad.close()

    # cria evaluations
    eva = open('evaluation_{0}.txt'.format(var), 'w')
    eva.close()
    eva2 = open('evaluationB_{0}.txt'.format(var), 'w')
    eva2.close()

    #cria plot
    #plot = open('plot_{0}.csv'.format(var), 'w')
    #plot.close()
    #plot = open('plot2_{0}.csv'.format(var), 'w')
    #plot.close()

    #cria ilha
    with open('island_{0}.txt'.format(var), 'w') as f:
        f.close()


def create_island(num_islands, num_threads):
    # cria main broadcast
    broad = open('broadcast.txt', 'w')
    broad.close()
    broad2 = open('broadcastEVA.txt', 'w')
    broad2.close()

    # cria verificador
    ver = open('verificador.txt', 'w')
    for i in range(num_threads):
        ver.write(str(0) + '\n')
    ver.close()

    # cria ilhas + broadcasters + evaluations
    p = Pool(num_threads)
    p.map(creator, num_islands)

