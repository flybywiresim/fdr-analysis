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
class LateralMode(Enum):
    NONE = 0
    HDG = 10
    TRACK = 11
    NAV = 20
    LOC_CPT = 30
    LOC_TRACK = 31
    LAND = 32
    FLARE = 33
    ROLLOUT = 34
    RWY = 40
    RWY_TRACK = 41
    GA_TRACK = 50

class LateralArmed(Enum):
    NONE = 0
    NAV = 1
    LOC = 2
    NAVLOC = 3


# support math text
plot.rcParams.update({'mathtext.default': 'regular'})

# create figure with subplots
figure, axes = plot.subplots(4, sharex=True)

# axis 1
ax1 = axes[0]
ax1.plot(time, fdr['ap_sm.input.AP_1_push'], label=r'$AP1_{push}$')
ax1.plot(time, fdr['ap_sm.input.AP_2_push'], label=r'$AP2_{push}$')
ax1.plot(time, fdr['ap_sm.input.AP_DISCONNECT_push'], label=r'$AP_{disconnect}$')
ax1.plot(time, fdr['ap_sm.input.HDG_push'], label=r'$HDG_{push}$')
ax1.plot(time, fdr['ap_sm.input.HDG_pull'], label=r'$HDG_{pull}$')
ax1.plot(time, fdr['ap_sm.input.APPR_push'], label=r'$APPR_{push}$')
ax1.plot(time, fdr['ap_sm.input.LOC_push'], label=r'$LOC_{push}$')
ax1.grid(True)
ax1.set_ylim(-0.1, +1.1)
ax1.legend()

# axis 2
ax2 = axes[1]
ax2.plot(time, fdr['ap_sm.output.lateral_mode'], label='Mode')
ax2.grid(True)
ax2.set_ylim(-0.25, 45)
ax2.legend()

# axis 3
ax3 = axes[2]
ax3.plot(time, fdr['ap_sm.output.lateral_mode_armed'], label='Armed')
ax3.grid(True)
ax3.set_ylim(-0.1, 4)
ax3.legend()

# axis 4
ax4 = axes[3]
ax4.plot(time, fdr['ap_sm.input.FD_active'], label='FD')
ax4.plot(time, fdr['ap_sm.output.enabled_AP1'], label='AP1')
ax4.plot(time, fdr['ap_sm.output.enabled_AP2'], label='AP2')
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
ax1.set_title("FDR Analysis - Autopilot - Lateral")

# enable simple data cursor with label
mplcursors.cursor([ax1, ax4], multiple=True).connect(
    "add",
    lambda sel: sel.annotation.set(
        text="{l:s}\n{y:.2f}\nt={x:.2f}".format(
            l=sel.artist.get_label(), x=sel.target[0], y=sel.target[1]),
        fontfamily='monospace',
        ma="right"
    )
)
mplcursors.cursor(ax2, multiple=True).connect(
    "add", 
    lambda sel: sel.annotation.set(
        text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0], y=LateralMode(int(sel.target[1])).name),
        fontfamily='monospace',
        ma="right"
    )
)
mplcursors.cursor(ax3, multiple=True).connect(
    "add", 
    lambda sel: sel.annotation.set(
        text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0], y=LateralArmed(int(sel.target[1])).name),
        fontfamily='monospace',
        ma="right"
    )
)

# maximize window
plot.get_current_fig_manager().window.state('zoomed')

# show it
plot.show()
