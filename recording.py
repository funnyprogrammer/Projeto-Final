import csv

def record_evolution(log, filename, highestValue, fitnessEvolution, alphabet, bestIndividual):
    fields = [filename, 'HIGHEST-VALUE-' + highestValue, log, fitnessEvolution, alphabet, bestIndividual]
    with open('spreadsheets/' + filename + ".csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='excel', delimiter=',')
        writer.writerow(fields)
        csvfile.close()
    return