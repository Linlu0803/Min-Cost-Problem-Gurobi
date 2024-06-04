import gurobipy as gp
from gurobipy import GRB
import json
import ast



def solve_mcf (nodes, arcs, start_solution):

    # Create the Gurobi model
    model = gp.Model("min-cost-problem")

    # Set Gurobi log file
    model.Params.LogFile = 'gurobi mit.log'
    
    # Enable verbose output
    model.Params.OutputFlag = 1
    model.Params.DisplayInterval = 1 
    model.Params.FeasibilityTol = 1e-9
    model.Params.OptimalityTol = 1e-9

    # create variable for flow : 0<flow< capacity(lb: lower bound, ub: upper bound, name: from i to j)
    flow = {}
    for arc in arcs:
        flow[arc['from'], arc['to']] = model.addVar(
            lb=0, ub=arc['upper_bound'], name=f"flow_{arc['from']}_{arc['to']}")
        if (arc['from'], arc['to']) in start_solution:
            flow[arc['from'], arc['to']].start = start_solution[(arc['from'], arc['to'])]
    # 0<=flow<=upper_bound


    for node in nodes:
        model.addConstr(
            gp.quicksum(flow[arc['from'], arc['to']] for arc in arcs if arc['to'] == node) - gp.quicksum(flow[arc['from'], arc['to']] for arc in arcs if arc['from'] == node)==nodes[node]['demand'],
            name=f"flow_balance_{node}_in")
    #flow_in - flow_out = demand


    # Set the objective function
    model.setObjective(
        gp.quicksum(flow[arc['from'], arc['to']] * arc['cost'] for arc in arcs ),
        GRB.MINIMIZE)
    #minimize sum (flow*cost)

    '''start_time = time.time()  # gain the start time'''

############################### Iteration speichern########################################
    '''def my_callback(model, where):
        if where == GRB.Callback.SIMPLEX:
            iter_count = model.cbGet(GRB.Callback.SPX_ITRCNT)
            obj_val = model.cbGet(GRB.Callback.SPX_OBJVAL)
            print(f"Iteration: {iter_count}, Objective Value: {obj_val}")
            # Write each iteration's information to a file
            with open("iterations.log", "a") as f:
                f.write(f"Iteration: {iter_count}, Objective Value: {obj_val}\n")
    '''

        #########################################################

    # Solve the model
    model.optimize()#my_callback

    '''end_time = time.time()  # gain the end time

    elapsed_time = end_time - start_time  # calculate the elapsed time

    print(f"Gurobi optimization elapsed time: {elapsed_time:.6f} seconds") # print the elapsed time
    '''

    if model.status == GRB.OPTIMAL: #GRB.OPTIMAL =" the optimization was successful"
        min_cost = model.objVal
        flow_values = {arc: flow[arc].X for arc in flow}
                        #  flow[arc].X = flow value of each arc
        return min_cost, flow_values
    # Return the flow values
    else:
        raise Exception("No optimal solution found")


    
