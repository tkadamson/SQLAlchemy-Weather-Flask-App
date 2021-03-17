# hw8-sqlalchemy-surfs-up

## Project Instrctions | Grade: A

### Step 1 - Climate Analysis and Exploration

To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Use the provided [starter notebook](climate_starter.ipynb) and [hawaii.sqlite](Resources/hawaii.sqlite) files to complete your climate analysis and data exploration.

* Use SQLAlchemy `create_engine` to connect to your sqlite database.

* Use SQLAlchemy `automap_base()` to reflect your tables into classes and save a reference to those classes called `Station` and `Measurement`.

* Link Python to the database by creating an SQLAlchemy session.

#### Precipitation Analysis

* Start by finding the most recent date in the data set.

* Using this date, retrieve the last 12 months of precipitation data by querying the 12 preceding months of data.

* Select only the `date` and `prcp` values.

* Load the query results into a Pandas DataFrame and set the index to the date column.

* Sort the DataFrame values by `date`.

* Plot the results using the DataFrame `plot` method.

* Use Pandas to print the summary statistics for the precipitation data.

#### Station Analysis

* Design a query to calculate the total number of stations in the dataset.

* Design a query to find the most active stations (i.e. which stations have the most rows?).
  * List the stations and observation counts in descending order.
  * Which station id has the highest number of observations?
  * Using the most active station id, calculate the lowest, highest, and average temperature.

* Design a query to retrieve the last 12 months of temperature observation data (TOBS).

  * Filter by the station with the highest number of observations.
  * Query the last 12 months of temperature observation data for this station.
  * Plot the results as a histogram with `bins=12`.

* Close out your session.

- - -

### Step 2 - Climate App

Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

* Use Flask to create your routes.

#### Routes

* `/`
  * Home page.
  * List all routes that are available.

* `/api/v1.0/precipitation`
  * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
  * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`
  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.
  * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

## Solution Explanation 

### SQLALchemy Exploration

After linking the given SQLite file to Python, and reflecting the data into classes using the SQLAlchemy automap_base(), I found the latest date in the dataset. Using the split function with datetime, I was able to calculate one year prior to the most recent date. Then I used those dates as bookends to query and plot precipitation levels by date. I also used the pandas .describe() function to get measures of central tendency for precipitation levels. 

I also used the dataset to determine the weather station with the most active station, station USC00519281. With that station as a filter, I used SQLAlchemy queries to find the minimum, maximum, and average temperatures. I also used the dates found above to query the observed temperature data and plotted a histogram of occurences. 

### Flask API

The second piece of this project was generating a Flask API for various parameters. The requested pages were:
* Dates and precipitation observations of the most active station for the previous year
* All stations
* Dates and temperature observations of the most active station for the previous year
* Given a start date, calculate the minimum, maximum and average temperatures from that date until the end of the data
* When given the start and the end date, calculate the minimum, maximum and average temperatures for dates between the start and end date inclusive.

For each of these pages, I made a Flask route, then performed the queries in a SQL Alchemy Session. Many of these queries wee as those in the previous section. Due to Flask constrains, I needed to unpack this data into a dictionary and then jsonify it to get a readable response. 

### Temperature Analysis 1

Finally, I completed one of the challenge assignments regarding temperatures in the months of June and Demember. After importing the csv into a pandas dataframe, I use the split and datetime functions to convert the date columns to a datetime format. Then I narrowed my dataframe to get two separate dataframes for June and December. 

Ussing those dataframes, I was able to calculate the mean temperatures for those two months, across all years. I then took a random sample of n=500 from each dataframe to do a ttest to determine of the diferences between those temperature observations was statistically significant. 
I used a two-sided t-test, because the calculated mean difference could be lower or higher, so we need both sides to capture any differences. The t-test yielded a p-value of essentially 0, meaning that there is a statistically significant difference between the mean temperature in June and December.
