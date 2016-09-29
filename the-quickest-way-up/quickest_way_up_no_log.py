''' Finding the minimum number of dice rolls to make it through a snakes and ladders game
Alisdair Robertson
29 Sept 2016 '''
import fileinput

class QuickestWay(object):
    ''' Class to scan the given input and perform the calculations '''
    def __init__(self):
        self.layers = {}        # dictionary of layers
        self.edges = {}         # dictionary of edges

    def bfs(self, verts, tunnels, current):
        ''' Breadth first search. Creates a tree of edges in which
        each edge points along the fastest route to it's parent '''

        next_layer = set([])                    # set of verticies for next layer

        for vert in current:                    # for every vert in the current layer
            for child in verts[vert]:           # for all if it's children

                if child not in self.layers:    # if child is not already in a layer
                    self.layers[child] = self.layers[vert] + 1      # set layer
                    self.edges[child] = vert                        # create child->parent edge
                    next_layer.add(child)                           # add child to next layer

                elif self.layers[child] >= self.layers[vert] + 1 and vert > self.edges[child]:
                    # child is in a layer, but we have a better (lower) offer for a layer
                    self.layers[child] = self.layers[vert] + 1      # set layer
                    self.edges[child] = vert                        # create child->parent edge
                    next_layer.add(child)                           # add child to next layer

        if next_layer:                              # if there's another layer
            self. bfs(verts, tunnels, next_layer)   # woo recursion

    def count_hops(self, start=100, rolls=0):
        ''' trace the shortest path through the tree given by the bfs '''
        if start == 1:
            return rolls                            # return rolls to get to square 1
        elif start not in self.edges:
            return -1                               # no way to get to square 1
        else:
            return self.count_hops(self.edges[start], rolls+1)

    def run(self):
        ''' scan the input from stdin and then run the search and count '''
        ladders = False                   # Start false so it gets flipped to true on the first run
        test_case_number = -1             # begin at -1 so first test case is 0
        test_case_data = []

        for line in fileinput.input():
            if line[0] == '#' or fileinput.isfirstline():  # skip first and comment lines
                continue

            elif len(line.split(' ')) == 1:                # if we're about to get tunnel input
                ladders = not ladders                      # flip ladders
                if ladders:
                    test_case_number += 1                  # move to next test case
                    test_case_data.append({})              # add empty dictionary for new test cases

            else:                                          # otherwise fill the tunnel information
                test_case_data[test_case_number][int(line.split(" ")[0])] = int(line.split(" ")[1])

        for tunnels in test_case_data:      # For each test case
            verticies = [set([]) for i in range(101)]

            for i in range(1, 100):         # For every vert
                if i in tunnels:
                    continue

                for dest in range(1, 7):    # For every potential child of that vert
                    if i+dest > 100:
                        continue

                    if i+dest in tunnels:                   # is it a tunnel?
                        verticies[i].add(tunnels[i+dest])   # yes -> link where the tunnel leads
                    else:
                        verticies[i].add(i+dest)            # no -> link the actual vert

            self.edges = {1:0}      # set up edge from start node to null node (avoids error)
            self.layers = {1:1}     # set node 1 as level 1

            self.bfs(verticies, tunnels, set([1]))  # create BFS tree from this vert set
            print self.count_hops()

QUICKEST_WAY = QuickestWay()
QUICKEST_WAY.run()
