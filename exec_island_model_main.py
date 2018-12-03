import exec_migration_island as emi
import exec_create_island as eci
import main as hW
import multiprocessing
import time
from functools import partial


num_threads = 5

if __name__ == '__main__':
    timing = 0
    case = 0
    start = time.time()
    num_islands = [0, 1, 2, 3, 4]
    keep_rolling = True
    x_var = 0
    cutter = False
    eci.create_island(num_islands, num_threads)
    p = multiprocessing.Pool(num_threads)
    m = multiprocessing.Manager()
    barrier = m.Barrier(num_threads, emi.do_migration, timeout = 5)
    x_var += 1

    print("Distribuição")
    #function distribution between islands
    func = partial(hW.initializeOp, barrier)
    p.map(func, num_islands)
    p.close()




