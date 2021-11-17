import argparse
import sys
import pandas as pd
import gmplot


def main(argv):
    # initialize argument parser
    parser = argparse.ArgumentParser(description='FDR file analysis')
    parser.add_argument(
        '-f',
        '--file',
        nargs=1,
        dest='file',
        required=True,
        help='FDR file to analyze'
    )
    # parse arguments
    args = parser.parse_args()

    # load csv file
    fdr = pd.read_csv(args.file[0])
    fdr.head()
    draw_graph(fdr)


def draw_graph(fdr):
    lat_samples = fdr['ap_sm.data.aircraft_position.lat'][1::50]
    lon_samples = fdr['ap_sm.data.aircraft_position.lon'][1::50]

    gmapOne = gmplot.GoogleMapPlotter(lat_samples[1], lon_samples[1], 6)
    gmapOne.scatter(lat_samples, lon_samples, '#ff0000', size=50, marker=False)
    gmapOne.plot(lat_samples, lon_samples, 'blue', edge_width=2.5)
    gmapOne.draw("map.html")


if __name__ == "__main__":
    main(sys.argv[1:])
