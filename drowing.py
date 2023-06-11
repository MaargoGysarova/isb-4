import multiprocessing as mp
import time
import matplotlib.pyplot as plt
import numpy as np
from hash import check_hash


def charting() -> None:
    """ Функция для рисования графика
    """
    times = np.empty(shape=0)
    for i in range(1, 36):
        start = time.time()
        with mp.Pool(i) as p:
            for result in p.map(check_hash, range(0, 1000000)):
                if result:
                    end = time.time() - start
                    times = np.append(times, end)
                    p.terminate()
                    break
                else:
                    print('Solution not found')
    plt.bar(range(len(times)), np.round(times, 2).tolist())
    plt.xlabel("Number of pools")
    plt.ylabel("Time, s")
    plt.title("Dependence of time on the number of pool")
    plt.show()


if __name__ == '__main__':
    charting()
