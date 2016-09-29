''' Finding the minimum number of dice rolls to make it through a snakes and ladders game
Alisdair Robertson
29 Sept 2016 '''
import fileinput

LOGGING = False

class QuickestWay(object):
    ''' Class to scan the given input and perform the calculations '''
    def __init__(self):
        self.layers = {} # dictionary of layers
        self.edges = {} # dictionary of edges

    def bfs(self, verts, tunnels, current):
        ''' Breadth first search. Creates a tree of edges in which
        each edge points along the fastest route to it's parent '''
        self.log("EXAMINING: %s", (str(current)))
        next_layer = set([]) # set of verticies for next layer

        for vert in current: # for every vert in the current layer

            self.log("at vert %d", (vert))

            for child in verts[vert]: # for all if it's children

                if child not in self.layers: # if child is not already in a layer

                    self.log("  child %d has no level yet, assigning %d",
                             (child, self.layers[vert] + 1))

                    # set the level, create child-parent edge, add child to next layer list
                    self.layers[child] = self.layers[vert]+1
                    self.edges[child] = vert
                    next_layer.add(child)

                elif self.layers[child] >= self.layers[vert] + 1 and vert > self.edges[child]:

                    self.log("  child %d of level %d HAS parent %d: we are at level %d," +
                             " changing it to have parent %d",
                             (child, self.layers[child], self.edges[child],
                              self.layers[vert]+1, vert))

                    # child should have lower layer
                    self.edges[child] = vert
                    self.layers[child] = self.layers[vert] + 1
                    next_layer.add(child)

        if next_layer:
            # call bfs for the next vertex, otherwise, method ends
            self. bfs(verts, tunnels, next_layer)

    def count_hops(self, start=100, rolls=0):
        ''' trace the shortest path through the tree given by the bfs '''
        if start == 1:
            return rolls # return rolls to get to square 1
        elif start not in self.edges:
            return -1 # no way to get to square 1 (e.g. all 6 squares before the finish have snakes)
        else:
            self.log("at %d, following to %d, current rolls %d", (start, self.edges[start], rolls))
            return self.count_hops(self.edges[start], rolls+1)

    @classmethod
    def log(cls, string, params=None):
        ''' method to handle the logging, means we can turn off all the logs easily'''
        if LOGGING:
            if params:
                print string % params
            else:
                print string

    def run(self):
        ''' scan the input from stdin and then run the search and count '''
        ladders = False # Start false so it gets flipped to true on the first run
        test_case_number = -1 # begin at -1 so first test case is 0
        test_case_data = []

        for line in fileinput.input():
            if line[0] == '#' or fileinput.isfirstline(): # skip first and comment lines
                continue
            elif len(line.split(' ')) == 1: # if we're about to get tunnel input
                ladders = not ladders # flip ladders
                if ladders:
                    test_case_number += 1 # move to next test case
                    test_case_data.append({}) # add empty dictionary for new test cases
            else:
                # fill the tunnel information
                test_case_data[test_case_number][int(line.split(" ")[0])] = int(line.split(" ")[1])

        # For each test case
        for tunnels in test_case_data:
            self.log("Testing a case: ")
            verticies = [set([]) for i in range(101)]
            # for every vert
            for i in range(1, 100):
                if i in tunnels:
                    self.log(" square %d has no children! it's a tunnel", (i))
                    continue
                self.log(" making children for vert %d", (i))
                # for every vert that this vert would link to
                for dest in range(1, 7):
                    if i+dest > 100:
                        self.log("   square %d is off the board!", (i+dest))
                        continue
                    # does it link somewhere
                    if i+dest in tunnels:
                        self.log("   giving vert %d a child %d (%d is linked)",
                                 (i, tunnels[i+dest], dest+i))
                        # enter the one it links to instead
                        verticies[i].add(tunnels[i+dest])
                    else:
                        # enter the vert this would link to
                        self.log("   giving vert %d a child %d", (i, i+dest))
                        verticies[i].add(i+dest)

            self.edges = {1:0} # set up edge from start node to null node (avoids error)
            self.layers = {1:1} # set node 1 as level 1
            # create BFS tree from this vert set
            self.bfs(verticies, tunnels, set([1]))
            print self.count_hops()

QUICKEST_WAY = QuickestWay()
QUICKEST_WAY.run()
