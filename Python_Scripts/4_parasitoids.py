# Import of the module numpy for using matrices 
import os
import numpy as np
import random

def over_patches(X):
    Best_clutch = [0] * N_PATCH
    Index = [1 + int((X - X_CRITICAL)/X_INC)] * int(1 + (X - X_CRITICAL)/X_INC)
    clutch = list(range(1, int(Index[0])))
    W = P_SURVIVAL * (1 - sum(p_benefit)) * F_vectors[int(Index[0]),1]
    for i in range(N_PATCH):
        W_partial = list(Benefit[range(1,int(Index[0]) + 1), i] + P_SURVIVAL * F_vectors[list(np.array(Index)-np.array(clutch)),1])
        Best = sorted(range(len(W_partial)), key=lambda i:W_partial[i]) # sorting list W_partial by indices (not the values)
        Best_clutch[i] = Best[0]
        W += p_benefit[i] * max(W_partial)
        if((len(W_partial)>1) and (W_partial[Best[0]] == W_partial[Best[1]])):
            print("Several possible equal choices")
    F_vectors[int(Index[0]) - 1, 0] = W
    Temp = (F_vectors[int(Index[0]) - 1, 0], Best_clutch[HOST_TYPE - 1])
    F_vectors.append(Temp)
    return(F_vectors)

def over_states():
    for i in range(2, int(MAX_INDEX) + 1):
        X = (i - 1) * X_INC + X_CRITICAL
        Temp = over_patches(X)
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
F_vectors = np.zeros((int(MAX_INDEX), 2))
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

def main(HostType, Output1, Output2):
    Clutch = list(range(X_MAX + 1))
    for i in range(X_MAX + 1):
        for j in range(4):
            Benefit[i, j] = host_coef[j, 0] + host_coef[j, 1] * Clutch[i] + host_coef[j, 2] * Clutch[i]**2 + host_coef[j, 3] * Clutch[i]**3
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
    
    y = Best_patch[HORIZON, range(1, int(MAX_INDEX) + 1)]
    x = range(HORIZON)
    #plot en 3D, google est ton ami
    ovip = cbind(x, Best.Patch[range(int(HORIZON) -1),40])
    ovip = t(ovip)
    np.savetxt(Output1, ovip, fmt="%.0f")
# Enregistrement des matrices de décision pour chaque type d'hôte
    bpatch = Best.Patch[range(int(HORIZON) -1),range(1,41)]
    bpatch = t(bpatch)
    np.savetxt(Output2, bpatch, fmt="%.0f")
    return()
    
HostType = 1
Output1 = "OVOPOSITION1.txt"
Output2 = "DM1.txt"
main(HostType, Output1, Output2)

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


########################################
#### Partie prédiction individuelle ####
########################################

rm(list = ls()) # Remove all objects from memory
Xmax <- 40
# Maximum value of X = eggs
DM1 = read.table(file = "DM1.txt") # Cols = x rows = time
DM2 <- read.table(file = "DM2.txt")
DM3 <- read.table(file = "DM3.txt")
DM4 <- read.table(file = "DM4.txt")
# Create an array for Decision matrix

DM <- array(0,c(20,Xmax,4)) # time, state, host
for (i in 1:20) {
  for (j in 1:Xmax) {
    DM[i,j,1] <- DM1[i,j]
    DM[i,j,2] <- DM2[i,j]
    DM[i,j,3] <- DM3[i,j]
    DM[i,j,4] <- DM4[i,j]
  }
}

# Probability of encountering host type
Pbenefit <- c(0.05, 0.05, 0.1, 0.8)
Times <- c(5,5,10,80) 
Host.Type <- c(rep(1,Times[1]),rep(2,Times[2]),rep(3,Times[3]), rep(4,Times[4])) # Create Vector for Host type probability
Psurvival <- 0.99 # Survival probability per time increment
Horizon <- 10 # Number of time steps
set.seed(10) # Initialise random number generator
N.Ind <- 1000 # Number of individuals
Output <- matrix(0,N.Ind,Horizon) # Allocate space for output
# Generate initial values of x from normal distribution
x.init <- ceiling(rnorm(N.Ind, mean = 20, sd = 5))

for (Ind in 1:N.Ind) { # Iterate over individuals
  # Generate vectors for choosing the Host type and probability of survival
  Host <- ceiling(100*runif(Horizon)) # Vector of host types
  Survival <- runif(Horizon) # Vector of survival probabilities
  Survival[Survival>Psurvival] <- 0 # Set all values of Survival > Psurvival = 0
  Survival[Survival!=0] <- 1 # Set all other values to 1
  x <- x.init[Ind] # Initial value of x
  
  for (Time in 1:Horizon){ # Iterate over time periods
    if(x>0) { # If eggs remaining calculate clutch size using DM
      Clutch.Size <- DM[Time,x,Host.Type[Host[Time]]]
      Output[Ind,Time] <- Clutch.Size # Store clutch size
      # Compute new value of x
      x <- x - Clutch.Size
    }
    x <- x*Survival[Time] # Set x = 0 if female does not survive
  } # end of Time loop
} # End of Ind loop

par(mfcol = c(5,2)) # Set graphics page to 5 rows and 2 columns
# Iterate over time and plot bar graphs of clutch size
for (i in 1:10 ){
  Data <-Output[,i]
  Data <- Data[Data>0] # Eliminate zeroes
  xbar <- mean(Data) # Mean clutch size
  
  print(c(i, mean(Data))) # Time, Output mean clutch size
  Data <- table(Data) # Tabulate data
  # Plot data using a bar graph, because x is integral
  barplot(Data, xlab = "Clutch Size", space = 0, xlim = c(0,5), main = paste("Time =",i), col = 1)
}
