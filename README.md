# transportation_problem
Python module to solve transportation problems.

## Table of Contents
* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Requirements](#requirements)
  * [Installation](#installation)
* [Usage](#usage)
* [Contact](#contact)

## About the Project

There are many great algorithm out there to solve a transportation problems.
However, i started to write my own module to find a potential solution and get a better understanding in impementing
algorithms in code. I tried to orient myself to the content of Wolfgang Domschke.

## Getting Started

My goal is to release a simple python module to calculate potential and optimal solutions. So clone the tp.py to
your python library folder and get started.

### Requirements

* Python > 3.6
* numpy library
* math library

### Installation

Clone module in your python path.

## Usage

Import the module. Create an object with demand, supply and cost informations and call one method to find a solution.
At the moment you can only call the column minma(=cm_rule) rule or north west corner rule(=nwc_rule) to get an
transport matrix and total costs. 

## Example

```
import tp
import np

supply_vector = np.array([20, 40, 30])
demand_vector = np.array([20, 20, 20, 15, 15])
cost_matrix = np.array([[10, 15, 9, 13, 12],
                        [11, 30, 4, 13, 12],
                        [12, 13, 4, 1, 122]])
                        
problem = tp.Solver(supply_vector, demand_vector, cost_matrix)

matrix, costs = problem.nwc_rule()

print(matrix)
print(costs)

```

## Contact

Dominik
