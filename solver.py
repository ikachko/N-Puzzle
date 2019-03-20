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
        line = f.readline()[:-1]
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

        try:
            for i in range(num_of_lines):
                line = f.readline()[:-1]
                str_nums = line.strip(' ').split(' ')

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
        except Exception as e:

            print("Error, ", e)
            return -1
    if len(matrix) != len(matrix[0]):
        print("Error: puzzle must be squared")
        return -1
    return matrix


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

    return puzzle


def main():
    #print("Hello")
    #print(len(sys.argv))

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
    for line in matrix:
        print(line)
    goal_list = make_goal(len(matrix))
    goal = [goal_list[i:i + 3] for i in range(0, len(goal_list), len(matrix))]
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


