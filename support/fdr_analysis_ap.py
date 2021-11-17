import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.widgets import Cursor


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
    draw_graph(fdr)


def draw_graph(fdr):
    # get simulation time
    time = fdr['fbw.sim.time.simulation_time']
    # create figure with subplots
    figure, axes = plt.subplots(9, sharex=True)
    i = 0
    # axis gs
    axes[i].plot(time, 100*fdr['ap_sm.data.V_gnd_kn'], label='Ground Speed (/100)', color="blue")
    axes[i].plot(time, 3.28084 * fdr['ap_sm.data.aircraft_position.alt'], label='Altitude ft', color="red")
    axes[i].plot(time, 100*fdr['ap_sm.data.Psi_magnetic_deg'], label='Track (/100)', color="green")
    axes[i].grid(True)
    axes[i].set_ylim(0, 40000)
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
    # axis ap on
    axes[i].plot(time, fdr['fbw.sim.data.autopilot_custom_on'], label='Autopilot On', color="blue", linewidth=1.0)
    axes[i].grid(False)
    axes[i].set_ylim(0, +1)
    axes[i].fill_between(time, fdr['fbw.sim.data.autopilot_custom_on'], color="blue")
    axes[i].legend()
    i += 1
    # axis ap1 push
    axes[i].plot(time, fdr['ap_sm.input.AP_1_push'], label='AP1 Push', linewidth=2.0, color="blue")
    axes[i].plot(time, fdr['ap_sm.input.AP_2_push'], label='AP2 Push', linewidth=2.0, color="green")
    axes[i].plot(time, fdr['ap_sm.input.AP_DISCONNECT_push'], label='AP Disconnect', linewidth=2.0, color="black")
    axes[i].plot(time, fdr['fbw.sim.data_computed.alpha_floor_command'], label='A.FLOOR', linewidth=5.0, color="magenta")
    axes[i].grid(False)
    axes[i].set_ylim(0, 1)
    axes[i].legend()
    i += 1
    # axis wind
    axes[i].plot(time, fdr['fbw.sim.data.ambient_wind_velocity_kn'], label='Wind kt', color="cyan")
    axes[i].grid(True)
    axes[i].set_ylim(0, 200)
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
    axes[i].plot(time, fdr['fbw.sim.data.simulation_rate'], label='Sim Rate', color="red")
    axes[i].grid(True)
    axes[i].set_ylim(0, 16)
    axes[i].legend()
    i += 1
    # axis dt
    axes[i].plot(time, fdr['fbw.sim.data.simulation_rate'] / fdr['fbw.sim.time.dt'], label='FPS', color="red")
    axes[i].grid(True)
    axes[i].set_ylim(0, 60)
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


if __name__ == "__main__":
    main(sys.argv[1:])

