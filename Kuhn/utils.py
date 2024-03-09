import random
from termcolor import colored
from config import VERBOSE
def game_print(text, color="white", verbose=VERBOSE):
    if verbose:
        print(colored(text, color))

def sample(pdf):
    total = sum(pdf)
    rand_num = random.uniform(0, total)
    cumulative_sum = 0
    for i in range(len(pdf)):
        cumulative_sum += pdf[i]
        if rand_num < cumulative_sum:
            return i