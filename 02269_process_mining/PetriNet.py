'''
First assigment in Process Mining
Modeling a simple PetriNet
'''

class PetriNet():
    def __init__(self):
        self.places = []
        self.transitions = {}
        self.in_transitions = {}
        self.out_transitions = {}
        self.edges = {}
        self.tokens = {} #should not be hard coded for future assignments 

    def add_place(self, id):
        self.places.append(id)

    def add_transition(self, name, id):
        self.transitions[id] = name

    def add_edge(self, source, target):
        self.edges[source] = target

        if target < 0 and target not in self.in_transitions: 
            self.in_transitions[target] = []

        if target > 0 and source not in self.out_transitions: 
            self.out_transitions[source] = []

        if source > 0:
            self.in_transitions[target].append(source)

        if source < 0: 
            self.out_transitions[source].append(target)

        return self

    def get_tokens(self, place):
        if place in self.tokens: 
            return self.tokens[place]
        else: 
            return 0 
        
    def is_enabled(self, transition):
        if transition in self.transitions.keys(): 
            for place in self.in_transitions[transition]: 
                if self.get_tokens(place) >= 1: 
                    return True 
                else: 
                    return False 

    def add_marking(self, place):
        if place not in self.tokens: 
            self.tokens[place] = 0
            self.tokens[place] += 1
          
        elif place in self.tokens: 
            self.tokens[place] += 1

        else: 
            print("Not a valid place number!")
      
    def increment_token(self, place): 
        if (place in self.tokens 
            and self.tokens[place] > 0): 
            self.tokens[place] -=1 

    def fire_transition(self, transition):
         if transition in self.transitions: 
            for place in self.in_transitions[transition]: 
                if self.get_tokens(place) < 0: 
                    print("Input place can't have less than 0 tokens")
                else: 
                    self.increment_token(place)

            for place in self.out_transitions[transition]: 
                if self.get_tokens(place) < 0: 
                    print("Outgoing place can't have less than 0 tokens")
                else: 
                    self.add_marking(place)
                    
    

