import fileinput

edgeList = []

def log(string, tuple=None):
    return
    if tuple:
        print string % tuple
    else:
        print string

for line in fileinput.input():
    if (line[0] == '#'): # skip comment lines
        continue

    # store special input on first run
    if fileinput.isfirstline():
        verts = int(line.split(" ")[0])
        edges = int(line.split(" ")[1])

    else:
        # populate array representing tree edges
        edgeList.append([
            int(line.split(" ")[0]),
            int(line.split(" ")[1])
        ])

# make an actual tree structure 
nodes = [[] for i in range(verts+1)]
# for every edge in the list, list it's children in the array of nodes
for edge in edgeList:
    # child node is edge[0]
    # parent node is edge[1]
    # log("for an edge adding child node %d to parent node %d", (edge[0], edge[1]))
    nodes[edge[1]].append(edge[0])

# Function to walk and prune trees with even number of verticies
def walkAndPrune(tree, rootIndex):
    pruned = 0 # each method call begins with no pruned subtrees
    for childIndex in tree[rootIndex]:
        subTreeNodes = countNodes(tree, childIndex)
        log("checking subtree from root node %d, subtree root %d, %d verts", (rootIndex, childIndex, subTreeNodes))
        if ((subTreeNodes % 2) == 0):
            # If subtree is even, prune it
            log("even num verts, pruning subtree from parent node %d subtree root %d (%d nodes)", (rootIndex, childIndex, subTreeNodes))
            pruned += 1

        # continue to walk and prune all subtrees
        pruned += walkAndPrune(tree, childIndex)

    return pruned

# Function to count the number of verts given the root node
def countNodes(tree, rootIndex):
    numNodes = 1 # start with 1 for the root node of this subtree
    # For every child of the node
    for childIndex in tree[rootIndex]:
        # count all of it's children
        numNodes += countNodes(tree, childIndex)
    # return the number of nodes in this subtree
    return numNodes

# Let's see what we scanned in
log("verts: " + str(verts))
log("edges: " + str(edges))
log("len nodes: " + str(len(nodes)))
log("nodes: " + str(nodes))

# run the algorithm on the root node, output result
print walkAndPrune(nodes, 1)