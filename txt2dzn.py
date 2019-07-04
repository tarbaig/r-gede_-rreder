import sys
import time

class Road:
    def __init__(self, line):
        self.id = int(line[0])
        triples = line[1:]
        self.triples = list(map(lambda trip:
                                list(map(int, trip.split(':'))), triples))

    def pertubationList(self):
        res = []
        for (start,end,cost) in self.triples:
            diff = end-start
            part = [cost]*diff
            res += part
        return res


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

def strNumWorksheets(inst):
    return "n_work_sheets = %d;" % (inst.numWorkSheets)

def strNumActivities(inst):
    numActivities = sum([ws.duration for ws in inst.worksheets])
    return "m_activities = %d;" % (numActivities)

def strHorizon(inst):
    return "horizon = %d;" % (inst.days)

def strRoads(inst):
    return "l_roads = %d;" % (inst.numRoads)

def strEast(inst):
    easts = [str(ws.east) for ws in inst.worksheets]
    return "east = [" + ",".join(easts) + "];"

def strLast(inst):
    lasts = [str(ws.last) for ws in inst.worksheets]
    return "last = [" + ",".join(lasts) + "];"

def strPrecedences(inst):
    precs = []
    for ws in inst.worksheets:
        befs = [str(bef) for (bef,af) in inst.precedenceConstraints if ws.id == af]
        foo = "{" + ",".join(befs) + "}"
        precs.append(foo)
    return "precedence = [" + ",".join(precs) + "];"

def strDurations(inst):
    durations = [str(ws.duration) for ws in inst.worksheets]
    return "duration = [" + ",".join(durations) + "];"

def strActivitiesRoads(inst):
    as2rs = []
    for ws in inst.worksheets:
        as2rs += [str(r) for r in ws.roadIDs]
    return "activities_to_roads = [" + ",".join(as2rs) + "];"

def strPertubationCosts(inst):
    perts = "pertubation_cost =\n [| "

    # First l-1 roads
    for i in range(len(inst.roads)-1):
        road = inst.roads[i]
        assert len(road.pertubationList()) == inst.days

        for c in road.pertubationList():
            perts += str(c) + ","
        perts += "\n  | "

    # Last road
    road = inst.roads[len(inst.roads)-1]
    pert = [str(c) for c in road.pertubationList()]
    perts += ",".join(pert)
    perts += " |];"
    return perts

def strSheetFirstAct(inst):
    actCount = 0
    starts = []
    for ws in inst.worksheets:
        starts += str(actCount)
        actCount += ws.duration
    return "sheet_to_first_act = [" + ",".join(starts) + "];"

def strAct2Sheet(inst):
    res = []
    for ws in inst.worksheets:
        res += [str(ws.id) for i in range(ws.duration)]
    return "act_to_sheet = [" + ",".join(res) + "];"

def createOutputFile(inst, outPath):
    with open(outPath, "w") as outF:
        outF.write(strNumWorksheets(inst))
        outF.write("\n")
        outF.write(strNumActivities(inst))
        outF.write("\n")
        outF.write(strHorizon(inst))
        outF.write("\n")
        outF.write(strRoads(inst))
        outF.write("\n")
        outF.write(strEast(inst))
        outF.write("\n")
        outF.write(strLast(inst))
        outF.write("\n")
        outF.write(strPrecedences(inst))
        outF.write("\n")
        outF.write(strDurations(inst))
        outF.write("\n")
        outF.write(strActivitiesRoads(inst))
        outF.write("\n")
        outF.write(strPertubationCosts(inst))
        outF.write("\n")
        outF.write(strSheetFirstAct(inst))
        outF.write("\n")
        outF.write(strAct2Sheet(inst))


def main():
    expArgs = 1

    if len(sys.argv) < 3:
        print("Too few arguments supplied")
        exit(1)

    inFileName = sys.argv[1]
    outFileName = sys.argv[2]

    # print(inFileName)

    inst = None

    with open(inFileName) as f:
        inst = Instance(f)

    starttime = time.time()
    inst.findImpliedPrecedenceConstraints()
    endtime = time.time()
    print("Finding implied: %f" % (endtime-starttime))

    createOutputFile(inst, outFileName)


    # print(inst.workcenters[0].availableWorkers)


if __name__ == '__main__':
    main()
