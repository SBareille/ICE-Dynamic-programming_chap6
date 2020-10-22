#####################################################################
#### Scénario 2 : Forager ou ne pas forager, un bon gros dilemme ####
#####################################################################

# Application de la programmation dynamique au choix de l'oiseau d'aller chasser ou non 
# Ici le X correspond à la condition de l'oiseau 
# L'oiseau a une certaine probabilité de perdre sa condition à chaque pas de temps
# Idem que dans les cas précédents, si l'oiseau va chasser, il a une certaine probabilité d'avoir un bénéfice et donc une certaine probabilité de ne pas avoir de bénéfice
# Autre paramètre important à comprendre : la condition de l'oiseau influence sa probabilité de mourir :
# Plus l'oiseau a une bonne condition (ie est mieux nourri donc plus gros), plus sa probabilité de mourir est importante

rm(list = ls()) # Enlève toutes les variables de la mémoire

# Fonction pour calculer la fitness quand l'individu est dans l'état X
FITNESS <- function(X, Xcritical, Xmax, Xmin, Cost, Benefit, Pbenefit, Pmortality, F.vectors) {
  # Etat dans le cas ou il y a un bénéfice
  # A noter que ici le bénéfice peut être -1 en cas de la perte de l'état de l'individu
  X.Food <- X + Benefit # Pas de notion de coût dans ce modèle. Le potentiel coût est compris dans la variable bénéfice
  # Si jamais X.Food est plus grand que Xmax alors X.food doit être mis à Xmax
  X.Food <- min(X.Food, Xmax)
  # If X.Food est plus faible ou égal à Xcritique, passage au Xcritique
  X.Food <- max(X.Food, Xcritical)
  # Etat dans le cas ou le forager ne gagne pas de bénéfice
  X.NoFood <- X 
  # If X.NoFood is less than Xcritical set X.NoFood to Xcritical
  X.NoFood <- max(X.NoFood, Xcritical)
  
  Term1 <- Pbenefit*F.vectors[X.Food,2] # If food is found
  Term2 <- (1-Pbenefit)*F.vectors[X.NoFood,2] # If food is not found
  W <- (1-Pmortality)*(Term1 + Term2) # Survival in patch
  return(W) # Return Fitness
} # End of function

# Function to iterate over patches
OVER.PATCHES <- function(X, F.vectors, Xcritical,Xmax, Xmin, Npatch, Cost, Benefit, Pbenefit, Pmortality) {
  
  RHS <- matrix(0,Npatch,1)
  for (i in 1:Npatch) { # Cycle over patches
    # Call Fitness function
    RHS[i] <- FITNESS(X, Xcritical, Xmax, Xmin, Cost, Benefit[i], Pbenefit[i], Pmortality[i,X], F.vectors)
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
Xmax <- 7 # Maximum value of X
Xcritical <- 1 # Value of X at which death occurs
Xmin <- Xcritical + 1 # Smallest value of X allowed
Cost <- 0 # Cost per period
# Probability of mortality if foraging
Pmin <- 0
Pmax <- 0.01
# Create mortality function. Make Pmin at stage 2
Pnoforage <- rep(0,Xmax) # Probability of mortality if not foraging
Pforage <- c(0,seq(from=Pmin, to=Pmax, length = Xmax-1)) # Foraging mortality
Pmortality <- rbind(Pnoforage,Pforage) # Mortality function
#Probability of foraging
Pbenefit <- c(0.4,0.8) # Probablity of "Benefit"
Benefit <- c(-1,1) # "Benefit"
Npatch <- 2 # Number of patches
Horizon <- 6 # Number of time steps

# Set up matrix for fitnesses
# Column 1 is F(x, t). Column 2 is F(x,t+1)
F.vectors <- matrix(0, Xmax,2) # Set all values to zero
F.vectors[Xmin:Xmax,2] <- seq(from = Xmin, to = Xmax) # Fitness finale
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

