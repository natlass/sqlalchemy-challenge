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
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= year_ago).all()
    
    
@app.route("/api/v1.0/stations")
def stations():
    all_station = session.query(Station).all()
    station_list = []
    for station in all_station:
        stat_dict = {}
        stat_dict["id"]=station.id
        stat_dict["station"] = station.station
        stat_dict["name"] = station.name
        stat_dict["latitude"] = station.latitude
        stat_dict["longitude"] = station.longitude
        stat_dict["elevation"] = station.elevation
        stat_dict.append(stat_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    
    
@app.route("/api/v1.0/<start>")
def start(start):
    

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    

if __name__ == "__main__":
    app.run(debug = True)