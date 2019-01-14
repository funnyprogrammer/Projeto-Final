import exec_migration_island as emi
import exec_create_island as eci
import main as hW
import multiprocessing
import time
from functools import partial


num_threads = 24

if __name__ == '__main__':
    start = time.time()
    timing = 0
    case = 0
    start = time.time()
    num_islands = []
    for j in range(num_threads):
        num_islands.append(j)
    keep_rolling = True
    x_var = 0
    cutter = False
    eci.create_island(num_islands, num_threads)
    p = multiprocessing.Pool(num_threads)
    m = multiprocessing.Manager()
    func2 = partial(emi.do_migration,num_threads)
    barrier = m.Barrier(num_threads, func2, timeout = 5)
    x_var += 1

    print("Distribuição")
    #function distribution between islands
    func = partial(hW.initializeOp, barrier)
    p.map(func, num_islands)
    p.close()

    end = time.time()
    print('tempo = ', end-start)




