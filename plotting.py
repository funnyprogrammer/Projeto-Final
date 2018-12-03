import matplotlib.pyplot as plt
plt.switch_backend('agg')

def plot_evolution(vetor_fitness, par, parameter, round):
    v_min = [i[0] for i in vetor_fitness]
    v_max = [i[1] for i in vetor_fitness]
    v_avg = [i[2] for i in vetor_fitness]
    plt.figure(1)
    plt.plot(v_min, label="Lowest fitness", linestyle=':', linewidth=1.0, color="red")
    plt.plot(v_avg, label="Average fitness", linewidth=2.0, color="orange")
    plt.plot(v_max, label="Highest fitness", linewidth=2.0, color="green")
    plt.ylabel("Fitness")
    plt.xlabel("Generation")
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=2, mode="expand", borderaxespad=0., prop={'size': 10})
    plt.ylim([0, 1.02])
    plt.draw()
    name = 'graphs/' 'graph-' + par + '-' + parameter + '-' + round + '.png'
    plt.savefig(name)
    plt.clf()
    return