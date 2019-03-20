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


def heuristic_calc(puzzle, n, goal):
    h = 0
    for i in range(1, n*n):
        i_p, j_p = find_element(puzzle, n, i)
        i_g, j_g = find_element(goal, n, i)
        h = h + math.fabs(i_p - i_g) + math.fabs(j_p - j_g)
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


def puzzle_finding(puzzle, n):
    goal = make_goal(n)
    open_set = []
    closed_set = []
    open_set.append(Step(puzzle, None, None))

    while len(open_set) > 0:
        best_index = 0
        for i in range(len(open_set)):
            if open_set[i].f < open_set[best_index].f:
                best_index = i
        best_step = open_set[best_index]

        if best_step.puzzle == goal:
            print('vse')
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
                    newStep.h = heuristic_calc(newStep.puzzle, n, goal)
                    newStep.calc_f()
                    newStep.prevStep = best_step
    print("unsolvable")
    return None


path = puzzle_finding([[1, 2, 3, 4], [10, 12, 14, 5], [0, 13, 15, 6], [9, 11, 8, 7]], 4)
m = 1
while path:
    for line in path.puzzle:
        for elem in line:
            print(str(elem))
    print("--------------")
    if path.move:
        print('move ' + str(m) + ': ' + path.move)
    path = path.prev
    m += 1
