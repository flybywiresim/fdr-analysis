import argparse
import os
import sys
from enum import Enum

import gmplot
import matplotlib.pyplot as plt
import mplcursors
import pandas as pd
from past.builtins import raw_input


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
    parser.add_argument(
        '-c',
        '--command',
        nargs=1,
        dest='command',
        required=False,
        help='FDR Chart Command (map, ap, aoa, apl, apv, athr)'
    )
    # parse arguments
    args = parser.parse_args()
    fdr = pd.read_csv(args.file[0])

    if not args.command:
        while True:  # use while True
            choice = menu()
            if choice == 1:
                print("Map")
                draw_map_graph(fdr)
            elif choice == 2:
                print("AP Disconnect Chart")
                draw_ap_graph(fdr)
            elif choice == 3:
                print("Angle of Attack Chart")
                draw_aoa_graph(fdr)
            elif choice == 4:
                print("AP Lateral Chart")
                draw_ap_lateral_graph(fdr)
            elif choice == 5:
                print("AP Vertical Chart")
                draw_ap_vertical_graph(fdr)
            elif choice == 6:
                print("A/THR Chart")
                draw_ath_graph(fdr)
            elif choice == 9:
                print("Exit")
                break
    else:
        if args.command[0] == 'map':
            print("Map")
            draw_map_graph(fdr)
        elif args.command[0] == 'ap':
            print("AP Disconnect Chart")
            draw_ap_graph(fdr)
        elif args.command[0] == 'aoa':
            print("Angle of Attack Chart")
            draw_aoa_graph(fdr)
        elif args.command[0] == 'apl':
            print("AP Lateral Chart")
            draw_ap_lateral_graph(fdr)
        elif args.command[0] == 'apv':
            print("AP Vertical Chart")
            draw_ap_vertical_graph(fdr)
        elif args.command[0] == 'athr':
            print("A/THR Chart")
            draw_ath_graph(fdr)


def menu():
    strs = ('Enter 1 for Route Map\n'
            'Enter 2 for AP Disconnect Chart\n'
            'Enter 3 for Angle of Attack (AoA) Chart\n'
            'Enter 4 for AP Lateral Chart\n'
            'Enter 5 for AP Vertical Chart\n'
            'Enter 6 for A/THR Chart\n'
            'Enter 9 to Exit\n'
            'Choice: ')
    choice = raw_input(strs)
    return int(choice)


def draw_map_graph(fdr):
    lat_samples = fdr['ap_sm.data.aircraft_position.lat'][1::50]
    lon_samples = fdr['ap_sm.data.aircraft_position.lon'][1::50]

    gmapOne = gmplot.GoogleMapPlotter(lat_samples[1], lon_samples[1], 6)
    gmapOne.scatter(lat_samples, lon_samples, '#ff0000', size=50, marker=False)
    gmapOne.plot(lat_samples, lon_samples, 'blue', edge_width=2.5)
    gmapOne.draw("map.html")
    os.system('map.html')


