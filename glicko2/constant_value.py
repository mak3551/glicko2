#: The actual score for win
WIN: float = 1.0
#: The actual score for draw
DRAW: float = 0.5
#: The actual score for loss
LOSS: float = 0.0

# If the player is unrated, these values are set.
R_INITIAL: float = 1500
RD_INITIAL: float = 350
SIGMA_INITIAL: float = 0.06

# In the Mark Glickman's paper,it is "τ" (in Step 1). It constrains the change in volatility over time.
# He says reasonable choices are between 0.3 and 1.2,
# though the system should be tested to decide which value results in greatest predictive accuracy.
# Smaller values of τ prevent the volatility measures from changing by large amounts.
TAU: float = 1.0

# convergence tolerance, ε (used in Step 5).
EPSILON: float = 0.000001
