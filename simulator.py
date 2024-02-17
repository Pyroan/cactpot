# Conclusions:
# Cactpot is pretty clever. With optimal play you will only score
#  Above the maximal-median for a given board about 50% of the time.
# This is a 100% improvement over choosing randomly, which results in
#  an above-median score 25% of the time.
# Optimal play (of the methods I've tested) involves filtering out all
#  rows that don't share the maximal-median (which seems to always be
#  precisely half of them), and then choosing from those the row with
#  the highest average score.
# This results in an average payout loss of somewhere
#  between 46% and 48% (rounded, n=10,000 and w/ confidence level c=0.99)
# Playing randomly would result in an average loss of
#  between 66% and 68% (n=10,000, c=0.99)
import csv
import json
import math
import random

from collections import Counter

from board import Board
from stats import *

with open('config.json') as f:
    config = json.load(f)
payouts = config['payouts']

''' runs a bunch of trials on mock cactpot boards'''
TRIALS_PER_TEST = 5000


def get_candidates(l, prefiltered_candidates=None):
    available_candidates = prefiltered_candidates or list(range(len(l)))
    candidates = []
    for i in available_candidates:
        if l[i] == max(l[j] for j in available_candidates):
            candidates += [i]
    return candidates


def permutations(k: int, a: list) -> list:
    '''
    literally just a generator for heap's algorithm, where `k` is the number of 
    missing values (5 at the top of the stack), and `a` is what those values
    are.
    (did it non-recursively because it makes generators play nice <3)
    '''
    c = [0]*k
    yield a
    i = 1
    while i < k:
        if c[i] < i:
            if i % 2:
                a[c[i]], a[i] = a[i], a[c[i]]
            else:
                a[0], a[i] = a[i], a[0]
            yield a
            c[i] += 1
            i = 1
        else:
            c[i] = 0
            i += 1


def generate_boards(alphabet: str, n) -> list[str]:
    digits = list(alphabet)
    boards = []
    for i in range(TRIALS_PER_TEST):
        random.shuffle(digits)
        boards.append(''.join(digits))
    return boards


def generate_possible_boards(board: str) -> list[Board]:
    '''
    generate all possible boards for the given set of known values
    '''
    missingno = list(set('123456789')-set(board))
    boards = []
    for i in permutations(len(missingno), missingno):
        newboard = Board(board.replace('?', '{}').format(*i))
        boards.append(newboard)
    return boards


def run_sim():
    losses = []
    # each row has its own set of data. each board generates data for 9 rows.
    test_boards = generate_boards('123456789', TRIALS_PER_TEST)
    for board in test_boards:
        obscured_board = ''.join(
            [board[i] if '010010101'[i] == '1' else '?' for i in range(len(board))])
        possible_payouts = [payouts[str(n)]
                            for n in Board(board).analyze_rows()]
        max_payout = max(possible_payouts)
        winning_rows = list(
            filter(lambda x: possible_payouts[x] == max_payout, range(0, 8)))
        # print(board, max_payout, winning_rows)

        possible_boards = generate_possible_boards(obscured_board)
        predicted_payouts = [[payouts[str(b.analyze_rows()[i])]for b in possible_boards]
                             for i in range(8)]

        row_avgs = [sum(p) // len(possible_boards) for p in predicted_payouts]
        row_medians = [sorted(p)[len(possible_boards)//2]
                       for p in predicted_payouts]
        row_avg_med_diffs = [row_medians[x] - row_avgs[x]
                             for x in range(len(row_medians))]
        row_modes = [max(Counter(p).keys()) for p in predicted_payouts]
        candidates = get_candidates(row_medians)
        candidates = get_candidates(row_avgs, candidates)

        c = random.choice(candidates)
        loss = 1-(possible_payouts[c]/max_payout)
        losses.append(loss)
        # print(c, f'{loss*100:.2f}%')
    print(f"Average loss: {average(losses)*100:.2f}%")

    standard_error = math.sqrt(
        variance(losses)/len(losses))
    print(f"std error: {standard_error*100:.2f} percentage points")
    moe = 3 * standard_error
    print(
        f"CI99: {(average(losses) - moe)*100:.2f}% ... {(average(losses)+moe)*100:.2f}%")

    # with open('sim_output.csv', 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(headers)
