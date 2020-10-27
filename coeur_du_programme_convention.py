# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 23:17:56 2020

@author: aubin
"""
import numpy as np

######################################################################################
####### Coeur du programme, utilisé par la suite pour les 5 autres scénarios #########
######################################################################################

def fitness(x_etat,i):
    """ Computes the fitness for a specific state and specific patch

    Keyword arguments:
    x_etat -- state of the animal
    i -- specific patch
    """
    x_food = x_etat - FORAGE_COST + benefit[i] # State in patch if forager finds food 
    x_food = min(x_food, X_MAX)
    x_food = max(x_food, X_CRITICAL)
    x_no_food = x_etat - FORAGE_COST
    x_no_food = max(x_no_food,X_CRITICAL)
    term1 = p_benefit[i] * f_vectors[x_food-1,1]
    term2 = (1-p_benefit[i]) * f_vectors[x_no_food-1,1]
    w_patch = (1-p_mortality[i]) * (term1+term2)
    return w_patch

def over_patches(x_etat):
    """ Computes the best fitness over the possible patches for a specific
    state

    Keyword arguments:
    x_etat -- state of the animal
    """
    for i in range(N_PATCH):
        rhs[i] = fitness(x_etat,i)
    f_vectors1 = np.matrix.copy(f_vectors)
    f_vectors1[x_etat-1,0] = max(rhs)
    best_patch = rhs.index(max(rhs)) + 1
    mat_temp = np.append(f_vectors1,[[f_vectors1[x_etat-1,0],best_patch]],axis=0)
    return mat_temp

def over_states():
    """ Computes the vector of fitness and best patches for a specific time
    """
    temp_store = np.zeros([X_MAX,2]) "crée Matrice avec X_max lignes avec deux colonnes de zéros"
    for x_etat in list(range(X_MIN,X_MAX+1)):
        mat_temp = over_patches(x_etat)
        temp_store[x_etat-1,] = np.matrix.copy(mat_temp[X_MAX,])
        mat_temp = mat_temp[list(range(X_MAX)),]
    return temp_store

X_MAX = 10
X_CRITICAL = 3
X_MIN = X_CRITICAL + 1
FORAGE_COST = 1
N_PATCH = 3
HORIZON = 20
p_mortality = [0, 0.004, 0.02]
p_benefit = [1, 0.4, 0.6]
benefit = [0, 3, 5]
rhs = [0]*N_PATCH
# Initialisation of the f_vector matrix that helps making the steps
f_vectors = np.zeros([X_MAX,2])
f_vectors[list(range(X_CRITICAL,X_MAX)),1] = 1

fxtt = np.zeros([HORIZON,X_MAX])
mat_best_patch = np.zeros([HORIZON,X_MAX])

TIME = HORIZON

while TIME > 1:
    TIME -= 1
    mat_temp1 = over_states()
    mat_best_patch[TIME,:] = np.matrix.copy(mat_temp1[:,1])
    fxtt[TIME,:] = np.matrix.copy(mat_temp1[:,0])
    f_vectors[:,1] = np.matrix.copy(mat_temp1[:,0])
mat_best_patch = np.append(mat_best_patch,[list(range(1,X_MAX+1))],axis=0)
mat_best_patch = mat_best_patch[:,list(range(X_CRITICAL,X_MAX))]
mat_best_patch = mat_best_patch[list(range(1,HORIZON+1)),:]
fxtt = np.append(fxtt,[list(range(1,X_MAX+1))],axis=0)
fxtt = fxtt[:,list(range(X_CRITICAL,X_MAX))]
fxtt = fxtt[list(range(1,HORIZON+1)),:]

print(mat_best_patch)
with np.printoptions(precision=3):
    print(fxtt)
