import database
import datetime
import calendar
import time
import random #testing
from flask import Flask
from flask import render_template
from flask import Response
from flask import jsonify

app = Flask(__name__)

db = database.database()

@app.route('/')
def hello_world():
  return 'Hello World!'

@app.route('/data/intensity/<trasto>')
@app.route('/data/intensity/<trasto>/<points>')
def intensity(trasto,points=100):
  outjson = {"label":"Intensity %s"%trasto,"data":[]}
  max_results = int(points)
  for i in db.select("data,intensitat from Lectura WHERE trasto_id=\"%s\" ORDER BY ID DESC LIMIT %d" %(trasto,max_results)):
    dt_human = i[0].strftime("%H:%M:%S %d/%m/%y")
    dt = time.mktime(i[0].timetuple()) *1000
    cu = float(i[1])
    outjson["data"].insert(0,[dt,cu])
  return jsonify(outjson)

@app.route('/data/intensity_rt/<trasto>')
def intensity_rt(trasto):
  outjson = {"data":[]}
  for i in db.select("data,intensitat from Lectura WHERE trasto_id=\"%s\" ORDER BY ID DESC LIMIT 5" %(trasto)):
    dt = time.mktime(i[0].timetuple()) *1000
    cu = float(i[1])
    outjson["data"].insert(0,[dt,cu])
  return jsonify(outjson)

@app.route('/chart/intensity/<device>')
@app.route('/chart/intensity/<device>/<points>')
def i_chart(device,points=100):
      return render_template('intensity.html',device=device,points=points)

@app.route('/chart/rt/intensity/<device>')
def i_chart_rt(device):
      return render_template('intensity_rt.html',device=device)


if __name__ == '__main__':
  app.run(host='0.0.0.0')
