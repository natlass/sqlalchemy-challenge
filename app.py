# Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect on an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save the tables
measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

# Flask set-up
app = Flask(__name__)

@app.route("/")
def main():
    """List all available routes"""
    return (
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        )

@app.route("/api/v1.0/precipitation")
def precip():
    """Convert the query results to a dictionary using date as the key and prcp as the value"""
    """Return JSON representation of the dictionary"""
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)
    
@app.route("/api/v1.0/stations")
def stations():
    all_station = session.query(Station.name).all()
    session.close()
    station_list = []
    for station in all_station:
        station_list.append(station)
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    session.close()
    print(last_date, year_ago)

    active_station = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).all()
    session.close()
    print(active_station[0][0])

    session.query(measurement.date, measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= '2016-08-23').all()
    session.close()

    
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    sel = [func.min(measurement.tobs), 
        func.round(func.avg(measurement.tobs),1), 
        func.max(measurement.tobs),]

    start_temp = session.query(*sel).\
        filter(measurement.date >= start).all()

    return (jsonify(start_temp))

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    session = Session(engine)

    sel = [func.min(measurement.tobs), 
        func.round(func.avg(measurement.tobs),1), 
        func.max(measurement.tobs),]

    end_temp = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()

    return jsonify(end_temp)

if __name__ == "__main__":
    app.run(debug = True)