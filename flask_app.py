

import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from flask import Flask, jsonify
import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
print(Base.classes.keys())


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Code from Jupyter Notebook file

app = Flask(__name__)




@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to the Surf's Up Hawaii weather page!<br/>"
        f"Available Routes<br/>"
        f"Precipitation:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"Stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"Temperature observations for the previous year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"All dates greater than the start date:<br/>"
        f"/api/v1.0/<start><br/>"
        f"All dates between selected start date and end date:<br/>"
        f"/api/v1.0<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
       
    # max date 
    maxdate = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).limit(1).all()
    maxdatedate = maxdate[0][0]
    maxdatedate
    #maxdatedate = (2017,8,23)
    # Calculate the date 1 year ago from the last data point in the database
    lastyear = dt.date(2017,8,23) - dt.timedelta(days=365)
    lastyear
    #lastyear = (2016,08,23)

    # Perform a query to retrieve the data and precipitation scores
    pastyeardata = session.query(Measurement.station,Measurement.date,Measurement.prcp,Measurement.tobs).filter(Measurement.date >= lastyear).order_by(Measurement.date)

    precipitationdata = []

    for rows in pastyeardata:
        row = {"date": "prcp"}
        row["date"] = rows[0]
        row["prcp"] = (rows[1])
        precipitationdata.append(row)

    return jsonify(precipitationdata)



@app.route("/api/v1.0/stations")
def stations():
    activestations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    stationslist = list(np.ravel(activestations))
    return jsonify(stationslist)

print("Got here")

@app.route("/api/v1.0/tobs")
def tobs():

    # max date 
    maxdate = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).limit(1).all()
    maxdatedate = maxdate[0][0]
    maxdatedate
    #maxdatedate = (2017,8,23)
    # Calculate the date 1 year ago from the last data point in the database
    lastyear = dt.date(2017,8,23) - dt.timedelta(days=365)
    lastyear
    #lastyear = (2016,08,23)

    # Perform a query to retrieve the data and precipitation scores
    pastyeardata = session.query(Measurement.station,Measurement.date,Measurement.prcp,Measurement.tobs).filter(Measurement.date >= lastyear).order_by(Measurement.date)

    templist = []
    for temp in pastyeardata:
        temperaturedict = {}
        temperaturedict["station"] = temp[0]
        temperaturedict["tobs"] = temp[1]

        templist.append(temperaturedict)
    
    return jsonify(templist)


@app.route("/api/v1.0/<start>")
def start(startdate):
    startflask = []

    minstart = session.query(func.min(Measurement.tobs)).filter(Measurement.date == startdate).all()
    maxstart = session.query(func.max(Measurement.tobs)).filter(Measurement.date == startdate).all()
    averagestart = session.query(func.avg(Measurement.tobs)).filter(Measurement.date == startdate).all()

    startflask = list(np.ravel(minstart,maxstart,averagestart))

    return jsonify(startflask)


@app.route("/api/v1.0/<start>/<end>")
def startend(startdated):
    startend = []

    minstartfinal = session.query(func.min(Measurement.tobs)).filter(Measurement.date == startdated).all()
    maxstartfinal = session.query(func.max(Measurement.tobs)).filter(Measurement.date == startdated).all()
    averagestartfinal = session.query(func.avg(Measurement.tobs)).filter(Measurement.date == startdated).all()


    startend = list(np.ravel(minstartfinal,maxstartfinal,averagestartfinal))

    return jsonify(startend)


if __name__ == '__main__':
    app.run(debug=True)