from PetriNet import PetriNet 
from dependency_graph import read_from_file
from dependency_graph import dependency_graph_file

'''
1. Event log 

2. Identify direct follow relations 

3. Identify causal dependencies 

4. Identify places and transitions 

5. Construct the Petri Net 

6. Construct the Output Model 



Nå skal alt bare kobles sammmen, det vil si at vi finner transitions (selve aktvitene over alle traces, bare en per), places (stedene mellom transitions), 
edges (blir koblingene mellom transitions og places), dette kommer vel egt fram av relasjoenene ? Alt dette kan kobles med infoen vi har nå. 
Må bruke petri net strukturen til å finne ut av det. 

'''

pn = PetriNet()

def alpha(log): 
    casual_dependencies(log)
    parallelism(log)
    check_choices(log)

    transitions = {}



def casual_dependencies(log): 

    dependency_dict = dependency_graph_file(log)
    print("dependency_dict: ", "\n",  dependency_dict, "\n")
    casual_dict = {}

    for prev_task, follows  in dependency_dict.items(): 
        print(prev_task, follows)
        for curr_task in follows: 
            reverse = curr_task in dependency_dict and prev_task in dependency_dict[curr_task]
            if not reverse: 
                if prev_task not in casual_dict: 
                    casual_dict[prev_task] = {}
                casual_dict[prev_task][curr_task] = dependency_dict[prev_task][curr_task]

    print("\n", "casual_dict:", "\n", casual_dict, "\n")
    return casual_dict

def parallelism(log): 

    dependency_dict = dependency_graph_file(log)
    
    parallelism_dict = {}
    for prev_task, follows in dependency_dict.items():
        for curr_task in follows:
            reverse = curr_task in dependency_dict and prev_task in dependency_dict[curr_task]
            if reverse:
                if prev_task not in parallelism_dict:
                    parallelism_dict[prev_task] = []
                parallelism_dict[prev_task].append(curr_task)

    print("parallelism_dict:", "\n", parallelism_dict, "\n")
    return parallelism_dict

def check_choices(log):

    dependency_dict = dependency_graph_file(log)
    
    choices_dict = {}
    
    for prev_task, follows in dependency_dict.items():
        if len(follows) > 1:
            choices_dict[prev_task] = list(follows.keys())
    print("choices_dict:", "\n", choices_dict)
    return choices_dict



log = "extension-log.xes"
mined_model = alpha(read_from_file(log))





