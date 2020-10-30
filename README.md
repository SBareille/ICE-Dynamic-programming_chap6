# ICE-Dynamic-programming_chap6

This repository contains the scripts and information of a university project, for the ICE (Introduction to Computational Ecology) teaching unit.
One of the main objectives of this teaching unit is to understand the algorithmic structure of programs in the field of ecology and to translate them from a language to another. 
In our specific case, the initial language is R and the translation is made to Python. The programs studied are part of a book specializing in ecological modelling (Roff, 2010).
The chapter of the book chosen by our team is n°6 : Dynamic Programming. 
The programs of this topic consist in a main program that applies the principles of dynamic programming to specific scenarios in order to obtain a "decision matrix". 
This decision matrix gives the best choice of a patch at a certain time for an individual to have the highest fitness at a goal time.
The decision matrix is subsequently used to make simulations of choices for individuals over a certain time frame or make predictions of population frequencies in the different patches for each time step.

The repository contains the initial programs in R from the book (Roff, 2010) for reference and the translated python scripts of the scenarios that we chose to study.

  A0_dynamic_programming_decision_matrix.py       computation of a decision matrix (scenario 0)
  
  A1_individual_prediction.py                     utilisation of the decision matrix for individual predictions
  
  A2_population_state_frequency_prediction.py     utilisation of the decision matrix for state frequency predictions
  
  B_decision_matrix_scaling_fitness.py            computation of a decision matrix, changing the definition of fitness (scenario 1)
  
  C_indexing_and_equivalent_choices.py            computation of a decision matrix, with equivalent choices, indexing and interpolation (scenario 3)

N.B : the script '4_parasitoids.py' is not finished and won't be presented.


Reference :
Roff, D. A. (2010). Modeling Evolution: an introduction to numerical methods. Oxford University Press.

Contributors : 
BAREILLE Servane,
BOURGADE Clément,
PECHIERAS Florian,
WOEHREL Aubin
