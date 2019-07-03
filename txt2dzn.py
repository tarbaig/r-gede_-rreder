import sys

class Road:
    def __init__(self, line):
        self.id = line[0]
        triples = line[1:]
        self.triples = map(lambda x: x.split(':'), triples)

class Workcenter:
    def __init__(self, line):
        self.id = line[0]
        self.availableWorkers = line[1]

class Worksheet:
    def __init__(self, line):
        self.id = line[0]
        self.workcenter = line[1]
        self.mandatory = line[2]
        self.importance = line[3]
        self.east = line[4]
        self.last = line[5]
        self.duration = line[6]

        # Roads / activities
        roadIDend = 7+self.duration
        self.roadIDs = line[7:roadIDend]
        self.requiredWorkers = line[roadIDend:]

class MaximumBlockedConstraint:
    def __init__(self, l):
        self.maxBlocked = l[1]
        self.roadIDs = l[2:]

# Precedence constraints

class Instance:
    def __init__(self, f):
        # First line
        line = f.readLine().split()
        self.days = line[0]
        self.numRoads = line[1]
        self.numWorkCenters = line[2]
        self.numWorkSheets = line[3]
        self.numActivities = line[4]

        # Roads
        self.roads = []
        for i in range(self.numRoads):
            self.roads.append(Road(readSplitLine(f)))

        # Workcenters
        self.workcenters = []
        for i in range(self.numWorkCenters):
            self.workcenters.append(Workcenter(readSplitLine(f)))

        # Worksheets
        self.worksheets = []
        for i in range(self.numWorkSheets):
            self.worksheets.append(Worksheet(readSplitLine(f)))

        # Maximum blocked roads and precedence
        self.maximumBlocked = []
        # self.precedence
        while line in f:
            if line[0] == 'M':
                self.maximumBlocked.append(MaximumBlockedConstraint(line.split()))
                





def readSplitLine(f):
    return f.readLine().split()

expArgs = 1

if len(sys.argv) < 2:
    print("Too few arguments supplied")
    exit(1)

inFileName = sys.argv[1]

# print(inFileName)

inst = None


with open(inFileName) as f:
    inst = Instance(f)
