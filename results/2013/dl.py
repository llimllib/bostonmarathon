import cPickle
import os
import sys
import time

import requests
from bs4 import BeautifulSoup

SEARCHURL = 'http://raceday.baa.org/2013/cf/public/iframe_ResultsSearch.cfm?mode=results'

def getbib(bib):
    """Get data for a bib number

    raises ConnectionError if there's trouble downloading the data
    raises ValueError if no runner with that bib number was found"""
    r = requests.post(SEARCHURL, {"BibNumber": bib})
    if r.status_code != 200:
        raise requests.ConnectionError

    soup = BeautifulSoup(r.text)
    table = soup.find("table", attrs={"class": "tablegrid_table"})
    rows = table.findAll("tr")

    bib, name, age, gender, city, state, country, ctz, _ = [t.text.strip() for t in rows[1].findAll("td")]

    k5, k10, k15, k20, half, k25, k30, k35, k40, pace, projected, official, overall, gender, division = [t.text.strip() for t in rows[2].findAll("td")][1:]

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
        "gender": gender,
        "division": division,
        "bib": bib,
        "name": name,
        "age": age,
        "city": city,
        "state": state,
        "country": country,
        "ctz": ctz
    }

class PartialResultsError(Exception):
    """wraps an exception and includes partial results"""
    def __init__(self, results, original_exc, traceback):
        Exception.__init__(self, "Partial Results Error")
        self.results = results
        self.original_exc = original_exc
        self.traceback = traceback

def getlist(lst, start=1):
    backoff = 1
    last = None
    results = {}
    try:
        for (i, elt) in enumerate(lst):
            if i>0 and i%100 == 0:
                # if we go through 100 bib #s and don't find a new one, assume we're done
                if last == len(results):
                    print "breaking, no new runners found"
                    break
                last = len(results)
                print i, len(results), elt

            try:
                result = getbib(elt)
            except requests.ConnectionError:
                print "failed on {}, backing off for {}".format(elt, backoff)
                time.sleep(backoff)
                backoff *= 2
                continue
            except ValueError:
                #if there's no runner with that bib number, we should get here
                continue

            backoff = 1

            results[elt] = result

    except:
        e = sys.exc_info()
        print "failed on bib #{}".format(elt)
        # pass on the results to main, but allow it to re-throw this error
        raise PartialResultsError(results, e[1], e[2])

    return results

def main():
    if os.path.isfile("results.partial.pkl"):
        results = cPickle.load(file("results.partial.pkl"))
    else:
        results = {}

    try:
        # the elite women have f# bibs
        print "elite women"
        fstart = max([int(x[1:]) for x in results.keys() if x.startswith("f")] + [1])
        results = getlist(['f%s'%i for i in range(fstart, 500)])

        ## the wheelchair runners have w# bibs
        print "wheelchair racers"
        wstart = max([int(x[1:]) for x in results.keys() if x.startswith("w")] + [1])
        results.update(getlist(['w%s'%i for i in range(wstart, 500)]))

        # the rest of the runners have # bibs
        print "the field"
        start = max([int(x) for x in results.keys() if isinstance(x, int)] + [1])
        results.update(getlist(range(start, 50000)))

    except PartialResultsError, e:
        results.update(e.results)
        cPickle.dump(results, open("results.partial.pkl", 'w'))
        raise e.original_exc, None, e.traceback

    # if we happen to break in between getlist() calls, dump the results
    except:
        cPickle.dump(results, open("results.partial.pkl", 'w'))
        raise

    cPickle.dump(results, open("results.pkl", 'w'))

if __name__ == "__main__":
    main()
