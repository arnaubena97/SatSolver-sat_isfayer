#!/usr/bin/env python3
import os
import sys
import random
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

def print_solution(solution):
    """Method to print the solution that satisfies all the clauses or unsatisfiable """
    if solution:
        #solution = sorted(solution, key=abs)
        print("s SATISFIABLE")
        print("v %s 0"  %" ".join(map(str, solution)))
        exit(0)
    else:
        print("s UNSATISFIABLE")
        exit(0)

def select_var1(clauses):
    literal_weight = defaultdict(int)
    for clause in clauses:
        for literal in clause:
            literal_weight[literal] += 2 ** -len(clause) #abs(literal)
    return max(literal_weight, key=literal_weight.get)

def select_var2(clauses):
    counter = defaultdict(int)
    for clause in clauses:
        for literal in clause:
            if literal in counter:
                counter[literal] += 2 ** -len(clause)
            else:
                counter[literal] = 2 ** -len(clause)
    return max(counter, key=counter.get)


def select_var3(clauses):
    counter = defaultdict(int)
    for clause in clauses:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 1
    return max(counter, key=counter.get)

def backtrack(clauses , interpretation):
    clauses, var = unit_prop(clauses)
    interpretation = interpretation + var
    if clauses == "C":
        return []
    if not clauses:
        return interpretation
    best_var =select_var2(clauses)
    return (backtrack(delete_aparitions(clauses, best_var), interpretation +[best_var]) or backtrack(delete_aparitions(clauses, -best_var), interpretation + [-best_var]))


def delete_aparitions(clauses, var):
    aux_clauses= []
    for clause in clauses:
        if var not in clause:
            if -var not in clause:
                aux_clauses.append(clause)
            else:
                aux_clause = []
                for aux_var in clause:
                    if aux_var is not -var:
                        aux_clause.append(aux_var)
                if not aux_clause:
                    return "C"
                aux_clauses.append(aux_clause)
    return aux_clauses

def sel_lenght1(clauses):
    aux_clauses = []
    for clause in clauses:
        if len(clause)==1:
            aux_clauses.append(clause[0])
    return aux_clauses

# This implements the while loop of the BCP function
def unit_prop(clauses):
    interpretation= []
    clauses_len1 = sel_lenght1(clauses) #llista de clausules de llargada 1
    while clauses_len1:
        var = clauses_len1.pop() #per totes les clausules que estan soles...
        clauses = delete_aparitions(clauses, var)
        interpretation+= [var]
        if clauses == "C":
            return "C", []
        if not clauses: #si ja no tenim mes clausules, retornem les clusules [] i la interpretacio
            return [], interpretation
        clauses_len1 = sel_lenght1(clauses)#mirem si hi ha alguna variable que hagi pugut quedar sola
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

    count = 0
    vars, clauses = read_file(file_name)
    solution = backtrack(clauses,[])
    #print_solution(solution)

    write_file(solution)
    command = "python3 comprove.py " + file_name + " " + "t.txt"
    os.system(command)


