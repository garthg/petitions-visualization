# run_preprocessing.sh -- Example invocation of preprocessing/makewebdb.py.
# 
# Copyright 2015 Garth Griffin
# Distributed under the GNU GPL v3. For full terms see the file LICENSE.
#
# This file is part of Antislavery Petitions Visualization.
# 
# Antislavery Petitions Visualization is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
# 
# Antislavery Petitions Visualization is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with
# Antislavery Petitions Visualization.  If not, see 
# <http://www.gnu.org/licenses/>.
# _____________________________________________________________________________
#
# Author: Garth Griffin
# Date: July 14, 2015
#
# This script shows an example invocation of the makewebdb.py script for
# assembling the data structures behind the visualization. For more extensive
# documentation of the inputs, see preprocessing/makewebdb.py in this
# repository.
#
inputrows=petition_dataset.tsv  # Input dataset from petitions-dataverse.
inputlatlng=preprocessing/geocoder_cache.tsv   # Geocoder output.
inputdoi=preprocessing/local_id_to_doi.tsv  # DOI map from petitions-dataverse.
outfile=web/static/data/mapviewdb.json  # Output file.
logfile=preprocessing/run_preprocessing_log.txt  # Log file.
cd `dirname $0`
echo "$0 invoked `date`" > $logfile
cmd="python preprocessing/makewebdb.py \
  $inputrows \
  $inputlatlng \
  $inputdoi \
  $inputdoioverrides \
  $outfile \
  2>&1 | tee -a $logfile"
echo "$cmd"
eval "$cmd"