def draw_ap_graph(fdr):
    # get simulation time
    time = fdr['fbw.sim.time.simulation_time']
    # create figure with subplots
    figure, axes = plt.subplots(11, sharex=True)
    i = 0
    # aircraft position, speed and direction
    axes[i].plot(time, fdr['fbw.sim.data.H_ft'], label='Altitude ft', color="red")
    axes[i].plot(time, 100 * fdr['ap_sm.data.V_gnd_kn'], label='Ground Speed (/100)', color="blue")
    axes[i].plot(time, 100 * fdr['ap_sm.data.V_ias_kn'], label='IAS Speed (/100)', color="cyan")
    axes[i].plot(time, 100 * fdr['ap_sm.data.Psi_magnetic_deg'], label='Track (/100)', color="green")
    axes[i].grid(True)
    axes[i].set_ylim(0, 45000)
    axes[i].legend()
    i += 1
    # weights
    axes[i].plot(time, fdr['fbw.sim.data.total_weight_kg'], label='GW', color="red")
    axes[i].grid(True)
    axes[i].set_ylim(40000, 80000)
    axes[i].legend()
    i += 1
    # temp
    axes[i].plot(time, fdr['fbw.sim.data.ambient_wind_velocity_kn'], label='Wind kt', color="cyan")
    axes[i].plot(time, fdr['fbw.sim.data.total_air_temperature_celsius'], label='TAT', color="red")
    axes[i].plot(time, fdr['athr.data.ISA_degC'], label='ISA', color="blue")
    axes[i].plot(time, fdr['athr.data.OAT_degC'], label='OAT', color="green")
    axes[i].plot(time, fdr['fbw.sim.data.ice_structure_percent'], label='ICE', color="magenta")
    axes[i].grid(True)
    axes[i].set_ylim(-70, 150)
    axes[i].legend()
    i += 1
    # axis inputs
    axes[i].plot(time, fdr['fbw.sim.input.delta_eta_pos'], label='Elevator Input', color="black")
    axes[i].plot(time, fdr['fbw.sim.input.delta_xi_pos'], label='Aileron Input', color="red")
    axes[i].fill_between(time, -1.0, -0.5, alpha=0.1, color='red')
    axes[i].fill_between(time, -0.5, 0.5, alpha=0.1, color='green')
    axes[i].fill_between(time, 0.5, 1.0, alpha=0.1, color='red')
    axes[i].grid(True)
    axes[i].set_ylim(-1, +1)
    axes[i].legend()
    i += 1
    # axis inputs
    axes[i].plot(time, fdr['fbw.sim.input.delta_zeta_pos'], label='Rudder Input', color="green")
    axes[i].fill_between(time, -1.0, -0.4, alpha=0.1, color='red')
    axes[i].fill_between(time, -0.4, 0.4, alpha=0.1, color='green')
    axes[i].fill_between(time, 0.4, 1.0, alpha=0.1, color='red')
    axes[i].grid(True)
    axes[i].set_ylim(-1, +1)
    axes[i].legend()
    i += 1
    # spoilers
    axes[i].plot(time, fdr['fbw.sim.data.spoilers_left_pos'], label='Spoiler Left', color="red")
    axes[i].plot(time, fdr['fbw.sim.data.spoilers_right_pos'], label='Spoiler Right', color="blue")
    axes[i].grid(True)
    axes[i].set_ylim(-1, 1)
    axes[i].legend()
    i += 1
    # axis ap on
    axes[i].plot(time, fdr['fbw.sim.data.autopilot_custom_on'], label='Autopilot On', color="blue", linewidth=1.0)
    axes[i].grid(False)
    axes[i].set_ylim(0, +1)
    axes[i].fill_between(time, fdr['fbw.sim.data.autopilot_custom_on'], color="blue")
    axes[i].legend()
    i += 1
    axes[i].plot(time, fdr['ap_sm.input.AP_1_push'], label='AP1 Push', linewidth=2.0, color="blue")
    axes[i].plot(time, fdr['ap_sm.input.AP_2_push'], label='AP2 Push', linewidth=2.0, color="green")
    axes[i].plot(time, fdr['ap_sm.input.AP_DISCONNECT_push'], label='AP Disconnect', linewidth=2.0, color="black")
    axes[i].plot(time, fdr['fbw.sim.data_computed.high_aoa_prot_active'],
                 label='High-AoA', linewidth=5.0, color="orange")
    axes[i].plot(time, fdr['fbw.sim.data_computed.alpha_floor_command'],
                 label='A.FLOOR', linewidth=5.0, color="magenta")
    axes[i].grid(False)
    axes[i].set_ylim(0, 1)
    axes[i].legend()
    i += 1
    # attitude
    axes[i].plot(time, fdr['fbw.sim.data.Theta_deg'], label='Pitch', color="black")
    axes[i].plot(time, fdr['fbw.sim.data.Phi_deg'], label='Roll', color="red")
    axes[i].grid(True)
    axes[i].set_ylim(-60, 60)
    axes[i].legend()
    i += 1
    # axis sim rate
    axes[i].plot(time, fdr['fbw.sim.data.simulation_rate'], label='Sim Rate', color="blue", linewidth=3.0)
    axes[i].plot(time, fdr['fbw.sim.data.simulation_rate'] / fdr['fbw.sim.time.dt'], label='FPS', color="red")
    axes[i].grid(True)
    axes[i].set_ylim(0, 64)
    axes[i].legend()
    i += 1
    # configure distances
    figure.subplots_adjust(
        left=0.03,
        bottom=0.02,
        right=0.98,
        top=0.95,
        wspace=0,
        hspace=0.2
    )
    # set title
    figure.suptitle("FDR Analysis - Autopilot Deactivation")
    # window size
    # figure.set_size_inches(12, 10)
    # maximize window
    plt.get_current_fig_manager().window.state('zoomed')
    # show it
    mplcursors.cursor()
    plt.show()


