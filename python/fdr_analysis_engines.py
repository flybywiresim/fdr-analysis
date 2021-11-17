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
figure, axes = plot.subplots(7, sharex=True)

# axis 1
ax1 = axes[0]
ax1.plot(time, fdr['engine.engineEngine1State'], label='Engine 1 State')
ax1.plot(time, fdr['engine.engineEngine2State'], label='Engine 2 State')
ax1.grid(True)
ax1.set_ylim(-0.1, 8)
ax1.legend()

# axis 2
ax2 = axes[1]
ax2.plot(time, fdr['engine.engineEngine1N1'], label='1-N1')
#ax2.plot(time, fdr['engine.engineEngine1N2'], label='1-N2')
ax2.plot(time, fdr['engine.engineEngine2N1'], label='2-N1')
#ax2.plot(time, fdr['engine.engineEngine2N2'], label='2-N2')
ax2.grid(True)
ax2.set_ylim(-10, 110)
ax2.legend()

# axis 3
ax3 = axes[2]
ax3.plot(time, fdr['engine.engineEngine1EGT'], label='1-EGT')
ax3.plot(time, fdr['engine.engineEngine2EGT'], label='2-EGT')
ax3.grid(True)
ax3.set_ylim(-70, 1000)
ax3.legend()

# axis 4
ax4 = axes[3]
ax4.plot(time, fdr['engine.engineEngine1FF'], label='1-FF')
ax4.plot(time, fdr['engine.engineEngine2FF'], label='2-FF')
ax4.grid(True)
ax4.set_ylim(0, 6000)
ax4.legend()

# axis 5
ax5 = axes[4]
ax5.plot(time, fdr['fbw.sim.data.H_ft'], label='H')
ax5.grid(True)
ax5.set_ylim(0, 40000)
ax5.legend()

# axis 6
ax6 = axes[5]
ax6.plot(time, fdr['fbw.sim.data.ambient_temperature_celsius'], label='SAT °C')
ax6.grid(True)
ax6.set_ylim(-70, 60)
ax6.legend()

# axis 7
ax7 = axes[6]
ax7.plot(time, fdr['fbw.sim.data.V_mach'], label='Mach')
ax7.grid(True)
ax7.set_ylim(0, 0.9)
ax7.legend()

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
ax1.set_title("FDR Analysis - Engines")

# enable simple data cursor with label
mplcursors.cursor(multiple=True).connect(
    "add", 
    lambda sel: sel.annotation.set(
        text="{l:s}\n{y:.2f}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0], y=sel.target[1]),
        fontfamily='monospace',
        ma="right"
    )
)

# maximize window
plot.get_current_fig_manager().window.state('zoomed')

# show it
plot.show()
