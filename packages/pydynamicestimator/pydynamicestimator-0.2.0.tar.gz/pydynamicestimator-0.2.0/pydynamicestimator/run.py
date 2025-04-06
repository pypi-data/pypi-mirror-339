# Created: 2024-12-01
# Last Modified: 2025-04-05
# (c) Copyright 2024 ETH Zurich, Milos Katanic
# https://doi.org/10.5905/ethz-1007-842
#
# Licensed under the GNU General Public License v3.0;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     https://www.gnu.org/licenses/gpl-3.0.en.html
#
# This software is distributed "AS IS", WITHOUT WARRANTY OF ANY KIND,
# express or implied. See the License for specific language governing
# permissions and limitations under the License.
#

# The code is based on the publication: Katanic, M., Lygeros, J., Hug, G.: Recursive dynamic state estimation for power systems with an incomplete nonlinear DAE model.
# IET Gener. Transm. Distrib. 18, 3657–3668 (2024). https://doi.org/10.1049/gtd2.13308
# The full paper version is available at: https://arxiv.org/abs/2305.10065v2
# See full metadata at: README.md
# For inquiries, contact: mkatanic@ethz.ch


from matplotlib import cm
from pydynamicestimator.utils import data_loader
from pathlib import Path
from pydynamicestimator.config import Config
import matplotlib.pyplot as plt
import importlib
from pydynamicestimator import system
import numpy as np
import logging
import sys
import csv
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run(config: Config) -> tuple[system.DaeEst, system.DaeSim]:

    """Initialize function and run appropriate routines"""

    clear_module("pydynamicestimator.system")
    importlib.reload(system)

    simfile = config.testsystemfile / 'sim_param.txt'
    simdistfile = config.testsystemfile / 'sim_dist.txt'
    estfile = config.testsystemfile / 'est_param.txt'
    estdistfile = config.testsystemfile / 'est_dist.txt'

    with open(simfile, 'rt') as fid:
        data_loader.read(fid, 'sim')

    with open(simdistfile, 'rt') as fid:
        data_loader.read(fid, 'sim')

    with open(estfile, 'rt') as fid:
        data_loader.read(fid, 'est')

    with open(estdistfile, 'rt') as fid:
        data_loader.read(fid, 'est')



    system.grid_sim.add_lines(system.line_sim)
    system.grid_est.add_lines(system.line_est)
    ######################################################## Simulation ###########################################################################################################
    for item in system.device_list_sim:
        if item.properties['xy_index']: item.xy_index(system.dae_sim, system.grid_sim)

    system.dae_sim.t = config.ts
    system.dae_sim.setup(**vars(config))

    system.grid_sim.setup(dae=system.dae_sim, bus_init=system.bus_init_sim)

    for item in system.device_list_sim:
        if item.properties['finit']: item.finit(system.dae_sim)

    for item in system.device_list_sim:
        if item.properties['fgcall']: item.fgcall(system.dae_sim)

    system.grid_sim.gcall(system.dae_sim)

    system.dae_sim.simulate(system.disturbance_sim)

    system.grid_sim.save_data(system.dae_sim)
    for item in system.device_list_sim:
        if item.properties['save_data']: item.save_data(system.dae_sim)

    ############################################################### Estimation #################################################################################################
    for item in system.device_list_est:
        if item.properties['xy_index']: item.xy_index(system.dae_est, system.grid_est)

    system.grid_est.setup(system.dae_est, system.grid_sim)
    system.dae_est.t = config.te
    system.dae_est.setup(**vars(config))
    system.dae_est.unknown = system.bus_unknown_est.bus

    for device_est in system.device_list_est:
        if device_est.properties['finit']:
            for idx_est in device_est.int.keys():
                device_sim = find_device_sim(idx_est)[0]
                if device_sim is not None:
                    device_est.init_from_simulation(device_sim, idx_est, system.dae_est, system.dae_sim)
                else:
                    logger.warning(f"Estimation device index {idx_est} not found simulation data. It will be ignored and the estimation will start from default initial value")


    for item in system.device_list_est:
        if item.properties['fgcall']: item.fgcall(system.dae_est)
        if item.properties['qcall']: item.qcall(system.dae_est)

    system.grid_est.gcall(system.dae_est)

    system.dae_est.estimate(dist=system.disturbance_est)

    for item in system.device_list_est:
        if item.properties['save_data']: item.save_data(system.dae_est)

    system.grid_est.save_data(system.dae_est)

    if config.plot: fplot(config)



    return system.dae_est, system.dae_sim


