# -*- coding: utf-8 -*-
""" Computes a matrix that gives, for each time step, the best patch to choose
in order to optimize the fitness of an individual

Usage :
======
python dynamic_programmming_decision_matrix.py
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
import numpy as np

# Setting the working directory
PATH = os.getcwd()
os.chdir(PATH)
print("Current Working Directory :", os.getcwd())


# FONCTION DEFINITIONS
def fitness(x_state, i, f_vectors):
    """ Computes the fitness (probability of surviving a time step)
    of a forager in one specific patch, knowing its state is x_state.

    Arguments:
    x_state -- state of the forager
    i -- specific patch
    f_vectors -- enables the calcultation of fitnesses at time t
                using the ones in time t+1

    Returns w_patch -- the fitness calculated
    """
    # First we calculate the possible states of a forager at the end of a time
    # step.
    # There are two possibilities : food was found or not.
    # The forager's state must be kept between X_CRITICAL
    # (in this case, the animal is dead), and X_MAX.
    x_food = x_state - FORAGE_COST + benefit[i]
    x_food = min(x_food, X_MAX)
    x_food = max(x_food, X_CRITICAL)
    x_no_food = x_state - FORAGE_COST
    x_no_food = max(x_no_food, X_CRITICAL)

    # Now we give the probability of surviving in patch i
    # knowing its previous state was x_state.
    # To do so we ponderate the two possible states
    # with the probability of their happening.
    # The probability of dying from a cause other than starvation in the patch
    # is also taken into account.
    # It enables to create ponderate second column
    term1 = p_benefit[i] * f_vectors[x_food - 1, 1]
    term2 = (1 - p_benefit[i]) * f_vectors[x_no_food - 1, 1]
    w_patch = (1 - p_mortality[i]) * (term1 + term2)
    return w_patch

def over_patches(x_state, f_vectors):
    """ Computes the best fitness over the possible patches
    for a specific state and a specific time.

    Arguments:
    x_state -- state of the animal
    rhs -- store the fitnesses for the 3 patches at a specific time
    f_vectors -- enables the calcultation of fitnesses at time t
                using the ones in time t+1

    Returns the best fitness and the associated best patch.
    """
    # The function loops over all 3 patches.
    # It registers the value of fitness for each patch in rhs.
    # Then it assignes the best fitness value in f_vectors for x_state,
    # and the best patch associated in best_patch.
    rhs = [0] * N_PATCH  # Saves the fitnesses for the 3 patches
    for i in range(N_PATCH):
        rhs[i] = fitness(x_state, i, f_vectors)
    f_vectors[x_state - 1, 0] = max(rhs)
    best_patch = rhs.index(max(rhs)) + 1
    return [f_vectors[x_state - 1, 0], best_patch]

def over_states(time, mat_best_patch, fxtt, f_vectors):
    """ Add in the best_patch and fxtt matrixes the calculated values
    for each State in a specific time.

    Arguments:
    time
    mat_best_patch -- stores the patch choice for each state value of each time
    fxtt -- stores the associated fitness for each state value of each time
    """
    for x_state in list(range(X_MIN, X_MAX + 1)):
        temp = over_patches(x_state, f_vectors)
        fxtt[time, x_state - 1] = temp[0]
        mat_best_patch[time, x_state - 1] = temp[1]

# MAIN PROGRAM
# Initialize parameters
X_MAX = 10 # Maximal state for a forager
X_CRITICAL = 3 # Minimal state for a forager (in this case it is dead)
X_MIN = X_CRITICAL + 1 # Minimal living state
FORAGE_COST = 1  # Metabolic cost to foraging per time step
N_PATCH = 3  # Number of patches
HORIZON = 20  # Number of time steps
p_mortality = [0, 0.004, 0.02]  # Probability to die from a cause other than
                                # starvation in the 3 patches
p_benefit = [1, 0.4, 0.6]  # Probability of finding food in the 3 patches
benefit = [0, 3, 5]  # State benefit if food is discovered for the 3 patches 

def main():
    """" ATTENTIONNNNN TROUVER NOM """
    # Initialisation of the f_vector matrix that enables the calcultation of
    # fitnesses at time t using the ones in time t+1.
    # In the second column we have fitnesses in time t+1 (used for calculation)
    # and in the first column the updated values of fitness in time t.
    # The survival at time = HORIZON is 1 for all state > X_CRITICAL
    # because we are only interested in individuals that are alive at the end
    # of the time period.
    f_vectors = np.zeros([X_MAX, 2])
    f_vectors[list(range(X_CRITICAL, X_MAX)), 1] = 1

    # Initialisation of the best_patch and fxtt matrixes which keep for each
    # time and each state the best_patch to choose and the fitness associated.
    fxtt = np.zeros([HORIZON, X_MAX])
    mat_best_patch = np.zeros([HORIZON, X_MAX])

    # We go back in time from t=HORIZON, when individuals are alive, to t=1,
    # as we calculate fitness in time t thanks to the fitness in time t+1
    # For each time we calculate a lign of best_patches and fxtt,
    # and then pass the values of fitness into the second column of f_vector.
    for time in reversed(range(HORIZON)):
        over_states(time, mat_best_patch, fxtt, f_vectors)
        f_vectors[:, 1] = np.matrix.copy(fxtt[time, :])

    # Finally, we output the best_patch and fxtt matrixes after formating
    mat_best_patch[HORIZON - 1, :] = list(range(1, X_MAX+1))
    mat_best_patch = mat_best_patch[:, list(range(X_CRITICAL, X_MAX))]
    print(__name__)
    fxtt[HORIZON - 1, : ] = list(range(1, X_MAX+1))
    fxtt = fxtt[:, list(range(X_CRITICAL, X_MAX))]
    return(mat_best_patch, fxtt)

if __name__ == "__main__":
    with np.printoptions(precision=3):
        print(main())
        
