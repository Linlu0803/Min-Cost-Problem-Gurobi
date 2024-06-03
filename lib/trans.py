

import json
import os

def transform_data(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    # Original nodes and arcs
    nodes = data['nodes']
    arcs = data['arcs']

    # Create new nodes dictionary and add source and sink
    new_nodes = {str(i): {} for i in nodes.keys()}
    new_nodes['source'] = {}
    new_nodes['sink'] = {}

    # Create new arcs list and add connections to source and sink
    new_arcs = []

    # Add arcs from source and to sink
    for node, attributes in nodes.items():
        if attributes['demand'] < 0:
            new_arcs.append({"from": "source", "to": node, "capacity": -attributes['demand']})
        elif attributes['demand'] > 0:
            new_arcs.append({"from": node, "to": "sink", "capacity": attributes['demand']})

    # Add existing arcs without the cost field
    for arc in arcs:
        new_arc = {
            "start": arc['from'],
            "end": arc['to'],
            "capacity": arc['upper_bound']
        }
        new_arcs.append(new_arc)

    # Create the new data dictionary
    new_data = {
        "nodes": new_nodes,
        "arcs": new_arcs
    }

    # Write the new data to the output file
    with open(output_file, 'w') as outfile:
        json.dump(new_data, outfile, indent=4)

if __name__ == "__main__":
    input_path = r'D:\Fub SS 2024\Metaheurisitk\Maxflowgurobi\Data\chvatal_small.json'
    output_path = r'D:\Fub SS 2024\Metaheurisitk\Maxflowgurobi\Data\transformed_chvatal_small.json'
    transform_data(input_path, output_path)
