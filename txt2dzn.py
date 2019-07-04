import sys
import time

class Road:
    def __init__(self, line):
        self.id = int(line[0])
        triples = line[1:]
        self.triples = list(map(lambda trip:
                                list(map(int, trip.split(':'))), triples))


class Workcenter:
    def __init__(self, line):
        line = lineToIntList(line)
        self.id = line[0]
        self.availableWorkers = line[1]


class Worksheet:
    def __init__(self, line):
        line = lineToIntList(line)
        self.id = line[0]
        self.workcenter = line[1]
        self.mandatory = line[2]
        self.importance = line[3]
        self.east = line[4]
        self.last = line[5]
        self.duration = line[6]

        # Roads / activities
        roadIDend = 7 + self.duration
        self.roadIDs = line[7:roadIDend]
        self.requiredWorkers = line[roadIDend:]


class MaximumBlockedConstraint:
    def __init__(self, l):
        l = lineToIntList(l[1:])
        self.maxBlocked = l[0]
        self.roadIDs = l[1:]


# Precedence constraints
class PrecedenceConstraint:
    def __init__(self, b, a):
        self.before = b
        self.after = a

    def toTuple(self):
        return (self.before, self.after)

    def fromLine(l):
        l = lineToIntList(l[1:])
        return PrecedenceConstraint(l[0],l[1])


class Instance:
    def __init__(self, f):
        # First line
        line = readSplitLine(f)
        line = lineToIntList(line)
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
        self.precedenceConstraints = set()

        for line in f:
            if line[0] == 'M':
                self.maximumBlocked.append(MaximumBlockedConstraint(line.split()))
            elif line[0] == 'P':
                self.precedenceConstraints.add(PrecedenceConstraint.fromLine(line.split()).toTuple())

    def findImpliedPrecedenceConstraints(self):
        changed = True
        oldSet = self.precedenceConstraints.copy()
        newSet = None
        while changed:  # Supposed to be a fixpoint calculation
            changed = False

            implied = [(bef1, af2)
               for (bef1, af1) in oldSet
               for (bef2, af2) in oldSet
               if af1 == bef2]

            newSet = oldSet.copy().union(set(implied))

            if oldSet != newSet:
                changed = True
                oldSet = newSet

        self.precedenceConstraints = newSet


def readSplitLine(f):
    return f.readline().split()


def lineToIntList(line):
    return list(map(int, line))


def main():
    expArgs = 1

    if len(sys.argv) < 2:
        print("Too few arguments supplied")
        exit(1)

    inFileName = sys.argv[1]

    # print(inFileName)

    inst = None

    with open(inFileName) as f:
        inst = Instance(f)

    starttime = time.time()
    inst.findImpliedPrecedenceConstraints()
    endtime = time.time()
    print("Finding implied: %f" % (endtime-starttime))



    # print(inst.workcenters[0].availableWorkers)


if __name__ == '__main__':
    main()
