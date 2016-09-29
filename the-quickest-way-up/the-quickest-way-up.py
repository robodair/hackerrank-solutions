import fileinput

def bfs(verts, tun, current):
    log("EXAMINING: %s", (str(current)))
    # store the verts for the next layer
    nextList = set([])
    # for every vert in the current layer
    for vert in current:
        log("at vert %d", (vert))
        if vert not in tun:
            if vert == 101:
                return 
            # for every child vert
            for child in verts[vert]:
                # if child has not already got a level assigned
                if child not in levels:
                    log("  child %d has no level yet, assigning %d", (child, levels[vert]+1))
                    # set the level for the child
                    levels[child] = levels[vert]+1
                    # create an edge entry from the child to the parent
                    edges[child] = vert
                    # add the child to the list of verts in the next array
                    nextList.add(child)

                else:
                    # if the child has already been linked to and the level is the same
                    log("  child %d of level %d HAS parent %d, we are at level %d", (child, levels[child], edges[child], levels[vert]+1))
                    if levels[child] >= levels[vert]+1:
                        log("   level of child is the same or above as what we are targeting")
                        # change the edge to link to this vert, if this vert is higher.
                        if vert > edges[child]:
                            edges[child] = vert 
                            levels[child] = levels[vert]+1
                            log("    changing it to have parent %d, changing level to %d", (vert, levels[child]))
                            # add the child to the list of verts in the next array
                            nextList.add(child)
                            
        else:
            log(" => skipping because this isn't a real node")
    if nextList:
        # call for the next vertex
        bfs(verts, tun, nextList)

def get_short_path(start, rolls=0):
    # if we're at the start, return
    if start == 1:
        log("found path with %d rolls", (rolls))
        return rolls
    elif start not in edges:
        # this has no way through
        return -1
    else:
        log("at %d, following to %d, current rolls %d", (start, edges[start], rolls))
        return get_short_path(edges[start], rolls+1)



def log(string, params=None):
    return
    if params:
        print string % params
    else:
        print string

ladders = False # Start false so it gets flipped to true on the first run

testCaseNumber = -1 # begin at -1 so first test case is 0
testCaseData = []

for line in fileinput.input():
    if line[0] == '#': # skip comment lines
        continue

    # Get number of testcases
    if fileinput.isfirstline():
        testCases = int(line)
        continue

    # if there is only one integer in line then we're about to listen to either snakes or ladders
    elif len(line.split(' ')) == 1:
        ladders = not ladders # flip ladders
        if ladders:
            testCaseNumber += 1 # move to next test case
            testCaseData.append({}) # add empty dictionary to test cases
        continue

    # fill the tunnel information
    testCaseData[testCaseNumber][int(line.split(" ")[0])] = int(line.split(" ")[1])

# For each test case
for tunnels in testCaseData:
    log("Testing a case: ")
    verticies = [set([]) for i in range(101)]
    # for every vert
    for i in range(1, 100):
        if i in tunnels:
            log(" square %d has no children! it's a tunnel", (i))
            continue
        log(" making children for vert %d", (i))
        # for every vert that this vert would link to
        for dest in range(1,7):
            if i+dest > 100:
                log("   square %d is off the board!", (i+dest))
                continue
            # does it link somewhere
            if (i+dest) in tunnels:
                log("   giving vert %d a child %d (%d is linked)", (i, tunnels[i+dest], dest+i))
                # enter the one it links to instead
                verticies[i].add(tunnels[i+dest])
            else:
                # enter the vert this would link to
                log("   giving vert %d a child %d", (i, i+dest))
                verticies[i].add(i+dest)
    
    edges = {} # dictionary of edges
    edges[1] = 0 # set up edge from start node to null node
    levels = {} # dictionary of levels
    # Begin at vert 1, assign level 1
    levels[1] = 1
    # find min number rolls for this vert set
    bfs(verticies, tunnels, set([1]))
    print get_short_path(100)
