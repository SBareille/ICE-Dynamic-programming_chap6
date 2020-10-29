# -*- coding: utf-8 -*-
""" 

Usage :
======
python C_pack hunting_interpolation.py
"""

__authors__ = ("BAREILLE Servane", "BOURGADE Clément", "PECHIERAS Florian", \
               "WOEHREL Aubin")
__contact__ = (" servane.bareille@etudiant.univ-rennes1.fr ", \
               " clement.bourgade@etudiant.univ-rennes1.fr ", \
               " florian.pechieras@etudiant.univ-rennes1.fr ", \
               " aubin.woerel@etudiant.univ-rennes1.fr ")
__copyright__ = " copyleft "
__date__ = "29/10/2020"

import numpy as np
import scipy.stats
#from scipy.stats import binom

def fitness(x_state, benefit_row_i, p_benefit_row_i, f_vectors):
    """ Computes the fitness of a hunter in specific pack size, knowing its state is x_state.

    Arguments:
    x_state -- state of the hunter
    benefit_row_i -- State benefit for one hunter if it mades 0 to 3 kills with its pack of size i.
    p_benefit_row_i --  Probability of killing 0 to 3 preys by a pack of size i
    f_vectors -- enables the calcultation of fitnesses at time t
                using the ones in time t+1
    """
    w_patch = 0
    x_store = x_state # Set x_state to Xstore to preserve value through loop
    for i_kill in range(0,4):
        x_state = x_store - COST + benefit_row_i[i_kill] # Calculate new state value
        x_state = min(x_state, X_MAX)
        x_state = max(x_state, X_CRITICAL)
        index = int((x_state - X_CRITICAL)/X_INC) # (arrondi en dessous)
        index = min(index, INDEX_MAX-1)

        qx = x_state - int(x_state) # qx for linear interpolation
        term1 = qx * f_vectors[index, 1]
        term2 = (1 - qx) * f_vectors[index, 1]
        w_patch = w_patch + p_benefit_row_i[i_kill] * (term1 + term2)
    return w_patch

def over_patches(x_state, f_vectors):
    """ scenario 3
    """
    
    """rhs = np.zeros([1, N_PATCH])  # Saves the fitnesses for the 3 patches
    for i in range(N_PATCH):
        rhs[0,i] = fitness(x_state, benefit[i,], p_benefit[i,], f_vectors)
    max(rhs)
    index = int((x_state - X_CRITICAL)/X_INC)
    index = min(index, INDEX_MAX)
    f_vectors[index, 0] = np.amax(rhs)
    #ok jusque là"""
    
    rhs = [0] * N_PATCH  # Saves the fitnesses for the 3 patches
    for i in range(N_PATCH):
        rhs[i] = fitness(x_state, benefit[i,], p_benefit[i,], f_vectors)
    index = int((x_state - X_CRITICAL)/X_INC)
    f_vectors[index, 0] = max(rhs)
    best_patch = rhs.index(max(rhs)) + 1

    rhs=np.asarray(rhs,dtype=np.float32)
    choice = 0
    if np.shape(np.where(rhs == max(rhs)))[1] > 1 :
        choice = 1 # vérifier si c'est time ou time-1 ou +1
    return [f_vectors[index, 0], best_patch, choice]


def over_states(time, mat_best_patch, fxtt, choices, f_vectors):
    for index in list(range(X_CRITICAL + 1, INDEX_MAX)):
        x_state = index * X_INC + X_CRITICAL # va bien de 1 à X_MAX
        temp = over_patches(x_state, f_vectors)
        fxtt[time, index] = temp[0]
        mat_best_patch[time, index] = temp[1]
        choices[time, index] = temp[2]
   
    """for index in list(range(2, INDEX_MAX + 1)):
        x_state = (index - 1) * X_INC + X_CRITICAL # va bien de 1 à X_MAX
        temp = over_patches(x_state, f_vectors)
        fxtt[time, x_state - 1] = temp[0]
        mat_best_patch[time, x_state - 1] = temp[1]
        choices[time, x_state - 1] = temp[2]"""


# Initialize parameters
X_MAX = 30 # Maximum value of X = gut capacity
X_CRITICAL = 0 # Value of X (gut content) at which death occurs
X_INC = 1 # Increment in state variable
INDEX_MAX = int((X_MAX - X_CRITICAL)/X_INC)# Maximum index value, floor (arondi en dessous)
N_PATCH = 4  # Number of patches = packs
COST = 6 # Daily food requirement

Y = 11.25 # Size of single prey
k = np.array([0,1,2,3]) # Number of kills
Pi = [0.15, 0.31, 0.33, 0.33]  # Probability of single kill for pack size
benefit = np.zeros([N_PATCH, len(k)])  # Rows = pack size + 1, Columns = number of kills
p_benefit = np.zeros([N_PATCH, len(k)])  # Probability of finding food in the 3 patches # Rows = pack size +1 , Columns = number of kills

for pack_size in range(1, 5) : # Iterate over pack sizes
    p_benefit[pack_size-1,:] = scipy.stats.binom.pmf(k, 3, Pi[pack_size-1]) # Calculate binomial probabilities using function dbinom
    benefit[pack_size-1, 1:4] = Y * k[1:4] / pack_size # Calculate benefits = amount per individual

HORIZON = 31  # Number of time steps


def main():
    """" ATTENTIONNNNN TROUVER NOM """
    # Initialisation of the f_vector matrix that enables the calcultation of
    # fitnesses at time t using the ones in time t+1.
    # In the second column we have fitnesses in time t+1 (used for calculation)
    # and in the first column the updated values of fitness in time t.
    # The survival at time = HORIZON is 1 for all state > X_CRITICAL
    # because we are only interested in individuals that are alive at the end
    # of the time period.
    f_vectors = np.zeros([INDEX_MAX + 1, 2])
    f_vectors[1:INDEX_MAX, 1] = 1

    # Initialisation of the best_patch and fxtt matrixes which keep for each
    # time and each state the best_patch to choose and the fitness associated.
    fxtt = np.zeros([HORIZON, INDEX_MAX + 1])
    mat_best_patch = np.zeros([HORIZON, INDEX_MAX + 1])
     # Matrix for flag indicating multiple equivalent choices. 0 = only one choice, 1 = more than one choice
    choices = np.zeros([HORIZON, INDEX_MAX + 1])

    # We go back in time from t=HORIZON, when individuals are alive, to t=1,
    # as we calculate fitness in time t thanks to the fitness in time t+1
    # For each time we calculate a lign of best_patches and fxtt,
    # and then pass the values of fitness into the second column of f_vector.
    for time in reversed(range(HORIZON)):
        over_states(time, mat_best_patch, fxtt, choices, f_vectors)
        f_vectors[:, 1] = np.matrix.copy(fxtt[time, :])
        # print(f_vectors)

    # Finally, we output the best_patch and fxtt matrixes after formating
    mat_best_patch[HORIZON - 1, :] = list(range(0, INDEX_MAX + 1))
    fxtt[HORIZON - 1, : ] = list(range(0, INDEX_MAX + 1))
    choices[HORIZON - 1, : ] = list(range(0, INDEX_MAX + 1))
    return(mat_best_patch, fxtt, choices)


if __name__ == "__main__":
    np.set_printoptions(precision=3, suppress=True)
    print(main()[0],"\n", main()[1],"\n", main()[2])