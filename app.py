from flask import Flask, jsonify
import numpy as np
import pandas as pd

import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#####################################
########## Database Setup ###########

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
# https://docs.sqlalchemy.org/en/13/orm/extensions/automap.html

Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a Session
session = Session(engine)

#####################################
########## Flask Setup ###########

app = Flask(__name__)

#####################################
########## Flask Routes ###########

@app.route("/")
def welcome():
    return (
        f"Welcome to the Surfside Hawaii!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    year_ago

    # Perform a query to retrieve the data and precipitation scores

    prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    prcp_list = []

    for x in prcp_results:
        prcp_dict = {}
        prcp_dict[x[0]] = x[1]
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    # What are the most active stations? (i.e. what stations have the most rows)?

    most_active_results = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    most_active_list = []

    for x in most_active_results:
        station_dict = {}
        station_dict[x[0]] = x[1]
        most_active_list.append(station_dict)

    return jsonify(most_active_list)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data.
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    most_active_station = "USC00519281"
    
    most_active_temperature_results = session.query(Measurement.tobs).filter(Measurement.station == most_active_station).\
    filter(Measurement.date >= year_ago).all()

    most_active_temperature_list = []

    for x in most_active_temperature_results:
        tobs_dict = {}
        tobs_dict[x[0]] = x[0]
        most_active_temperature_list.append(tobs_dict)

    return jsonify(most_active_temperature_list)
























if __name__== '__main__':
    app.run(debug=True)