import numpy as np
import pandas as pd
from ortools.algorithms import pywrapknapsack_solver


def bubbleSort(x: list) -> list:
    for i in range(len(x)):
        for j in range(i, len(x)):
            if x[j] < x[i]:
                temp = x[i]
                x[i] = x[j]
                x[j] = temp
    return x


def cleanseTeam(x: list) -> list:
    # position restraints
    positionMax = [GK, DEF, MID, ATT]
    positions = []
    for index, position in enumerate(positionMax):
        for i in range(position):
            positions.append(index + 1)
    print(positions)
    for index in x:
        if t["element_type"][index].astype(int) in positions:
            positions.remove(t["element_type"][index].astype(int))
        else:
            x.remove(index)
    
    teams = []
    for i in range(1, 21):
        for j in range(3):
            teams.append(i)

    # max. three players per team
    for index in x:
        if t["team"][index].astype(int) in teams:
            teams.remove(t["team"][index].astype(int))
        else:
            x.remove(index)
    
    return x


def printTeam(x: list):
    for player in x:
        print(t["full_name"][player])

t = pd.read_csv("2122_with_xP.csv")

budget = [1000]
capacity = 15
costs = [t["now_cost"].astype(float).tolist()]
points = t["xP"].astype(float).tolist()

GK = 2
DEF = 5
MID = 5
ATT = 3
TEAM = 3

solver = pywrapknapsack_solver.KnapsackSolver(
    pywrapknapsack_solver.KnapsackSolver.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER , "KnapsackExample"
)

solver.Init(points, costs, budget)
computed_value = solver.Solve()
packed_items = []
packed_costs = []
total_cost = 0

print(f"Total value: {computed_value}")

for i in range(len(points)):
    if solver.BestSolutionContains(i):
        packed_items.append(i)
        packed_costs.append(costs[0][i])
        total_cost += costs[0][i]

# print(f"Total cost: {total_cost}")
print("Packed items:")
printTeam(packed_items)
# print(f"Packed costs: {packed_costs}")
# print(f"Items packed: {len(packed_items)}")

packed_items = bubbleSort(packed_items)
packed_items = cleanseTeam(packed_items)
print("")
print("Cleansed items:")
printTeam(packed_items)

