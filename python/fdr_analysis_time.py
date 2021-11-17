#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plot
import mplcursors
import pandas

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
fdr = pandas.read_csv(args.file[0])

# get simulation time
time = fdr['fbw.sim.time.simulation_time']

# support math text
plot.rcParams.update({'mathtext.default': 'regular'})

# create figure with subplots
figure, axes = plot.subplots(4, sharex=True)

# axis 1
ax1 = axes[0]
ax1.plot(time, fdr['fbw.sim.data.simulation_rate'], label='Simulation Rate')
ax1.grid(True)
ax1.set_ylim(-0.1, 8)
ax1.legend()

# axis 2
ax2 = axes[1]
ax2.plot(time, fdr['fbw.sim.time.dt'], label=r'$\deltaT$')
ax2.fill_between(time, 1/10, 1, alpha=0.1, color='red')
ax2.fill_between(time, 1/15, 1/10, alpha=0.1, color='orange')
ax2.grid(True)
ax2.set_ylim(0, 0.2)
ax2.legend()

# axis 3
ax3 = axes[2]
ax3.plot(time, fdr['fbw.sim.data.simulation_rate'] / fdr['fbw.sim.time.dt'], label='FPS')
ax3.grid(True)
ax3.set_ylim(0, 80)
ax3.legend()

# axis 3
ax4 = axes[3]
ax4.plot(time, 1 / fdr['fbw.sim.time.dt'], label='Sample Rate')
ax4.fill_between(time, 10, 15, alpha=0.1, color='orange')
ax4.fill_between(time, 0, 10, alpha=0.1, color='red')
ax4.grid(True)
ax4.set_ylim(0, 80)
ax4.legend()

# configure distances
figure.subplots_adjust(
    left=0.03,
    bottom=0.04,
    right=0.99,
    top=0.97,
    wspace=0,
    hspace=0.1
)

# set title
ax1.set_title("FDR Analysis - Time")

# enable simple data cursor with label
mplcursors.cursor(multiple=True).connect(
    "add",
    lambda sel: sel.annotation.set(
        text="{l:s}\n{y:.2f}\nt={x:.2f}".format(
            l=sel.artist.get_label(), x=sel.target[0], y=sel.target[1]),
        fontfamily='monospace',
        ma="right"
    )
)

# maximize window
plot.get_current_fig_manager().window.state('zoomed')

# show it
plot.show()
