# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 10:34:34 2020

"""
# Import of the module numpy for using matrices 
import numpy as np

######################################################################################
####### Coeur du programme, utilisé par la suite pour les 5 autres scénarios #########
######################################################################################

def fitness(x_etat, i):
    """ Computes the fitness for a specific state and specific patch

    Keyword arguments:
    x_etat -- state of the animal
    i -- specific patch
    """
    x_food = x_etat - FORAGE_COST + benefit[i]
    x_food = min(x_food, X_MAX)
    x_food = max(x_food, X_CRITICAL)
    x_no_food = x_etat - FORAGE_COST
    x_no_food = max(x_no_food, X_CRITICAL)
    term1 = p_benefit[i] * f_vectors[x_food - 1, 1]
    term2 = (1 - p_benefit[i]) * f_vectors[x_no_food - 1, 1]
    w_patch = (1 - p_mortality[i]) * (term1 + term2)
    return w_patch

def over_patches(x_etat):
    """ Computes the best fitness over the possible patches for a specific state

    Keyword arguments:
    x_etat -- state of the animal
    """
    for i in range(N_PATCH):
        rhs[i] = fitness(x_etat, i)
    f_vectors[x_etat - 1, 0] = max(rhs)
    best_patch = rhs.index(max(rhs)) + 1
    return [f_vectors[x_etat - 1, 0], best_patch]

def over_states():
    """ Computes the vector of fitness and best patches for a specific time
    """
    for x_etat in list(range(X_MIN, X_MAX + 1)):
        temp = over_patches(x_etat)
        fxtt[time, x_etat - 1] = temp[0]
        mat_best_patch[time, x_etat - 1] = temp[1]

X_MAX = 10
X_CRITICAL = 3
X_MIN = X_CRITICAL + 1
CRIT_MAX_RANGE = list(range(X_CRITICAL, X_MAX))
FORAGE_COST = 1
N_PATCH = 3
HORIZON = 20
p_mortality = [0, 0.004, 0.02]
p_benefit = [1, 0.4, 0.6]
benefit = [0, 3, 5]
rhs = [0] * N_PATCH
# Initialisation of the f_vector matrix that helps making the steps
f_vectors = np.zeros([X_MAX, 2])
f_vectors[CRIT_MAX_RANGE, 1] = 1

fxtt = np.zeros([HORIZON, X_MAX])
mat_best_patch = np.zeros([HORIZON, X_MAX])

for time in reversed(range(HORIZON)):
    over_states()
    f_vectors[:, 1] = np.matrix.copy(fxtt[time, :])
mat_best_patch[HORIZON - 1, :] = list(range(1, X_MAX+1))
mat_best_patch = mat_best_patch[:, CRIT_MAX_RANGE]

fxtt[HORIZON - 1, : ] = list(range(1,X_MAX+1))
fxtt = fxtt[:, CRIT_MAX_RANGE]

print(mat_best_patch)
with np.printoptions(precision = 3):
    print(fxtt)
