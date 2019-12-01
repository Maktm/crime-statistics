"""
Sample plotly code.
"""

import plotly
import plotly.figure_factory as ff

def main():
    fips = ['06021', '06023', '06027',
            '06029', '06033']
    values = range(len(fips))

    fig = ff.create_choropleth(fips=fips, values=values)
    fig.layout.template = None

    plotly.offline.plot(fig, filename='index.html')

if __name__ == '__main__':
    main()
