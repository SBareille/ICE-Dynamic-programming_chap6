#################################################################
#### Scénario 3 : cas de choix équivalent, exemple des lions ####
#################################################################

rm(list = ls()) # Remove all objects from memory
# Function to calculate fitness when organism is in state X
FITNESS <- function(X, Xcritical, Xmax, Xinc, Cost, Benefit,Pbenefit, F.vectors){
  # Note that the state value X is passed
  # Note also that in this function Benefit and Pbenefit are vectors
  # Iterate over the four kill values (0,1,2,3)
  Max.Index <- 1+(Xmax-Xcritical)/Xinc # Get maximum index value
  W <- 0 # Set Fitness to zero
  Xstore <- X # Set X to Xstore to preserve value through loop
  for (I.Kill in 1:4){ # Begin loop
    
    X <- Xstore-Cost+Benefit[I.Kill] # Calculate new state value
    X <- min(X, Xmax) # If X greater than Xmax then X must be set to Xmax
    X <- max(X, Xcritical) # If X less than or equal to Xcritical then set to Xcritical
    Index <- 1+(X-Xcritical)/Xinc # Convert to Index value
    # Index value probably not an integer
    # So consider two integer values on either size of X
    Index.lower <- floor(Index) # Choose lower integer
    Index.upper <- Index.lower + 1 # Upper integer
    # Must stop index exceeding Max.Index. Note that QX=0 in this case
    Index.upper <- min(Index.upper, Max.Index)
    Qx <- X - floor(X) # qx for linear interpolation
    W <- W + Pbenefit[I.Kill]*(Qx*F.vectors[Index.upper,2]+(1-Qx)*F.vectors[Index.lower,2])
  } # End of I.Kill loop
  
  return(W) # Return Fitness
} # End of function

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
# Function to iterate over patches i.e. over PACKS
OVER.PATCHES <- function(X, F.vectors, Xcritical,Xmax, Xinc, Npatch, Cost, Benefit, Pbenefit) {
  RHS <- matrix(0,Npatch,1) # Set matrix for Right Hand Side of equation
  
  for (i in 1:Npatch) { # Cycle over patches = pack sizes
    # Call Fitness function. Pass Benefit and Pbenefit as vectors
    RHS[i] <- FITNESS(X, Xcritical, Xmax, Xinc, Cost, Benefit[i,],Pbenefit[i,], F.vectors)
  } # End of i loop
  
  Best <- order(RHS, na.last = TRUE, decreasing = TRUE) # Now find optimal patch Best row is in Best[1]
  Index <- 1+(X-Xcritical)/Xinc # Get Index value
  F.vectors[Index,1] <- RHS[Best[1]] # Get best W = F(x,t,T)
  Best.Patch <- Best[1] # Get best patch ( = pack). Remember to convert from index value
  Temp <- c(F.vectors[Index,1], Best.Patch)  # Concatenate F(x,t) and the optimal patch (= pack) number
  Temp <- rbind(F.vectors, Temp) # Add Temp to bottom of F.vectors and rename to Temp
  
  # Create 1x2 vector to hold decision on more than one choice
  # We only need one cell but it is convenient to use 2 for concatenation onto Temp, as indicated below
  # Set Choice to zero
  Choice <- c(0,0)
  if(RHS[Best[1]]==RHS[Best[2]]){
    Choice <- c(1,1) # Equal fitnesses
  }
  
  Temp <- rbind(Temp,Choice) # Bind to bottom of matrix
  return (Temp)
} # End of function

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
# Function to iterate over states of X
OVER.STATES <- function(F.vectors, Xcritical, Xmax, Xinc, Npatch,Cost, Benefit, Pbenefit, Max.Index) {
  Store <- matrix(0,Max.Index,3) # Create matrix for output
  for (Index in 2:Max.Index) { # Iterate over states of X
    # For given X call Over.Patches to determine F(x,t) and best patch
    X <- (Index-1)*Xinc+Xcritical
    Temp <- OVER.PATCHES(X, F.vectors, Xcritical, Xmax, Xinc, Npatch, Cost, Benefit, Pbenefit)
    # Extract components. Penultimate row is F(x,t,T) and best patch
    n <- nrow(Temp)- 2
    F.vectors <- Temp[1:n,]
    Store[Index,1:2] <- Temp[n+1,] # Save F(x,t,T) and best patch
    Store[Index,3] <- Temp[n+2,1] # Save Flag for several choices
  } # End of X loop
  
  # Add Store values to end of F.vectors for pass back to main program
  Temp <- cbind(F.vectors, Store) # Combined by columns
  return(Temp) # Return F.vectors and Store
} # End of function

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
# MAIN PROGRAM
# Initialize parameters
Xmax <- 30 # Maximum value of X = gut capacity
Xcritical <- 0 # Value of X at which death occurs
Xinc <- 1 # Increment in state variable
Max.Index <- 1+(Xmax-Xcritical)/Xinc # Maximum index value
Cost <- 6
# Cost = Daily food requirement
Npatch <- 4 # Number of patches = packs

