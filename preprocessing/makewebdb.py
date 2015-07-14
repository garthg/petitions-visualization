"""makewebdb.py -- Assembles final data file for Map View.

Copyright 2015 Garth Griffin
Distributed under the GNU GPL v3. For full terms see the file LICENSE.

This file is part of Antislavery Petitions Visualization.

Antislavery Petitions Visualization is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

Antislavery Petitions Visualization is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along with
Antislavery Petitions Visualization. If not, see <http://www.gnu.org/licenses/>.
________________________________________________________________________________

Author: Garth Griffin (http://garthgriffin.com)
Date: June 15, 2015

This script assembles a data structure for use in the Map View of Anti-Slavery
and Anti-Segregation Petitions.

The input files are constructed in other pre-processing steps, described below.

1. dataset_tsv
This is the output from the Antislavery Petitions processing pipeline, which
is available online at https://github.com/garthg/petitions-dataverse and is
constructed using antislaverypetitions.py from that repository:
  `
  python antislaverypetitions.py
    --input_tsv=petitions_spreadsheet.tsv
    --output_tsv=use_in_map_view.tsv 
    --contact_email=your_email@here.com
  `
This will write a file "use_in_map_view.tsv" that can be passed as dataset_tsv
for this script. A copy of the file is included in the root of this repository
as petition_dataset.tsv. See the petitions-dataverse repository for more
details.

2. latlng_tsv
This is the output of the geocoder.py script in this directory, which is run
as follows, using the same input file as above:
  `python geocoder.py use_in_map_view.tsv geocoder_cache.tsv`
This will write or incrementally update a file "geocoder_cache.tsv" that can be
passed as latlng_tsv for this script.

3. doi_tsv
This is a mapping of local dataset IDs in dataset_tsv to the online Dataverse
DOIs. It is generated from the update.py file in the Antislavery Petitions
processing pipeline, available online at
https://github.com/garthg/petitions-dataverse. A copy of the output is included
in this repository at preprocessing/local_id_to_doi.tsv. See the
petitions-dataverse repository for more details.

4. outfile
This is path to write the output. It will write a json file suitable for use in
the Map View web application. In this repository, that should be written to
web/static/data/mapviewdb.json.

Input arguments summary (passed in order on command line):
  dataset_tsv: Tab-delimited dataset, one entry per row.
  latlng_tsv: Tab-delimited file with latitude/longitude coordinates for places.
  doi_tsv: Tab-delimited file mapping Local IDs to Dataverse DOIs for dataset.
  outfile: Path to write the output data structure as JSON.

See run_preprocessing.sh script in the root of this repository for an example
invocation of this script.
"""
import sys
import re
import collections
import json
import tsvfile

dataset_tsv = sys.argv[1]
latlng_tsv = sys.argv[2]
doi_tsv = sys.argv[3]
outfile = sys.argv[4]

rows = tsvfile.ReadDicts(dataset_tsv)
print 'Read %d dataset rows from file: %s' % (len(rows), dataset_tsv)
latlng_rows = tsvfile.ReadDicts(latlng_tsv)
print 'Read %d lat-lng pairs from file: %s' % (len(latlng_rows), latlng_tsv)

# Example output as json:
# {
#   "latlngForPlace": {
#     "Boston": [42.000, 57.000],
#     ...
#   },
#   "rowsForYear": {
#     1845:[17,18,...],
#     ...
#   },
#   "rowsForPlace": {
#     "42.000,57.000":[3,12,...],
#     ...
#   },
#   "rows": [
#     {
#       "creation date": "1843-01-25", 
#       "dataverse id": "doi:10.7910/DVN/IQDMG", 
#       "location": "Hopedale", 
#       "pds url": "http://nrs.harvard.edu/urn-3:FHCL:11005498", 
#       "people": [ "Adin Ballou",  "Abby H. Price" ], 
#       "signatures": 2, 
#       "time end": "1843-01-25", 
#       "time start": "1843-01-25", 
#       "title": "House Unpassed Legislation 1843, Docket 1290A, ...",
#       "topic": "Against the fugitive slave laws"
#     },
#     ...
#   ]
# }
#

simple_row_transforms = [
    ('Publication URL', 'pds url'),
    ('Geographic Coverage', 'location', '(unknown location)'),
    ('Production Date', 'creation date'),
    ('Time Period Covered End', 'time end'),
    ('Time Period Covered Start', 'time start'),
    ('Title', 'title', '(untitled)'),
    ]

