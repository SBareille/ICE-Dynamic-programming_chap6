######################################################################################
####### Coeur du programme, utilisé par la suite pour les 5 autres scénarios #########
######################################################################################


# Portion du programme pour obtenir la matrice de décision ----

rm(list = ls()) # Remove all objects from memory

# Function to calculate fitness when organism is in state X
FITNESS <- function(X, Xcritical, Xmax, Xmin, Cost, Benefit, Pbenefit, Pmortality, F.vectors) {
  # State in patch if forager finds food
  X.Food <- X - Cost + Benefit
  # If X.Food greater than Xmax then X.Food must be set to Xmax
  X.Food <- min(X.Food, Xmax)
  # If X.Food less than or equal to Xcritical then set to Xcritical
  X.Food <- max(X.Food, Xcritical)
  # State in patch if forager does not find food
  X.NoFood <- X - Cost
  # If X.NoFood is less than Xcritical set X.NoFood to Xcritical
  X.NoFood <- max(X.NoFood, Xcritical)
  
  Term1 <- Pbenefit*F.vectors[X.Food,2] # If food is found
  Term2 <- (1-Pbenefit)*F.vectors[X.NoFood,2] # If food is not found
  W <- (1-Pmortality)*(Term1 + Term2) # Survival in patch
  return(W) # Return Fitness
} # End of function

# Function to iterate over patches
OVER.PATCHES <- function(X, F.vectors, Xcritical,Xmax, Xmin, Npatch, Cost, Benefit, Pbenefit, Pmortality) {
  
  for (i in 1:Npatch) { # Cycle over patches
    # Call Fitness function
    RHS[i] <- FITNESS(X, Xcritical, Xmax, Xmin, Cost, Benefit[i], Pbenefit[i], Pmortality[i], F.vectors)
  } # End of i loop
  
  # Now find optimal patch Best row is in Best[1]
  Best <- order(RHS, na.last = TRUE, decreasing = TRUE)
  F.vectors[X,1] <- RHS[Best[1]]
  Best.Patch <- Best[1]
  # Concatenate F(x,t) and the optimal patch number
  Temp <-c(F.vectors[X,1], Best.Patch)
  
  # Add Temp to bottom of F.vectors and rename to Temp
  Temp <- rbind(F.vectors, Temp)
  return (Temp)
} # End of function

# Function to iterate over states of X
OVER.STATES <- function(F.vectors, Xcritical, Xmax, Xmin, Npatch, Cost, Benefit, Pbenefit, Pmortality) {
  
  Store <- matrix(0,Xmax,2) # Create matrix for output
  for (X in Xmin:Xmax) { # Iterate over states of X
    # For given X call Over.Patches to determine F(x,t) and best patch
    Temp <- OVER.PATCHES(X, F.vectors, Xcritical, Xmax, Xmin, Npatch, Cost, Benefit, Pbenefit, Pmortality)
    # Extract components. Last row is F(x,t) and best patch
    n <- nrow(Temp)-1
    F.vectors <- Temp[1:n,]
    Store[X,] <- Temp[n+1,] # Save F(x,t) and best patch
    } # End of X loop
  
  # Add Store values to end of F.vectors for pass back to main program
  Temp <- cbind(F.vectors, Store) # Combined by columns
  return(Temp) # Return F.vectors and Store
} # End of function

# MAIN PROGRAM
# Initialize parameters
Xmax <- 10 # Maximum value of X
Xcritical <- 3 # Value of X at which death occurs
Xmin <- Xcritical + 1 # Smallest value of X allowed
Cost <- 1 # Cost per period
Pmortality <- c(0, 0.004, 0.02) # Probability of mortality
Pbenefit <- c(1, 0.4, 0.6) # Probability of finding food
Npatch <- 3 # Number of patches
RHS <- matrix(0,Npatch,1) # Preallocate Right Hand Side of equn
Benefit <- c(0, 3, 5) # Benefit if food is discovered
Horizon <- 20 # Number of time steps

# Set up matrix for fitnesses
# Column 1 is F(x, t). Column 2 is F(x,t+1)
F.vectors <- matrix(0, Xmax,2) # Set all values to zero
F.vectors[Xmin:Xmax,2] <- 1 
# Set values > Xmin equal 1
# Create matrices for output
FxtT <- matrix(0,Horizon,Xmax) # F(x,t)
Best.Patch <- matrix(0,Horizon,Xmax) # Best patch number
# Start iterations
Time <- Horizon

