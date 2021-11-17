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
figure, axes = plot.subplots(5, sharex=True)

# axis 1
ax1 = axes[0]
ax1.plot(time, fdr['fbw.sim.input.delta_eta_pos'], label=r'$\delta\eta$')
ax1.fill_between(time, -1.0, -0.5, alpha=0.1, color='red')
ax1.fill_between(time, -0.5, 0.5, alpha=0.1, color='green')
ax1.fill_between(time, 0.5, 1.0, alpha=0.1, color='red')
ax1.grid(True)
ax1.set_ylim(-1.1, 1.1)
ax1.legend()

# axis 2
ax2 = axes[1]
ax2.plot(time, fdr['fbw.sim.input.delta_xi_pos'], label=r'$\delta\xi$')
ax2.fill_between(time, -1.0, -0.5, alpha=0.1, color='red')
ax2.fill_between(time, -0.5, 0.5, alpha=0.1, color='green')
ax2.fill_between(time, 0.5, 1.0, alpha=0.1, color='red')
ax2.grid(True)
ax2.set_ylim(-1.1, 1.1)
ax2.legend()

# axis 3
ax3 = axes[2]
ax3.plot(time, fdr['fbw.sim.input.delta_zeta_pos'], label=r'$\delta\zeta$')
ax3.fill_between(time, -1.0, -0.4, alpha=0.1, color='red')
ax3.fill_between(time, -0.4, 0.4, alpha=0.1, color='green')
ax3.fill_between(time, 0.4, 1.0, alpha=0.1, color='red')
ax3.grid(True)
ax3.set_ylim(-1.1, 1.1)
ax3.legend()

# axis 4
ax4 = axes[3]
ax4.plot(time, fdr['ap_sm.input.AP_1_push'], label=r'$AP1_{push}$')
ax4.plot(time, fdr['ap_sm.input.AP_2_push'], label=r'$AP2_{push}$')
ax4.plot(time, fdr['ap_sm.input.AP_DISCONNECT_push'], label=r'$AP_{disconnect}$')
ax4.plot(time, fdr['fbw.sim.data_computed.high_aoa_prot_active'], label='High-AoA')
ax4.plot(time, fdr['fbw.sim.data_computed.alpha_floor_command'], label=r'$\alpha_{floor}$')
ax4.grid(True)
ax4.set_ylim(-0.1, 1.1)
ax4.legend()

# axis 5
ax5 = axes[4]
ax5.plot(time, fdr['ap_sm.output.enabled_AP1'], label='AP1')
ax5.plot(time, fdr['ap_sm.output.enabled_AP2'], label='AP2')
ax5.grid(True)
ax5.set_ylim(-0.1, 1.1)
ax5.legend()

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
ax1.set_title("FDR Analysis - AP Disconnect")

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
