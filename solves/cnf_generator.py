from itertools import combinations
from utils import get_neighbors, var

def create_cnf(grid):
    rows, cols = len(grid), len(grid[0])
    cnf = []
    for i in range(rows):
        for j in range(cols):
            cell = grid[i][j]
            if cell == 'T':
                cnf.append([var(i, j, cols)])
            elif cell == 'G':
                cnf.append([-var(i, j, cols)])
            elif isinstance(cell, int):
                neighbors = get_neighbors(grid, i, j)
                known_traps = [var(x, y, cols) for x, y in neighbors if grid[x][y] == 'T']
                unknown = [var(x, y, cols) for x, y in neighbors if grid[x][y] == '_']
                remaining = cell - len(known_traps)
                if remaining == 0:
                    for v in unknown:
                        cnf.append([-v])
                elif remaining == len(unknown):
                    for v in unknown:
                        cnf.append([v])
                else:
                    for combo in combinations(unknown, len(unknown) - remaining + 1):
                        cnf.append(list(combo))
                    for combo in combinations(unknown, remaining + 1):
                        cnf.append([-v for v in combo])
    return cnf