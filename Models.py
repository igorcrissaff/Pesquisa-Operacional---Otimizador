from pulp import *
from pulp.constants import LpCategories

x = LpVariable("x", 0)
y = LpVariable("y", 0) 

def solve(objective, restrictions:list):
    model = LpProblem(sense=LpMaximize)
    
    model += objective
    for restriction in restrictions:
        model += restriction

    status = model.solve() 
    status = LpStatus[status]
    
    if status != 'Optimal':
        return None
    
    return {
        "x": value(x),
        "y": value(y),
        "z": value(model.objective),
    }

def verify_model(model):
    expected_keys = ['title', 'objective', 'sense', 'restrictions']
    keys = model.keys()
    return keys == expected_keys

if __name__ == "__main__":
    solve(100*x+50*y, [
        x<=1500,
        y<=6000,
        10*x+8*y<=25000,
        x+y<=4500
    ])