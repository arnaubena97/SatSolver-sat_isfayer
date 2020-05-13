# SAT_isfayer

## Table of contents
* [General info](#general-info)
* [Requirements](#Requirements)
* [Partial SAT Solver](#Partial-SAT-Solver)
* [Complete SAT Solver](#Complete-SAT-Solver)
* [Generate CNF formula](#Generate-CNF-formula)
* [Contributors](#Contributors)
* [License](#License)



## General info

Project based on developing a partial and complete SAT Solver.
These two SAT Solver are two assignments of the Advanced IA subject

## Requirements
Project is created with:
* Python 3.6

## Partial SAT Solver

The partial SAT Solver is based on Walk SAT which is a local search algorithm.
 This is able to know if there is an interpretation that satisfies the formula 
 introduced in CNF but it may be that he is looking for an interpretation indefinitely since he cannot know if the uninduced formula does not have any interpretation that satisfies it.

To run this SAT Solver, execute the next command in the folder of the SAT:

```bash
$ python3.6 sat_isfayer <name_test.cnf>
```

You can see our implementation in the local_search folder or click [hear](https://github.com/arnaubena97/sat_isfayer/tree/master/local_search)

## Complete SAT Solver

The complete SAT Solver are based in DPLL SAT.(update information)

To run this SAT Solver, execute the next command in the folder of the SAT:

```bash
$ python3.6 sat_isfayer_pro <name_test.cnf>
```

You can see our implementation in the complete_search folder or click [hear](https://github.com/arnaubena97/sat_isfayer/tree/master/complete_search)


## Generate CNF formula

In the folder [bench_sat](https://github.com/arnaubena97/sat_isfayer/tree/master/bench_sat) 
there is a file called *rnd-cnf-gen.py* and its function is o create a CNF formula correctly, we will use a random generator. 
They generates a correct CNF formula and prints it on terminal but if
 you want to save the formula in a .cnf file we will put: ```> name_test.cnf``` at the end of the command.
 It is important that the file format is ".cnf"
 To use this random generator, put this in your terminal:

```bash
$ python rnd-cnf-gen.py <num-vars> <num-clauses> <clause-length> [<random-seed>]
```


##Contributors
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/arnaubena97"><img src="https://avatars0.githubusercontent.com/u/10574631?s=460&v=4" width="100px;" alt=""/><br /><sub><b>Arnau Benavides</b></sub></a></td>
    <td align="center"><a href="https://github.com/Albert1703"><img src="https://avatars3.githubusercontent.com/u/26384877?s=460&v=4" width="100px;" alt=""/><br /><sub><b>Albert Roca</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/ricardPlana"><img src="https://avatars1.githubusercontent.com/u/38788944?s=400&u=ac4e767f356cdce3c1f60d5b04540729a120fef0&v=4" width="100px;" alt=""/><br /><sub><b>Ricard Plana</b></sub></a><br /></td>

  </tr>
 </table>
<!-- ALL-CONTRIBUTORS-LIST:END -->

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)