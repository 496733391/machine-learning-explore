#! /usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing import Pool


def min_max(compare_list):
    return max(compare_list)


if __name__ == '__main__':
    all_list = list(range(100))
    process_pool = Pool(4)
    process_list = []
    for i in range(4):
        process_list.append(process_pool.apply_async(func=min_max, args=(all_list[i:i+25], )))
    result_list = []

    for process in process_list:
        result_list.append(process.get())
    print(result_list)

    result_list2 = process_pool.map_async(min_max, (all_list[0:25], all_list[25:50])).get()
    print(result_list2)

    process_pool.close()
    process_pool.join()
