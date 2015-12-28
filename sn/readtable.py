#!/usr/bin/env python
## (c) 2015 David A. van Leeuwen

## The oposite of create table, bu here were use pandas to read the csv, as plain csv is kind-of hard.

import pandas, argparse, re

def read(file):
    records = pandas.read_csv(file).to_dict("records") ## this is how we'd like to see the data
    return {r["id"]: r for r in records}

## a different way to do the same, this could be an exercise
def scan(file):
    fd = open(file, "r")
    line = fd.readline()
    columns = line.strip().split(",")
    columns = [c.strip('"') for c in columns]
    d = dict()
    intre = re.compile("^\d+$")
    for line in fd:
        fields = line.strip().split(",")
        r = dict()
        for i in range(0,len(fields)):
            v = fields[i]
            if v[0] == '"' and v[-1] == '"':
                v = v[1:-1]
            elif v == "NA":
                v = None
            elif intre.match(v):
                v = int(v)
            else:
                v = float(v)
            r[columns[i]] = v
        d[r["id"]] = r
    return d

## Test this
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("file")
    args = p.parse_args()

    print read(args.file)
    



