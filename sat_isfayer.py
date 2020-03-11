#!/usr/bin/python3
'''
SAT Solver description ..
'''
#Libraries

import sys
import random
import os
import time

MAX_TRIES = 100000


class parser_file(object):
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
                


class solver():
    def __init__(self, file_name=""):
        self.formula = parser_file(file_name)
        self.best_satisfa = 0
        self.best_solution = None

    def all_combinations(self):
        
        for _ in range(MAX_TRIES):
            satisfiable=0
            random_solution = interpretations(self.formula.num_variables)
            aux_clauses = self.copy(self.formula.clauses)
            flag = False
            for clause in aux_clauses:
                count_fail = 0
                for var in random_solution.candidate:
                    if var in clause:
                        #aux_clauses.remove(clause)
                        satisfiable += 1
                        #print(var, clause, satisfiable)
                        if satisfiable == self.formula.num_clauses:
                            return random_solution
                        break
                    else:
                        count_fail+=1
                        if count_fail == self.formula.num_variables: flag = True 
                if flag: break
                    
        print("No solution found")


    def copy(self, list):
        """Copy the values of this instance of the class Interpretation to another instance"""
        c = [x for x in list]
        return c

    def new_solve(self, max_restarts = 10, max_tries= 100, random_condition = 0.03):
        for _ in range(max_restarts):
            possible_solution = interpretations(self.formula.num_variables)
            for _ in range(max_tries):
                if random.random() < random_condition:
                    possible_solution = possible_solution.get_random_walk()

                else:
                    possible_solution = possible_solution.get_best_child(self.formula.clauses)
    
                if possible_solution.satisfiables(self.formula.clauses) > self.best_satisfa:
                    self.best_solution = possible_solution.copyClass()
                    self.best_satisfa = possible_solution.satisfiables(self.formula.clauses)
                    if self.best_satisfa == self.formula.num_clauses: 
                        return self.best_solution, self.best_satisfa
        return self.best_solution, self.best_satisfa



class interpretations():
    def __init__(self, N):
        self.num_variables = N
        self.candidate = self.randomSolution(N)


    def randomSolution(self, num_variables):
        random_solution = [x for x in range(1, num_variables + 1)]
        for var in range(len(random_solution)):
            if random.random() < 0.5:
                random_solution[var] *= -1
        return random_solution

    def satisfiables(self, clauses):
        num_satisfa = 0
        flag = False
        for clause in clauses:
            count_fail = 0
            for var in self.candidate:
                if var in clause:
                    num_satisfa += 1
                    if num_satisfa == len(clauses):
                        return num_satisfa
                    break
                else:
                    count_fail+=1
                    if count_fail == self.num_variables: flag = True 
            if flag: break

        return num_satisfa
                
    def print_solution(self):
        print("s SATISFIABLE")
        print("v %s 0"  %" ".join(map(str, self.candidate)))
            
    def get_childs(self):
        childs = []
        for i in range(self.num_variables):
            new_child = self.copyClass()
            value = random.randint(0, self.num_variables - 2)
            new_child.candidate[value] = -1 * new_child.candidate[value]
            childs.append(new_child)
        return childs

    def get_random_walk(self):
        childs = self.get_childs()
        return childs[random.randint(0, len(childs) -1)]

    def copyClass(self):

        c = interpretations(self.num_variables)
        c.candidate = [x for x in self.candidate]
        return c

    def get_best_child(self, clauses):
        childs = self.get_childs()
        best_child = 0
        best_cost = 0
        for num_child, child in enumerate(childs):
            if child.satisfiables(clauses) >= best_cost:
                best_child = num_child
                best_cost = child.satisfiables(clauses)
        return childs[best_child]

#Main

if __name__ == "__main__":

    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        print("\n Command: python %s <file_name.cnf> \n" %sys.argv[0])
        exit(0)


    # temps_inici = time.time()
    # solve = solver(file_name)
    # solution = solve.all_combinations()
    # temps_final= time.time()
    # solution.print_solution()
    # print("temps:" + str(temps_final- temps_inici))
    

    temps_inici = time.time()
    solve = solver(file_name)
    solution, cost = solve.new_solve()
    temps_final= time.time()
    solution.print_solution()
    print(str(cost) + "   temps:" + str(temps_final- temps_inici))
    exit(0)





