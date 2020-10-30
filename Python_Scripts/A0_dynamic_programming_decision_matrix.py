# -*- coding: utf-8 -*-
""" The following program is based on the initial scenario of optimal foraging
from the 6th chapter of Roff, 2010.
Check the README.txt of the depository for more ecological context.

The main objective of this script is to compute a "decision matrix", given a
set of parameters that correspond to the biological context of the problem.
The decision matrix is simply a matrix with rows corresponding to time steps
and columns to the possible states in which an animal can be. Each matrix cell
(i.e. at a certain time step and a certain state) corresponds to the
identification number of the best patch an animal should choose if it wants to
maximise it's fitness (the final time step being the main goal).

The problem is solved using the principles of dynamic programming. Therefore,
the main objective, which is obtaining the decision matrix, is divided into
sub-problems. Algorithmically, each subproblem is translated into a function :

    function 'fitness' : The smallest sub-problem is to compute the fitness of
an animal if it forages on a specific patch (for a given time step and a given
state). In this specific problem, the fitness at a certain time step t is
computed based on the possible fitnesses of the time t+1. There is therefore
a need of knowing the final fitnesses to compute to whole decision matrix by
iterating backwards the computation of the fitnesses.

    function 'over_patches' : The second sub-problem is to choose the best
patch between all the patches the animal can choose from, at a certain time
step and in a certain state. The choice of the patch is based on the
maximization of the fitness.

    function 'over_states' : The third sub-problem is to obtain the best patch
for every state an animal can be in, for a specific time step.

The whole program therefore works as nested blocks : 'over_state' is iterated
for every time step and calls the function 'over_patches' that itself calls the
function 'fitness'.

Reference :
Roff, D. A. (2010). Modeling Evolution: an introduction to numerical methods.
Oxford University Press

Usage :
======
python A0_dynamic_programmming_decision_matrix.py
"""

__authors__ = ("BAREILLE Servane", "BOURGADE Clément", "PECHIERAS Florian", \
               "WOEHREL Aubin")
__contact__ = (" servane.bareille@etudiant.univ-rennes1.fr ", \
               " clement.bourgade@etudiant.univ-rennes1.fr ", \
               " florian.pechieras@etudiant.univ-rennes1.fr ", \
               " aubin.woerel@etudiant.univ-rennes1.fr ")
__copyright__ = " copyleft "
__date__ = "29/10/2020"


# Import of the modules
import os
import numpy as np

# Setting the working directory and printing it
PATH = os.getcwd()
os.chdir(PATH)
print("Current Working Directory :", os.getcwd(), "\n")



# Definition of the functions, each of one corresponding to a sub-problem.

def fitness(x_state, i, f_vectors):
    """ Computes the fitness of the foraging animal for a specific patch
    (in a specific state and at a specific time).

    Arguments:
    x_state -- state of the forager
    i -- patch identification number
    f_vectors -- temporary matrix that enables the computation of fitnesses
    at time t using the ones in time t+1

    Returns :
    w_patch -- the computated fitness for the specific patch
    """

    # First we calculate the possible states of a forager at the end of a time
    # step.
    # There are two possibilities : food was found or not.
    # In case food was found, the forager has a benefit corresponding to the
    # benefit of the patch.
    # The forager's state must be kept between X_CRITICAL
    # (if it reaches that value, the animal dies) and X_MAX.
    x_food = x_state - FORAGE_COST + benefit[i]
    x_food = min(x_food, X_MAX)
    x_food = max(x_food, X_CRITICAL)
    x_no_food = x_state - FORAGE_COST
    x_no_food = max(x_no_food, X_CRITICAL)


    # We then ponderate the fitnesses of the two possible states (at the time
    # step that follows the one we compute) with the probability of the
    # occurence of these states (thanks to p_benefit).
    # The values of fitnesses are contained in f_vectors.
    # The probability of dying from a cause other than starvation in the patch
    # is also taken into account as p_mortality.
    # The fitness of the patch is returned as w_patch.
    term1 = p_benefit[i] * f_vectors[x_food - 1, 1]
    term2 = (1 - p_benefit[i]) * f_vectors[x_no_food - 1, 1]
    w_patch = (1 - p_mortality[i]) * (term1 + term2)
    return w_patch

