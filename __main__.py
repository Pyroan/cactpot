'''i'm special and my wheels are best'''
import argparse
import json
import re
from collections import Counter

from colorama import Fore, Style, just_fix_windows_console

import simulator
from board import Board

just_fix_windows_console()


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


if __name__ == "__main__":
    simulator.run_sim()
    exit()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'board', type=str, help="A 9-character string representing a cactpot board. Values ordered lexicographically. Replace unknown values with `?` e.g. '12??5???9'")

    args = parser.parse_args()
    board_str = args.board

    # board validation for some reason
    board_str_without_unknowns = [*filter(lambda x: x != '?', board_str)]
    if not re.fullmatch(r'[0-9\?]{9}', board_str) or len(set(board_str_without_unknowns)) != len(board_str_without_unknowns):
        raise ValueError("Invalid cactpot board!")

    possible_boards = generate_possible_boards(board_str)
    row_averages = [sum(payouts[str(b.analyze_rows()[i])] for b in possible_boards) // len(possible_boards)
                    for i in range(8)]
    print("Average Payouts:")
    board = Board(board_str)
    for i in range(len(row_averages)):
        if row_averages[i] == max(row_averages):
            board.highlight_row(i, Style.BRIGHT+Fore.GREEN)
    board.draw(row_averages)
    print("Median Payouts:")
    row_medians = [sorted(payouts[str(b.analyze_rows()[i])] for b in possible_boards)[
        len(possible_boards)//2]for i in range(8)]
    board = Board(board_str)
    for i in range(len(row_medians)):
        if row_medians[i] == max(row_medians):
            board.highlight_row(i, Style.BRIGHT+Fore.GREEN)
    board.draw(row_medians)
