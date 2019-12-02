"""
Generates the three HTML files based on the data
inside of the database using plotly.
"""

import us
import psycopg2
import plotly
import plotly.graph_objects as go

from configparser import ConfigParser

def configure(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

def plot_crime():
    print("* Generating crime map...")
    table = []
    conn = None
    try:
        config = configure()
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        cur.execute('SELECT state, count FROM crimes ORDER BY state')
        row = cur.fetchone()
        while row is not None:
            table.append(row)
            row = cur.fetchone()
    except Exception as error:
        print(error)
    states = [us.states.lookup(row[0]).abbr for row in table]
    values = [row[1] for row in table]
    fig = go.Figure(data=go.Choropleth(
        locations=states,
        z=values,
        locationmode='USA-states',
        colorscale='Reds'
    ))
    plotly.offline.plot(fig, filename='crimes.html')
    print("* Successfully generated crime map!")

def plot_population():
    print("* Generating population map...")
    table = []
    conn = None
    try:
        config = configure()
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        cur.execute('SELECT state, popcount FROM population ORDER BY state')
        row = cur.fetchone()
        while row is not None:
            table.append(row)
            row = cur.fetchone()
    except Exception as error:
        print(error)
    states = [us.states.lookup(row[0]).abbr for row in table]
    values = [row[1] for row in table]
    fig = go.Figure(data=go.Choropleth(
        locations=states,
        z=values,
        locationmode='USA-states',
        colorscale='Greens'
    ))
    plotly.offline.plot(fig, filename='population.html')
    print("* Successfully generated population map!")

def plot_unemployment():
    print("* Generating unemployment map...")
    table = []
    conn = None
    try:
        config = configure()
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        cur.execute('SELECT state, rate FROM unemployment ORDER BY state')
        row = cur.fetchone()
        while row is not None:
            table.append(row)
            row = cur.fetchone()
    except Exception as error:
        print(error)
    states = [us.states.lookup(row[0]).abbr for row in table]
    values = [row[1] for row in table]
    fig = go.Figure(data=go.Choropleth(
        locations=states,
        z=values,
        locationmode='USA-states',
        colorscale='Blues'
    ))
    plotly.offline.plot(fig, filename='unemployment.html')
    print("* Successfully generated unemployment map!")

def main():
    plot_crime()
    plot_population()
    plot_unemployment()

if __name__ == '__main__':
    main()