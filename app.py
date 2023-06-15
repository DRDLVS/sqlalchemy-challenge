import os
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
#################################################


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask("__name__")
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return '''
    Welcome to the Climate App
    <br/>
    <br/>
    <br/>
    Available Routes:
    <br/>
    <br/>
    <a href="/api/v1.0/precipitation">&#8226; /api/v1.0/precipitation</a>
    <br/>
    <a href="/api/v1.0/stations">&#8226; /api/v1.0/stations</a>
    <br/>
    <a href="/api/v1.0/tobs">&#8226; /api/v1.0/tobs</a>

    '''
    
#########################################################################################

@app.route("/api/v1.0/precipitation")

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#########################################################################################

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = [row[0] for row in results]
    return jsonify(stations)

if __name__ == '__main__':
    app.run(debug=True)
#########################################################################################

@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#########################################################################################

if __name__ == '__main__':
    app.run(debug=True)