def draw_aoa_graph(fdr):
    # get simulation time
    time = fdr['fbw.sim.time.simulation_time']

    # support math text
    plt.rcParams.update({'mathtext.default': 'regular'})

    # create figure with subplots
    figure, axes = plt.subplots(5, sharex=True)

    # axis 1
    ax1 = axes[0]
    ax1.plot(time, fdr['fbw.sim.input.delta_eta_pos'], label=r'$\delta\eta$ (Elevator Input)')
    ax1.grid(True)
    ax1.set_ylim(-1, +1)
    ax1.legend()

    # axis 2
    ax2 = axes[1]
    ax2.plot(time, fdr['fbw.sim.data.alpha_deg'], label=r'$\alpha$')
    ax2.plot(time, fdr['fbw.sim.data_speeds_aoa.alpha_filtered_deg'], label=r'$\alpha_{filtered}$')
    ax2.plot(time, fdr['fbw.sim.data_speeds_aoa.alpha_prot_deg'], label=r'$\alpha_{prot}$')
    ax2.plot(time, fdr['fbw.sim.data_speeds_aoa.alpha_floor_deg'], label=r'$\alpha_{floor}$')
    ax2.plot(time, fdr['fbw.sim.data_speeds_aoa.alpha_max_deg'], label=r'$\alpha_{max}$')
    ax2.grid(True)
    ax2.set_ylim(-5, 20)
    ax2.legend()

    # axis 3
    ax3 = axes[2]
    ax3.plot(time, fdr['fbw.sim.data.Theta_deg'], label=r'$\Theta$ (Pitch)')
    ax3.plot(time, fdr['fbw.sim.data.eta_deg'], label=r'$\eta$ (Elevator)')
    ax3.grid(True)
    ax3.set_ylim(-33, 33)
    ax3.legend()

    # axis 4
    ax4 = axes[3]
    ax4.plot(time, fdr['athr.data.engine_N1_1_percent'], label='1-N1')
    ax4.plot(time, fdr['athr.data.engine_N1_2_percent'], label='2-N1')
    ax4.grid(True)
    ax4.set_ylim(0, 100)
    ax4.legend()

    # axis 5
    ax5 = axes[4]
    ax5.plot(time, fdr['fbw.sim.data_computed.high_aoa_prot_active'], label='high_aoa_prot_active')
    ax5.plot(time, fdr['fbw.sim.data_computed.alpha_floor_command'], label='alpha_floor_command')
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
    ax1.set_title("FDR Analysis - AoA")

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
    plt.get_current_fig_manager().window.state('zoomed')

    # show it
    plt.show()
    
    
def draw_ap_lateral_graph(fdr):
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
    plt.rcParams.update({'mathtext.default': 'regular'})

    # create figure with subplots
    figure, axes = plt.subplots(4, sharex=True)

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
            text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0],
                                                  y=LateralMode(int(sel.target[1])).name),
            fontfamily='monospace',
            ma="right"
        )
    )
    mplcursors.cursor(ax3, multiple=True).connect(
        "add",
        lambda sel: sel.annotation.set(
            text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0],
                                                  y=LateralArmed(int(sel.target[1])).name),
            fontfamily='monospace',
            ma="right"
        )
    )

    # maximize window
    plt.get_current_fig_manager().window.state('zoomed')

    # show it
    plt.show()


