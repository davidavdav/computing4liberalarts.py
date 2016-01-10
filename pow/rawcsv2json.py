#!/usr/bin/env python
# (c) 2016 David A. van Leeuwen

## This file converts a "raw" tye of csv file from the PoW database into a json.

## Specifically,
## - we use a short label (first line in the general CSV header)
## - "NULL" entries are simply left out
## - numbers are interpreted as numbers, not strings

import argparse, json, logging, csv, re, sys

floatre = re.compile("^\d+\.\d+$")
intre = re.compile("^\d+$")

def read_header(file="h.txt"):
    header=[]
    for line in open(file):
        header.append(line.strip())
    logging.info("%d lines in header", len(header))
    return header

def process_csv(file, header):
    out=[]
    stdin = file == "-"
    fd = sys.stdin if stdin else open(file)
    reader = csv.reader(fd)
    for nr, row in enumerate(reader):
        logging.debug("%d fields in line %d", len(row), nr)
        d = dict()
        out.append(d)
        for i, field in enumerate(row):
            if field != "NULL":
                if floatre.match(field):
                    d[header[i]] = float(field)
                elif intre.match(field):
                    d[header[i]] = int(field)
                else:
                    d[header[i]] = field.decode("utf-8")
    if not stdin:
        fd.close()
    return out

if __name__ == "__main__":
    p =argparse.ArgumentParser()
    p.add_argument("raw", nargs="*", default=["-"])
    p.add_argument("--header", type=str, default="h.txt")
    args = p.parse_args()
    logging.basicConfig(level=logging.INFO)
    header = read_header(args.header)
    out = []
    for file in args.raw:
        out += process_csv(file, header)
    print json.dumps(out, indent=4, ensure_ascii=False).encode("utf-8")

