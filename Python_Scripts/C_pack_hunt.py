# -*- coding: utf-8 -*-
""" The following program computes the "decision matrix" of the third
scenario of chapter 6 in Roff, 2010.
Check the README.txt of the depository for more ecological context.

The main objective of this script is to compute a "decision matrix", given a
set of parameters that corresponds to the biological context of the problem.
The decision matrix is simply a matrix with rows corresponding to time steps
and columns to the possible states in which an animal can be. Each matrix cell
(i.e. at a certain time step and a certain state) corresponds to the
identification number of the best patch an animal should choose if it wants to
maximise its fitness (the final time step being the main goal).

In this specific scenario, the problem is to know for a Lion if it should 
hunt in a pack or not in order to maximize its fitness, depending on
its gut content (the state of the animal) and the time step.
Therefore, in this context, the patch corresponds to the size of the pack
(from 1 to 4 animals).

Since values of gut content could be continuous and not discrete,
an interpolation method is implemented to obtain values of fitness depending
on the values of the closest precedent fitnesses.
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
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
#from scipy.stats import binom

def fitness(x_state, benefit_row_i, p_benefit_row_i, f_vectors):
    """ Computes the fitness of a hunter (i.e. a Lion) in a specific pack size, 
    knowing its gut content value is x_state.
    
    Arguments:
    x_state -- state of the hunter, i.e. its gut content value
    benefit_row_i -- List of state benefits (gut content benefits) 
                     for a hunter for each possible number of prey 
                     kills (0 to 3) when the size of the pack is 'i'.
    p_benefit_row_i -- Probability of killing 0 to 3 preys by a pack of size i
    f_vectors -- enables the calculation of fitnesses at time t
                using the ones in time t+1
    """
    w_patch = 0 # Initilisation of the fitness variable.
    x_store = x_state # Set x_state to Xstore to preserve value through loop.
    for i_kill in range(0,4): # Loops over the possible number of prey kills.
        x_state = x_store - COST + benefit_row_i[i_kill] # New state value.
        x_state = min(x_state, X_MAX) # Caps x_state to X_MAX value.
        x_state = max(x_state, X_CRITICAL) # x_state can't be under X_CRITICAL.
        
        # Index corresponding to the column number of the matrix for a specific 
        # state value. We use this index since in this scenario the value of 
        # the state does not necessarly correspond to the value of the column.
        index = int((x_state - X_CRITICAL)/X_INC) 
        index = min(index, INDEX_MAX-1)
        
        # Qx  used for linear interpolation. See Roff, 2010 for more details 
        # on the interpolation method.
        qx = x_state - int(x_state) 
        term1 = qx * f_vectors[index, 1]
        term2 = (1 - qx) * f_vectors[index, 1]
        
        # Interpolated value of fitness corresponds to Term1 + Term2 and is 
        # multiplied by the probability of benefit for the i_kill number 
        # of preys killed.
        w_patch = w_patch + p_benefit_row_i[i_kill] * (term1 + term2)
    return w_patch

def over_patches(x_state, f_vectors):
    """ Computes the best fitness a hunter can have (in a specific state
    and at a specific time) and gives the corresponding patch.

    Arguments:
    x_state -- state of the hunter
    f_vectors -- temporary matrix that enables the computation of fitnesses
    at time t using the ones in time t + 1.
    Returns :
    1 - the best fitness
    2 - the associated best patch
    3 - the value 1 if there is a choice or 0 if not
    """

    rhs = [0] * N_PATCH  # Saves the fitnesses of every patch (size of pack).
    for i in range(N_PATCH): 
        rhs[i] = fitness(x_state, benefit[i,], p_benefit[i,], f_vectors)
    index = int((x_state - X_CRITICAL)/X_INC)
    # Saving the best value of fitness as the new fitness value and the 
    # associated best patch value.
    f_vectors[index, 0] = max(rhs)
    best_patch = rhs.index(max(rhs)) + 1 

    # Test if the animal can make a choice, i.e. that two sizes of packs give 
    # a same value of fitness.
    rhs = np.asarray(rhs,dtype=np.float32) 
    choice = 0
    if np.shape(np.where(rhs == max(rhs)))[1] > 1 : # Existence of a choice.
        choice = 1
    return [f_vectors[index, 0], best_patch, choice]


def over_states(time, mat_best_patch, fxtt, choices, f_vectors):
    """ Adds in the "best_patch", "fxtt" and "choice" matrixes the computed 
    values corresponding to each state (at a specific time).

    Arguments:
    time -- time step of the fitnesses to compute
    mat_best_patch -- Matrix of best patch choices
    fxtt -- Matrix of associated best fitnesses
    choices -- Matrix of existence of possible choice
    f_vectors -- temporary matrix that enables the computation of fitnesses
    at time t using the ones in time t+1
    """
    # Loops over all possible state values.
    for index in list(range(X_CRITICAL + 1, INDEX_MAX)): 
        x_state = index * X_INC + X_CRITICAL 
        temp = over_patches(x_state, f_vectors)
        fxtt[time, index] = temp[0]
        mat_best_patch[time, index] = temp[1]
        choices[time, index] = temp[2]


# Initialization of parameters
X_MAX = 30 # Maximum value of X = maximum gut capacity.
X_CRITICAL = 0 # Value of X (gut content) at which death occurs.
X_INC = 1 # Incrementing value of state variable.
INDEX_MAX = int((X_MAX - X_CRITICAL)/X_INC) # Maximum index value (floored)
N_PATCH = 4  # Number of patches, i.e. number of possible packs
COST = 6 # Daily food requirement.

Y = 11.25 # Size of a single prey.
k = np.array([0,1,2,3]) # Number of kills per size of pack.
Pi = [0.15, 0.31, 0.33, 0.33]  # Probability of single kill for pack size.
benefit = np.zeros([N_PATCH, len(k)])  # Rows = pack size + 1, Columns = number of kills.
p_benefit = np.zeros([N_PATCH, len(k)])  # Probability of finding food in the 3 patches # Rows = pack size +1 , Columns = number of kills

for pack_size in range(1, 5) : # Iterate over pack sizes
    p_benefit[pack_size-1,:] = scipy.stats.binom.pmf(k, 3, Pi[pack_size-1]) # Calculate binomial probabilities using function dbinom
    benefit[pack_size-1, 1:4] = Y * k[1:4] / pack_size # Calculate benefits = amount per individual
HORIZON = 31  # Number of time steps


def main():
    """ Main function of the program. Computes the decision matrix,
    the associated best fitnesses, and the matrix of existence of choice"""
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
    a,b,c = main()
    print(a,"\n", b,"\n", c)
    
    plt.clf()
    fig = plt.figure()
    
    plt.subplot(1,3,1)
    im = plt.imshow(main()[0], cmap = 'gray', vmin = 1, vmax = 4)
    plt.colorbar(im, orientation = 'horizontal')
    
    plt.subplot(1,3,2)
    im2 = plt.imshow(main()[1], cmap = 'gray', vmin = 0, vmax = 1)
    plt.colorbar(im2, orientation = 'horizontal')
    
    plt.subplot(1,3,3)
    im3 = plt.imshow(main()[2], cmap = 'gray', vmin = 0, vmax = 1)
    plt.colorbar(im3, orientation = 'horizontal')

    plt.show()
