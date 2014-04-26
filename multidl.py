#!/usr/bin/env python

import cPickle
import multiprocessing
import os
import sys
import time

import requests
from bs4 import BeautifulSoup

ARCHIVEURL = 'http://registration.baa.org/cfm_Archive/iframe_ArchiveSearch.cfm?mode=results&RequestTimeout=600&snap=47418326&'
_2014URL = 'http://raceday.baa.org/2014/cf/public/iframe_ResultsSearch.cfm?mode=results'

def bibworker(bibyear):
    try:
        bib, year = bibyear
        return getbib(bib, year)
    except KeyboardInterrupt:
        return {}

def getbib(bib, year, backoff=1):
    """Get data for a bib number

    raises ValueError if no runner with that bib number was found"""
    fourteen = True if year == "2014" else False
    try:
        url = _2014URL if fourteen else ARCHIVEURL
        r = requests.post(url, {"BibNumber": bib, "RaceYearLowID": year, "RaceYearHighID": 0})
        if r.status_code != 200:
            raise requests.ConnectionError
    except requests.ConnectionError:
        print "failed on {}, backing off for {}".format(bib, backoff)
        if backoff < 128:
            time.sleep(backoff)
            return getbib((bib, year), backoff*2)
        else:
            print "completely unable to parse {}".format(bib)
            return {}

    soup = BeautifulSoup(r.text)
    table = soup.find("table", attrs={"class": "tablegrid_table"})
    rows = table.findAll("tr")

    try:
        if fourteen:
            bib, name, age, gender, city, state, country, ctz, _ = [t.text.strip() for t in rows[1].findAll("td")]
            k5, k10, k15, k20, half, k25, k30, k35, k40, pace, projected, official, overall, genderdiv, division = [t.text.strip() for t in rows[2].findAll("td")][1:]
            return {
                "5k": k5,
                "10k": k10,
                "20k": k20,
                "half": half,
                "25k": k25,
                "30k": k30,
                "35k": k35,
                "40k": k40,
                "pace": pace,
                "official": official,
                "overall": overall,
                "genderdiv": genderdiv,
                "division": division,
                "bib": bib,
                "name": name,
                "age": age,
                "gender": gender,
                "city": city,
                "state": state,
                "country": country,
                "ctz": ctz
            }
        else:
            _, bib, name, age, gender, city, state, country, _ = [t.text.strip() for t in rows[1].findAll("td")]
            overall, genderdiv, division, official, net = [t.text.strip() for t in rows[2].findAll("td")][1:]
            return {
                "overall": overall,
                "genderdiv": genderdiv,
                "division": division,
                "official": official,
                "net": net,
                "bib": bib,
                "name": name,
                "age": age,
                "gender": gender,
                "city": city,
                "state": state,
                "country": country,
            }
    except ValueError:
        # there is no runner at this bib #
        return {}

class PartialResultsError(Exception):
    """wraps an exception and includes partial results"""
    def __init__(self, results, original_exc, traceback):
        Exception.__init__(self, "Partial Results Error")
        self.results = results
        self.original_exc = original_exc
        self.traceback = traceback

def getlist(lst, year):
    processpool = multiprocessing.Pool(5)
    lst = [(l, year) for l in lst]
    results = {}
    nils = 0
    n = 0
    lastbib = 0
    try:
        for result in processpool.imap(bibworker, lst):
            if result:
                lastbib = result['bib']
                results.update({result['bib']: result})

            n += 1
            if n % 100 == 0: print n, lastbib

            if result == {}:
                nils += 1
            else:
                nils = 0

            # if we get 100 misses in a row, assume we're past the end
            #if nils > 500:
            #    break
    except:
        processpool.terminate()
        e = sys.exc_info()
        # pass on the results to main, but allow it to re-throw this error
        raise PartialResultsError(results, e[1], e[2])

    return results

def main(year):
    dir_ = "results/{}".format(year)
    if not os.path.isdir(dir_):
        os.mkdir(dir_)

    full = "{}/results.pkl".format(dir_)
    partial = "{}/results.partial.pkl".format(dir_)
    if os.path.isfile(partial):
        results = cPickle.load(file(partial))
    else:
        results = {}

    try:
        # the elite women have f# bibs
        fstart = max([int(x[1:]) for x in results.keys() if x.startswith("f")] + [1])
        print "elite women, starting at {}".format(fstart)
        results.update(getlist(['f%s'%i for i in range(fstart, 500)], year))

        ## the wheelchair runners have w# bibs
        wstart = max([int(x[1:]) for x in results.keys() if x.startswith("w")] + [1])
        print "wheelchair racers, starting at {}".format(wstart)
        results.update(getlist(['w%s'%i for i in range(wstart, 500)], year))

        # the rest of the runners have # bibs
        start = max([int(x) for x in results.keys() if x.isdigit()] + [1])
        print "the field, starting at {}".format(start)
        results.update(getlist([str(x) for x in range(start, 50000)], year))

    except PartialResultsError, e:
        results.update(e.results)
        cPickle.dump(results, open(partial, 'w'))
        raise e.original_exc, None, e.traceback

    # if we happen to break in between getlist() calls, dump the results
    except:
        cPickle.dump(results, open(partial, 'w'))
        raise

    cPickle.dump(results, open(full, 'w'))

if __name__ == "__main__":
    year = sys.argv[-1]
    main(year)
