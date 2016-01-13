#!/usr/bin/env python
# (c) 2016 David A. van Leeuwen

import json, csv

x = json.load(open("bar"))
with open("bar.csv", "w") as out:
    w = csv.DictWriter(out, ["state", "year"], extrasaction="ignore")
    w.writeheader()
    for row in x:
        w.writerow(row)

