# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 21:19:05 2020

@author: serva
"""
import numpy as np
import scipy.stats
#from scipy.stats import binom

def fitness(x_state, benefit_row_i, p_benefit_row_i, f_vectors):
    """ Computes the fitness of a hunter in specific pack size, knowing its state is x_state.

    Keyword arguments:
    x_state -- state of the hunter
    benefit_row_i -- State benefit for one hunter if it mades 0 to 4 kills with its pack of size i.
    p_benefit_row_i --  # Probability of killing 0 to 4 preys by a pack of size i
    f_vectors -- enables the calcultation of fitnesses at time t
                using the ones in time t+1
    """
    w_patch = 0
    x_store = x_state # Set x_state to Xstore to preserve value through loop
    for i_kill in range(0,4):
        x_state = x_store - COST + benefit_row_i[i_kill] # Calculate new state value
        x_state = min(x_state, X_MAX)
        x_state = max(x_state, X_CRITICAL)
        index = 1 + int((x_state - X_CRITICAL)/X_INC) # (arrondi en dessous)
        index = min(index, INDEX_MAX)

        qx = x_state - int(x_state) # qx for linear interpolation
        term1 = qx * f_vectors[index, 1]
        term2 = (1 - qx) * f_vectors[index-1, 1]
        w_patch = w_patch + p_benefit_row_i[i_kill] * (term1 + term2)
    return w_patch

def over_patches(x_state):
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
  

    n <- nrow(temp)- 2
    f_vectors = temp- Temp[1:n,]
    Store[Index,1:2] <- Temp[n+1,] # Save F(x,t,T) and best patch
    Store[Index,3] <- Temp[n+2,1] # 

    
    n <- nrow(Temp)-1
    F.vectors <- Temp[1:n,]
    Store[X,] <- Temp[n+1,] # Save F(x,t) and best patch
    } # End of X loop
  
  # Add Store values to end of F.vectors for pass back to main program
  Temp <- cbind(F.vectors, Store) # Combined by columns       


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
