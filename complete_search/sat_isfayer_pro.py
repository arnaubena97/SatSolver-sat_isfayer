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
        aux_solution = [x for x in range(1, num_vars+1)]
        for var in solution:
            if aux_solution[abs(var)-1] != var:
                aux_solution[abs(var)-1] = var
        print("s SATISFIABLE")
        print("v %s 0"  %" ".join(map(str, aux_solution)))
        exit(0)
    else:
        print("s UNSATISFIABLE")
        exit(0)

def select_var1(clauses):
    """heuristic1"""
    literal_weight = defaultdict(int)
    for clause in clauses:
        for literal in clause:
            literal_weight[literal] += 2 ** -len(clause) #abs(literal)
    return max(literal_weight, key=literal_weight.get)

def select_var2(clauses):
    """heuristic2"""
    counter = defaultdict(int)
    for clause in clauses:
        for literal in clause:
            if literal in counter:
                counter[literal] += 2 ** -len(clause)
            else:
                counter[literal] = 2 ** -len(clause)
    return max(counter, key=counter.get)

def select_var3(clauses):
    """heuristic3"""
    counter = defaultdict(int)
    for clause in clauses:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return max(counter, key=counter.get)

def backtrack(clauses, interpretation):
    clauses, var = unit_prop(clauses)
    interpretation = interpretation + var
    if clauses == "conflict":
        return []
    if not clauses:
        return interpretation
    best_var =select_var1(clauses)
    return(backtrack(delete_aparitions(clauses, best_var), interpretation +[best_var])
           or backtrack(delete_aparitions(clauses, -best_var), interpretation + [-best_var]))

def delete_aparitions(clauses, variable):
    """delete apartitions of variable or -variable in clause"""
    aux_clauses = []
    for clause in clauses:
        if -variable in clause:
            one_clause =[]
            for var in clause:
                if var != -variable:
                    one_clause.append(var)
            if one_clause == []:
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
    interpretation= []
    clauses_len1 = find_lenght1(clauses) #llista de clausules de llargada 1
    while clauses_len1:
        var = clauses_len1.pop() #per totes les clausules que estan soles...
        clauses = delete_aparitions(clauses, var)
        interpretation+= [var]
        if clauses == "conflict":
            return "conflict", []
        if not clauses: #si ja no tenim mes clausules, retornem les clusules [] i la interpretacio
            return [], interpretation
        clauses_len1 = find_lenght1(clauses)#mirem si hi ha alguna variable que hagi pugut quedar sola
    return clauses, interpretation

#Main
if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        print("\n Command: python %s <file_name.cnf> \n" %sys.argv[0])
        exit(0)

    vars, clauses = read_file(file_name)
    solution = backtrack(clauses,[])
    print_solution(solution, vars)



