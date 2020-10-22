############################################################
#### Scénario 4 : choix des hôtes chez les parasitoides ####
############################################################

setwd("~/Etudes/Rennes1/S3/ICE/Projet/Scripts/ScriptsR")

rm(list = ls()) # Remove all objects from memory


# Function to iterate over patches i.e. over Hosts
OVER.PATCHES <- function(X, F.vectors, Xcritical, Xmax, Xinc, Npatch, Benefit, Pbenefit, Psurvival, HostType) {
  # Create matrix for storing best clutch size for each host type
  Best.Clutch <- matrix(0,Npatch)
  Index <- 1+(X-Xcritical)/Xinc # Index for X is X+1
  # Vector of clutch sizes to Index - 1
  Clutch <- seq(from = 1, to = Index-1)
  # Start fitness accumulation with component for case of not finding a host
  W <- Psurvival*(1-sum(Pbenefit))*F.vectors[Index,2]
  
  for (i in 1:Npatch) { # Cycle over patches  = Hosts
    # Calculate "partial" fitness, W.partial for each clutch size
    W.partial <- Benefit[2:Index,i]+Psurvival*F.vectors[Index-Clutch,2]
    # Find largest W.partial and hence best clutch size
    Best <- order(W.partial, na.last = TRUE, decreasing = TRUE)
    Best.Clutch[i] <- Best[1] # Store value of best clutch for host i
    # Increment fitness
    W <- W + Pbenefit[i]*W.partial[Best[1]]
    # Test for several equal optimal choices
    # Only examine W.partial that contain more than one entry
    if((length(W.partial)>1) & (W.partial[Best[1]] == W.partial[Best[2]])) {
      print("Several possible equal choices")
    }
  } # End of i loop
  
  F.vectors[Index,1] <- W
  # Update F(x,t)
  # Concatenate F(x,t,T) and the optimal clutch values for host type 
  Temp <- c(F.vectors[Index,1], Best.Clutch[HostType])
  # Add Temp to bottom of F.vectors and rename to Temp
  Temp <- rbind(F.vectors, Temp)
  return (Temp)
} # End of function

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
# Function to iterate over states of X
OVER.STATES <- function(F.vectors, Xcritical, Xmax, Xinc, Npatch, Benefit, Pbenefit, Psurvival, Max.Index, HostType) {
  
  Store <- matrix(0,Max.Index,2) # Create matrix for output
  
  for (Index in 2:Max.Index) { # Iterate over states of X
    # For given X call Over.Patches to determine F(x,t,T) and best patch
    X <- (Index - 1)*Xinc+Xcritical
    Temp <- OVER.PATCHES(X, F.vectors, Xcritical, Xmax, Xinc, Npatch, Benefit, Pbenefit, Psurvival, HostType)
    # Extract components. Last row is F(x,t) and best clutch size for host 2
    n <- nrow(Temp)-1
    F.vectors <- Temp[1:n,]
    Store[Index,] <- Temp[n+1,] # Save F(x,t,T) and best clutch size
  } # End of X loop
  # Add Store values to end of F.vectors for pass back to main program
  Temp <- cbind(F.vectors, Store) # Combined by columns
  return(Temp) # Return F.vectors and Store
} # End of function

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
# Fonction de la boucle du programme principal. A été faite sous forme de fonction dans ce cas car on fait tourner le programme pour chaque type d'hôte (i.e. 4 fois)
# Pas présenté de cette manière dans le pdf mais le mettre sous forme de fonction permet de tout faire tourner dans un seul script pour la suite (i.e. prédictions individuelles)
# Arguments de la fonction Main : 
# HostType = type d'hôte pour lequel on veut ressortir la matrice de décision correspondante
# Output1 = Nom du fichier pour lequel on enregistre le dernier pas de temps
# Output2 = Nom du fichier pour lequel on enregistre la matrice de décision complète

