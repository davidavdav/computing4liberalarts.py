#!/usr/bin/env python

import gzip, csv, re, os

yearre = re.compile("(\d{4})-")

dest = "pfw/years"

with gzip.open("pfw/raw/Person.csv.gz") as fd:
    reader = csv.reader(fd)
    for i, row in enumerate(reader):
        if i<4:
            continue
        name = row[1]
        date = row[52]
        if "NULL" in [name, date]:
            continue
        #        for j, v in enumerate(row):
        #   if v != "NULL":
        #       print j, v
        m = yearre.search(date)
        if m:
            year = m.groups(0)[0]
            f = os.path.join(dest, year)
            with open(f, "a") as out:
                writer = csv.writer(out, quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow(row)
            print name, year
