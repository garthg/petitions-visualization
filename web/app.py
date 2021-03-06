"""app.py -- Bare bones Flask server to serve homepage and Map View.

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
Antislavery Petitions Visualization.  If not, see
<http://www.gnu.org/licenses/>.
________________________________________________________________________________

Author: Garth Griffin (http://garthgriffin.com)
Date: July 9, 2015.

This is a minimal Flask server. It is actually just reading in the template 
files and then sending them out to the client, there is no template logic used
in the rendering. Its purposes are to support the specification of custom URLs
and to enable easy deployment of the Map View prototype via Flask cloud
services.

Related files:

templates/home.html
This is simple a placeholder html page to be replaced with a real homepage
at a later date.

templates/mapview.html
This document contains the entirety of the Map View user interface, including
the html document structure, CSS styling, third-party loaded CSS and JavaScript
libraries, and custom JavaScript for user interaction.

static/data/mapviewdb.json
This file is generated by the preprocessing code, and contains all the data
necessary to render the user interface and link it to the dataset in Dataverse.
"""
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/map')
def mapview():
  return render_template('mapview.html')

if __name__ == '__main__':
  app.run()
  #app.run(debug=True)
