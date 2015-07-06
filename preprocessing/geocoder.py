"""tsvfile.py -- Helper methods for tabular data in tab-delimited files.

Copyright 2015 Garth Griffin
Distributed under the GNU GPL v3. For full terms see the file LICENSE.

This file is part of PetitionsVisualization.

PetitionsVisualization is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

PetitionsVisualization is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
PetitionsVisualization.  If not, see <http://www.gnu.org/licenses/>.
________________________________________________________________________________

Author: Garth Griffin (http://garthgriffin.com)
Date: July 6, 2015. 

This script uses the Google Geocoding API to geocode locations.

Usage:
  python geocoder.py <input_tsv> <output_tsv>

where <input_tsv> is a tab-delimited file with a column "Geographic Coverage"
containing location names.

It will add new rows to the tab-delimted file <output_tsv> with one row for
each successfully-geocoded unique location in the input, with the following four
columns:
  latitude: The geocoded latitude.
  longitude: The geocoded longitude.
  name: The input name.
  parsed: The parsed location as reported by the Google Geocoding API.

For more information on the Google Geocoding API:
https://developers.google.com/maps/documentation/geocoding/
"""
import sys
from datetime import datetime
import time
import httplib2
import traceback
import json
import os
import tsvfile

infile = sys.argv[1]
lookup_file = sys.argv[2]

input_col = 'Geographic Coverage'

curr_map = {}
curr_map_rows = []
if os.path.isfile(lookup_file):
  print 'Loading lookup table from file: %s' % lookup_file
  curr_map_rows = tsvfile.ReadDicts(lookup_file)
  curr_map = tsvfile.GroupByUnique(curr_map_rows, 'name')
  print 'Loaded %d lookup entries.' % len(curr_map)

QUERY_BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address='

rows = tsvfile.ReadDicts(infile)
http = httplib2.Http()

ctr = 0
total_http = 0
should_sleep = False
for row in rows:
  ctr += 1
  print '%d/%d' % (ctr, len(rows))
  location = None
  curr_latlng = None
  output = {}
  try:
    location = row[input_col]
    if location in curr_map:
      print 'Cache hit for location: %s' % location
      continue
    print 'Running query for location: %s' % location
    query = location+' Massachusetts USA'
    query = query.replace(' ', '%20')
    query = '%22'+query+'%22'
    query_url = QUERY_BASE_URL + query
    if should_sleep:
      time.sleep(1)
      should_sleep = False
    if total_http > 2000:
      print '%s: Ran 2000 http requests, wait 24 hours before continuing.' % (
          datetime.utcnow())
      sys.exit(0)
    resp, content = http.request(query_url)
    should_sleep = True
    total_http += 1
    if not resp['status'] == '200':
      print 'Http error with row %d with location: %s' % (ctr, location)
      continue
    data = json.loads(content)
    if not data['status'] == 'OK':
      print 'Result error with row %d with location: %s' % (ctr, location)
      continue
    results = data['results']
    if len(results) == 0:
      print 'No match found for row %d with location: %s' % (ctr, location)
      continue
    if len(results) > 1:
      print 'WARNING: Using first of multiple matches for location %s: %s' % (
          location, str(results))
    match = results[0]
    latlng_data = match['geometry']['location']
    output['name'] = location
    output['parsed'] = match['formatted_address']
    output['latitude'] = latlng_data['lat']
    output['longitude'] = latlng_data['lng']
  except KeyboardInterrupt: raise KeyboardInterrupt
  except SystemExit: raise SystemExit
  except:
    print 'Error with row %d with location: %s' % (ctr, location)
    print traceback.format_exc()
  if output:
    curr_map[location] = output
    curr_map_rows.append(output)
    tsvfile.WriteDicts(lookup_file, curr_map_rows, '.tmp-geocode-file.tsv')
  print 'Total http requests sent: %d' % total_http
print '%s: finished. Total http requests sent: %d' % (datetime.utcnow(),
    total_http)
