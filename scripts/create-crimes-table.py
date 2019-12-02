"""
Script used to create the crimes table. The format of the
table is as follows:
    -----------------------------
    |   State   |   Crime Rate  |
    -----------------------------
    |   Kansas  |   4.2         |
    |   ...     |   ...         |
    -----------------------------
"""

from pandas import DataFrame, read_csv
import pandas as pd

from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
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

def main():
    df = pd.read_excel('../datasets/crime-by-state.xls')
    df = df.fillna(method='ffill')
    crimes = (df.groupby('State', as_index=False).apply(
        lambda x: x if len(x)==1 else x.iloc[[-2]]).reset_index(level=0, drop=True))
    crimes = crimes[['State', 'Violent crime']]
    print(crimes)

if __name__ == '__main__':
    main()