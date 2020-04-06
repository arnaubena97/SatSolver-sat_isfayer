
import sys
import random

def read_file(file_name):
    """File reader and parser the num of variables, num of clauses and put the clauses in a list"""
    clauses =[]
    with open(file_name) as all_file:
        for line in all_file:
            if line.startswith('c'): continue #ignore comments
            if line.startswith('p'):
                num_variables = int(line.split(' ')[2]) # set num_variables
                continue
            clauses.append(list(map(int, line[:-3].split(' ')))) # set clauses
    return num_variables, clauses

def print_sol(solution):
    """Method to print the solution that satisfies all the clauses """
    print("s SATISFIABLE")
    print("v %s 0"  %" ".join(map(str, solution)))
    exit(0)

class walksat_solver():

    def __init__(self, clauses, num_variables):
        """Constructor of the solver"""
        self.clauses = clauses
        self.num_variables = num_variables
        self.formula=[]
        self.list_positions = self.create_positions()
        self.index_clauses_satisfied = []

    def randomSolution(self):
        """Create a random solution of cnf formula. Ex: [-1, 2, 3, -4, ...]"""
        random_formula = [x if random.random() < 0.5 else -x for x in range(self.num_variables + 1)]
        return random_formula[1:]

    def create_positions(self):
        """Return a list with the clause index that apear in the clauses.
           First position is empty, and the index of list is the variable.
        Ex: [ [], [2], [2, 3], ....] """
        vars_positions = [[] for _ in range(self.num_variables * 2 + 1)]
        for index, clause in enumerate(self.clauses):
            for var in clause:
                vars_positions[var].append(index)
        return vars_positions

    def calculate_all_clauses_satisfy(self):
        """Returns a list with the number of variables that
           satisfy the clause with the same index.
           Method for all clauses.
           Ex: [1, 0, 2, 2] in test_0.cnf """
        list_variables_satisfies = []
        for clause in range(len(self.clauses)):
            number_sat = self.clause_satisfy(clause)
            list_variables_satisfies.append(number_sat)
        return list_variables_satisfies

    def clause_satisfy(self, index):
        """Returns an integer, which is the number of
           variables in the formula that satisfy the
           clause indicated by the index.
           Ex: index = 1 --> cluse[1] = [1, -2, 3, ..] """
        satisfy = 0
        for variable in self.clauses[index]:
            if variable in self.formula:
                satisfy += 1
        return satisfy

    def select_all_unsatisfied(self):
        """Returns a list of indexes whose clause
           is not satisfied."""
        clauses_not_satisfied = []
        for index, value in enumerate(self.index_clauses_satisfied):
            if value == 0:
                clauses_not_satisfied.append(index)
        return clauses_not_satisfied

    def get_clause_unsatisfied(self, list_all_unsatisfied):
        """Returns a randomly selected unsatisfied clause"""
        return self.clauses[random.choice(list_all_unsatisfied)]

    def update(self, variable, x):
        """It is responsible for updating the list of
           the number of variables that satisfy the clause"""
        for index in self.list_positions[x * variable]:
            self.index_clauses_satisfied[index] += x

    def change_variable(self, clause_to_review):
        """Is responsible for assessing which is
           the best variable in the clause to change"""

        worst_wrong = sys.maxsize
        bests_variables = []
        for variable in clause_to_review:
            wrong = 0
            for index in self.list_positions[-variable]:
                if not self.index_clauses_satisfied[index] > 1:
                    wrong += 1
            if wrong <= worst_wrong:
                worst_wrong = wrong
                bests_variables.append(variable)

        return random.choice(bests_variables)

    def solve(self, max_tries=50, max_flips=3000):
        """Implementation of the solver"""
        for _ in range(max_tries):
            self.formula = self.randomSolution()
            self.index_clauses_satisfied = self.calculate_all_clauses_satisfy()
            for _ in range(max_flips):

                index_all_unsatisfied = self.select_all_unsatisfied()
                if len(index_all_unsatisfied)==0:
                    print_sol(self.formula)

                clause_to_review = self.get_clause_unsatisfied(index_all_unsatisfied)
                variable = self.change_variable(clause_to_review)
                self.update(variable, 1)
                self.update(variable, -1)
                self.formula[abs(variable)-1] *= -1

#Main
if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        print("\n Command: python %s <file_name.cnf> \n" %sys.argv[0])
        exit(0)

    num_variables, clauses = read_file(file_name)
    sat = walksat_solver(clauses, num_variables)
    sat.solve()
    exit(0)