# Calculate benefit as a function of pack size (rows)
# and number of kills (columns)
Benefit <- matrix(0,4,4) # Rows = pack size, Columns = number of kills + 1
Pbenefit <- matrix(0,4,4) # Rows = pack size, Columns = number of kills + 1
Pi <- c(0.15, 0.31, 0.33, 0.33) # Probability of single kill for pack size
Y <- 11.25 # Size of single prey
k <- c(0,1,2,3) # Number of kills

for (PackSize in 1:4){ # Iterate over pack sizes
  Pbenefit[PackSize,] <- dbinom(x = k, size = 3, prob = Pi[PackSize]) # Calculate binomial probabilities using function dbinom
  Benefit[PackSize,2:4] <- Y*k[2:4]/PackSize # Calculate benefits = amount per individual
}

Horizon <- 31 # Number of time steps
# Set up matrix for fitnesses
# Column 1 is F(x, t). Column 2 is F(x, t+1)
F.vectors <- matrix(0, Max.Index,2)
F.vectors[2:Max.Index,2] <- 1 # Cell 1,2 = 0 = Dead
# Create matrices for output
FxtT <- matrix(0,Horizon,Max.Index) # F(x,t,T)
Best.Patch <- matrix(0,Horizon,Max.Index) # Best patch number
CHOICES <- matrix(0,Horizon,Max.Index) # Matrix for flag indicating multiple equivalent choices. 0 = only one choice, 1 = more than one choice

# Start iterations
Time <- Horizon # Initialize Time

while (Time > 1) {
  Time <- Time - 1 # Decrement Time by 1 unit
  # Call OVER.STATES to get best values for this time step
  Temp <- OVER.STATES(F.vectors, Xcritical, Xmax, Xinc,Npatch, Cost, Benefit, Pbenefit, Max.Index)
  # Extract F.vectors
  TempF <- Temp[,1:2]
  # Update F1
  for (J in 2:Max.Index) { 
    F.vectors[J,2] <- TempF[J,1]
  }
  # Store results
  Best.Patch[Time,] <- Temp[,4]
  FxtT[Time,] <- Temp[,3]
  CHOICES[Time,] <- Temp[,5]
} # End of Time loop


# Output information. For display add states to last row of matrices
# Note that state variable conversion from index value
Index <- seq(from = 1, to = Max.Index)
Best.Patch[Horizon,] <- (Index-1)*Xinc+Xcritical
FxtT[Horizon,] <- (Index-1)*Xinc+Xcritical
Best.Patch[,1:Max.Index] # Print Decision matrix
signif(FxtT[,1:Max.Index],3) # Print Fxt of Decision matrix : 3 sig places
CHOICES[,1:Max.Index] # Print matrix indicating choice flag

# Plot data
y <- Best.Patch[Horizon,2:Max.Index]
x <- seq(from = 1, to = Horizon-1)
par(mfrow = c(2,2))
persp(x, y, Best.Patch[1:30,2:Max.Index], xlab = "Time",ylab = "x  =  Gut contents", zlab =  "Optimal Pack size", theta = 20, ph = 25, lwd = 1) # 3D plot
image(x, y, Best.Patch[1:30,2:Max.Index], col = terrain.colors(50), xlab = "Time", ylab = "x = Gut contents", las = 1) # Colored grid
image(x, y, CHOICES[1:30,2:Max.Index], col = terrain.colors(50), xlab = "Time", ylab = "x = Gut contents", las = 1) # Colored grid


