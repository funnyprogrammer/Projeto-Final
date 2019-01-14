import csv

def record_evolution(log, filename, highestValues, fitnessEvolution, alphabet, bestIndividual, duration, currentGeneration):
    fields = [filename, ' | NEEDED GENERATIONS: ' + str(currentGeneration + 1), ' | DURATION: ' + str(duration), ' | HIGHEST-VALUES: ' + str(highestValues), ' | ALPHABET: ' + str(alphabet), ' | BEST INDIVIDUAL: ' + str(bestIndividual), ' | LOG: ' + str(log), ' | FITNESS EVOLUTION: ' + str(fitnessEvolution)]
    with open('spreadsheets/' + filename + ".csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', delimiter=',')
        writer.writerow(fields)
        csvfile.close()
    return