# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:06:10 2020

@author: Clement
"""
# Modules are imported
import os  
import random 
import matplotlib.pyplot as plt 
import numpy as np  



# We're about to run 10 times the stochastique
# dynamic of individuals starting at x = 4
# The decision matrix that was obtained previously shall be imported 
# to lead the similated individuals.
# The index line at the end of this matrix is of no use for the following part.
PATH = os.getcwd()
os.chdir(PATH)
print("Current Working Directory : ", os.getcwd())
mat_best_patch = np.loadtxt('decision_matrix.txt')
mat_best_patch = np.delete(mat_best_patch, (19), axis=0)





# Setting the parameters up.
# HORIZON is the number of time steps the individual shall go through.
X_MAX = 10
X_CRITICAL = 3
X_MIN = X_CRITICAL + 1
FORAGE_COST = 1
p_mortality = [0, 0.004, 0.02]
p_benefit = [1, 0.4, 0.6]
benefit = [0, 3, 5]
N_PATCH = 3
HORIZON = 15   
Output = np.zeros([HORIZON, X_MAX])
Time = list(range(1, HORIZON + 1))


# We set the seed in order to simulate steady results each time the program is run

#random.seed(41)  
for replicate in range(1, 11):   # 10 replicats
    X = 4
    for i in list(range(0, HORIZON)):  # 1 replicat --> 15 pas de temps
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
fig.suptitle('10 stockastic projections...')
ax1.plot(Time, Output[:, 1])
ax2.plot(Time, Output[:, 2])
ax3.plot(Time, Output[:, 3])
ax4.plot(Time, Output[:, 4])
ax5.plot(Time, Output[:, 5])
ax6.plot(Time, Output[:, 6])
ax7.plot(Time, Output[:, 7])
ax8.plot(Time, Output[:, 8])
ax9.plot(Time, Output[:, 9])
ax10.plot(Time, Output[:, 0])

