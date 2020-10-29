# -*- coding: utf-8 -*-
""" The following program computes the transition matrix for a specific time.
Each cell of the transition matrix corresponds to the proportion
of individuals going from an initial state at time t (corresponds to a line)
to a final state at time t + 1 (corresponds to a column).

For more information and biological context,
check in advance the README.txt file of the github depository
and the script A0_dynamic_programming_decision_matrix.
"""

__authors__ = ("BAREILLE Servane", "BOURGADE Clément", "PECHIERAS Florian", \
               "WOEHREL Aubin")
__contact__ = (" servane.bareille@etudiant.univ-rennes1.fr ", \
               " clement.bourgade@etudiant.univ-rennes1.fr ", \
               " florian.pechieras@etudiant.univ-rennes1.fr ", \
               " aubin.woerel@etudiant.univ-rennes1.fr ")
__copyright__ = " copyleft "
__date__ = "22/10/2020"


# Import of the modules.
import os
import sys
import numpy as np

# Checks if the script A0 used as a module to compute the decision matrix
# is in the working directory. Imports it if its the case or sends an error
# if not.
if os.path.isfile(os.getcwd()+"\\A0_dynamic_programming_decision_matrix.py"):
    import A0_dynamic_programming_decision_matrix as ns
else :
    print("Please insert the A0_dynamic_programming_decision_matrix.py file" \
         " in your working directory or change the directory.")
    sys.exit()


# Importing the best patch matrix and putting three columns with zeros
# on the left to make indexes correspond easier with state values.
mat_best_patch = ns.main()[0]
mat_best_patch = np.concatenate((np.zeros([np.shape(mat_best_patch)[0],3]), \
                                 mat_best_patch), axis = 1)

# Initialization of parameters
X_MAX = 10  # Maximum possible state a forager can be in.
X_CRITICAL = 3  # State at which a forager dies.
X_MIN = X_CRITICAL + 1  # Minimum possible state for a forager to live in.
FORAGE_COST = 1  # Metabolic cost of foraging.
N_PATCH = 3  # Number of patches.
TIME = 2  # Current time step for which we want the transition matrix.
p_mortality = [0, 0.004, 0.02]  # Vector of death probabilities from a cause
                                # other than starvation, for each patch.
p_benefit = [1, 0.4, 0.6]  # Probability of finding food in each patch.
benefit = [0, 3, 5]  # Benefit if food is discovered, for each patch.

trans_density = np.zeros([X_MAX, X_MAX])  # Initialisation of the transition
                                          # matrix.


# Calculation the transition density for each state possible.
# Each cell gives the probability, given that an animal is in state z at
# time t − 1,  that by following the optimal behavior it moves into state
# x at time t.
# For more details of the mathematical backgroung,
# see Roff, 2010 paragraphe 6.1.6

for x_state1 in range(X_MIN, X_MAX + 1): # Looping over all state.
    K = int(mat_best_patch[TIME, x_state1 - 1]) # Choice of best patch.
    x = min(x_state1 - FORAGE_COST + benefit[K-1], X_MAX) # State if benefit.
    trans_density[x_state1 - 1, x - 1] = (1 - p_mortality[K - 1]) *\
        p_benefit[K - 1] # Output in transition matrix if benefit
    x = x_state1 - FORAGE_COST # State if no benefit.
    if x > X_CRITICAL & K != 1: # If individual is alive and patch != 1
                                # (condition necessary since the probability
                                # of benefit on patch 1 is equal to 1)
        trans_density[x_state1 - 1, x - 1] = (1 - p_mortality[K - 1]) *\
            (1 - p_benefit[K - 1]) # Output in transition matrix if no benefit
        trans_density[x_state1 - 1, X_CRITICAL - 1] = p_mortality[K - 1] # Dead
    else:
        trans_density[x_state1 - 1, X_CRITICAL - 1]  = p_mortality[K - 1] + \
            (1 - p_mortality[K - 1]) * (1 - p_benefit[K - 1])
print(trans_density)
