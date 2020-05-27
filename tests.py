

from tsp_wrapper import TSP


def run_tests():
    """
    """
    print('**************************** Hello in my Program :) ******************************\
        \n******************************* Maysaa Alsafadi ***********************************\n')
    print('Start tests\n')

    print('>>>> Run test single threaded')
    test_single_threaded()
    print('done\n')

    print('>>>> Run test concurrent single threaded')
    test_concurrent_single_threaded()
    print('done\n')

    print('>>>> Run test multi threaded')
    test_multi_threaded()
    print('done')


def test_single_threaded():
    """
    """
    nb_city = 10
    nb_step = int(1e2)

    beta_mult = 1.02
    nb_run = 1
    accept_nb_step = 100
    p1 = 0.2
    p2 = 0.8

    tsp = TSP(nb_city, nb_run, nb_step, beta_mult, accept_nb_step, p1, p2)
    tsp.generate_cities(seed=54321)

    sol = tsp.search_single_thread('search', check_signature=True, dated=False)
    print(sol[:3])


def test_concurrent_single_threaded():
    """
    """
    nb_city = 50
    nb_run = int(4)
    nb_step = int(1e4)

    beta_mult = 1.02
    accept_nb_step = 100
    p1 = 0.2
    p2 = 0.8

    tsp = TSP(nb_city, nb_run, nb_step, beta_mult, accept_nb_step, p1, p2)
    tsp.generate_cities(seed=54321)

    tsp.search_concurrent('search', check_signature=True, dated=False)
    # print(tsp.res)

    best_sols = sorted([e['dist'] for e in tsp.res['solutions']])
    print('Shortest paths found:')
    print(best_sols)


def test_multi_threaded():
    """
    """

    nb_city = 50
    nb_run = int(4)
    nb_step = int(1e4)

    beta_mult = 1.02
    accept_nb_step = 100
    p1 = 0.2
    p2 = 0.8

    tsp = TSP(nb_city, nb_run, nb_step, beta_mult, accept_nb_step, p1, p2)

    tsp.generate_cities(seed=54321)

    tsp.search_omp('search', dated=False)

    # print(tsp.res)

    best_sols = sorted([e['dist'] for e in tsp.res['solutions']])
    print('Shortest paths found:')
    print(best_sols)
