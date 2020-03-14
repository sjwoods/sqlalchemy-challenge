import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from statistics import mean

from flask import Flask, jsonify

postgresStr = "postgresql://postgres:password@localhost:5432/Hawaii"
engine = create_engine(postgresStr)
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurements
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)
@app.route("/")
def welcome():
    return(
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/May26"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation"""
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    precip = list(np.ravel(results))
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for previous year."""
    results = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').all()
    temps = list(np.ravel(results))
    return jsonify(temps)

@app.route("/api/v1.0/temp/May26")
def stats():
    """Return TMIN, TAVG, TMAX."""
    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= '2016-05-26').all()
    temps = list(np.ravel(results)) 
    #print(temps)
    highest = max(temps)
    lowest = min(temps)
    average = mean(temps)
    return (
        f"Highest temperature {highest}<br>"
        f"Lowest temperature {lowest}<br>"
        f"Avg temperature {average}<br>"
    )

if __name__ == '__main__':
    app.run()