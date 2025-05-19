from pysat.solvers import Glucose3 
def solve_pysat(CNF):
    solverSAT = Glucose3()
    # đi trong từng mệnh đề trong CNF
    for clause in CNF:
        solverSAT.add_clause(clause)
    if solverSAT.solve():
        return solverSAT.get_model()
    return None
    