def over_patches(x_state, f_vectors):
    """ Computes the best fitness a forager can have (in a specific state
    and at a specific time) and gives the corresponding patch.

    Arguments:
    x_state -- state of the forager
    f_vectors -- temporary matrix that enables the computation of fitnesses
    at time t using the ones in time t+1

    Returns :
    1 - the best fitness
    2 - the associated best patch
    """
    # Loops over possible patches.
    # It registers the values of fitness for each patch in rhs.
    rhs = [0] * N_PATCH
    for i in range(N_PATCH):
        rhs[i] = fitness(x_state, i, f_vectors)

    # Assignes the best fitness value in f_vectors for x_state,
    # and the best patch associated in best_patch.
    f_vectors[x_state - 1, 0] = max(rhs)
    best_patch = rhs.index(max(rhs)) + 1
    return [f_vectors[x_state - 1, 0], best_patch]

def over_states(time, mat_best_patch, fxtt, f_vectors):
    """ Adds in the "best_patch" and "fxtt" matrixes the computed values
    corresponding to each state (at a specific time).

    Arguments:
    time -- time step of the fitnesses to compute
    mat_best_patch -- Matrix of best patch choices
    fxtt -- Matrix of associated best fitnesses
    f_vectors -- temporary matrix that enables the computation of fitnesses
    at time t using the ones in time t+1
    """
    for x_state in list(range(X_MIN, X_MAX + 1)):
        temp = over_patches(x_state, f_vectors)
        fxtt[time, x_state - 1] = temp[0]
        mat_best_patch[time, x_state - 1] = temp[1]


# Initialization of parameters
X_MAX = 10  # Maximum possible state a forager can be in.
X_CRITICAL = 3  # State at which a forager dies.
X_MIN = X_CRITICAL + 1  # Minimum possible state for a forager to live in.
FORAGE_COST = 1  # Metabolic cost of foraging.
N_PATCH = 3  # Number of patches.
HORIZON = 20  # Number of total time steps.
p_mortality = [0, 0.004, 0.02]  # Vector of death probabilities from a cause
                                # other than starvation, for each patch.
p_benefit = [1, 0.4, 0.6]  # Probability of finding food in each patch.
benefit = [0, 3, 5]  # Benefit if food is discovered, for each patch.

def main():
    """" Main function of the program. Computes the decision matrix and
    the associated best fitnesses """
    # Initialisation of the f_vector matrix that enables the calcultation of
    # fitnesses at time t using the ones in time t+1.
    # The second column corresponds to the fitnesses of time t+1 used for
    # the computation of the fitnesses of time t, updated in the first column.
    # The survival at time = HORIZON is arbitrarily assigned to 1 for
    # all states > X_CRITICAL because we are only interested in individuals
    # that are alive at the end of the time period.
    f_vectors = np.zeros([X_MAX, 2])
    f_vectors[list(range(X_CRITICAL, X_MAX)), 1] = 1

    # Initialisation of the best_patch and fxtt matrixes which keep for each
    # time and each state the best_patch to choose and the fitness associated.
    fxtt = np.zeros([HORIZON, X_MAX])
    mat_best_patch = np.zeros([HORIZON, X_MAX])

    # Going back in time from t=HORIZON, when individuals are alive, to t=1.
    # For each time step, over_state is called to compute the best patches
    # and fitnesses and then passes the new values of fitnesses
    # into the second column of f_vector.
    for time in reversed(range(HORIZON-1)):
        over_states(time, mat_best_patch, fxtt, f_vectors)
        f_vectors[:, 1] = np.matrix.copy(fxtt[time, :])

    # Output the mat_best_patch and fxtt matrixes after formating. The list of
    # values of states are given in the last line of each matrix for better
    # readability. The columns corresponding to the dead are deleted.
    mat_best_patch[HORIZON - 1, :] = list(range(1, X_MAX+1))
    mat_best_patch = mat_best_patch[:, list(range(X_CRITICAL, X_MAX))]
    fxtt[HORIZON - 1, : ] = list(range(1, X_MAX+1))
    fxtt = fxtt[:, list(range(X_CRITICAL, X_MAX))]
    return(mat_best_patch, fxtt)


# In case this script is run, prints the outputs of main()
if __name__ == "__main__":
    with np.printoptions(precision=3):
        print(main()[0], "\n\n", main()[1])
        