MAIN <- function(HostType, Output1, Output2) {
  # MAIN PROGRAM
  # Initialize parameters
  Xmax <- 40 # Maximum value of X = eggs
  Xcritical <- 0 # Lowest value of X =  0 eggs
  Xinc <- 1 # Increment in state variable
  Max.Index <- 1+(Xmax-Xcritical)/Xinc # Max Index value
  Psurvival <- 0.99 # Survival probty per time increment
  Npatch <- 4 # Number of patches = hosts
  # Create host coefficient matrix from which to get Benefits
  Host.coeff <- matrix(0,4,4)
  Host.coeff[1,] <- c(-0.2302,2.7021, -0.2044,0.0039)
  Host.coeff[2,] <- c(-0.1444,2.2997, -0.1170,0.0013)
  Host.coeff[3,] <- c(-0.1048,2.2097, -0.0878,0.0004222)
  Host.coeff[4,] <- c(-0.0524,2.0394, -0.0339,-0.0003111)
  # Calculate benefit as a function of
  # clutch size (rows) and Host type (columns)
  Clutch <- seq(from = 0, to = Xmax)
  Benefit <- matrix(0, Xmax+1, 4) # Zero to Xmax
  for (I.Host in 1:4) { # Iterate over host types
    Benefit[,I.Host] <- Host.coeff[I.Host,1] + Host.coeff[I.Host,2]*Clutch + Host.coeff[I.Host,3]*Clutch^2 + Host.coeff[I.Host,4]*Clutch^3
  }
  Benefit[1,] <- 0 # Reset first row to zero
  SHM <- c(9,12,14,23) # Set single host maximum. See text for derivation
  # Make all values > than SHM = 0. Note that we use 2 because of zero class
  for (i in 1:4){
    Benefit[(SHM[i]+2):Max.Index,i] <- 0
  }
  # Probability of encountering host type
  Pbenefit <- c(0.05, 0.05, 0.1, 0.8)
  Horizon <- 21 # Number of time steps
  # Set up matrix for fitnesses
  # Column 1 is F(x, t). Column 2 is F(x, t+1) Both are zero
  F.vectors <- matrix(0, Max.Index,2)
  # Create matrices for output
  FxtT <- matrix(0,Horizon,Max.Index) # F(x,t,T)
  # Best clutch size for host 2
  Best.Patch <- matrix(0,Horizon,Max.Index)
  
  # Start iterations
  Time <- Horizon
  # Initialize Time
  while(Time > 1) {
    Time <- Time - 1 # Decrement Time by 1 unit
    # Call OVER.STATES to get best values for this time step
    Temp <- OVER.STATES(F.vectors, Xcritical, Xmax, Xinc, Npatch, Benefit, Pbenefit, Psurvival, Max.Index, HostType)
    # Extract F.vectors
    TempF <- Temp[,1:2]
    # Update F1
    for (J in 2:Max.Index) {
      F.vectors[J,2] <- TempF[J,1]
    }
    # Store results
    Best.Patch[Time,] <- Temp[,4]
    FxtT[Time,] <- Temp[,3]
  } # End of Time loop
  
  # Output information. For display add states to last row of matrices
  Index <- seq(from = 1, to = Max.Index)
  Best.Patch[Horizon,] <- (Index-1)*Xinc + Xcritical
  FxtT[Horizon,] <- (Index-1)*Xinc+Xcritical
  print(Best.Patch[,1:Max.Index]) # Print Decision matrix
  print(signif(FxtT[,1:Max.Index],3)) # Print Fxt of Decision matrix: 3 sig places
  
  # Plot data as 3d plot and colored grid
  y <- Best.Patch[Horizon,2:Max.Index]
  x <- seq(from = 1, to = Horizon - 1)
  par(mfrow = c(1,2))
  persp(x, y, Best.Patch[1:20,2:Max.Index], xlab = "Time", ylab = "x", zlab = "Optimal clutch size", theta = 20, ph = 25, lwd = 1) #3D plot
  image(x, y, Best.Patch[1:20,2:Max.Index], col = terrain.colors(50), xlab = "Time", ylab = "x", las = 1) # Colored grid
  
  # Output text file for future plotting to test predictions
  DATA <- cbind(x, Best.Patch[1:Horizon-1,41])
  DATA <- t(DATA)
  write(DATA,file = Output1, nc = 2)
  
  # Enregistrement des matrices de décision pour chaque type d'hôte
  DATA <- Best.Patch[1:Horizon - 1,2:41]
  DATA <- t(DATA)
  write(DATA, file = Output2, nc = 40)
}


## On fait tourner le programme pour l'hôte n°1
HostType = 1
Output1 = "OVOPOSITION1.txt"
Output2 = "DM1.txt"
MAIN(HostType, Output1, Output2)

## Idem pour l'hôte n°2
HostType = 2
Output1 = "OVOPOSITION2.txt"
Output2 = "DM2.txt"
MAIN(HostType, Output1, Output2)

## Idem pour l'hôte n°3
HostType = 3
Output1 = "OVOPOSITION3.txt"
Output2 = "DM3.txt"
MAIN(HostType, Output1, Output2)

## Idem pour l'hôte n°4
HostType = 4
Output1 = "OVOPOSITION4.txt"
Output2 = "DM4.txt"
MAIN(HostType, Output1, Output2)








########################################
#### Partie prédiction individuelle ####
########################################

rm(list = ls()) # Remove all objects from memory
Xmax <- 40
# Maximum value of X = eggs
DM1 <- read.table(file = "DM1.txt") # Cols = x rows = time
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
