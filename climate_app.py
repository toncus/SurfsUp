# Step 4 - Climate App
# Now that you have completed your initial analysis, design a Flask api based on the queries that you have just developed.

#  Use FLASK to create your routes.

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify
import numpy as np
import pandas as pd

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

#print(Base.classes.keys())

# Save reference to the table
Station = Base.classes.stations
Measurement = Base.classes.measurements

# Define a session
session = Session(engine)
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return ("Available Routes:<br/> \
            /api/v1.0/precipitation<br/> \
            /api/v1.0/stations<br/> \
            /api/v1.0/tobs<br/> \
            /api/v1.0/start<br/> \
            /api/v1.0/start/end")

@app.route("/api/v1.0/precipitation")
def dates():
    """ Return a list of all dates and temperature observations
    """
    # Query all dates and temperature observations for last year
    results = session.query(Measurement.date, Measurement.tobs).\
              filter(Measurement.date.between('2017-01-01', '2017-12-31')).all()

    #Convert query results to dictionary
    all_observations = []
    for temp in results:
        temp_dict = {}
        temp_dict["date"] = temp.date
        temp_dict["tobs"] = temp.tobs
        all_observations.append(temp_dict)

    # Convert list of tuples into normal list
    return jsonify(all_observations)

@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Measurement.station).\
                      filter(Measurement.date.between('2017-01-01', '2017-12-31')).all()
                      
    all_stations = []
    for station in station_results:
        station_dict = {}
        station_dict["station"]=station.station
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results = session.query(Measurement.tobs).\
                    filter(Measurement.date.between('2017-01-01', '2017-12-31')).all()
                      
    all_tobs = []
    for tob in tobs_results:
        tob_dict = {}
        tob_dict["Temp. Observations"]= tob.tobs
        all_tobs.append(tob_dict)

    return jsonify(all_tobs)

#@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/start")

def temp_details(start = '2017-01-01'):
    """Return temperature details for a given start date."""

    # Temperature details for a given start date
    temperature_details = session.query(Measurement.tobs).\
                        filter(Measurement.date == start).all()
    temperature_details_df = pd.DataFrame(temperature_details, columns=['Observations_Count'])
    tobs = temperature_details_df['Observations_Count']
    
    min_temp = min(tobs)
    max_temp = max(tobs)
    avg_temp = np.mean(tobs)

    temp_details = []
    
    temp_start__dict = {}
    temp_start__dict['Min Temperature'] = float(min_temp)
    temp_start__dict['Max Temperature'] = float(max_temp)
    temp_start__dict['Avg Temperature'] = float(avg_temp)
    temp_details.append(temp_start__dict)

    return jsonify(temp_details)

if __name__ == '__main__':
    app.run(debug = True)