#!/usr/bin/python3
'''
SAT Solver description ..
'''
#Libraries

import sys
import random
import os



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
                if line.startswith('p'): continue #ignore numer of clauses and variables
                self.clauses.append(map(int, line[:-3].split(' ')))

    def print_cnf(self):

        # print(self.num_clauses)
        # print(self.num_variables)
        
        print(self.clauses)
                

        




#Main

if __name__ == "__main__":

    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        print("Command: python %s <file_name.cnf>", sys.argv[0])
        exit(0)

    cnf = cnf_formula(file_name)
    cnf.print_cnf()



