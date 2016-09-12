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
def main():
  devices = []
  for i in db.select("id from Trasto"):
    if len(i[0]) > 2 and str(i[0][0])=='F': devices.append(i[0])
  return render_template('main.html',devices=devices)

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

@app.route('/data/all/<device>')
@app.route('/data/all/<device>/<points>')
def all(device,points=100):
  outjson = []
  for t in ["Power","Temp1","Temp2"]:
    outjson.append({"label":"%s %s"%(t,device),"data":[]})
  max_results = int(points)
  for i in db.select("data,intensitat,tensio,temperatura1,temperatura2 from Lectura WHERE trasto_id=\"%s\" ORDER BY ID DESC LIMIT %d" %(device,max_results)):
    dt_human = i[0].strftime("%H:%M:%S %d/%m/%y")
    dt = time.mktime(i[0].timetuple()) *1000
    inte = float(i[1])
    volt = float(i[2])
    wats = inte * volt
    temp1 = float(i[3])
    temp2 = float(i[4])
    outjson[0]["data"].insert(0,[dt,wats])
    outjson[1]["data"].insert(0,[dt,temp1])
    outjson[2]["data"].insert(0,[dt,temp2])
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

@app.route('/chart/<device>')
@app.route('/chart/<device>/<points>')
def chart_all(device,points=100):
      return render_template('all.html',device=device,points=points)


@app.route('/chart/rt/intensity/<device>')
def i_chart_rt(device):
      return render_template('intensity_rt.html',device=device)


if __name__ == '__main__':
  app.run(host='0.0.0.0')
