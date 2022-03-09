import math
import concurrent
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing as mp
import time


def integrate(f, a, b, cur_job_num=0, n_jobs=1, n_iter=20000000):
    start_time = time.time()
    acc = 0
    step = (b - a) / n_iter
    iter_in_one_job = n_iter // n_jobs
    start_iter = iter_in_one_job * cur_job_num
    end_iter = min(n_iter, iter_in_one_job * (cur_job_num + 1))
    for i in range(start_iter, end_iter):
        acc += f(a + i * step) * step
    return acc, f'Job number: {cur_job_num}, start time: {start_time}, iterations from {start_iter} to {end_iter}, ' \
                f'acc: {acc}\n'


def run_integrate(function, a, b, n_jobs, pool_executor, logs_file):
    start_time = time.time()
    logs_file.write(f'Integration with {n_jobs} jobs:\n')
    submitions = []
    with pool_executor(max_workers=n_jobs) as executor:
        result = 0
        for i in range(n_jobs):
            submitions.append(executor.submit(integrate, function, a, b, i, n_jobs))
        for t in concurrent.futures.as_completed(submitions):
            acc, log = t.result()
            result += acc
            logs_file.write(log)
    logs_file.write(f'Result: {result}\n\n')
    end_time = time.time()
    return end_time - start_time, result


if __name__ == '__main__':
    with open('artifacts/medium_logs.txt', "w") as logs_file, \
            open('artifacts/medium_statistics.txt', "w") as file:
        file.write(f'Processes:\n')
        for n_jobs in range(1, 2 * mp.cpu_count() + 1):
            process_time, process_result = run_integrate(math.cos, 0, math.pi / 2, n_jobs, ProcessPoolExecutor,
                                                         logs_file)
            file.write(f'\tJob number: {n_jobs}, ')
            file.write(f'time: {process_time}, ')
            file.write(f'result: {process_result}\n')
        file.write(f'Threads:\n')
        for n_jobs in range(1, 2 * mp.cpu_count() + 1):
            threads_time, threads_result = run_integrate(math.cos, 0, math.pi / 2, n_jobs, ThreadPoolExecutor,
                                                         logs_file)
            file.write(f'\tJob number: {n_jobs}, ')
            file.write(f'time: {threads_time}, ')
            file.write(f'result: {threads_result}\n')

