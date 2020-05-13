#!/usr/bin/env python3
import os
import sys
import random
from collections import defaultdict


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

def print_solution(solution):
    """Method to print the solution that satisfies all the clauses or unsatisfiable """
    if solution:
        print("s SATISFIABLE")
        print("v %s 0"  %" ".join(map(str, solution)))
        exit(0)
    else:
        print("s UNSATISFIABLE")
        exit(0)

def heuristic_1(clauses):
    literal_weight = defaultdict(int)
    for clause in clauses:
        for literal in clause:
            literal_weight[abs(literal)] += 2 ** -len(clause)
    #print(max(literal_weight, key=literal_weight.get))
    return max(literal_weight, key=literal_weight.get)


def backtrack(clauses , interpretation):
    clauses, var = assign_unit(clauses)
    interpretation = interpretation + var
    if clauses == -1:
        return []
    if not clauses:
        return interpretation
    best_var = heuristic_1(clauses)
    res = backtrack(bcp(clauses, best_var), interpretation + [best_var])
    # if no solution when assigning to True, try to assign to False
    if not res:
        res = backtrack(bcp(clauses, -best_var), interpretation + [-best_var])
    return res

def bcp(clauses, unit):
    new_cnf = []
    for clause in clauses:
        if unit in clause:
            continue
        if -unit in clause:
            new_clause = [literal for literal in clause if literal != -unit]
            if not new_clause:
                return -1
            new_cnf.append(new_clause)
        else:
            new_cnf.append(clause)
    return new_cnf

# This implements the while loop of the BCP function
def assign_unit(clauses):
    interpretation= []  # contains the bool assignments for each variable
    unit_clauses = [clause for clause in clauses if len(clause) == 1]
    while unit_clauses:
        unit = unit_clauses[0][0]
        clauses = bcp(clauses, unit)  # assign true to unit
        interpretation+= [unit]
        if clauses == -1:
            return -1, []
        # base case: empty conjunct so it is SAT
        if not clauses:
            return clauses, interpretation
        unit_clauses = [clause for clause in clauses if len(clause) == 1]  # update
    return clauses, interpretation

def write_file(solution):
    f = open("t.txt", "w")
    if solution:
        f.write("s SATISFIABLE\n")
        f.write(("v %s 0" % " ".join(map(str, solution))))

    else:
        f.write("s UNSATISFIABLE")




#Main
if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        print("\n Command: python %s <file_name.cnf> \n" %sys.argv[0])
        exit(0)

    vars, clauses = read_file(file_name)
    solution = backtrack(clauses,[])
    print_solution(solution)

    #write_file(solution)
    #command = "python3 comprove.py " + file_name + " " + "t.txt"
    #os.system(command)


