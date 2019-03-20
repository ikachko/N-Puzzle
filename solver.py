#!/usr/bin/python

import sys
import getopt
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

def get_inv_count(puzzle):
    inv_count = 0
    puzzle_line = []
    for line in puzzle:
        puzzle_line += line
    for i in range(len(puzzle_line) - 1):
        for j in range(i + 1, len(puzzle_line)):
            if puzzle_line[i] > puzzle_line[j]:
                inv_count += 1
    return inv_count

def is_solvable(puzzle):
    return is_valid(puzzle) and (get_inv_count(puzzle) % 2 == 0)

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

def main():
    argv_len = len(sys.argv)
    if argv_len > 2 or argv_len <= 0:
        print_usage()
        return
    elif argv_len == 2:
        matrix = read_from_file(sys.argv[1])
    else:
        matrix = read_from_stdin()
    if matrix == -1:
        return

    if not is_solvable(matrix):
        print("Matrix is not solvable/is not valid")
        return
    print("\nMatrix to solve:")
    for line in matrix:
        print(line)
    goal = make_goal(len(matrix))
    print("\nGoal:")
    for line in goal:
        print(line)
    print("\n===============================\nSolution:")
    solution_sequence = puzzle_finding(matrix, goal, 0)
    m = 1
    while solution_sequence:
        for line in solution_sequence.puzzle:
            print(line)
        if solution_sequence.move:
            print('\nMove ' + str(m) + ': ' + solution_sequence.move)
        solution_sequence = solution_sequence.prev
        m += 1

if __name__ == "__main__":
    main()


