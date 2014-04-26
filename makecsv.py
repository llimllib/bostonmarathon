#!/usr/bin/env python

import cPickle
import csv
import os
import re
import sys

TIME_RE = re.compile("^\d+:")

def minutes(time):
    """Convert a race time into minutes

    given a time in the format hh:mm:ss, return the number of minutes"""
    parts = [int(x) for x in time.split(':')]
    return parts[0] * 60 + parts[1] + parts[2]/60.

def bibsort(a):
    try:
        return int(a)
    except:
        return int(a[1:])

def main(year):
    dir_ = "results/{}".format(year)
    if not os.path.isdir(dir_):
        raise ValueError("Unable to find dir {}".format(dir_))

    results = cPickle.load(file("{}/results.pkl".format(dir_)))
    csvout = csv.writer(file("{}/results.csv".format(dir_), 'w'))

    first = results[results.keys()[0]]
    cols = first.keys()

    csvout.writerow(cols)

    for key in sorted(results, key=bibsort):
        row = []
        for col in cols:
            dat = results[key][col].encode("utf8")
            if TIME_RE.match(dat):
                dat = "{:.2f}".format(minutes(dat))
            row.append(dat)
        assert len(row) == len(cols)
        csvout.writerow(row)

if __name__ == "__main__":
    year = sys.argv[-1]
    main(year)
