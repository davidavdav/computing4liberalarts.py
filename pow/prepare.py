#!/usr/bin/env python

## Read the wikipedia person.csv database, and split by birth year (if found)
## Reading everything into memory, first, for speed efficiency reasons, does not work.
## Keeping open files for every year, does not work, as there are too many open files.
## Therefore we flush the file for a year every 1000 lines or so

import gzip, csv, re, os, sys

yearre = re.compile("(-?\d{4})-")

dest = "pfw/years"

years = dict()
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
            yearlist = years.get(year)
            if not yearlist:
                yearlist = []
                years[year] = yearlist
            yearlist.append(row)
            if len(yearlist)>1000:
                with open(os.path.join(dest, year), "a") as out:
                    writer = csv.writer(out, quoting=csv.QUOTE_NONNUMERIC)
                    writer.writerows(yearlist)
                years[year] = []
                print name, year

sys.stdout.write("Writing remainders to disc")
for year in years:
    f = os.path.join(dest, year)
    with open(f, "a") as out:
        writer = csv.writer(out, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(years[year])
        sys.stdout.write(".")
        sys.stdout.flush()
print "done"
