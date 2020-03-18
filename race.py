#!/usr/bin/python3

# Libraries

import sys
import os
import glob
import re
import stat
import subprocess

out_file = "out.txt" # Solver output
limits_file = "tmp-limits.sh" # Limits script file
timeout = 10 # Timeout for each run
inc_to = 2 # Multiplier for timeout
inc_bug = 10000 # Multiplier for bug

# Parse CPU time in file
def get_time(out_file):
    time = None
    r = re.compile(r"^user (\d+\.\d+)")
    for l in open(out_file, "r"):
        s = re.search(r, l)
        if s:
            time = s.group(1)
            break
    return time

# Parse SATISFIABLE in file
def get_sat(out_file):
    r = re.compile(r"^s SATISFIABLE")
    for l in open(out_file, "r"):
        s = re.search(r, l)
        if s:
            return True
    return False

# Parse solver solution in file
def get_solution(out_file):
    r = re.compile(r"^v (.+)")
    for l in open(out_file, "r"):
        s = re.search(r, l)
        if s:
            sol = s.group(1).split()
            sol.insert(0, "0") # Adds a 0 at the begginig to make variable 'i' at potition 'i'
            try:
                return list(map(int, sol))
            except:
                return None
            break
    return None

# Check if the solution is a real solution to the benchmark file
def check_solution(solution, benchmark_file):
    instance = open(benchmark_file, "r")
    for l in instance:
        if l[0] in ["c", "p"]: # Pass comments and program line
            continue
        sl = list(map(int, l.split()))
        sl.pop() # Remove last 0
        length = len(sl)
        for lit in sl:
            if lit == solution[abs(lit)]: # Satisfies clause
                break
            else:
                length -= 1
        if length == 0: # Falsified clause
            return False
    return True

# Check the correctness of the solution
def check_correctness(benchmark_file, out_file):
    sat = get_sat(out_file)
    if sat:
        solution = get_solution(out_file)
        if solution != None:
            return check_solution(solution, benchmark_file)
    return None

if __name__ == '__main__' :

    if len(sys.argv) != 3:
        sys.exit("Use: %s <benchmark_folder> <solver>")

    benchmark_folder = sys.argv[1]
    solver = sys.argv[2]

    # Check benchmark folder and solver
    if os.path.isdir(benchmark_folder):
        benchmark_folder = os.path.abspath(benchmark_folder)
    else:
        sys.exit("ERROR: Benchmark folder not found (%s)." % benchmark_folder)

    if os.path.isfile(solver):
        solver = os.path.abspath(solver)
    else:
        sys.exit("ERROR: Solver not found (%s)." % solver)

    # Check solver
    if not (os.stat(solver).st_mode & stat.S_IXUSR):
        sys.exit("ERROR: Solver %s without execute (x) permission." % solver)
    #Create file limits.sh
    with open(limits_file, "w") as f:
        f.write("#!/bin/bash\nulimit -t %i\n$1 $2\n" % timeout)
    st = os.stat(limits_file)
    os.chmod(limits_file, st.st_mode | stat.S_IXUSR)

    # Get all the instances
    benchmark_files = glob.glob("%s/*.cnf" % benchmark_folder)
    if not benchmark_files:
        sys.exit("ERROR: Benchmark files in \"%s/*.cnf\" not found." % benchmark_folder)
    benchmark_files.sort()
    total_time = 0
    # Run the solver for al the instances
    for bf in benchmark_files:
        sys.stdout.write("File %s... " % os.path.basename(bf))
        sys.stdout.flush()
        # Run the solver under limits
        with open(out_file, 'w') as output:
            subprocess.run(['time', '-p', './%s' % limits_file, solver, bf], stdout = output, stderr = subprocess.STDOUT)
        #Check result
        correct = check_correctness(bf, out_file)
        if correct == True: # The solution is correct
            #Get Time
            time = get_time(out_file)
            if time == None: # This should not happend
                time = timeout * inc_to
                sys.stdout.write("Time not found! time = %.2f\n" % time)
            else:
                time = float(time)
                sys.stdout.write("OK! time = %.2f\n" % time)
        elif correct == None: # There is no solution
            time = timeout * inc_to
            sys.stdout.write("No solution found! time = %i\n" % time)
        elif correct == False: # There is a bug in the solution
            time = timeout * inc_bug
            sys.stdout.write("Wrong solution! time = %i\n" % time)
        total_time += time
        sys.stdout.write("Current time = %.2f\n" % total_time)
    # Remove temp files
    os.system("rm %s" % out_file)
    os.system("rm %s" % limits_file)

    # Results
    sys.stdout.write("Total time = %.2f\n" % total_time)
