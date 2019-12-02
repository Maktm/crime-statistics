"""
Script used to create the crimes table. The format of the
table is as follows:
    -----------------------------
    |   State   |   Crime Count |
    -----------------------------
    |   Kansas  |   422         |
    |   ...     |   ...         |
    -----------------------------
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
        cur.execute("""INSERT into crimes(state, count)
            VALUES ('{}', {})""".format(row[0], row[1]))
    print("* Writing changes to database..")
    conn.commit()
    cur.close()
    print("* Successfully completed")

def create_table():
    commands = (
        """CREATE TABLE crimes (
            state VARCHAR(255) PRIMARY KEY,
            count INTEGER NOT NULL
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
    print("* Reading data from crime-by-state.xls")
    df = pd.read_excel('../datasets/crime-by-state.xls')
    df = df.fillna(method='ffill')
    crimes = (df.groupby('State', as_index=False).apply(
        lambda x: x if len(x)==1 else x.iloc[[-2]]).reset_index(level=0, drop=True))
    crimes = crimes[['State', 'Violent crime']]
    rows = []
    for excel_row in crimes.values:
        row = tuple(excel_row)
        state = row[0].lower()
        rate = row[1]
        if state == 'district of columbia3':
            state = 'district of columbia'
        rows.append((state, rate))

    print("* Creating table...")
    create_table()
    insert_data(rows)

if __name__ == '__main__':
    main()