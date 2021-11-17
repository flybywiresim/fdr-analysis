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
class AutothrustRequestedMode(Enum):
    NONE = 0
    SPEED = 1
    THRUST_IDLE = 2
    THRUST_CLB = 3

class AutothrustStatus(Enum):
    DISENGAGED = 0
    ENGAGED_ARMED = 1
    ENGAGED_ACTIVE = 2

class AutothrustMode(Enum):
    NONE = 0
    MAN_TOGA = 1
    MAN_GA_SOFT = 2
    MAN_FLEX = 3
    MAN_DTO = 4
    MAN_MCT = 5
    MAN_THR = 6
    SPEED = 7
    MACH = 8
    THR_MCT = 9
    THR_CLB = 10
    THR_LVR = 11
    THR_IDLE = 12
    A_FLOOR = 13
    TOGA_LK = 14

class AutothrustModeMessage(Enum):
    NONE = 0
    THRLK = 1
    LVRTOGA = 2
    LVRCLB = 3
    LVRMCT = 4
    LVRASYM = 5

class AutothrustThrustLimit(Enum):
    NONE = 0
    CLB = 1
    MCT = 2
    FLEX = 3
    TOGA = 4
    REVERSE = 5

# support math text
plot.rcParams.update({'mathtext.default': 'regular'})

# create figure with subplots
figure, axes = plot.subplots(6, sharex=True)

# axis 1
ax1 = axes[0]
ax1.plot(time, fdr['athr.input.ATHR_push'], label=r'$ATHR_{push}$')
ax1.plot(time, fdr['athr.input.ATHR_disconnect'], label=r'$ATHR_{disconnect}$')
ax1.grid(True)
ax1.set_ylim(-0.1, +1.1)
ax1.legend()

# axis 2
ax2 = axes[1]
ax2.plot(time, fdr['ap_sm.output.autothrust_mode'], label='Requested Mode')
ax2.grid(True)
ax2.set_ylim(-0.2, 4)
ax2.legend()

# axis 3
ax3 = axes[2]
ax3.plot(time, fdr['athr.input.TLA_1_deg'], label='TLA_1')
ax3.plot(time, fdr['athr.input.TLA_2_deg'], label='TLA_2')
ax3.grid(True)
ax3.set_ylim(-20, 45)
ax3.legend()

# axis 4
ax4 = axes[3]
ax4.plot(time, fdr['athr.output.status'], label='Status')
ax4.grid(True)
ax4.set_ylim(-0.2, 2.2)
ax4.legend()

# axis 5
ax5 = axes[4]
ax5.plot(time, fdr['athr.output.mode'], label='Mode')
ax5.grid(True)
ax5.set_ylim(-0.2, 14.2)
ax5.legend()

# axis 6
ax6 = axes[5]
ax6.plot(time, fdr['athr.output.mode_message'], label='Message')
ax6.grid(True)
ax6.set_ylim(-0.2, 5.2)
ax6.legend()

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
mplcursors.cursor([ax1, ax3], multiple=True).connect(
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
        text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0], y=AutothrustRequestedMode(int(sel.target[1])).name),
        fontfamily='monospace',
        ma="right"
    )
)
mplcursors.cursor(ax4, multiple=True).connect(
    "add",
    lambda sel: sel.annotation.set(
        text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0], y=AutothrustStatus(int(sel.target[1])).name),
        fontfamily='monospace',
        ma="right"
    )
)
mplcursors.cursor(ax5, multiple=True).connect(
    "add", 
    lambda sel: sel.annotation.set(
        text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0], y=AutothrustMode(int(sel.target[1])).name),
        fontfamily='monospace',
        ma="right"
    )
)
mplcursors.cursor(ax6, multiple=True).connect(
    "add", 
    lambda sel: sel.annotation.set(
        text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0], y=AutothrustModeMessage(int(sel.target[1])).name),
        fontfamily='monospace',
        ma="right"
    )
)

# maximize window
plot.get_current_fig_manager().window.state('zoomed')

# show it
plot.show()
