# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
from sqlalchemy import select


#################################################
# Database Setup
#################################################
engine= create_engine("sqlite:////Users/edgarguevara/Desktop/data_bootcamp/homework/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base= automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement= Base.classes.measurement
station= Base.classes.station


latest_date = dt.date(2017, 8, 23)
year_ago = latest_date - dt.timedelta(days=365)

# Create our session (link) from Python to the DB
session= Session(engine)

#################################################
# Flask Setup
#################################################
app= Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """list all available API routes"""
    return(
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br.>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation= select([measurement.date, measurement.prcp]).where(measurement.date >= year_ago).order_by(measurement.date).all()
    results= []
    for date, prcp in precipitation:
        results_dict = {}
        results_dict["date"]= date
        results_dict["prcp"]= prcp
        results.append(results_dict)
    return jsonify(results)


#stations
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(station.station).all()
    session.close()
    names = list(np.ravel(stations))

    return jsonify(names)


#tobs
@app.route("/api/v1.0/tobs")
def jsonified():
    
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)


    most_active_station = session.query(measurement.station, func.count(measurement.tobs))\
                                .group_by(measurement.station)\
                                .order_by(func.count(measurement.tobs).desc())\
                                .first()[0]

    active_station = session.query(measurement.date, measurement.tobs).\
                    filter(measurement.date >= one_year_ago).\
                    filter(measurement.station == most_active_station).\
                    order_by(measurement.date).all()

    temp_bin = []
    for sts in active_station: 
        list_temp_dict = {}
        list_temp_dict["Station ID"] = sts[0]
        list_temp_dict["Temperature"] = sts[1]
        temp_bin.append(list_temp_dict)

    return jsonify(temp_bin)






if __name__ == "__main__":
    app.run(debug=True)