class PetriNet():


    '''
Enabling: A transition can fire if all its input places have enough tokens.
Firing: When a transition fires, tokens move according to the transition’s
input and output specifications, changing the state of the Petri net.
Reachability: Determines if you can get from one marking to another by 
firing a sequence of transitions.
    '''
    def __init__(self):
        self.places = []
        self.transitions = {}
        self.in_transitions = {}
        self.out_transitions = {}
        self.edges = {}
        self.tokens = {1:0, 2:0, 3:0, 4:0}

    def add_place(self, id):
        self.places.append(id)

    def add_transition(self, name, id):
        self.transitions[name] = id


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
        return self.tokens[place]
        
    def is_enabled(self, transition):
        print(transition)
        print(self.transitions)

        if transition in self.transitions.values(): 
            print(transition)
            for places in self.in_transitions.values(): 
                for place in places: 
                    if self.get_tokens(place) >= 1: 
                        print("yahoo")
        
            #siste jeg gjorde før jeg la meg: 
                #feilen ligger i at jeg sjekker ALLE PLACES i alle transititons når jeg bare skal 
                # sjekke alle placene til en transition, derfor alle yahooene i terminalen blir printet ut. 

        '''
        if transition in self.transitions.values: 
            print("transition")
            for place in transition: 
                print("place")
                if self.get_tokens(place) >= 0: 
                    print ("token", self.get_tokens)
                    return True
        return False
        '''
            #må sjekke om p places input til transition er over 1. 
            # det betyr for at transition jeg får inn her må sjekkes mot hvilken 
            # places som går mot den, også sjekke om get_tokens på en eller flere av places er over 1

            #en transition er lagret som (name, id)
            #transition in/out er lagret som (id t, id p)


    def add_marking(self, place):
        if place in self.tokens: 
            self.tokens[place] += 1
        else: 
            print("Not a valid place number!")

      
    def increment_token(self, place): 
        if (place in self.tokens 
            and self.tokens[place] > 0): 
            self.tokens[place] -=1 

    ##def fire_transition(self, transition):
        # code here
         # TODO 

        
p = PetriNet()

p.add_place(1)  # add place with id 1
p.add_place(2)
p.add_place(3)
p.add_place(4)
p.add_transition("A", -1)  # add transition "A" with id -1
p.add_transition("B", -2)
p.add_transition("C", -3)
p.add_transition("D", -4)

p.add_edge(1, -1)
p.add_edge(-1, 2)
p.add_edge(2, -2).add_edge(-2, 3)
p.add_edge(2, -3).add_edge(-3, 3)
p.add_edge(3, -4)
p.add_edge(-4, 4)


print("places:", p.places)
print("transitions:", p.transitions)
print("edges:", p.edges)
print("in transitions:", p.in_transitions)
print("out transitions:", p.out_transitions)
print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))
p.add_marking(1)  # add one token to place id 1



print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

'''    



print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

p.fire_transition(-1)  # fire transition A
print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

p.fire_transition(-3)  # fire transition C
print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

p.fire_transition(-4)  # fire transition D
print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

p.add_marking(2)  # add one token to place id 2
print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

p.fire_transition(-2)  # fire transition B
print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

p.fire_transition(-4)  # fire transition D
print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# by the end of the execution there should be 2 tokens on the final place
print(p.get_tokens(4))

'''