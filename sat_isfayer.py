'''
SAT Solver description ..
'''
#Libraries

import sys
import random
import os
import time

MAX_TRIES = 100000


class read_file(object):
    """Class to read and parse the file of CNF formula """

    def __init__(self, file_name=""):
        """Constructor of the read class"""
        self.num_variables = 0
        self.num_clauses = 0
        self.clauses = []
        if os.path.isfile(file_name): #comprove if the file exist
            self.read_file(file_name)
        else:
            print("Doesn't exist %s", file_name)
            exit(1)
    
    def read_file(self, file_name):
        """file reader and parser the num of variables, num of clauses and put the clauses in a list"""
        with open(file_name) as all_file:
            for line in all_file:
                if line.startswith('c'): continue #ignore comments
                if line.startswith('p'):
                    self.num_variables = int(line.split(' ')[2]) # set num_variables
                    self.num_clauses = int(line[:-1].split(' ')[3]) # set num_clauses
                    continue
                self.clauses.append(list(map(int, line[:-3].split(' ')))) # set clauses

    def print_cnf(self):
        """Print all variables of read_file class"""
        print(self.num_clauses)
        print(self.num_variables)
        print(self.clauses)
                

class solver():
    def __init__(self, data):
        self.data = data
        self.best_satisfa = 0
        self.best_solution = None

    def new_solve(self, max_restarts = 10, max_tries= 100, random_condition = 0.03):
        for _ in range(max_restarts):
            possible_solution = interpretations(self.data.num_variables)
            for _ in range(max_tries):
                if random.random() < random_condition:
                    possible_solution = possible_solution.get_random_walk()
                else:
                    possible_solution = possible_solution.get_best_child(self.data.clauses)
    
                if possible_solution.satisfiables(self.data.clauses) > self.best_satisfa:
                    self.best_solution = possible_solution.copyClass()
                    self.best_satisfa = possible_solution.satisfiables(self.data.clauses)
                    if self.best_satisfa == self.data.num_clauses: 
                        return self.best_solution, self.best_satisfa
        return self.best_solution, self.best_satisfa

class interpretations():

    def __init__(self, N):
        """Constructor of interpretation. Need one parameter, N is the number of variables
            of the cnf formula"""
        self.num_variables = N
        self.candidate = self.randomSolution(N)

    def randomSolution(self, num_variables):
        """Create a random solution of cnf formula. Ex: [-1, 2, 3, -4, ...]"""
        random_solution = [x for x in range(1, num_variables + 1)]
        for var in range(len(random_solution)):
            if random.random() < 0.5:
                random_solution[var] = -random_solution[var]
        return random_solution

    def satisfiables(self, clauses):
        """Returns the number of clauses satisfiables"""
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
        """Method to print the solution that satisfies the """
        print("s SATISFIABLE")
        print("v %s 0"  %" ".join(map(str, self.candidate)))
            
    def get_childs(self):
        childs = []
        for _ in range(self.num_variables):
            new_child = self.copyClass()
            value = random.randint(0, self.num_variables - 2)
            new_child.candidate[value] = -new_child.candidate[value]
            childs.append(new_child)
        return childs

    def get_random_walk(self):
        childs = self.get_childs()
        return childs[random.randint(0, len(childs) -1)]

    def copyClass(self):
        """Method to copy the class, not the reference"""

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
    temps_inici = time.time()
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        print("\n Command: python %s <file_name.cnf> \n" %sys.argv[0])
        exit(0)


    data= read_file(file_name)
    solve = solver(data)
    solution, cost = solve.new_solve()
    solution.print_solution()
    temps_final = time.time()
    print(str(cost) + "   temps: " + str(temps_final- temps_inici))
    exit(0)





