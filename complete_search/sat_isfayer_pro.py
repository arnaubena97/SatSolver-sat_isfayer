#!/usr/bin/env python3
import sys
from collections import defaultdict
sys.setrecursionlimit(10**9)

def read_file(file_name):
    """File reader and parser the num of variables, num of clauses and put the clauses in a list"""
    clauses =[]
    with open(file_name) as all_file:
        for line in all_file:
            if line.startswith('c'): continue #ignore comments
            if line.startswith('p'):
                num_variables = int(line.split()[2]) # set num_variables
                continue
            if line.strip() == "": continue
            clause = list(map(int, line.split()))
            clause.pop()
            clauses.append(clause)
    return num_variables, clauses

def print_solution(solution, num_vars):
    """Method to print the solution that satisfies all the clauses or unsatisfiable """
    if solution:
        aux_solution = [x for x in range(1, num_vars+1)]## to put all variables in interpretation
        for var in solution:
            if aux_solution[abs(var)-1] != var:
                    aux_solution[abs(var)-1] = var
        print("s SATISFIABLE")
        print("v %s 0"  %" ".join(map(str, aux_solution)))
        exit(0)
    else:
        print("s UNSATISFIABLE")
        exit(0)

def select_var2(clauses):
    """heuristic2"""
    counter = defaultdict(int)
    for clause in clauses:
        for literal in clause:
            counter[literal] += 2 ** -len(clause)
    return max(counter, key=counter.get)

def select_var1(clauses):
    """heuristic1"""
    counter = defaultdict(int)
    for clause in clauses:
        for literal in clause:
            counter[literal] += 1
    return max(counter, key=counter.get)

def dpll(clauses, best_var=0, interpretation=[]):
    """Function to explore all posibilities to find a solution"""
    if best_var != 0:
        clauses = delete_aparitions(clauses, best_var)
        interpretation += [best_var]
    clauses, var = unit_prop(clauses)
    interpretation = interpretation + var
    if clauses == "conflict":
        return []
    if not clauses:
        return interpretation
    best_var =select_var2(clauses)
    return(dpll(clauses, best_var, interpretation) # branch variable
           or dpll(clauses, -best_var, interpretation))# branch oposite variable

def delete_aparitions(clauses, variable):
    """delete apartitions of variable or -variable in clause"""
    aux_clauses = []
    for clause in clauses:
        if -variable in clause:
            one_clause =[]
            for var in clause:
                if var != -variable:
                    one_clause.append(var)
            if one_clause == []: # unsat
                return "conflict"
            aux_clauses.append(one_clause)
        if variable not in clause and -variable not in clause:
            aux_clauses.append(clause)
    return aux_clauses

def find_lenght1(clauses):
    """find the clauses of lenght 1 to satisfy"""
    aux_clauses = []
    for clause in clauses:
        if len(clause)==1:
            aux_clauses.append(clause[0])
    return aux_clauses

def unit_prop(clauses):
    """put true the variables in clause 1 of length"""
    interpretation= []
    clauses_len1 = find_lenght1(clauses) #look if a variable is alone in clause
    while clauses_len1:
        var = clauses_len1.pop() #for all clauses that they are alone
        clauses = delete_aparitions(clauses, var)
        interpretation+= [var]
        if clauses == "conflict":
            return "conflict", [] #return conflict because can't be possible to asing it(UNSAT if they explore all)
        if not clauses: #don't more clause, return [] and interpretation(SATISFIABLE)
            return [], interpretation
        clauses_len1 = find_lenght1(clauses)#look if a variable is alone in clause for new iteration
    return clauses, interpretation

#Main
if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        print("\n Command: python %s <file_name.cnf> \n" %sys.argv[0])
        exit(0)
    vars, clauses = read_file(file_name)
    solution = dpll(clauses)
    print_solution(solution, vars)


