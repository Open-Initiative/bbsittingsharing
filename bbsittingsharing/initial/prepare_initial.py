from glob import glob
import csv, json, io

outfile = io.open("bbsittingsharing/fixtures/initial_data.json", "w+", encoding="utf-8")

object_list = []
for filename in glob('bbsittingsharing/fixtures/*.csv'):
    if filename == 'bbsittingsharing/fixtures/group.csv':
        model = 'auth.group'
    else:
        model = "bbsittingsharing." + filename.split('/')[-1].split('.')[0]
    infile = io.open(filename, encoding="utf-8")
    objects = list(csv.DictReader(infile))
    for fields in objects:
        object_list.append({'model': model, 'fields': fields})
outfile.write(json.dumps(object_list))
