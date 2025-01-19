states_Dict = {"Pennsylvania": 0,
               "Arizona" : 1,
               "New Mexico": 2,
               "Wisconsin": 3,
               "Florida": 4,
               "Georgia": 5,
               }

Dem_prop = np.array([0.43, 0.45,0.47, 0.46, 0.43, 0.42])
Ind_prop = np.array([0.1, 0.09, 0.12, 0.1, 0.07, 0.14])
Rep_prop = np.array([0.47, 0.46,0.40, 0.44, 0.5, 0.44])
elect_col = np.array([19, 11, 5, 10, 30, 16])

import numpy as np
from itertools import permutations

def GetUniqueParts(n):
    p = [0] * n     # An array to store a partition
    k = 0         # Index of last element in a partition
    p[k] = n     # Initialize first partition
    pure_strategies = []
    while True:
         
 
            # Generate next partition
            # and add this partition to list of partitions
            pure_strategies.append(p[:k + 1])
            # Find the rightmost non-one value in p[]. 
            # Also, update the rem_val so that we know
            # how much value can be accommodated
            rem_val = 0
            while k >= 0 and p[k] == 1:
                rem_val += p[k]
                k -= 1
 
            # if k < 0, all the values are 1 
            if k < 0:

                return
 

            # Decrease the p[k] found above and
            p[k] -= 1
            rem_val += 1
 
            # these values at different positions after p[k]
            while rem_val > p[k]:
                p[k + 1] = p[k]
                rem_val = rem_val - p[k]
                k += 1
 
            # Copy rem_val to next position 
    
            p[k + 1] = rem_val
            k += 1

def GetPureStrategies(n):
    parts = GetUniqueParts(n)
    pure_strategies = []
    for part in parts:
        pure_strategies.append(permutations(part))
    return pure_strategies

def Payoff(A, B):
    sum_of_AB = A + B
    sum_of_AB[sum_of_AB == 0] = 1
    Democrat_wins = A/(sum_of_AB) * Ind_prop + Dem_prop
    Republican_wins = B/(sum_of_AB) * Ind_prop + Rep_prop
    return np.sum(elect_col[Democrat_wins > Republican_wins]) - np.sum(elect_col[Democrat_wins < Republican_wins])

def GetPayoffMatrix(n):
    pure_strategies = GetPureStrategies(n)
    Payoff_matrix = np.zeros((len(pure_strategies), len(pure_strategies)))
    for i in range(len(pure_strategies)):
        for j in range(len(pure_strategies)):
            Payoff_matrix[i,j] = Payoff(pure_strategies[i], pure_strategies[j])
    return Payoff_matrix

def GetStrategy(RegSum, StSum):
    strategy = np.copy(RegSum)
    strategy[strategy<0] = 0

    if np.sum(strategy)> 0:
        strategy = strategy/np.sum(strategy)
    else:
        strategy = 1/N * np.ones(N)
    StSum += strategy

    return strategy, StSum

def regret_minimisation(iter, payoff_matrix):
    StSumA = np.zeros(N)
    StSumB = np.zeros(N)
    RegSumA = 1/N * np.ones(N)
    RegSumB = 1/N * np.ones(N)

    for i in range(1, iter+1):
        strategyA, StSumA = GetStrategy(RegSumA, StSumA)
        strategyB, StSumB = GetStrategy(RegSumB, StSumB)
        StA = np.random.choice(range(N), p = strategyA)
        StB = np.random.choice(range(N), p = strategyB)

        regretA = payoff_matrix[:, StB] - Payoff(StA, StB)
        regretB = payoff_matrix[StA, :] - Payoff(StA, StB)

        RegSumA += regretA
        RegSumB += regretB

    return StSumA, StSumB

def GetAvrStrategy(StrSum):
    
    avstr = np.zeros(N)

    if np.sum(StrSum) > 0:
        avstr = StrSum/np.sum(StrSum)
    else:
        avstr = 1/N * np.ones(N)

    return avstr