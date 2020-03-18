# SAT_isfayer

## Table of contents
* [General info](#general-info)
* [Requirements](#Requirements)
* [Generate formula](#Generate formula)
* [Run solver](#Run solver)

## General info

Project based on developing a completed/partial SAT Solver. This is a implementation of a WalkSAT Solver.
	
## Requirements
Project is created with:
* Python 3.6

## Generate formula
To create a CNF formula correctly, we will use:

```bash
$ python rnd-cnf-gen.py <num-vars> <num-clauses> <clause-length> [<random-seed>]
```
If we want to save the formula in a .cnf file we will put: ```> file.cnf``` at the end of the command

## Run solver
To run this SAT Solver, execute the next command:

```bash
$ python3.6 sat_isfayer <name_test.cnf>
```

## License
To see license: [MIT](https://choosealicense.com/licenses/mit/)