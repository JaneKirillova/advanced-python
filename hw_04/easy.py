from multiprocessing import Process
from threading import Thread
import time

ARGUMENT = 100000
THREADS_NUM = 10


def fibonacci(n):
    fib1 = fib2 = 1
    result = [fib1, fib2]
    n = n - 2
    for i in range(n):
        fib1, fib2 = fib2, fib1 + fib2
        result.append(fib2)
    return result


def count_time_sync():
    start_time = time.time()
    for _ in range(THREADS_NUM):
        fibonacci(ARGUMENT)
    end_time = time.time()
    return end_time - start_time


def count_time(function, argument, workers_num, worker):
    start_time = time.time()
    workers = [worker(target=function, args=(argument,)) for _ in range(workers_num)]
    for w in workers:
        w.start()
    for w in workers:
        w.join()
    end_time = time.time()
    return end_time - start_time


if __name__ == '__main__':
    sync_time = count_time_sync()
    threads_time = count_time(fibonacci, ARGUMENT, THREADS_NUM, Thread)
    process_time = count_time(fibonacci, ARGUMENT, THREADS_NUM, Process)
    with open('artifacts/easy_statistics.txt', "w") as file:
        file.write(f'Sync time: {sync_time} seconds\n')
        file.write(f'Threads time: {threads_time} seconds\n')
        file.write(f'Process time: {process_time} seconds\n')
