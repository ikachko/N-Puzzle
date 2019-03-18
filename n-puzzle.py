class Step:
    def __init__(self, puzzle):
        self.prevStep = None
        self.puzzle = puzzle
        self.f = 0
        self.move = None


def find_zero(puzzle, n):
    for i in range(n):
        for j in range(n):
            if puzzle[i][j] == 0:
                return i, j


def find_steps(best_step, n):
    s = []
    i, j = find_zero(best_step.puzzle, n)
    if (i != 0):
        newPuzzle = best_step.puzzle
        buff = newPuzzle[i][j]
        newPuzzle[i][j] = newPuzzle[i - 1][j]
        newPuzzle[i - 1][j] = buff
        s.append(Step(newPuzzle))
    if (i != n - 1):
        newPuzzle = best_step.puzzle
        buff = newPuzzle[i][j]
        newPuzzle[i][j] = newPuzzle[i + 1][j]
        newPuzzle[i + 1][j] = buff
        s.append(Step(newPuzzle))
    if (j != 0):
        newPuzzle = best_step.puzzle
        buff = newPuzzle[i][j]
        newPuzzle[i][j] = newPuzzle[i][j - 1]
        newPuzzle[i][j - 1] = buff
        s.append(Step(newPuzzle))
    if (j != n - 1):
        newPuzzle = best_step.puzzle
        buff = newPuzzle[i][j]
        newPuzzle[i][j] = newPuzzle[i][j + 1]
        newPuzzle[i][j + 1] = buff
        s.append(Step(newPuzzle))
    return s


def puzzle_finding(puzzle):
    n = 3
    goal = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
    open_set = []
    closed_set = []
    open_set.append(Step(puzzle))

    while len(open_set) > 0:
        bestIndex = 0
        for i in range(len(open_set)):
            if open_set[i].f < open_set[bestIndex].f:
                bestIndex = i
        bestStep = open_set[bestIndex]
        if bestStep.puzzle == goal:
            print('vse')
            return 137
        open_set.remove(bestStep)
        closed_set.append(bestStep)
        newSteps = find_steps(bestStep, n)
        # finding best G
        # prev = bestStep


puzzle_finding([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]])
