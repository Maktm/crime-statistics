"""
Script used to create the crimes table. The format of the
table is as follows:
    ---------------------------------
    |   State       |  Unemployment |
    ---------------------------------
    |   New York    |  2.2          |
    |   ...         |   ...         |
    ---------------------------------
"""

import pandas as pd

from configparser import ConfigParser

import psycopg2

def configure(filename='../database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def insert_data(rows):
    print('* Insert data into table')

    config = configure()
    conn = psycopg2.connect(**config)
    cur = conn.cursor()
    for row in rows:
        cur.execute("""INSERT into unemployment(state, rate)
            VALUES ('{}', {})""".format(row[0], row[1]))
    print("* Writing changes to database..")
    conn.commit()
    cur.close()
    print("* Successfully completed")

def create_table():
    commands = (
        """CREATE TABLE unemployment(
            state VARCHAR(255) PRIMARY KEY,
            rate INTEGER NOT NULL
        )""",
    )

    conn = None
    try:
        config = configure()
        conn = psycopg2.connect(**config)
        cur = conn.cursor()

        for command in commands:
            print("* Executing query: {}".format(command))
            cur.execute(command)
        cur.close()
        conn.commit()
    except Exception as error:
        print(error)

def main():
    df = pd.read_excel('../datasets/unemployment-by-state.xlsx')
    unemployment = df[['State', 'Unemployment Rate']]
    rows = []
    for excel_row in unemployment.values:
        row = tuple(excel_row)
        state = row[0].lower()
        rate = row[1]
        rows.append((state, rate))
    rows = sorted(rows, key=lambda tup: tup[0])

    create_table()
    insert_data(rows)

if __name__ == '__main__':
    main()