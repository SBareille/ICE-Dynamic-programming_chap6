# -*- coding: utf-8 -*-
""" Simulates the stochastic dynamic of 10 individuals starting at x = 4

Usage :
======
python A1_individual_prediction.py
"""

__authors__ = ("BAREILLE Servane", "BOURGADE Clément", "PECHIERAS Florian", \
               "WOEHREL Aubin")
__contact__ = (" servane.bareille@etudiant.univ-rennes1.fr ", \
               " clement.bourgade@etudiant.univ-rennes1.fr ", \
               " florian.pechieras@etudiant.univ-rennes1.fr ", \
               " aubin.woerel@etudiant.univ-rennes1.fr ")
__copyright__ = " copyleft "
__date__ = "22/10/2020"


# Import the modules
import os  
import random 
import matplotlib.pyplot as plt 
import numpy as np
import A0_dynamic_programming_decision_matrix as ns


# The decision matrix that was obtained previously shall be imported 
# frrom the ns module to lead the similated individuals.
# The index line at the end of this matrix is of no use for the following part.
PATH = os.getcwd()
os.chdir(PATH)
print("Current Working Directory : ", os.getcwd())
mat_best_patch = ns.main()[0]
mat_best_patch = np.delete(mat_best_patch, (19), axis=0)

# Initialize parameters
X_MAX = 10 # Maximal state for a forager
X_CRITICAL = 3 # Minimal state for a forager (in this case it is dead)
X_MIN = X_CRITICAL + 1 # Minimal living state
FORAGE_COST = 1  # Metabolic cost to foraging per time step
N_PATCH = 3  # Number of patches
HORIZON = 15  # Number of time steps
p_mortality = [0, 0.004, 0.02]  # Probability to die from a cause other than
                                # starvation in the 3 patches
p_benefit = [1, 0.4, 0.6]  # Probability of finding food in the 3 patches
benefit = [0, 3, 5]  # State benefit if food is discovered for the 3 patches 

Output = np.zeros([HORIZON, X_MAX])

# We set the seed in order to simulate steady results each time the program is run
random.seed(7)

for replicate in range(1, 11):   # 10 replicats
    X = 4
    for i in range(0, HORIZON):  # 1 replicat --> 15 pas de temps
        if X > X_CRITICAL:
            patch = int(mat_best_patch[i, X - 4])
            if random.random() < p_mortality[patch - 1]:
                print("Replicate", replicate, "Dead from predator\n")
                X = 0
                Output[i, replicate-1] = patch
            else:     # si il a pas clamsé, alors on continue, sinon on met son X à 0
                INDEX = 0
                if random.random() < p_benefit[patch - 1]:
                    INDEX = 1
                X = X - FORAGE_COST + benefit[patch - 1] * INDEX
                X = min(X, X_MAX)
                if X < X_MIN:
                    print("Replicate", replicate, "Dead from starvation\n")
                Output[i, replicate-1] = patch

# This part is used to make a graphic output.
# First a subdivised plot is created, then it is filled with the simulations 
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
