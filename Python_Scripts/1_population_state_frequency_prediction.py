# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:18:34 2020

@author: Home
"""
# Import of the modules.
import os
import numpy as np


# Setting the working directory.
PATH = os.getcwd()
os.chdir(PATH)
print("Current Working Directory :", os.getcwd())


# Import of the decision matrix that was created in the script \ 
# dynamic_programming_decision_matrix.py and output as a txt file.
mat_best_patch = np.loadtxt('decision_matrix.txt')


# Initialisation of the parameters.
X_MAX = 10 # Maximum state possible.
X_CRITICAL = 3  # State at which death occurs.
X_MIN = X_CRITICAL + 1  # Minimum viable state (if under this value : death).
FORAGE_COST = 1  # Cost of foraging.
N_PATCH = 3  # Type of patches.
TIME = 2  # Current time step for which we want the transition matrix.
p_mortality = [0, 0.004, 0.02]  # Probability of mortality for each patch.
p_benefit = [1, 0.4, 0.6]  # Probability of benefit for each patch.
benefit = [0, 3, 5]  # Benefit for each patch.
trans_density = np.zeros([X_MAX, X_MAX])  # Initialisation of the transition matrix.


#  Calculation the transition density for each state possible.
#  Each cell gives the probability, given that an animal is in state z at
#  time t − 1,  that by following the optimal behavior it moves into state x at time t.
#  For more details of the mathematical backgroung, see Roff, 2010 paragraphe 6.1.6

for x_etat1 in range(X_MIN, X_MAX + 1):
    K = int(mat_best_patch[TIME, x_etat1 - 1])
    x = min(x_etat1 - FORAGE_COST + benefit[K-1], X_MAX)
    trans_density[x_etat1 - 1, x - 1] = (1 - p_mortality[K - 1]) * p_benefit[K - 1]
    x = x_etat1 - FORAGE_COST
    if x > X_CRITICAL:
        trans_density[x_etat1 - 1, x - 1] = (1 - p_mortality[K - 1]) * (1 - p_benefit[K - 1])
        trans_density[x_etat1 - 1, X_CRITICAL - 1] = p_mortality[K - 1]
    else:
        trans_density[x_etat1 - 1, X_CRITICAL - 1]  = p_mortality[K - 1] + \
            (1 - p_mortality[K - 1]) * (1 - p_benefit[K - 1])
        
print(trans_density)
       
