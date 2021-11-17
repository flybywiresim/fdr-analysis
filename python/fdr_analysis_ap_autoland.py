#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plot
import mplcursors
import pandas
from enum import Enum

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

# define enums
class VerticalMode(Enum):
    NONE = 0
    ALT = 10
    ALT_CPT = 11
    OP_CLB = 12
    OP_DES = 13
    VS = 14
    FPA = 15
    ALT_CST = 20
    ALT_CST_CPT = 21
    CLB = 22
    DES = 23
    GS_CPT = 30
    GS_TRACK = 31
    LAND = 32
    FLARE = 33
    ROLLOUT = 34
    SRS = 40
    SRS_GA = 41

class VerticalArmed(Enum):
    NONE = 0
    ALT = 1
    ALT_CST = 2
    ALT_ALT_CST = 3
    CLB = 4
    ALT_CLB = 5
    DES = 8
    GS = 16
    ALT_GS = 17
    ALT_CST_GS = 18
    CLB_GS = 20
    DES_GS = 24


# support math text
plot.rcParams.update({'mathtext.default': 'regular'})

# create figure with subplots
figure, axes = plot.subplots(4, sharex=True)

# axis 1
ax1 = axes[0]
ax1.plot(time, fdr['ap_sm.output.vertical_mode'], label='Mode')
ax1.grid(True)
ax1.set_ylim(-0.25, 45)
ax1.legend()

# axis 2
ax2 = axes[1]
ax2.plot(time, fdr['ap_sm.data.H_radio_ft'], label=r'$H_R$')
ax2.grid(True)
ax2.set_ylim(0, 500)
ax2.legend()

# axis 3
ax3 = axes[2]
ax3.plot(time, fdr['ap_sm.data.H_dot_ft_min'], label=r'$\.H$')
ax3.plot(time, fdr['ap_sm.data_computed.H_dot_radio_fpm'], label=r'$\.H_{RA}$')
ax3.grid(True)
ax3.set_ylim(-1000, 0)
ax3.legend()

# axis 4
ax4 = axes[3]
ax4.plot(time, fdr['ap_sm.data.on_ground'], label='on_ground')
ax4.grid(True)
ax4.set_ylim(-0.1, 1.1)
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
ax1.set_title("FDR Analysis - Autopilot - Vertical")

# enable simple data cursor with label
mplcursors.cursor(ax1, multiple=True).connect(
    "add",
    lambda sel: sel.annotation.set(
        text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(
        ), x=sel.target[0], y=VerticalMode(int(sel.target[1])).name),
        fontfamily='monospace',
        ma="right"
    )
)
mplcursors.cursor([ax2, ax3, ax4], multiple=True).connect(
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
