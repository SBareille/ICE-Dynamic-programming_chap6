# -*- coding: utf-8 -*-
""" The following program simulates the stochastic dynamic of 10 individuals
starting out at a state x = 4. For more information and biological context,
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


# Import of the modules
import os
import sys
import random
import matplotlib.pyplot as plt
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


# The decision matrix that is needed for the individual simulations
# is computed thanks to the ns module.
# The index line at the end of this matrix is of no use for the following part
# and is therefore deleted.
mat_best_patch = ns.main()[0]
mat_best_patch = np.delete(mat_best_patch, (19), axis=0)

# Initialization of parameters
X_MAX = 10  # Maximum possible state a forager can be in.
X_CRITICAL = 3  # State at which a forager dies.
X_MIN = X_CRITICAL + 1  # Minimum possible state for a forager to live in.
FORAGE_COST = 1  # Metabolic cost of foraging.
N_PATCH = 3  # Number of patches.
HORIZON = 15  # Number of total time steps for simulations.
p_mortality = [0, 0.004, 0.02]  # Vector of death probabilities from a cause
                                # other than starvation, for each patch.
p_benefit = [1, 0.4, 0.6]  # Probability of finding food in each patch.
benefit = [0, 3, 5]  # Benefit if food is discovered, for each patch.

Output = np.zeros([HORIZON, X_MAX])

# We set the seed in order to simulate steady results each time the
# program is run.
random.seed(7)

# 10 replicates corresponding to 10 simulations (ie individuals) are done.
# Each individual starts at the state 4. For each individual, a loop is made
# over the total number of time steps. At each time step, the patch to forage
# on is chosen from the decision matrix and the new state value is computed.
# The value depends on if the animal gets the benefit or not.
for replicate in range(1, 11): # Individual simulations.
    X = 4 # Initial state of the forager.
    for i in range(0, HORIZON):  # Time steps.
        if X > X_CRITICAL: # If the animal is still alive.
            patch = int(mat_best_patch[i, X - 4]) # The best patch is chosen.
            if random.random() < p_mortality[patch - 1]: # If animal dies.
                print("Replicate", replicate, "Dead from predator\n")
                X = 0
                Output[i, replicate-1] = patch
            else:     # If animal doesn't die.
                INDEX = 0
                if random.random() < p_benefit[patch - 1]: # If animal
                                                           # gets the benefit.
                    INDEX = 1
                X = X - FORAGE_COST + benefit[patch - 1] * INDEX # New state.
                X = min(X, X_MAX)
                if X < X_MIN:
                    print("Replicate", replicate, "Dead from starvation\n")
                Output[i, replicate-1] = patch

# This part is used to make a graphic output.
# First a subdivised plot is created, then it is filled with the simulation
# records one by one.
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8), (ax9, ax10)) \
    = plt.subplots(5, 2, sharex=True, sharey=True)
fig.suptitle('10 stochastic projections...')
Time = list(range(1, HORIZON + 1))
ax1.plot(Time, Output[:, 0])
ax2.plot(Time, Output[:, 1])
ax3.plot(Time, Output[:, 2])
ax4.plot(Time, Output[:, 3])
ax5.plot(Time, Output[:, 4])
ax6.plot(Time, Output[:, 5])
ax7.plot(Time, Output[:, 6])
ax8.plot(Time, Output[:, 7])
ax9.plot(Time, Output[:, 8])
ax10.plot(Time, Output[:, 9])
