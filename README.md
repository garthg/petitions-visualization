# Antislavery Petitions Visualization

Author: Garth Griffin (http://garthgriffin.com)  
Date: July 10, 2015  

This project builds on the work of the Antislavery Petitions Massachusetts
Dataverse [1]. The current deployment is for a Map View that enables easy
geographic and temporal exploration of the dataset. A live demo is available
at http://antislaverypetitions.pythonanywhere.com or you can run the demo
locally by following the instructions in the Usage section of this README.
A detailed writeup of the project will be made available as well.

The project has been done in collaboration with Radcliffe Institute for
Advanced Study [2] and with help from the Harvard Institute of Quantitative
Social Science [3].


## Usage:

The web application uses Flask. To install the dependencies, run:  
`pip install flask httplib2`

To run the demo locally, cd to this directory and run:   
`python web/app.py`

Running the development server should make the app available at
http://localhost:5000 in your web browser.

To make updates to the dataset underlying the application, use the code
pipeline in the preprocessing/ directory:
geocoder.py -- For geocoding locations.
makewebdbpy -- For assemebling the data file used in the web application.

Implementation details will be available in the detailed writeup.


## Acknowledgements:

Supported by the National Endowment for the Humanities (PW-5105612),
Massachusetts Archives of the Commonwealth, Radcliffe Institute for Advanced
Study at Harvard University, Center for American Political Studies at Harvard
University, Institutional Development Initiative at Harvard University, and
Harvard University Library.


## Copyright and license:

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

Please see the file LICENSE for the license text.


## Links:

[1] https://github.com/garthg/petitions-dataverse  
[2] https://www.radcliffe.harvard.edu/  
[3] http://www.iq.harvard.edu/  
