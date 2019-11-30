#!/usr/bin/env python
# coding: utf-8



import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

Session=sessionmaker(bind = engine)
session = Session()

###################################################

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")

def welcome():
    return(
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    print (precip)
    return jsonify(precip)

@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start,end):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)