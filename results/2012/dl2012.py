import cPickle
import os
import time

import requests
from bs4 import BeautifulSoup

url = 'http://raceday.baa.org/2013/cf/public/iframe_ResultsSearch.cfm?mode=results'

if os.path.isfile("results2012.partial.pkl"):
    results = cPickle.load(file("results2012.partial.pkl"))
else:
    results = {}

backoff = 1
start = max(results.keys())+1 if results else 1
for i in range(start, 50000):
    try:
        if i%100 == 0:
            print i, max(results.keys())

        try:
            r = requests.post(url, {"BibNumber": i, "RaceYearLowID": 2012, "RaceYearHighID": 0})
        except requests.ConnectionError:
            print "failed on {}, backing off for {}".format(i, backoff)
            time.sleep(backoff)
            backoff *= 2
            continue

        if r.status_code != 200:
            print "failed on {}, backing off for {}".format(i, backoff)
            time.sleep(backoff)
            backoff *= 2
            continue

        backoff = 1

        soup = BeautifulSoup(r.text)
        table = soup.find("table", attrs={"class": "tablegrid_table"})
        rows = table.findAll("tr")
        try:
            bib, name, age, gender, city, state, country, ctz, _ = [t.text.strip() for t in rows[1].findAll("td")]
        except ValueError:
            #if there's no runner with that bib number, we should get here
            continue

        k5, k10, k15, k20, half, k25, k30, k35, k40, pace, projected, official, overall, genderclass, division = [t.text.strip() for t in rows[2].findAll("td")][1:]

        results[i] = {
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
            "genderclass": genderclass,
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
    except:
        print "failed on bib #{}".format(i)
        cPickle.dump(results, open("results2012.partial.pkl", 'w'))
        raise

cPickle.dump(results, open("results2012.pkl", 'w'))