def draw_ap_vertical_graph(fdr):
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
    plt.rcParams.update({'mathtext.default': 'regular'})

    # create figure with subplots
    figure, axes = plt.subplots(4, sharex=True)

    # axis 1
    ax1 = axes[0]
    ax1.plot(time, fdr['ap_sm.input.AP_1_push'], label=r'$AP1_{push}$')
    ax1.plot(time, fdr['ap_sm.input.AP_2_push'], label=r'$AP2_{push}$')
    ax1.plot(time, fdr['ap_sm.input.AP_DISCONNECT_push'], label=r'$AP_{disconnect}$')
    ax1.plot(time, fdr['ap_sm.input.ALT_push'], label=r'$ALT_{push}$')
    ax1.plot(time, fdr['ap_sm.input.ALT_pull'], label=r'$ALT_{pull}$')
    ax1.plot(time, fdr['ap_sm.input.VS_push'], label=r'$VS_{push}$')
    ax1.plot(time, fdr['ap_sm.input.VS_pull'], label=r'$VS_{pull}$')
    ax1.plot(time, fdr['ap_sm.input.EXPED_push'], label=r'$EXPED_{push}$')
    ax1.plot(time, fdr['ap_sm.input.APPR_push'], label=r'$APPR_{push}$')
    ax1.plot(time, fdr['ap_sm.input.LOC_push'], label=r'$LOC_{push}$')
    ax1.grid(True)
    ax1.set_ylim(-0.1, +1.1)
    ax1.legend()

    # axis 2
    ax2 = axes[1]
    ax2.plot(time, fdr['ap_sm.output.vertical_mode'], label='Mode')
    ax2.grid(True)
    ax2.set_ylim(-0.25, 45)
    ax2.legend()

    # axis 3
    ax3 = axes[2]
    ax3.plot(time, fdr['ap_sm.output.vertical_mode_armed'], label='Armed')
    ax3.grid(True)
    ax3.set_ylim(-0.1, 25)
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
    ax1.set_title("FDR Analysis - Autopilot - Vertical")

    # enable simple data cursor with label
    mplcursors.cursor([ax1, ax4], multiple=True).connect(
        "add",
        lambda sel: sel.annotation.set(
            text="{l:s}\n{y:.2f}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0], y=sel.target[1]),
            fontfamily='monospace',
            ma="right"
        )
    )
    mplcursors.cursor(ax2, multiple=True).connect(
        "add",
        lambda sel: sel.annotation.set(
            text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0],
                                                  y=VerticalMode(int(sel.target[1])).name),
            fontfamily='monospace',
            ma="right"
        )
    )
    mplcursors.cursor(ax3, multiple=True).connect(
        "add",
        lambda sel: sel.annotation.set(
            text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0],
                                                  y=VerticalArmed(int(sel.target[1])).name),
            fontfamily='monospace',
            ma="right"
        )
    )

    # maximize window
    plt.get_current_fig_manager().window.state('zoomed')

    # show it
    plt.show()


def draw_ath_graph(fdr):
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
    plt.rcParams.update({'mathtext.default': 'regular'})

    # create figure with subplots
    figure, axes = plt.subplots(6, sharex=True)

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
            text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0],
                                                  y=AutothrustRequestedMode(int(sel.target[1])).name),
            fontfamily='monospace',
            ma="right"
        )
    )
    mplcursors.cursor(ax4, multiple=True).connect(
        "add",
        lambda sel: sel.annotation.set(
            text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0],
                                                  y=AutothrustStatus(int(sel.target[1])).name),
            fontfamily='monospace',
            ma="right"
        )
    )
    mplcursors.cursor(ax5, multiple=True).connect(
        "add",
        lambda sel: sel.annotation.set(
            text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0],
                                                  y=AutothrustMode(int(sel.target[1])).name),
            fontfamily='monospace',
            ma="right"
        )
    )
    mplcursors.cursor(ax6, multiple=True).connect(
        "add",
        lambda sel: sel.annotation.set(
            text="{l:s}\n{y:s}\nt={x:.2f}".format(l=sel.artist.get_label(), x=sel.target[0],
                                                  y=AutothrustModeMessage(int(sel.target[1])).name),
            fontfamily='monospace',
            ma="right"
        )
    )

    # maximize window
    plt.get_current_fig_manager().window.state('zoomed')

    # show it
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
