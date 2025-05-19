from pysat.solvers import Glucose3

def solve_pysat(cnf):
    solver = Glucose3()
    for clause in cnf:
        solver.add_clause(clause)
    if solver.solve():
        return solver.get_model()
    else:
        return None