#!/usr/bin/python3
'''
SAT Solver description ..
'''
#Libraries

import sys
import random
import os
from itertools import product

MAX_TRIES = 1000000


class cnf_formula(object):
    """Class to read and his methods """

    def __init__(self, file_name=""):
        """Constructor of the cnf_formula class"""
        self.num_variables = 0
        self.num_clauses = 0
        self.clauses = []
        if os.path.isfile(file_name): #comprove if the file exist
            self.read_file(file_name)
        else:
            print("Doesn't exist %s", file_name)
            exit(1)
    
    def read_file(self, file_name):
        """file reader and parser to store in the variables of the class"""
        with open(file_name) as all_file:
            for line in all_file:
                if line.startswith('c'): continue #ignore comments
                if line.startswith('p'):
                    self.num_variables = int(line.split(' ')[2]) # set num_variables
                    self.num_clauses = int(line[:-1].split(' ')[3]) # set num_clauses
                    continue
                self.clauses.append(map(int, line[:-3].split(' '))) # set clauses

    def print_cnf(self):
        print(self.num_clauses)
        print(self.num_variables)
        print(self.clauses)
                

def combi(var):
    return list(product(*((x, -x) for x in var)))


class solver():
    def __init__(self, file_name=""):
        self.formula = cnf_formula(file_name)
        #self.formula.print_cnf()
        self.best_cost = None

    def all_combinations(self):
        random_solution = self.randomSolution(self.formula.num_variables)
        satisfiable=0
        for _ in range(MAX_TRIES):
            for var in random_solution:
                for clause in self.formula.clauses:
                    #print (clause, var)
                    if var in clause:
                        self.formula.clauses.remove(clause)
                        satisfiable += 1
                    if satisfiable == self.formula.num_clauses:
                        self.print_solution(random_solution)
        print("No solution found")

    def print_solution(self, solution):
        print("s SATISFIABLE")
        print("v %s 0"  %" ".join(map(str, solution)))
        exit(0)

    def randomSolution(self, num_variables):
        random_solution = [x for x in range(1, num_variables + 1)]
        for var in range(len(random_solution)):
            if random.random() < 0.5:
                random_solution[var] *= -1
        return random_solution

#Main

if __name__ == "__main__":

    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        print("\n Command: python %s <file_name.cnf> \n" %sys.argv[0])
        exit(0)

    solve = solver(file_name)
    solve.all_combinations()




