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




















if __name__== '__main__':
    app.run(debug=True)