#!/usr/bin/python

import sys
import getopt
from n_puzzle import puzzle_finding


def print_usage():
    print("Usage:\nsolver.py file_name")


def read_from_file(file_name: str):
    try:
        f = open(file_name, 'r')
    except IOError:
        print("Could not read file: ", file_name)
        return -1

    line_length = 0
    num_of_lines = 0

    matrix = []

    while f.readable():
        line = f.readline()[:-1].strip()
        if not line:
            break
        if line[0] == '#':
            continue
        if num_of_lines == 0:
            if type(line.split(' ') == str):
                num_of_lines = int(line)
            else:
                print("Error")
                return -1
        for i in range(num_of_lines):
            line = f.readline()[:-1].strip()
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
    if len(matrix) != len(matrix[0]):
        print("Error: puzzle must be squared")
        return -1
    return matrix


def is_valid(puzzle):
    puzzle_str = list(''.join(str(item) for innerlist in puzzle for item in innerlist)).sort()
    puzzle_set_str = list(set(puzzle_str)).sort()
    if puzzle_str != puzzle_set_str or '0' not in puzzle_str:
        print(puzzle_str)
        print(puzzle_set_str)
        return False
    return True


def get_inv_count(puzzle):
    inv_count = 0
    for i in range(len(puzzle) - 1):
        for j in range(i + 1, len(puzzle[i])):
            if (puzzle[i] > puzzle[j]):
                inv_count += 1
    return inv_count


def is_solvable(puzzle):
    if not is_valid(puzzle):
        return False

    inv_count = get_inv_count(puzzle)
    if inv_count % 2 == 0:
        return True
    return False


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
    argv_len = len(sys.argv)
    if argv_len > 2 or argv_len <= 0:
        print_usage()
        return
    elif argv_len == 2:
        matrix = read_from_file(sys.argv[1])
    else:
        matrix = -1
    # else:
    #     matrix = read_from_stdin()

    if matrix == -1:
        return
    print("\nMatrix to solve:")
    matrix_printer(matrix)
    goal = make_goal(len(matrix))
    print("\nGoal:")
    matrix_printer(goal)
    print("\n===============================\nSolution:")
    solution_sequence = puzzle_finding(matrix, goal, 0, 0)

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


