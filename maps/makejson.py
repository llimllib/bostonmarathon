import json
import csv

meta = json.load(file("country_meta.json"))
pop = csv.reader(file("country_pop.csv"))

tempdata = {}
for country in meta:
    fields = country['fields']
    tempdata[fields['name'].title()] = {
        "id": fields['iso_3166_1_numeric'],
        "name": fields['name'].title(),
        "three": fields['iso_3166_1_a3']
    }

headers = pop.next()
for row in pop:
    row = [s.decode("utf8") for s in row]
    #assert row[1] in tempdata, "{} not in tempdata".format(row[1].encode('utf8'))
    if not row[1] in tempdata: continue

    tempdata[row[1]]['population'] = int(row[2].replace(",", ""))

outdata = {}
for key, val in tempdata.iteritems():
    if not 'population' in val:
        print "skipping", key
        continue
    outdata[val["id"]] = {
        "name": val['name'],
        "three": val['three'],
        "population": val["population"]
    }

fout = file("countrydata.json", 'w')
fout.write(json.dumps(outdata, indent=2))
