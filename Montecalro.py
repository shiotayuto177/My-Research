import numpy as np
from multiprocessing import Pool
def calc_pi_partial(n):
    print(n)
    cnt = 0
    for _ in range(n):
        x = np.random.random()
        y = np.random.random()
        if x*x + y*y < 1:
            cnt += 1
    return cnt
def calc_pi_parallel(total_n, num_processes):
    # 各プロセスに割り当てるpartial_nを求める
    partial_n = total_n // num_processes
    with Pool(num_processes) as pool:
        # 各プロセスでcalc_pi_partialを実行
        counts = pool.map(calc_pi_partial, [partial_n] * num_processes)
        print(counts)
    # 全部のカウントを合計して、円周率を計算
    pi_estimate = (sum(counts) * 4.0) / total_n
    print(pi_estimate)
    return pi_estimate

