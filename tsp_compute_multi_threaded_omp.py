
############
# to compile
# $ pythran -DUSE_XSIMD -fopenmp -march=native tsp_compute_multi_threaded_omp.py

# pythran export search_for_best_omp(int, float list list, int, float, int, float, float, bool)


import math
import random as rd


def dist(cities, i, j):
    """
    """
    dx = cities[i][0] - cities[j][0]
    dy = cities[i][1] - cities[j][1]
    return math.sqrt(dx**2 + dy**2)


def dist_path(cities, path):
    """
    """
    N = len(path)
    # print(path)
    li_dist = [dist(cities, path[k], path[k+1]) for k in range(N - 1)]
    li_dist += [dist(cities, path[0], path[N-1])]
    return sum(li_dist)


def search_for_best_omp(n_run,
                        cities,
                        nb_step,
                        beta_mult=1.005,
                        accept_nb_step=100,
                        p1=0.2,
                        p2=0.6,
                        check_signature=False):
    """
    exported
    """

    nb_city = len(cities)
    init_path = [k for k in range(nb_city)]

    res = []

    # omp parallel for
    for x in range(n_run):

        beta = 1.0
        n_accept = 0
        best_energy = float('inf')

        path = init_path[:]
        energy = dist_path(cities, path)

        # # init for omp
        i = 0
        j = 0

        compute_energy = 0
        if check_signature:
            store = set()

        for step in range(nb_step):

            if n_accept == accept_nb_step:
                beta *= beta_mult
                n_accept = 0

            p = rd.uniform(0.0, 1.0)
            if p < p1:
                # reverse section i-j
                i = rd.randint(1, nb_city-2)
                j = rd.randint(i+1, nb_city-1)
                new_path = path[:i]+[path[k] for k in range(j, i-1, -1)]+path[j+1:]

            elif p < p2:
                # move i to j
                new_path = path[:]
                i = rd.randint(1, nb_city - 1)
                b = new_path.pop(i)
                j = rd.randint(1, nb_city - 2)
                new_path.insert(j, b)

            else:
                # swap i and j
                new_path = path[:]
                i = rd.randint(1, nb_city - 1)
                j = rd.randint(1, nb_city - 1)
                new_path[i] = path[j]
                new_path[j] = path[i]

            process = True
            if check_signature:
                uuid = signature(new_path)
                if uuid in store:
                    process = False

            if process:
                new_energy = dist_path(cities, new_path)
                compute_energy += 1

                if check_signature:
                    store.add(uuid)

                if rd.uniform(0.0, 1.0) < math.exp(-beta * (new_energy - energy)):
                    n_accept += 1
                    energy = new_energy
                    path = new_path[:]
                    if energy < best_energy:
                        best_energy = energy
                        best_path = path[:]

        # omp critical
        if check_signature:
            store_stats = {
                'nb_step': nb_step,
                'store_len': len(store),
                'ratio': len(store)/nb_step,
                'compute_energy': compute_energy,
            }
            res.append((best_energy, best_path, store_stats))

        else:
            res.append((best_energy, best_path, {}))

    return res


def signature(path):
    """
    """
    i = path.index(0)
    cand_1 = path[i:]+path[:i]
    cand_2 = cand_1[0:1]+cand_1[1:][::-1]

    if cand_1[1] < cand_2[1]:
        cand = cand_1
    else:
        cand = cand_2

    return tuple(cand)
