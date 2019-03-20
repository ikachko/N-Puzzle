#!/usr/bin/python

import sys
import argparse
from n_puzzle import puzzle_finding


def print_usage():
    print("Usage:\nsolver.py file_name")


def read_from_stdin():
    data = sys.stdin.readlines()
    return validate_data(data)

def validate_data(data):
    line_length = 0
    num_of_lines = 0

    matrix = []

    for line in data:
        if line[0] == '#':
            continue
        line = line.split('#')[0]
        if num_of_lines == 0:
            spl = line.split(' ')
            if type(spl == str):
                num_of_lines = int(line)
            else:
                print("Error: wrong matrix size parameter")
                return -1
            if num_of_lines <= 2:
                print("Size must be > 2")
                return -1
            continue
        str_nums = list(filter(None, line.split(' ')))
        if type(str_nums) != list:
            print("Error")
            return -1

        num_count = len(str_nums)
        if line_length == 0:
            line_length = num_count
        elif line_length != num_count:
            print("Error: number of digits must be the same")
            return -1

        numbers = [int(n) for n in str_nums]
        matrix.append(numbers)
    if not matrix:
        return -1
    if len(matrix) != len(matrix[0]):
        print("Error: puzzle must be squared")
        return -1
    if len(matrix) != num_of_lines:
        print("Error: invalid size")
        return -1
    return matrix


def read_from_file(file_name: str):
    try:
        f = open(file_name, 'r')
    except IOError:
        print("Could not read file: ", file_name)
        return -1

    data = list(filter(None, f.read().split('\n')))
    matrix = validate_data(data)
    return matrix


def is_valid(puzzle):
    puzzle_line = []
    for line in puzzle:
        puzzle_line += line
    puzzle_line.sort()
    if puzzle_line[-1] != (len(puzzle) ** 2 - 1):
        return False
    puzzle_set = list(set(puzzle_line))
    puzzle_set.sort()
    if puzzle_line != puzzle_set or 0 not in puzzle_line:
        return False
    return True

def find_zero_pos(puzzle):
    i = len(puzzle) - 1
    j = len(puzzle) - 1
    while i >= 0:
        while j >= 0:
            if puzzle[i][j] == 0:
                return len(puzzle) - i
            j -= 1
        i -= 1

def get_inv_count(puzzle):
    inv_count = 0
    puzzle_line = []
    for line in puzzle:
        puzzle_line += line
    for i in range(len(puzzle_line) - 1):
        for j in range(i + 1, len(puzzle_line)):
            if puzzle_line[i] != 0 and puzzle_line[j] != 0 and puzzle_line[i] > puzzle_line[j]:
                inv_count += 1
    return inv_count


def is_solvable(puzzle):
    inv_count = get_inv_count(puzzle)
    pos = find_zero_pos(puzzle)
    grid_width = len(puzzle[0])

    is_solvable = (((grid_width % 2 != 0) and (inv_count % 2 == 0)) or ((grid_width % 2 == 0) and ((pos % 2 != 0) == (inv_count % 2 == 0))))
    # if len(puzzle) % 2 != 0:
    #     solvable = (inv_count % 2 == 0)
    # else:
    #
    #     if pos % 2 == 0:
    #         solvable = (inv_count % 2 == 0)
    #     else:
    #         solvable = (inv_count % 2 != 0)
    #
    return is_valid(puzzle) and is_solvable

def make_goal(s):
    ts = s*s
    puzzle = [-1 for i in range(ts)]
    cur = 1
    x = 0
    ix = 1
    y = 0
    iy = 0
    while True:
        puzzle[x + y*s] = cur
        if cur == 0:
            break
        cur += 1
        if x + ix == s or x + ix < 0 or (ix != 0 and puzzle[x + ix + y*s] != -1):
            iy = ix
            ix = 0
        elif y + iy == s or y + iy < 0 or (iy != 0 and puzzle[x + (y+iy)*s] != -1):
            ix = -iy
            iy = 0
        x += ix
        y += iy
        if cur == s*s:
            cur = 0
    goal = [puzzle[i:i + s] for i in range(0, len(puzzle), s)]
    return goal


def matrix_printer(matrix):
    n = len(matrix)
    for i in range(n):
        sys.stdout.write('|')
        for j in range(n):
            sys.stdout.write(str(matrix[i][j]))
            if j != n - 1:
                sys.stdout.write('\t')
            else:
                sys.stdout.write('|')
        print()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--serch_type", type=int, default=0, help="Type of heurictique. Could be 1 or 2.")
    parser.add_argument("-t", "--typeof_heuristic", type=int, default=0, help="Number of passes")
    parser.add_argument("-f", "--file_name", type=str, default='', help="Filename")
    args = parser.parse_args()

    if args.typeof_heuristic < 0 or args.typeof_heuristic > 2:
        print("Type of heuristic could be 0, 1 or 2.")
        sys.exit(1)
    if args.serch_type < 0 or args.serch_type > 2:
        print("Type of serch could be 1 or 2.")
        sys.exit(1)

    # argv_len = len(sys.argv)
    # if len(args):
    #     parser.print_usage()
    #     return
    if args.file_name != '':
        matrix = read_from_file(args.file_name)
    else:
        matrix = read_from_stdin()
    if matrix == -1:
        return
    # if not is_solvable(matrix):
    #     print("Matrix is not solvable/is not valid")
    #     return
    print("\nMatrix to solve:")
    matrix_printer(matrix)
    goal = make_goal(len(matrix))
    print("\nGoal:")
    matrix_printer(goal)
    print("\n===============================\nSolution:")
    solution_sequence = puzzle_finding(matrix, goal, args.typeof_heuristic, args.serch_type)

    steps = []
    while solution_sequence:
        steps.append(solution_sequence)
        solution_sequence = solution_sequence.prev
    print("Number of moves to solve: " + str(len(steps) - 1) + "\n")
    steps = steps[::-1]
    m = 0
    for step in steps:
        if step.move:
            print('\nMove ' + str(m) + ': ' + step.move)
        matrix_printer(step.puzzle)
        m += 1

if __name__ == "__main__":
    main()


