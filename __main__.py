'''fuck everyone who's written their own solver i'm writing mine because i'm special
and my wheels are best'''
import argparse
import json
import re
from collections import Counter

with open('config.json') as f:
    config = json.load(f)
payouts = config['payouts']


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


def analyzeRows(board: list[int]):
    '''
    return an array of the sum of each 'row' in the cactpot board
    '''
    rowsums = [0]*8
    # LR diagonal
    rowsums[0] = sum(board[0::4])
    # Columns
    for i in range(3):
        rowsums[i+1] = sum(board[i::3])
    # RL Diagonal
    rowsums[4] = sum(board[2:7:2])
    # Rows
    for i in range(3):
        rowsums[i+5] = sum(board[3*i:3*(i+1)])
    return rowsums


def analyze_possible_boards(board: str):
    '''
    compute the possible payouts for each row for all possible boards given
    the known board information
    '''
    missingno = list(set('123456789')-set(board))
    row_results = []
    for i in permutations(len(missingno), missingno):
        newboard = board.replace('?', '{}').format(*i)
        newboard = [*map(int, list(newboard))]
        row_results.append(analyzeRows(newboard))
    return row_results


def printboard(board: list, rowsums: list[int]):
    vals = (*rowsums[:6], *board[:3], rowsums[6],
            *board[3:6], rowsums[7], *board[6:])
    print(
        '''\
  {:5}  {:^5} {:^5} {:^5}  {:<5}  
      ↘    ↓     ↓     ↓    ↙
        ┌─────┬─────┬─────┐
{:>5} → │  {}  │  {}  │  {}  │
        ├─────┼─────┼─────┤
{:>5} → │  {}  │  {}  │  {}  │
        ├─────┼─────┼─────┤
{:>5} → │  {}  │  {}  │  {}  │
        └─────┴─────┴─────┘
    '''.format(*vals)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'board', type=str, help="A 9-character string representing a cactpot board. Values ordered lexicographically. Replace unknown values with `?` e.g. '12??5???9'")

    args = parser.parse_args()
    board = args.board

    # board validation for some reason
    board_without_unknowns = [*filter(lambda x: x != '?', board)]
    if not re.fullmatch(r'[0-9\?]{9}', board) or len(set(board_without_unknowns)) != len(board_without_unknowns):
        raise ValueError("Invalid cactpot board!")

    row_results = analyze_possible_boards(board)
    row_averages = [sum(payouts[str(r[i])] for r in row_results) // len(row_results)
                    for i in range(len(row_results[0]))]
    row_medians = [sorted(payouts[str(r[i])] for r in row_results)[
        len(row_results)//2] for i in range(len(row_results[0]))]
    # print(Counter(payouts[str(r[3])] for r in row_results))
    print("Average Payouts:")
    printboard(board, row_averages)
    print("Median Payouts:")
    printboard(board, row_medians)
