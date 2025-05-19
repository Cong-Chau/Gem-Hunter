def satisfies_partial(assignment, clause):
    satisfied = False
    undecided = False
    for lit in clause:
        var = abs(lit)
        if var not in assignment:
            undecided = True
            continue
        val = assignment[var]
        if (lit > 0 and val) or (lit < 0 and not val):
            satisfied = True
            break
    return satisfied or undecided

def is_partial_valid(cnf, assignment):
    return all(satisfies_partial(assignment, clause) for clause in cnf)

def backtrack(cnf, num_vars, assignment={}, var=1):
    if var > num_vars:
        return assignment if is_partial_valid(cnf, assignment) else None

    for val in [False, True]:
        assignment[var] = val
        if is_partial_valid(cnf, assignment):
            result = backtrack(cnf, num_vars, assignment, var + 1)
            if result:
                return result
        del assignment[var]
    return None
