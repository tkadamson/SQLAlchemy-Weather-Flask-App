import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask Setup
app = Flask(__name__)

@app.route('/')
def home():
    return(
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>Precipiation Records</a><br/>"
        f"<a href='/api/v1.0/stations'>Stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>Temperature Observations</a><br/>"
        f"<a href='/api/v1.0/<start>'>Temperature Date To Present</a><br/>"
        f"Given a date parameter, returns minimum, maximum, and average temperatures from chosen date to present<br/>"
        f"<a href='/api/v1.0/<start>/<end>'>Temperature in Date Range</a><br/>"
        f"Given start date and end date parameters, returns minimum, maximum, and average temperatures in the date range<br/>"
    )

@app.route('/api/v1.0/precipitation')
def preciptation():
    #Open session and query data
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    #Unpack results into a list of dictionaries
    full_results = []

    for item in results:
        item_dict = {}
        item_dict['date'] = item[0]
        item_dict['prcp'] = item[1]
        full_results.append(item_dict)
    
    return(jsonify(full_results))

@app.route('/api/v1.0/stations')
def stations():
    #Open session and query data
    session = Session(engine)

    results = session.query(Measurement.station).distinct().all()

    session.close()

    #Unpack results into a list of dictionaries
    full_results = list(np.ravel(results))

    return jsonify(full_results)

@app.route('/api/v1.0/tobs')
def tobs():
    #Open session and query data
    session = Session(engine)

    #Max station found in jupyter notebook analysis
    max_station = 'USC00519281'

    #Min date calculations (same as jupyter analysis)
    # Find the most recent date in the data set.
    max_date = session.query(func.max(Measurement.date)).all()

    #Get object as a string
    max_date = [date[0] for date in max_date]
    max_date = max_date[0]

    #Split string so that date can be inserted into a datetime()
    max_date = max_date.split("-")

    # Calculate the date one year from the last date in data set.
    min_date = dt.datetime(int(max_date[0])-1, int(max_date[1]), int(max_date[2]))

    #Query results for flask page
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > min_date).filter(Measurement.station == max_station).all()

    session.close()

    #Unpack results into a list of dictionaries
    full_results = []

    for item in results:
        item_dict = {}
        item_dict['date'] = item[0]
        item_dict['tobs'] = item[1]
        full_results.append(item_dict)
    
    return(jsonify(full_results))

@app.route('/api/v1.0/<start>')
def startdate(start):

    session = Session(engine)

    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    min_temp = list(np.ravel(min_temp))
    max_temp = list(np.ravel(max_temp))
    avg_temp = list(np.ravel(avg_temp))

    temp_dict = {'max': max_temp[0], 'min': min_temp[0], 'avg': avg_temp[0]}

    return jsonify(temp_dict)

@app.route('/api/v1.0/<start>/<end>')
def daterange(start, end):
    session = Session(engine)

    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    min_temp = list(np.ravel(min_temp))
    max_temp = list(np.ravel(max_temp))
    avg_temp = list(np.ravel(avg_temp))

    temp_dict = {'max': max_temp[0], 'min': min_temp[0], 'avg': avg_temp[0]}

    return jsonify(temp_dict)

if __name__ == '__main__':
    app.run(debug=True)