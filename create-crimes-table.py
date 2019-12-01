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

def main():
    df = pd.read_excel('datasets/crime-by-state.xls')
    df = df.fillna(method='ffill')
    print(df)

if __name__ == '__main__':
    main()
