import gurobipy as gp
from gurobipy import GRB

def solve_mcf (nodes, arcs, source, sink):
    
    model = gp.Model("min-cost-problem")

    # Set Gurobi log file
    model.Params.LogFile = 'gurobi.log'
    
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
    # 0<=flow<=upper_bound


    for node in nodes:
        model.addConstr(
            gp.quicksum(flow[arc['from'], arc['to']] for arc in arcs if arc['end'] == node) - gp.quicksum(flow[arc['from'], arc['to']] for arc in arcs if arc['end'] == node)==nodes[node]['demand'],
            name=f"flow_balance_{node}_in")
    #flow_in - flow_out = demand


    # Set the objective function
    model.setObjective(
        gp.quicksum(flow[arc['from'], arc['to']] * arc['cost'] for arc in arcs ),
        GRB.MINIMIZE)
    #minimize sum (flow*cost)

    # Solve the model
    model.optimize()

    if model.status == GRB.OPTIMAL: #GRB.OPTIMAL =" the optimization was successful"
        min_cost = model.objVal
        flow_values = {arc: flow[arc].X for arc in flow}
                        #  flow[arc].X = flow value of each arc
        return min_cost, flow_values
    # Return the flow values
    else:
        raise Exception("No optimal solution found")


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # Create a new model
    m = gp.Model("max_flow")

    # Create variables
    flow = m.addVars(arcs, name="flow")

    # Objective function
    m.setObjective(sum(flow[i,j] for i,j in arcs.select(source, '*')), GRB.MAXIMIZE)

    # Flow conservation constraints
    m.addConstrs(
        (flow.sum('*',j) - flow.sum(j,'*') == nodes[j]['demand'] for j in nodes if j not in [source, sink]),
        name="node")

    # Capacity constraints
    m.addConstrs(
        (flow[i,j] <= arcs[i,j]['capacity'] for i,j in arcs),
        name="capacity")

    # Compute optimal solution
    m.optimize()

    # Return the flow values
    return {arc: flow[arc].x for arc in flow}       