'''
SAT Solver description ..
'''
#Libraries

import sys
import random
import os
import time

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


class solver_walksat():
    def __init__(self, data):
        self.clauses = data.clauses
        self.num_variables = data.num_variables
        self.best_cost = 0
        self.index_costs = []
        self.formula = []
        self.clauses_not_sat = []
        #self.vars_positions = self.create_positions()
    
    def solve(self, max_tries = 20, max_flips=200):

        for _ in range(max_tries):
            self.formula = self.randomSolution()
            for _ in range(max_flips):
                self.index_costs = self.calculateIndexCosts()

                if 0 not in self.index_costs:
                    print_sol(self.formula)
                    return
                self.best_change()

    def best_change(self):
        vars_not_sat = []
        best_cost = len(self.clauses) +2
        new_formula = self.formula.copy()
        best_formula=[]

        for index, cost in enumerate(self.index_costs):
            if cost == 0:
                clause = self.clauses[index].copy()
                for var in clause:
                    vars_not_sat.append(var)

        for variable in vars_not_sat:
            new_formula = self.formula.copy()
            new_formula[abs(variable) -1] = variable
            list_costs = self.calculateIndexCosts()
            cost = self.count_zero(list_costs)
            if best_cost > cost:
                best_formula = new_formula.copy()
                best_cost = cost
        self.formula = best_formula.copy()
        return

    def create_positions(self):
        vars_positions = [[]] * (self.num_variables*2 +1)
        for index, clause in enumerate(self.clauses):
            for var in clause:
                aux_list = []
                aux_list = vars_positions[var].copy()
                aux_list.append(index)
                vars_positions[var] = aux_list.copy()
        return vars_positions

    def count_zero(self, costs):
        count = 0
        for value in costs:
            if value == 0:
                count +=1
        return count
 
    def randomSolution(self):
        """Create a random solution of cnf formula. Ex: [-1, 2, 3, -4, ...]"""
        random_solution = [x for x in range(1, self.num_variables + 1)]
        for var in range(len(random_solution)):
            if random.random() < 0.5:
                random_solution[var] = -random_solution[var]
        return random_solution

    def calculateIndexCosts(self):
        index_sat = []
        for clause in self.clauses:
            number_sat = 0
            for variable in self.formula:
                if variable in clause:
                    number_sat +=1
            index_sat.append(number_sat)
        return index_sat

def print_sol(solution):
        """Method to print the solution that satisfies the """
        print("s SATISFIABLE")
        print("v %s 0"  %" ".join(map(str, solution)))
        exit(0)

#Main

if __name__ == "__main__":
    temps_inici = time.time()
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        print("\n Command: python %s <file_name.cnf> \n" %sys.argv[0])
        exit(0)

    data= read_file(file_name)
    solver = solver_walksat(data)
    solver.solve()


