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
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"Note: to access values between a start and end date enter both dates using format: YYYY-mm-dd/YYYY-mm-dd"
    )

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Link to DB
    session=Session(engine)

    """Return prcp and date data"""
    beg_date='2016-08-23'
    sel=[Measurement.date, func.sum(Measurement.prcp)]
    precip= session.query(*sel).\
        filter(Measurement.date >= beg_date).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    # End link
    session.close()

    # Adding data to a dict
    precip_dates = []
    precip_totals = []

    for date, dailytotal in precip:
        precip_dates.append(date)
        precip_totals.append(dailytotal)
    
    precip_dict = dict(zip(precip_dates, precip_totals))
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
        # Link to DB
    session=Session(engine)

    """Return list of active stations in Hawaii"""
    sel=[Measurement.station]
    active_stations= session.query(*sel).\
        group_by(Measurement.station).all()

    # End link
    session.close()

    # Return JSON list of stations from query data
    list_stations=list(np.ravel(active_stations))
    return jsonify (list_stations)


@app.route("/api/v1.0/tobs")
def tobs():
        # Link to DB
    session=Session(engine)

    """Return most active stations temperature observation data"""
    beg_date = '2016-08-23'
    sel = [Measurement.date, 
        Measurement.tobs]
    station_temps = session.query(*sel).\
            filter(Measurement.date >= beg_date, Measurement.station == 'USC00519281').\
            group_by(Measurement.date).\
            order_by(Measurement.date).all()

    # End link
    session.close()

    # Adding data to a dict
    obs_dates=[]
    temp_obs=[]

    for date, obs in station_temps:
        obs_dates.append(date)
        temp_obs.append(obs)

    most_active=dict(zip(obs_dates, temp_obs))
    return jsonify(most_active)

# Can combine both routes by making a default endpoint unless otherwise specified.
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def range_start(start,end=None):
    '''Return temp data between two points of time.'''
    session=Session(engine)
    if end == None:
        enddate = session.query(func.max(Measurement.date)).\
                    scalar()
    else:
        enddate = str(end)
    startdate = str(start)
    results = session.query(func.min(Measurement.tobs).label('min_temp'),
                            func.avg(Measurement.tobs).label('avg_temp'),
                            func.max(Measurement.tobs).label('max_temp')).\
                filter(Measurement.date.between(startdate,enddate)).\
                first()
    session.close()
    datapoints = list(np.ravel(results))
    return jsonify(datapoints)
# Converted dates to strings seemed to help with a type error I was getting. 

if __name__ == '__main__':
    app.run(debug=True) 