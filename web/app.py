from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello():
  return '<html><body>Homepage<br><a href="/map">Map</a></body></html>'

@app.route('/map')
def mapview():
  return render_template('mapview.html')

if __name__ == '__main__':
  app.run()
  #app.run(debug=True)
