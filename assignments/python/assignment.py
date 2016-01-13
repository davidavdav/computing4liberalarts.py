#!/usr/bin/env python
# (c) 2016 David A. van Leeuwen

import json

def readstations(file="stations.csv"):
    stations = dict()
    csv = open(file)
    names = csv.readline().strip().split(",")
    for line in csv:
        words = line.strip().split(",")
        location = words[0]
        stations[location] = {names[i]:words[i] for i in range(1,len(words))}
    return stations

def collectrain(data):
    """Accumulate rain by month by location"""
    acc = dict()
    for x in data:
        station = x["station"]
        accpm = acc.get(station)
        if not accpm:
            acc[station] = [0.0 for i in range(12)]
            accpm = acc[station]
        year, month, day = [int(v) for v in x["date"].split("-")]
        accpm[month-1] += float(x["value"]) / 10
    return acc

def accpy(accpm):
    return {station:sum(rain) for station, rain in accpm.iteritems()}

## unused
def accoverstations(accpm):
    return [sum([accpm[station][i] for station in accpm]) for i in range(12)]

def relativerainpm(accpm):
    py = accpy(accpm)
    return {station:[rainpm / py[station] for rainpm in rain] for station, rain in accpm.iteritems()}

def relativerainps(accpy):
    tot = sum(accpy.values())
    return {station:accpy[station]/tot for station in accpy}

def makeoutput(stations, accpm):
    rel = relativerainpm(accpm)
    py = accpy(accpm)
    relpy = relativerainps(py)
    out = dict()
    for location, stationentry in stations.iteritems():
        station = stationentry["Station"]
        out[location] = {"station": station,
                         "relativePRCP": rel[station],
                         "state": stationentry["State"],
                         "PRCP": accpm[station],
                         "totalPRCP": py[station],
                         "locationPRCP": relpy[station]}
    return out

if __name__ == "__main__":
    stations = readstations()
    data = json.load(open("precipitation.json"))
    accpm = collectrain(data)
    out = makeoutput(stations, accpm)
    json.dump(out, open("result.json", "w"), indent=4, sort_keys=True)
