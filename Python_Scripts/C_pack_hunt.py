# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 21:19:05 2020

@author: serva
"""
import numpy as np
import scipy.stats
#from scipy.stats import binom

def fitness():
    """ scenario 3"""
    w_patch = 0
    x_store = x # Set X to Xstore to preserve value through loop
    for i_kill in range(1,5):
        x = x_store - COST + BENEFIT[i_kill] # Calculate new state value
        x = min(x, X_MAX)
        x = max(x, X_CRITICAL)
        index = 1 + int((x - X_CRITICAL)/X_INC) # (arrondi en dessous)
        index = min(index, INDEX_MAX) 
        
        qx = x - int(x) # qx for linear interpolation
        term1 = qx * f_vectors[index, 1]
        term2 = (1 - qx) * f_vectors[index-1, 1]
        w_patch = w_patch + p_benefit[i_kill] * (term1 + term2)
    return w_patch

def over_patches():
    """ scenario 3
    """
    rhs = np.zeros([1, N_PATCH])  # Saves the fitnesses for the 3 patches
    for i in range(N_PATCH):
        rhs[i] = fitness()
    max(rhs)
    index = 1 + int((x - X_CRITICAL)/X_INC)
    # index = min(index, INDEX_MAX)

    f_vectors1 = np.matrix.copy(f_vectors)
    f_vectors1[index - 1,0] = max(rhs)
    best_patch = rhs.index(max(rhs)) + 1
    mat_temp = np.append(f_vectors1,[[f_vectors1[index - 1,0],best_patch]],axis=0)

    # il semble que pour opti on puisse faire : 
    # f_vectors[index - 1, 0] = max(rhs)
    # best_patch = rhs.index(max(rhs)) + 1
    
    if len(np.where(max(rhs)) > 1 :
        choices[time,] = [1,1] # vérifier si c'est time ou time-1 ou +1

    # return [f_vectors[index - 1, 0], best_patch] # si opti
    return mat_temp


def over_states():
    for index in list(range(2, INDEX_MAX + 1)):
        x = (index - 1) * X_INC + X_CRITICAL
        temp = over_patches()
        #fxtt[time, x_state - 1] = temp[0]
        #mat_best_patch[time, x_state - 1] = temp[1]
    
    return mat_temp
  


# Initialize parameters
X_MAX = 30 # Maximum value of X = gut capacity
X_CRITICAL = 0 # Value of X (gut content) at which death occurs
X_INC = 0.33 # Increment in state variable
INDEX_MAX = 1 + int((X_MAX - X_CRITICAL)/X_INC)# Maximum index value, floor (arondi en dessous)
N_PATCH = 4  # Number of patches = packs
COST = 6 # Daily food requirement

Y = 11.25 # Size of single prey
k = np.array([0,1,2,3]) # Number of kills
Pi = [0.15, 0.31, 0.33, 0.33]  # Probability of single kill for pack size
benefit = np.zeros([N_PATCH, len(k)])  
p_benefit = np.zeros([N_PATCH, len(k)])  # Probability of finding food in the 3 patches

for pack_size in range(1, 5) : # Iterate over pack sizes
    p_benefit[pack_size-1,:] = scipy.stats.binom.pmf(k, 3, Pi[pack_size-1]) # Calculate binomial probabilities using function dbinom
    benefit[pack_size-1, 1:4] = Y * k[1:4] / pack_size # Calculate benefits = amount per individual

HORIZON = 31  # Number of time steps

f_vectors = np.zeros([INDEX_MAX, 2])
f_vectors[1:INDEX_MAX, 1] = 1
fxtt = np.zeros([HORIZON, INDEX_MAX])
mat_best_patch = np.zeros([HORIZON, INDEX_MAX])
choices = np.zeros([HORIZON, INDEX_MAX]) # Matrix for flag indicating multiple equivalent choices. 0 = only one choice, 1 = more than one choice
