import copy
import math


class Step:
    def __init__(self, puzzle, prev, move):
        self.prev = prev
        self.puzzle = puzzle
        self.f = 0
        self.g = 0
        self.h = 0
        self.move = move

    def calc_f(self):
        self.f = self.g + self.h


def heuristic_calc(puzzle, n, goal, h_type):
    h = 0
    if h_type == 0:
        for i in range(1, n*n):
            i_p, j_p = find_element(puzzle, n, i)
            i_g, j_g = find_element(goal, n, i)
            h = h + math.fabs(i_p - i_g) + math.fabs(j_p - j_g)
    elif h_type == 1:
        for i in range(1, n*n):
            i_p, j_p = find_element(puzzle, n, i)
            i_g, j_g = find_element(goal, n, i)
            h = h + math.sqrt(math.pow(i_p - i_g, 2) + math.pow(j_p - j_g, 2))
    else:
        for i in range(1, n*n):
            i_p, j_p = find_element(puzzle, n, i)
            i_g, j_g = find_element(goal, n, i)
            h = h + math.sqrt(math.sqrt(math.pow(i_p - i_g, 4) + math.pow(j_p - j_g, 4)))
    return h


def find_element(puzzle, n, element):
    for i in range(n):
        for j in range(n):
            if puzzle[i][j] == element:
                return i, j


def find_steps(best_step, n):
    s = []
    i, j = find_element(best_step.puzzle, n, 0)
    if i != 0:
        new_puzzle = copy.deepcopy(best_step.puzzle)
        new_puzzle[i][j], new_puzzle[i - 1][j] = new_puzzle[i - 1][j], new_puzzle[i][j]
        s.append(Step(new_puzzle, best_step, 'Up'))
    if i != n - 1:
        new_puzzle = copy.deepcopy(best_step.puzzle)
        new_puzzle[i][j], new_puzzle[i + 1][j] = new_puzzle[i + 1][j], new_puzzle[i][j]
        s.append(Step(new_puzzle, best_step, 'Down'))
    if j != 0:
        new_puzzle = copy.deepcopy(best_step.puzzle)
        new_puzzle[i][j], new_puzzle[i][j - 1] = new_puzzle[i][j - 1], new_puzzle[i][j]
        s.append(Step(new_puzzle, best_step, 'Left'))
    if j != n - 1:
        new_puzzle = copy.deepcopy(best_step.puzzle)
        new_puzzle[i][j], new_puzzle[i][j + 1] = new_puzzle[i][j + 1], new_puzzle[i][j]
        s.append(Step(new_puzzle, best_step, 'Right'))
    return s


def puzzle_exsist_in_set(puzzle, set):
    for elem in set:
        if elem.puzzle == puzzle:
            return 1
    return 0


def puzzle_finding(puzzle, goal, h_type, serch_type):
    n = len(puzzle)
    open_set = []
    closed_set = []
    open_set.append(Step(puzzle, None, None))

    while len(open_set) > 0:
        best_index = 0
        for i in range(len(open_set)):
            if serch_type == 0 and open_set[i].f < open_set[best_index].f:
                best_index = i
            elif serch_type == 1 and open_set[i].g < open_set[best_index].g:
                best_index = i
            elif serch_type == 2 and open_set[i].h < open_set[best_index].h:
                best_index = i
        best_step = open_set[best_index]

        if best_step.puzzle == goal:
            print('Open set states: ' + str(len(open_set)))
            print('Maximum number of states: ' + str(len(open_set) + len(closed_set)))
            return best_step

        open_set.remove(best_step)
        closed_set.append(best_step)
        newSteps = find_steps(best_step, n)

        for newStep in newSteps:
            if puzzle_exsist_in_set(newStep.puzzle, closed_set) == 0:
                best_path = 0
                temp_g = best_step.g + 1
                if puzzle_exsist_in_set(newStep.puzzle, open_set) == 1:
                    if temp_g < newStep.g:
                        newStep.g = temp_g
                        best_path = 1
                else:
                    newStep.g = temp_g
                    open_set.append(newStep)
                    best_path = 1

                if best_path == 1:
                    newStep.h = heuristic_calc(newStep.puzzle, n, goal, h_type)
                    newStep.calc_f()
                    newStep.prevStep = best_step
    print("unsolvable")
    return None
