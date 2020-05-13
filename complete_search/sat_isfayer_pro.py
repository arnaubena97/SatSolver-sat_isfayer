#!/usr/bin/env python3
import sys
import random


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


#Main
if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        print("\n Command: python %s <file_name.cnf> \n" %sys.argv[0])
        exit(0)

    vars, clauses = read_file(file_name)
