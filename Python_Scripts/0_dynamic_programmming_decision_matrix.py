# -*- coding: utf-8 -*-
""" Docstring d' une ligne dé crivant brièvement ce que fait le programme .

Usage :
======
python 0_dynamic_programmming_decision_matrix.py argument1 argument2

argument1 : un entier signifiant un truc
argument2 : une chaîne de caract è res dé crivant un bidule
"""

__authors__ = ("BAREILLE Servane", "BOURGADE Clément", "PECHIERAS Florian", "WOEHREL Aubin")
__contact__ = (" servane.bareille@etudiant.univ-rennes1.fr ", " clement.bourgade@etudiant.univ-rennes1.fr ", "etc." )
__copyright__ = " copyleft "
__date__ = "22/10/2020"


# Import the modules
import os 
import numpy as np

# Setting the working directory
PATH = os.getcwd()
os.chdir(PATH)
print("Current Working Directory :", os.getcwd())


# Save the decision matrix in txt file (to use in other scripts)
np.savetxt("decision_matrix.txt", mat_best_patch, fmt="%.0f")

#############################################################################
################################# Scenario 0 ################################
#############################################################################

def fitness(x_state, i):
    """ Computes the fitness (probability of surviving a time step) of a forager in one specific patch, knowing its previous state was x_state

    Keyword arguments:
    x_state -- state of the forager
    i -- specific patch
    """
    # First we calculate the possible states of a forger at the end of a time step .
    # There are two possibilities : food was found or not.
    # The forager's state must be kept between X_CRITICAL (in this case, the animal is dead), and X_MAX.
    x_food = x_state - FORAGE_COST + benefit[i]
    x_food = min(x_food, X_MAX)
    x_food = max(x_food, X_CRITICAL)
    x_no_food = x_etat - FORAGE_COST
    x_no_food = max(x_no_food, X_CRITICAL)
    
    # Now we give the probability of surviving in patch i knowing its previous state was x_state.
    # To do so we ponderate these two possibilities with the probability of their happening.
    # The probability of dying from a cause other than starvation in the patch is also taken into account.
    # It enables to create ponderate second column
    term1 = p_benefit[i] * f_vectors[x_food - 1, 1]
    term2 = (1 - p_benefit[i]) * f_vectors[x_no_food - 1, 1]
    w_patch = (1 - p_mortality[i]) * (term1 + term2)
    return w_patch

def over_patches(x_state):
    """ Computes the best fitness over the possible patches for a specific state.

    Keyword arguments:
    x_state -- state of the animal
    """
    for i in range(N_PATCH):
        rhs[i] = fitness(x_state, i)  # Cycle over patches ???????
    f_vectors[x_state - 1, 0] = max(rhs)
    best_patch = rhs.index(max(rhs)) + 1  # Concatenate F(x,t) and the optimal patch number
    return [f_vectors[x_state - 1, 0], best_patch]

def over_states():
    """ Computes the vector of fitness and best patches for a specific time.
    """
    for x_state in list(range(X_MIN, X_MAX + 1)):  # Iterate over states of X ????? Attention x critical ??
        temp = over_patches(x_state)
        fxtt[time, x_state - 1] = temp[0]
        mat_best_patch[time, x_state - 1] = temp[1]

# MAIN PROGRAM 
X_MAX = 10
X_CRITICAL = 3
X_MIN = X_CRITICAL + 1
FORAGE_COST = 1  # Metabolic cost to foraging per time step
N_PATCH = 3  # Number of patches
HORIZON = 20  # Number of time steps
p_mortality = [0, 0.004, 0.02]  # Probability to die from a cause other than starvation in the 3 different patches
p_benefit = [1, 0.4, 0.6]  # Probability of finding food in the 3 different patches
benefit = [0, 3, 5]  # State benefit if food is discovered for the 3 different patches
rhs = [0] * N_PATCH  # Preallocate Right Hand Side of equn ????
# Initialisation of the f_vector matrix that helps making the steps
f_vectors = np.zeros([X_MAX, 2])
f_vectors[list(range(X_CRITICAL, X_MAX)), 1] = 1

fxtt = np.zeros([HORIZON, X_MAX])
mat_best_patch = np.zeros([HORIZON, X_MAX])

for time in reversed(range(HORIZON)):
    over_states()
    f_vectors[:, 1] = np.matrix.copy(fxtt[time, :])
mat_best_patch[HORIZON - 1, :] = list(range(1, X_MAX+1))
mat_best_patch = mat_best_patch[:, list(range(X_CRITICAL, X_MAX))]

fxtt[HORIZON - 1, : ] = list(range(1, X_MAX+1))  #Creates a matrix.....
fxtt = fxtt[:, list(range(X_CRITICAL, X_MAX))]  # Output information. For display add states (¼wts) to last row of matrices

print(mat_best_patch)  # Prints Decision matrix.
with np.printoptions(precision = 3):
    print(fxtt)  # Prints Fxt of Decision matrix: 3 sig places.
