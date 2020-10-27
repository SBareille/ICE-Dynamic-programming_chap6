# Import of the module numpy for using matrices 
import os
import numpy as np
import random

def over_patches():
    Best_clutch = [0] * N_PATCH
    Clutch = range(1, int(Index))
    W = P_SURVIVAL * (1 - sum(P_BENEFIT)) * F_vectors[Index,1]
    for i in range(Npatch):
        W_partial = Benefit[range(1,int(Index)), i] + P_SURVIVAL * F.vectors[Index-Clutch-1,1]
        Best = W_partial.sort(reverse = TRUE)
        Best_clutch[i] = Best[0]
        W += p_benefit[i] * max(W.partial)
        if((len(W.partial>1)) and (W.partial[Best[0]] == W.partial[Best[1]])):
            print("Several possible equal choices")
    F_vectors[Index - 1, 0] = W
    Temp = (F_vectors[Index - 1, 0], Best_Clutch[HOST_TYPE])
    F_vectors.append(Temp)
    return(F_vectors)

def over_states():
    for i in range(1, int(MAX_INDEX)):
        X = (Index - 1) * X_INC + X_CRITICAL
        Temp = over_patches()
        D = Temp[-1,:]
        del(Temp[-1,:])
        F_vectors = np.transpose(Temp)
        np.c_[F_vectors, D]
    return(F_vectors)

X_MAX = 40
X_CRITICAL = 0
X_INC = 1
N_PATCH = 4
p_benefit = [0.05, 0.05, 0.1, 0.8]
P_SURVIVAL = 0.99
MAX_INDEX = 1 + (X_MAX - X_CRITICAL)/X_INC
##INDEX = range(1,int(MAX_INDEX) + 1)
Index = 1 + (X - X_CRITICAL)/X_INC
F_vectors = np.zeros((int(MAX_INDEX), 2))
Clutch = range(X_MAX + 1)
Benefit = np.zeros((X_MAX + 1, 4))
SHM = [9, 12, 14, 23]
HORIZON = 21
Best_patch = np.zeros((HORIZON, int(MAX_INDEX)))

HOST_TYPE = 1

host_coef = np.zeros((4,4))
host_coef[0,:] = [-0.2302, 2.7021, -0.2044, 0.0039]
host_coef[1,:] = [-0.1444, 2.2997, -0.1170, 0.0013]
host_coef[2,:] = [-0.1048, 2.2097, -0.0878, 0.0004222]
host_coef[3,:] = [-0.0524, 2.0394, -0.0339, -0.0003111]

def main():
    for i in range(4):
        Benefit[:, i] = host_coef[i, 0] + hist_coef[i, 1] * Clutch + host_coef[i, 2] * Clutch**2 + host_coef[i, 3] * Clutch**3
    Benefit[0,:] = 0
    Time = HORIZON
    while Time > 1:
        Time -= 1
        Temp = over_states()
        TempF = Temp[:,3]
        for j in range(1, int(MAX_INDEX) + 1):
            F_vectors[j, 1] = TempF[j, 0]
        Best_patch[Time, :] = Temp[:, 3]
        FxtT[Time, :] = Temp[:, 2]
    Best_patch[HORIZON, :] = (Index - 1) * X_INC + X_CRITICAL
    FxtT[HORIZON, :] = (Index - 1) * X_INC + X_CRITICAL
    print(Best_patch[:, range(1, int(MAX_INDEX) + 1)])
    with np.printoptions(precision = 3):
        print(FxtT[:, range(int(MAX_INDEX) + 1)])
    
        #plot en 3D, google est ton ami
    y = Best_patch[HORIZON, range(1, int(MAX_INDEX) + 1)]
    x = range(HORIZON)
    return()
    
HostType = 1
Output1 = "OVOPOSITION1.txt"
Output2 = "DM1.txt"
main()

## Idem pour l'hôte n°2
HostType = 2
Output1 = "OVOPOSITION2.txt"
Output2 = "DM2.txt"
main()

## Idem pour l'hôte n°3
HostType = 3
Output1 = "OVOPOSITION3.txt"
Output2 = "DM3.txt"
main()

## Idem pour l'hôte n°4
HostType = 4
Output1 = "OVOPOSITION4.txt"
Output2 = "DM4.txt"
main()