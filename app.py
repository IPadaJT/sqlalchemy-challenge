# Import depenencies
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Connect to Hawaii db
engine=create_engine("sqlite:///Resources/hawaii.sqlite")
# Reflect db 
Base= automap_base()
# Reflect tables
Base.prepare(engine, reflect=True)
# Save references for each table 
Measurement=Base.classes.measurement
Station=Base.classes.station

# Init Flask
app=Flask(__name__)

## Flask Routes

# Welcome/Homepage Route
@app.route('/')
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f'/api/v1.0/tobs'
        f'/api/v1.0/start'
        f'/api/v1.0/start/end'
        f'Use YYYY-mm-dd/YYYY-mm-dd format when inputting start and end dates'
    )

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Link to DB
    session=Session(engine)

    """Return prcp and date data"""
    prcp_query_results=session.query(Measurement.prcp, Measurement.date).all()

    # End link
    session.close()

    # Adding data to a dict
    prcp_query_data=[]
    for prcp, date in prcp_query_results:
        prcp_dict={}
        prcp_dict['precipitation']= prcp
        prcp_dict['date']= date
        prcp_query_data.append(prcp_dict)

    return jsonify(prcp_query_data)

if __name__ == '__main__':
    app.run(debug=True) 