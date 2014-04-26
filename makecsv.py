#!/usr/bin/env python

import cPickle
import csv
import os
import sys

def main(year):
    dir_ = "results/{}".format(year)
    if not os.path.isdir(dir_):
        raise ValueError("Unable to find dir {}".format(dir_))

    results = cPickle.load(file("{}/results.pkl".format(dir_)))
    csvout = csv.writer(file("{}/results.csv".format(dir_), 'w'))

    first = results[results.keys()[0]]
    cols = first.keys()

    csvout.writerow(cols)

    for key in sorted(results):
        row = [results[key][col].encode("utf8") for col in cols]
        assert len(row) == len(cols)
        csvout.writerow(row)

if __name__ == "__main__":
    year = sys.argv[-1]
    main(year)