def fplot(config: Config):
    """Plot voltage and differential states based on configuration settings."""
    logging.basicConfig(level=logging.WARNING)  # Set logging level

    

    # Plot voltage profiles if enabled
    if config.plot_voltage:

        viridis = cm.get_cmap('viridis', system.dae_est.grid.nn)
        for i, node in enumerate(system.dae_est.grid.buses):
            try:
                # Plot estimation data
                est_voltage = np.sqrt(
                    system.grid_est.yf[node][0, :] ** 2 + system.grid_est.yf[node][1, :] ** 2
                )
                plt.plot(
                    system.dae_est.time_steps, est_voltage,
                    color=viridis(i), linestyle=':'
                )
            except KeyError:
                logging.warning(f"Node {node} not estimated.")

            try:
                # Plot simulation data
                sim_voltage = np.sqrt(
                    system.grid_sim.yf[node][0, :] ** 2 + system.grid_sim.yf[node][1, :] ** 2
                )
                plt.plot(
                    system.dae_sim.time_steps, sim_voltage,
                    color=viridis(i), label=f"{node}"
                )
            except KeyError:
                logging.warning(f"Node {node} does not exist in simulation.")

        plt.legend()
        plt.title("Voltage Profiles")
        plt.xlabel("Time")
        plt.ylabel("Voltage Magnitude")
        plt.savefig('voltage.png')

    # Plot differential states if enabled
    if config.plot_diff:
        # with open("results_est.csv", "
        # w") as file:
        #     pass  # Opening in 'w' mode clears the file
        # with open("desc_est.txt", "w") as file:
        #     pass  # Opening in 'w' mode clears the file


        for device_est in system.device_list_est:
            if device_est.properties['fplot']:


                # filename = 'desc_est.txt'
                # for state in device_est.states:
                #     with open(filename, "a") as f:
                #         f.write(device_est._name)
                #         f.write('\n')
                #         f.write(device_est._descr[state])
                #         f.write(str(device_est.__dict__[state]))
                #         f.write('\n')

                # config.plot_machines.reverse()
                num_units = device_est.n
                num_states = device_est.ns


                # Create subplots with shared x-axis
                figure, axis = plt.subplots(num_units, num_states, sharex=True, figsize=(25, 10))
                axis = np.atleast_2d(axis)
                figure.supxlabel("Time (s)", fontsize=12)


                if 'delta' in device_est.states:
                    # Align delta angles with the reference unit
                    n_est_ref = 0 # First device taken as reference angle
                    reference_est = device_est.xf['delta'][n_est_ref].copy()
                    device_sim, n_sim_ref = find_device_sim(next(iter(device_est.int)))
                    reference_sim = device_sim.xf['delta'][n_sim_ref].copy()

                for idx, n_est in device_est.int.items():
                    try:
                        device_sim, n_sim = find_device_sim(idx)

                    except ValueError as e:
                        logging.warning(f"Machine {idx} not found in simulation or estimation: {e}")
                        continue
                    if 'delta' in device_est.states:
                        device_sim.xf['delta'][n_sim] -= reference_sim
                        device_est.xf['delta'][n_est] -= reference_est

                    for col, state in enumerate(device_est.states):
                        t_sim = np.arange(system.dae_sim.T_start, system.dae_sim.T_end, system.dae_sim.t)
                        t_est = np.arange(system.dae_est.T_start, system.dae_est.T_end, system.dae_est.t)

                        try:
                            # Plot simulation data
                            axis[n_est, col].plot(
                                t_sim,
                                device_sim.xf[state][n_sim][round(system.dae_sim.T_start / system.dae_sim.t):round(system.dae_sim.T_end / system.dae_sim.t)],
                            )
                            # Plot estimation data
                            axis[n_est, col].plot(
                                t_est,
                                device_est.xf[state][n_est][round(system.dae_est.T_start / system.dae_est.t):round(system.dae_est.T_end / system.dae_est.t)],
                                linestyle=':'
                            )

                            # Label the y-axis only in the first column
                            if col == 0:
                                axis[n_est, col].set_ylabel(f"Device {idx}")

                            # Add a title to each column indicating the state
                            if n_est == 0:
                                axis[n_est, col].set_title(state)

                        except KeyError:
                            logging.warning(f"State '{state}' not found for unit {device_est}.")

                # Adjust layout for clarity
                figure.suptitle(f"Differential States of {device_est._name}", fontsize=14)
                plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Show all plots
    plt.savefig('diffstates.png')
    plt.show()


def clear_module(module_name):
    """Remove all attributes from a module, preparing it for a clean reload."""
    if module_name in sys.modules:
        module = sys.modules[module_name]
        module_dict = module.__dict__
        to_delete = [
            name for name in module_dict
            if not name.startswith("__")  # Avoid special and built-in attributes
        ]
        for name in to_delete:
            del module_dict[name]


def find_device_sim(idx_est):
    device_sim_found = next((device_sim for device_sim in system.device_list_sim if any(idx_est == idx_sim for idx_sim in device_sim.int.keys())), None)
    n_sim = device_sim_found.int[idx_est] if device_sim_found else None
    return device_sim_found, n_sim

