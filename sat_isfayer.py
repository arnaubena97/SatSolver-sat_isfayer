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
        """File reader and parser the num of variables, num of clauses and put the clauses in a list"""
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
        """Constructor of the solver"""
        self.clauses = data.clauses
        self.num_variables = data.num_variables
        self.index_costs = []
        self.formula = []
        self.vars_positions = []
    
    def solve(self, max_tries = 50, max_flips=1000):
        """Solver based in walksat"""
        for _ in range(max_tries):
            self.formula = self.randomSolution()
            self.vars_positions = self.create_positions()
            self.index_costs = self.calculate_all_clauses_satisfy()
            for _ in range(max_flips):
                if 0 not in self.index_costs:
                    print_sol(self.formula)
                    return
                self.change_var()


    def change_var(self):
        """It is responsible for changing the variable that satisfies us more clauses"""
        clause_change = self.select_clause()
        best_cost = len(self.clauses) +1
        best_formula = []
        best_index_costs = []
        for variable in clause_change:
            new_index_costs = self.index_costs.copy()
            new_formula = self.formula.copy()
            new_formula[abs(variable) -1] = variable
            all_positions = self.vars_positions[variable] + self.vars_positions[-variable]

            for index in all_positions:
                satisfies = self.clause_satisfy(index, new_formula)
                new_index_costs[index] = satisfies

            cost = self.count_zero(new_index_costs)

            if cost < best_cost:
                best_cost = cost
                best_formula = new_formula.copy()
                best_index_costs = new_index_costs.copy()

        self.formula = best_formula.copy()
        self.index_costs = best_index_costs.copy()

    def select_clause(self):
        """Returns a randomly selected unsatisfied clause"""
        clauses_not_satisfied = []
        for index, value in enumerate(self.index_costs):
            if value == 0:
                clauses_not_satisfied.append(self.clauses[index])
        return clauses_not_satisfied[random.randint(0, len(clauses_not_satisfied) -1)]


    def count_zero(self, list_costs):
        """Returns the number of 0 that is in the list that 
           we pass by parameter"""
        count = 0
        for value in list_costs:
            if value == 0:
                count +=1
        return count

    def create_positions(self):
        """Return a list with the clause index that apear in the clauses.
           First position is empty, and the index of list is the variable.
        Ex: [ [], [2], [2, 3], ....] """
        vars_positions = [[]] * (self.num_variables*2 +1)
        for index, clause in enumerate(self.clauses):
            for var in clause:
                aux_list = []
                #print(var, len(vars_positions), self.num_variables)
                aux_list = vars_positions[var].copy()
                aux_list.append(index)
                vars_positions[var] = aux_list.copy()
        return vars_positions

    def randomSolution(self):
        """Create a random solution of cnf formula. Ex: [-1, 2, 3, -4, ...]"""
        random_solution = [x for x in range(1, self.num_variables + 1)]
        for var in range(len(random_solution)):
            if random.random() < 0.5:
                random_solution[var] = -random_solution[var]
        return random_solution

    def clause_satisfy(self, index, formula):
        """Retorna un entero, que es el numero de variables de 
           la formula que satisfacen la clausula que nos 
           indican con el index
           Ex: index = 1 --> cluse[1] = [1, -2, 3, ..] """
        satisfy = 0
        for variable in self.clauses[index]:
            if variable in formula:
                satisfy +=1
        return satisfy

    def calculate_all_clauses_satisfy(self):
        """Returns a list with the number of variables that 
           satisfy the clause with the same index.
           Method for all clauses.
           Ex: [1, 0, 2, 2] in test_0.cnf """
        index_satisfiable = []
        for clause in range(len(self.clauses)):
            number_sat = self.clause_satisfy(clause, self.formula)
            index_satisfiable.append(number_sat)
        return index_satisfiable

def print_sol(solution):
        """Method to print the solution that satisfies all the clauses """
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

    #Read the file
    data= read_file(file_name)
    #Create the solver
    solver = solver_walksat(data)
    #Solve
    solver.solve()