# Initialize Time
while (Time > 1) {
  Time <- Time - 1
  # Decrement Time by 1 unit
  # Call OVER.STATES to get best values for this time step
  Temp <- OVER.STATES(F.vectors, Xcritical, Xmax, Xmin, Npatch, Cost, Benefit, Pbenefit, Pmortality)
  # Extract F.vectors
  TempF <- Temp[,1:2]
  # Update F1
  for (J in Xmin: Xmax) { 
    F.vectors[J,2] <- TempF[J,1]
  }
  # Store results
  Best.Patch[Time,] <- Temp[,4]
  FxtT[Time,] <- Temp[,3]
} # End of Time loop


# Output information. For display add states (¼wts) to last row of matrices
X <- seq(from = 1, to = Xmax)
Best.Patch[Horizon,] <- X
FxtT[Horizon,] <- X
Best.Patch[,Xmin:Xmax] # Print Decision matrix
signif(FxtT[,Xmin:Xmax],3) # Print Fxt of Decision matrix: 3 sig places










# Portion de programme pour la prédiction individuelle utilisant la matrice de décision ----

# Initialize parameters
set.seed(10) # Set random number seed
Xmax <- 10 # Maximum value of X
Xcritical <- 3 # Value of X at which death occurs
Xmin <- Xcritical + 1 # Smallest value of X allowed
Cost <- 1 # Cost per period
Pmortality <- c(0, 0.004, 0.02) # Probability of mortality
Pbenefit <- c(1, 0.4, 0.6) # Probability of finding food
Benefit <- c(0, 3, 5) # Benefit if food is discovered
Npatch <- 3 # Number of patches
Horizon <- 15 # Number of time steps
Output <- matrix(0,Horizon,10) # Matrix to hold output
Time <- seq(1, Horizon) # Values for x axis in plot
par(mfrow = c(5,2)) # Dividegraphpageinto5x2panels

for (Replicate in 1:10) { # Iterate over 10 replicates
  X <- 4 # Animal starts in state 4
  
  for (i in 1:Horizon) { # Iterate over time
    
    if(X > Xcritical) { # Check that animal still alive
      Patch <-Best.Patch[i,X] # Select patch
      # Check if animal survives predation
      # Generate random number
      if(runif(1) < Pmortality[Patch]) {
        cat("Replicate",Replicate,"Dead from predator\n") 
      }
      # Now find new weight
      # Set multiplier to zero, which corresponds to no food found
      Index <- 0
      if (runif(1) < Pbenefit[Patch]) {
        Index <- 1
      }
      # food is discovered
      X <- X - Cost + Benefit[Patch]*Index
      # If X greater than Xmax then X must be set to Xmax
      X <- min(X, Xmax)
      # If X less than X then animal dies
      if(X < Xmin){
        cat("Replicate", Replicate, "Dead from starvation\n")
      }
      Output[i,Replicate] <- Patch # Store data
      
    } # End of if(X > Xcritical)
  } # End of time loop
  plot(Time, Output[,Replicate], type = "l", ylab = "Patch selected")
} # End of replicate loop










# Portion de programme pour obtenir l'état attendu, en utilisant la matrice de décision ----
# Plutôt que de répéter n fois des scénarios depuis un certain état donné, le programme suivant permet d'obtenir la distribution dans un chacun des états

# Set initial parameter values
Xmax <- 10 # Maximum value of state
Xcritical <- 3 # Critical value of state
Xmin <- Xcritical+1 # Lowest value of state
Cost <- 1 # Metabolic cost
Time <- 2 # Current state to be considered
Npatch <- 3 # Npatch is number of patches
Pmortality <- c(0, 0.004, 0.02)# Probability of mortality Beta
Pbenefit <- c(1, 0.4, 0.6) # Probability of finding food Lambda
Benefit <- c(0, 3, 5) # Benefit if food is discovered Y
# Set transition density matrix to zero
Trans.density <- matrix(0, Xmax, Xmax)

# Step 1 Cycle over all values of z from Xmin to Xmax
for (z in Xmin:Xmax) { # Iterate over states

  # Select the best patch from the Decision matrix at row Time
  K <- Best.Patch[Time,z] # Decision matrix is called Best.Patch
  # Calculate w(x,t|z)
  # Found food and survives predator
  x <- min(z-Cost+Benefit[K], Xmax)
  # Assign probability
  Trans.density[z,x]<- (1-Pmortality[K])*Pbenefit[K]
  # Food not found
  x <- z-Cost
  # State exceeds the critical value
  if(x > Xcritical){
    # Animal survives
    Trans.density[z,x]<-(1-Pmortality[K])*(1-Pbenefit[K])
    # Animal does not survive
    Trans.density[z,Xcritical]<- Pmortality[K]
  } # end of if statement
  # State is less than critical
  else { # Note that in R the { immediately follows else
    Trans.density[z,Xcritical]<- Pmortality[K]+(1-Pmortality[K])*(1-Pbenefit[K])
  } # End of else statement
} # end of z loop
Trans.density # Write out matrix


