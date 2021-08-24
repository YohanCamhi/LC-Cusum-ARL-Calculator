import math
import random
import statistics


def create_random_list(size, prob_one):
    """
    Creates a random list composed of ones and zeroes of size size and with prob_one probability of ones
    """
    nb_ones = int(size * prob_one)
    nb_zeros = size - nb_ones

    array = [0] * nb_zeros + [1] * nb_ones
    random.shuffle(array)
    return array


def create_cumulative_sum(data, wt0, wt1):
    """
    Computes the cumulative sum of data.
    Returns a new list where each element corresponds to the cumulative sum of data, where data must be a list 0 or 1s.
    Cumulative sum can not go below zero.
    """
    ret = []
    last_res = 0
    for i in data:
        if i == 0:
            last_res = last_res + wt0
        elif i == 1:
            last_res = last_res + wt1
        else:
            raise RuntimeError("Unexpected value")
        if last_res < 0:
            last_res = 0
        ret.append(last_res)
    return ret


def calculate_wt(p0, lbda, xt):
    """
    Calculates wt0 or wt1 given the adequate performance (p0) and the equivalence zone (lbda)
    """
    return math.log(
        (
                (p0 ** xt) * ((1 - p0) ** (1 - xt))
        ) /
        (
                ((p0 + lbda) ** xt) * ((1 - p0 - lbda) ** (1 - xt))
        )
    )


def calculate_arl(h, wt0, wt1, failure_rate, run, n):
    """
    Calculates the average runtime length for a given failure rate by simulating `run` number of runs with
    randomly generated samples with `failure_rate`failures, and wt0, wt1 and h for the lc-cusum parameters
    """
    run_length = []
    for i in range(run):
        data = create_random_list(n, failure_rate)
        cusum = create_cumulative_sum(data, wt0, wt1)
        index = 0
        for index, entry in enumerate(cusum, start=1):
            if entry > h:
                break
        run_length.append(index)
    mean = statistics.mean(run_length)
    return mean


def main():
    random.seed()

    try:
        p0 = float(input("Please enter the adequate performance value (p0): "))
        lbda = float(input("Please enter the equivalence zone value (δ): "))
        h = float(input("Please enter the lc-cusum limit (h): "))
        run = int(input("Please enter the number of runs you wish to simulate: "))
        n = int(input("Please enter the number of subjects you wish to simulate per run: "))
    except ValueError:
        print("Error: all the values must be numbers")
        return -1

    if not 0 < p0 < 1:
        print("Error: p0 must be a real number between zero and one.")
        return -1

    if not 0 < lbda < 1:
        print("Error: δ must be a real number between zero and one.")
        return -1

    wt0 = calculate_wt(p0, lbda, 0)
    wt1 = calculate_wt(p0, lbda, 1)

    acceptable_failure_rate = p0
    unacceptable_failure_rate = p0 + lbda

    print(f"Calculating ARL with parameters:\n"
          f"p0                          : {p0}\n"
          f"δ                           : {lbda}\n"
          f"h                           : {h}\n"
          f"number of runs              : {run}\n"
          f"number of subjects in a run : {n}\n"
          f"wt0                         : {wt0}\n"
          f"wt1                         : {wt1}\n"
          f"acceptable failure rate     : {acceptable_failure_rate}\n"
          f"unacceptable failure rate   : {unacceptable_failure_rate}")

    arl0 = calculate_arl(h, wt0, wt1, unacceptable_failure_rate, run, n)
    print(f"ARL0 : {arl0}")

    arl1 = calculate_arl(h, wt0, wt1, acceptable_failure_rate, run, n)
    print(f"ARL1 : {arl1}")

    return 0


if __name__ == '__main__':
    main()
    input("Please press enter to continue...")
