import numpy as np

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

#@app.route('/api/v1.0/precipitation')


#@app.route('/api/v1.0/stations')


#@app.route('/api/v1.0/tobs')


#@app.route('/api/v1.0/<start>')


#@app.route('/api/v1.0/<start>/<end>')

if __name__ == '__main__':
    app.run(debug=True)