output = {}

doi_rows = tsvfile.ReadDicts(doi_tsv)
print 'Read %d doi rows from file: %s' % (len(doi_rows), doi_tsv)
doi_dict = dict([(x['Local ID'], x['DOI'])
  for x in doi_rows])

def field_from_description(description_text, field):
  target_re = re.compile('<p>'+field+': ?([^<]*) </p>')
  result = re.search(target_re, description_text)
  if not result:
    print 'WARNING: Failed to find field: %s' % field
    return None
  return result.groups(0)[0]

output_rows = []
output_doi_rows = []
ctr = 0
for row in rows:
  # Initialize empty dict to store the formatted row data for this row.
  ctr += 1
  output_row = {}
  # Copy some fields directly.
  for x in simple_row_transforms:
    if x[0] not in row or not row[x[0]] and len(x) == 3:
      output_row[x[1]] = x[2]
    else:
      output_row[x[1]] = row[x[0]]
    #output_row[x[1]] = row[x[0]]
  # Prepare to parse the remainder of the output fields from the Description.
  description = row['Description']
  # Topic parsed from Description.
  output_row['topic'] = field_from_description(description, 'Petition subject')
  if not output_row['topic']:
    print 'WARNING: Row %d: Failed to parse topic' % ctr
    output_row['topic'] = '(unknown topic)'
  # People parsed from Description.
  description_people = re.sub(r'</li>','|',
      re.sub(r'</?ol>', '', re.sub(r'<li>', '', description)))
  people_raw = field_from_description(description_people, 'Selected signatures')
  if not people_raw:
    print 'WARNING: Row %d: Failed parsing people on row.' % ctr
    output_row['people'] = []
  else:
    people = filter(None, people_raw.split('|'))
    output_row['people'] = people
  # Signature count from Descripiont.
  signatures = field_from_description(description, 'Total signatures')
  if not signatures:
    print 'WARNING: Row %d: No signature count.' % ctr
    if output_row['people']:
      output_row['signatures'] = len(output_row['people'])
    else:
      output_row['signatures'] = 0
  else:
    output_row['signatures'] = int(re.sub(r'[^0-9]','',signatures))
  # PDS URL of the original petitions from Description.
  # Must parse the PDS URL. If not available, we will skip this row.
  pds_url = None
  if row['Local ID'] in doi_dict:
    pds_url = doi_dict[row['Local ID']]
  else:
    print 'ERROR. Skipping row %d. No DOI for local ID: %s' % (
        ctr, row['Local ID'])
    continue
  output_row['dataverse id'] = pds_url
  # If we got this far, append the output row.
  output_rows.append(output_row)
output_rows.sort(key=lambda x: x['time start'])
output['rows'] = output_rows

# Build latitude/longitude index.
latlng_dict = dict(map(
  lambda x: ((x[0] if x[0] else 'None'), (
    float(x[1]['latitude']), float(x[1]['longitude']))),
  tsvfile.GroupByUnique(latlng_rows, 'name').items()))
output['latlngForPlace'] = latlng_dict

# Build year and place indexes.
rows_for_year = collections.defaultdict(set)
rows_for_place = collections.defaultdict(set)
for i in xrange(len(output_rows)):
  row = output_rows[i]
  if row['time start']:
    time_start = re.sub('[^0-9 ]','',re.sub('-',' ',row['time start']))
    time_end = re.sub('[^0-9 ]','',re.sub('-',' ',row['time end']))
    for j in xrange(int(time_start[:4]),int(time_end[:4])+1):
      rows_for_year[j].add(i)
  else:
    rows_for_year['None'].add(i)
  row['location'] = row['location'].strip('[]?')
  location = row['location']
  if not location:
    location = '(unknown location)'
  rows_for_place[location].add(i)
for r in rows_for_year: rows_for_year[r] = sorted(list(rows_for_year[r]))
output['rowsForYear'] = rows_for_year 
for r in rows_for_place: rows_for_place[r] = sorted(list(rows_for_place[r]))
output['rowsForPlace'] = rows_for_place 

# Write output.
output_string = json.dumps(output)
with open(outfile, 'wb') as fid:
  fid.write(output_string)
print 'Wrote %d characters to file: %s' % (len(output_string), outfile)

