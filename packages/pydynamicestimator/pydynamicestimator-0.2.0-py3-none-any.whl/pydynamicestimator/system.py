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


from __future__ import annotations  # Postponed type evaluation
from scipy.linalg import cho_solve
from scipy.linalg import cholesky
from scipy.linalg import block_diag
from pydynamicestimator.devices.synchronous import *
from pydynamicestimator.devices.static import *
from pydynamicestimator.devices.inverter import *
from pydynamicestimator.devices.device import Element
from typing import Literal
from pydynamicestimator.measurements.measurements import *
from casadi import *
import numpy as np
import pandas as pd
from tabulate import tabulate
np.set_printoptions(threshold=np.inf)
np.random.seed(30)


class Grid:

    def __init__(self) -> None:

        self.y_adm_matrix: Optional[np.ndarray] = None  # Admittance matrix
        self.z_imp_matrix: Optional[np.ndarray] = None  # Impedance matrix
        self.incident_matrix: Optional[np.ndarray] = None
        self.Bsum: Optional[np.ndarray] = None # sum of shunt susceptance at each node
        self.Gsum: Optional[np.ndarray] = None  # sum of shunt conductance at each node
        self.nb: int = 0  # Number of branches
        self.nn: int = 0  # Number of nodes
        self.buses: list = []  # list of all system buses

        self.Sb: float = 100
        # Indices corresponding to branches
        self.idx_i: list = []
        self.idx_j: list = []
        self.idx_i_re: list = []
        self.idx_j_re: list = []
        self.idx_i_im: list = []
        self.idx_j_im: list = []

        self.yinit: dict = {}  # Init voltages
        self.yf: dict = {}  # Output voltages
        self.sf: dict = {}  # Output power

        self.line: Optional[Line] = None
        # Dictionary indices for fast look up
        self.idx_branch: dict = {}
        self.idx_bus: dict = {}
        self.idx_bus_re: dict = {}
        self.idx_bus_im: dict = {}
        # Matrices to calculate all branch currents
        self.C_branches_forward: Optional[np.ndarray] = None
        self.C_branches_reverse: Optional[np.ndarray] = None
        self.C_branches: Optional[np.ndarray] = None  # stacked together

    def save_data(self, dae: Dae) -> None:

        for idx, bus in enumerate(self.buses):
            self.yf[str(bus)] = dae.y_full[2 * idx:2 * idx + 2, :]

        for idx, bus in enumerate(self.buses):
            self.sf[bus] = np.zeros([2, dae.nts])

            for t in range(dae.nts):
                u_power = stack_volt_power(dae.y_full[2 * idx, t], dae.y_full[2 * idx + 1, t])
                self.sf[bus][:, t] = u_power.dot(self.y_adm_matrix[2 * idx: 2 * idx + 2, :]).dot(dae.y_full[:, t])

    def init_symbolic(self, dae: Dae) -> None:
        dae.ny = (self.nn * 2)
        dae.y = SX.sym('y', dae.ny)
        dae.g = SX(np.zeros(dae.ny))
        dae.grid = self

    def gcall(self, dae: Dae) -> None:
        dae.g += self.y_adm_matrix @ dae.y

    def guncall(self, dae: Dae) -> None:
        dae.g -= self.y_adm_matrix @ dae.y

    def add_lines(self, line: Line) -> None:
        self.line = line
        for bus_i, bus_j in zip(line.bus_i, line.bus_j):
            self.add_bus(bus_i, self.idx_i, self.idx_i_re, self.idx_i_im)
            self.add_bus(bus_j, self.idx_j, self.idx_j_re, self.idx_j_im)
            self.idx_branch[(bus_i, bus_j)] = self.nb
            self.nb += 1

    def add_bus(self, bus: str, idx: list, idx_re: list, idx_im: list) -> None:

        if bus not in self.buses:
            self.buses.append(bus)
            idx.append(self.nn)
            idx_re.append(2 * self.nn)
            idx_im.append(2 * self.nn + 1)
            self.idx_bus[bus] = self.nn
            self.nn += 1
        else:
            idx.append(self.buses.index(bus))
            idx_re.append(2 * self.buses.index(bus))
            idx_im.append(1 + 2 * self.buses.index(bus))

    def build_y(self, **kwargs) -> None:
        self.y_adm_matrix = np.zeros([2 * self.nn, 2 * self.nn])
        self.C_branches_forward = np.zeros([2*self.nb, 2 * self.nn])
        self.C_branches_reverse = np.zeros([2*self.nb, 2 * self.nn])

        r = self.line.r
        x = self.line.x
        g = self.line.g
        b = self.line.b
        trafo = self.line.trafo

        if kwargs.get('dist') == 'short':
            short_index = self.get_branch_index(kwargs['bus_i_short'], kwargs['bus_j_short'])[0][0]
            if kwargs.get('clear') == 0:

                rtemp = complex(self.line.r[short_index])
                xtemp = complex(self.line.x[short_index])
                gtemp = complex(self.line.g[short_index])
                btemp = complex(self.line.b[short_index])
                zt = complex(rtemp, xtemp)
                yt = kwargs['Y_short']
                zp = zt * (1 + zt * yt / 4)
                yp = zt * yt / zp + complex(gtemp, btemp)
                r[short_index] = zp.real
                x[short_index] = zp.imag
                g[short_index] = yp.real
                b[short_index] = yp.imag
            else:
                r[short_index] = 1e308
                x[short_index] = 1e308
                g[short_index] = 0
                b[short_index] = 0

        # Calculate Y matrix values
        z_inv = 1 / (r**2 + x**2)
        y_off_diag_real = -r * z_inv / trafo
        y_off_diag_imag = -x * z_inv / trafo
        y_diag_real = g / 2 + r * z_inv / trafo ** 2
        y_diag_imag = -b / 2 + x * z_inv / trafo ** 2

        # Update Y matrix with vectorized operations
        np.add.at(self.y_adm_matrix, (self.idx_i_re, self.idx_j_re), y_off_diag_real)
        np.add.at(self.y_adm_matrix, (self.idx_i_re, self.idx_j_im), y_off_diag_imag)
        np.add.at(self.y_adm_matrix, (self.idx_i_im, self.idx_j_re), -y_off_diag_imag)
        np.add.at(self.y_adm_matrix, (self.idx_i_im, self.idx_j_im), y_off_diag_real)

        np.add.at(self.y_adm_matrix, (self.idx_j_re, self.idx_i_re), y_off_diag_real)
        np.add.at(self.y_adm_matrix, (self.idx_j_re, self.idx_i_im), y_off_diag_imag)
        np.add.at(self.y_adm_matrix, (self.idx_j_im, self.idx_i_re), -y_off_diag_imag)
        np.add.at(self.y_adm_matrix, (self.idx_j_im, self.idx_i_im), y_off_diag_real)

        # Update diagonal elements
        np.add.at(self.y_adm_matrix, (self.idx_i_re, self.idx_i_re), y_diag_real)
        np.add.at(self.y_adm_matrix, (self.idx_i_re, self.idx_i_im), y_diag_imag)
        np.add.at(self.y_adm_matrix, (self.idx_i_im, self.idx_i_re), -y_diag_imag)
        np.add.at(self.y_adm_matrix, (self.idx_i_im, self.idx_i_im), y_diag_real)

        np.add.at(self.y_adm_matrix, (self.idx_j_re, self.idx_j_re), g / 2 + r * z_inv)
        np.add.at(self.y_adm_matrix, (self.idx_j_re, self.idx_j_im), -b / 2 + x * z_inv)
        np.add.at(self.y_adm_matrix, (self.idx_j_im, self.idx_j_re), b / 2 - x * z_inv)
        np.add.at(self.y_adm_matrix, (self.idx_j_im, self.idx_j_im), g / 2 + r * z_inv)

        if kwargs.get('dist') == 'fault' and kwargs.get('clear') is not True:
            re, im = self.get_node_index(kwargs['bus_short'])[1:3]
            np.add.at(self.y_adm_matrix, (re, re), kwargs['Y_short'])
            np.add.at(self.y_adm_matrix, (im, im), kwargs['Y_short'])

        even_rows = np.arange(0, 2*self.nb, 2)
        odd_rows = np.arange(1, 2*self.nb, 2)

        np.add.at(self.C_branches_forward, (even_rows, self.idx_i_re), -y_off_diag_real + g / 2)
        np.add.at(self.C_branches_forward, (even_rows, self.idx_i_im), -y_off_diag_imag - b / 2)
        np.add.at(self.C_branches_forward, (odd_rows, self.idx_i_re), y_off_diag_imag + b / 2)
        np.add.at(self.C_branches_forward, (odd_rows, self.idx_i_im), -y_off_diag_real + g / 2)

        np.add.at(self.C_branches_forward, (even_rows, self.idx_j_re), -r * z_inv)
        np.add.at(self.C_branches_forward, (even_rows, self.idx_j_im), -x * z_inv)
        np.add.at(self.C_branches_forward, (odd_rows, self.idx_j_re), x * z_inv)
        np.add.at(self.C_branches_forward, (odd_rows, self.idx_j_im), -r * z_inv)

        np.add.at(self.C_branches_reverse, (even_rows, self.idx_j_re), -y_off_diag_real + g / 2)
        np.add.at(self.C_branches_reverse, (even_rows, self.idx_j_im), -y_off_diag_imag - b / 2)
        np.add.at(self.C_branches_reverse, (odd_rows, self.idx_j_re), y_off_diag_imag + b / 2)
        np.add.at(self.C_branches_reverse, (odd_rows, self.idx_j_im), -y_off_diag_real + g / 2)

        np.add.at(self.C_branches_reverse, (even_rows, self.idx_i_re), -r * z_inv)
        np.add.at(self.C_branches_reverse, (even_rows, self.idx_i_im), -x * z_inv)
        np.add.at(self.C_branches_reverse, (odd_rows, self.idx_i_re), x * z_inv)
        np.add.at(self.C_branches_reverse, (odd_rows, self.idx_i_im), -r * z_inv)

        self.C_branches = np.vstack((self.C_branches_forward, self.C_branches_reverse))
        self.z_imp_matrix = np.linalg.inv(self.y_adm_matrix)

    def get_branch_index(self, node1: list, node2: list) -> tuple[np.ndarray, np.ndarray]:
        # Sort the node pair and look it up in the dictionary
        # the first one sequence doesn't matter
        # the second one matters
        ids1 = []
        ids2 = []
        if not isinstance(node1, list):
            node1 = [node1]
        if not isinstance(node2, list):
            node2 = [node2]

        for n1, n2 in zip(node1, node2):
            key = (n1, n2)
            key_r = (n2, n1)

            if key in self.idx_branch:
                idx = self.idx_branch[key]
                ids1.append(idx)
                ids2.append(idx)
            elif key_r in self.idx_branch:
                idx = self.idx_branch[key_r]
                ids1.append(idx)
                ids2.append(idx + self.nb)
            else:
                ids1.append(None)
                ids2.append(None)

        return np.array(ids1), np.array(ids2)

    def get_node_index(self, buses: list) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        # Calculate the real and imaginary indices in one step
        if not buses:
            return np.array([]), np.array([]), np.array([])  # Return empty arrays safely, if list of buses empty
        var_indices = [(self.idx_bus[bus], 2 * self.idx_bus[bus], 2 * self.idx_bus[bus] + 1) for bus in buses]
        idx, idx_re, idx_im = zip(*var_indices)
        return np.array(idx), np.array(idx_re), np.array(idx_im)


class GridSim(Grid):

    def init_from_power_flow(self, dae: DaeSim, static: BusInit) -> None:

        y = SX.sym('y', self.nn * 2)
        y_init = []
        g = SX(np.zeros(self.nn*2))

        for idx, bus in enumerate(self.buses):
            y_init.extend([1, 0])
            static_idx = static.bus.index(bus)
            y_real = y[2*idx]
            y_imag = y[2*idx + 1]

            if static.type[static_idx] == 'PQ':
                u_power = horzcat(vertcat(y_real, y_imag), vertcat(+y_imag, -y_real))
                g[2*idx:2*idx + 2] = u_power @ self.y_adm_matrix[2 * idx: 2 * idx + 2, :] @ y + np.array([static.p[static_idx], static.q[static_idx]]) / self.Sb

            elif static.type[static_idx] == 'PV':
                u_power = horzcat(y_real, +y_imag)
                g[2*idx] = u_power @ self.y_adm_matrix[2 * idx: 2 * idx + 2, :] @ y + static.p[static_idx] / self.Sb
                g[2*idx + 1] = sqrt(y[2*idx] ** 2 + y[2*idx + 1] ** 2) - static.v[static_idx]

            elif static.type[static_idx] == 'slack':
                g[2*idx] = sqrt(y_real ** 2 + y_imag ** 2) - static.v[static_idx]
                g[2*idx + 1] = y_imag

        z = Function('z', [y], [g])
        G = rootfinder('G', 'newton', z)
        try:
            solution = G(y_init)
        except:
            raise Exception(
                'Power flow cannot be solved. Check if the grid data and static power consumption data are realistic. Generated power should be negative. Only one bus can be slack.')
        if (solution == y_init).is_one():
            raise Exception('Power flow not solved')
        # save the initial data into yinit dictionary

        for idx, bus in enumerate(self.buses):
            self.yinit[str(bus)] = np.array(solution[2 * idx:2 * idx + 2].T)[0]

        dae.yinit = np.array(list(self.yinit.values())).reshape(self.nn * 2)
        dae.iinit = self.y_adm_matrix @ dae.yinit

        self.print_init_power_flow(dae)

    def print_init_power_flow(self, dae: DaeSim) -> None:
        # Print results of initialization
        print('\nPower flow for initialization successfully solved')

        # ---- BUS RESULTS ----
        idx_bus_re = [i for i in range(2 * self.nn) if i % 2 == 0]
        idx_bus_im = [i for i in range(2 * self.nn) if i % 2 != 0]

        vinit_re = np.array(dae.yinit[idx_bus_re])
        vinit_im = np.array(dae.yinit[idx_bus_im])

        vinit_mag = np.sqrt(vinit_re ** 2 + vinit_im ** 2)  # p.u.
        vinit_phase = np.arctan(vinit_im / vinit_re)  # radians

        iinit_re = np.array(dae.iinit[idx_bus_re])
        iinit_im = np.array(dae.iinit[idx_bus_im])

        Pinit = (vinit_re * iinit_re + vinit_im * iinit_im) * self.Sb
        Qinit = (vinit_im * iinit_re - vinit_re * iinit_im) * self.Sb

        # calculate power (P & Q) loss due to shunts
        self.build_Gsum()
        self.build_Bsum()
        iinit_shunt_re = self.Gsum * vinit_re - self.Bsum * vinit_im
        iinit_shunt_im = self.Bsum * vinit_re + self.Gsum * vinit_im

        Ploss_shunt = (vinit_re * iinit_shunt_re + vinit_im * iinit_shunt_im) * self.Sb
        Qloss_shunt = (vinit_im * iinit_shunt_re - vinit_re * iinit_shunt_im) * self.Sb

        power_flow_bus_table = pd.DataFrame({
            "Bus": self.buses,
            "V Magnitude (p.u.)": vinit_mag,
            "V Phase (deg)": vinit_phase * 180 / np.pi,
            "P Generation (kW)": Pinit,
            "Q Generation (kVAr)": Qinit,
            "P shunt loss (kW)": Ploss_shunt,
            "Q shunt loss (kVAr)": Qloss_shunt})

        power_flow_bus_table = tabulate(power_flow_bus_table, headers='keys')

        # ---- BRANCH RESULTS ----
        # calculate the voltage across each branch (v_from - v_to)
        self.build_incident_matrix()
        V_branch = self.incident_matrix @ dae.yinit

        # find the admittance at each branch
        y_adm_branch = np.zeros((2 * self.nb, 2 * self.nb))
        y_adm_re = -self.y_adm_matrix[self.idx_i_re, self.idx_j_re]
        y_adm_im = -self.y_adm_matrix[self.idx_i_im, self.idx_j_re]
        for k in range(self.nb):
            y_adm_branch[2 * k, 2 * k] = y_adm_re[k]
            y_adm_branch[2 * k, 2 * k + 1] = -y_adm_im[k]
            y_adm_branch[2 * k + 1, 2 * k] = y_adm_im[k]
            y_adm_branch[2 * k + 1, 2 * k + 1] = y_adm_re[k]

        # calculate the initial line currents through each branch
        ilinit = y_adm_branch @ V_branch

        idx_branch_re = [i for i in range(2 * self.nb) if i % 2 == 0]
        idx_branch_im = [i for i in range(2 * self.nb) if i % 2 != 0]

        # calculate the from_bus power injection
        Pinit_ij = (dae.yinit[self.idx_i_re] * ilinit[idx_branch_re] + dae.yinit[self.idx_i_im] * ilinit[
            idx_branch_im]) * self.Sb
        Qinit_ij = (dae.yinit[self.idx_i_im] * ilinit[idx_branch_re] - dae.yinit[self.idx_i_re] * ilinit[
            idx_branch_im]) * self.Sb

        # calculate the to_bus power injection
        Pinit_ji = -(dae.yinit[self.idx_j_re] * ilinit[idx_branch_re] + dae.yinit[self.idx_j_im] * ilinit[
            idx_branch_im]) * self.Sb
        Qinit_ji = -(dae.yinit[self.idx_j_im] * ilinit[idx_branch_re] - dae.yinit[self.idx_j_re] * ilinit[
            idx_branch_im]) * self.Sb

        Ploss = Pinit_ij + Pinit_ji
        Qloss = Qinit_ij + Qinit_ji

        power_flow_branch_table = pd.DataFrame({
            "From Bus": [self.buses[i] for i in self.idx_i],
            "To Bus": [self.buses[j] for j in self.idx_j],
            "From Bus P (kW)": Pinit_ij,
            "From Bus Q (kVAr)": Qinit_ij,
            "To Bus P (kW)": Pinit_ji,
            "To Bus Q (kVAr)": Qinit_ji,
            "P Loss (kW)": Ploss,
            "Q Loss (kVAr)": Qloss
        })

        power_flow_branch_table = tabulate(power_flow_branch_table, headers='keys')

        print('=======================================================================================================')
        print('Power Flow: Bus Results')
        print('=======================================================================================================')
        print(power_flow_bus_table)
        print('-------------------------------------------------------------------------------------------------------')
        print(f'Total P Generation: {np.sum(Pinit)} kW')
        print(f'Total Q Generation: {np.sum(Qinit)} kVAr')
        print(f'\nTotal P Loss from shunts: {np.sum(Ploss_shunt)} kW')
        print(f'Total Q Loss from shunts: {np.sum(Qloss_shunt)} kVAr')
        print('=======================================================================================================')
        print('Power Flow: Branch Results')
        print('=======================================================================================================')
        print(power_flow_branch_table)
        print('-------------------------------------------------------------------------------------------------------')
        print(f'Total P Loss from line impedances: {np.sum(Ploss)} kW')
        print(f'Total Q Loss from line impedances: {np.sum(Qloss)} kVAr')
        print('-------------------------------------------------------------------------------------------------------')

    def build_Gsum(self) -> None:
        # finds the sum of the shunt conductances (g) at each node due to line parameters
        g = self.line.g

        self.Gsum = np.zeros(self.nn)
        np.add.at(self.Gsum, self.idx_i, g/2)
        np.add.at(self.Gsum, self.idx_j, g/2)

    def build_Bsum(self) -> None:
        # finds the sum of the shunt susceptances (b) at each node due to line parameters
        b = self.line.b

        self.Bsum = np.zeros(self.nn)
        np.add.at(self.Bsum, self.idx_i, b/2)
        np.add.at(self.Bsum, self.idx_j, b/2)

    def build_incident_matrix(self) -> None:
        # build incident matrix for network (+1 indicates start node; -1 indicates end node)
        self.incident_matrix = np.zeros([self.nb * 2, self.nn * 2])

        for k in range(self.nb):
            self.incident_matrix[2*k, self.idx_i_re[k]] = 1
            self.incident_matrix[2*k+1, self.idx_i_im[k]] = 1
            self.incident_matrix[2*k, self.idx_j_re[k]] = -1
            self.incident_matrix[2*k+1, self.idx_j_im[k]] = -1

    def setup(self, dae: DaeSim, bus_init: BusInit) -> None:

        self.build_y()
        self.init_from_power_flow(dae, bus_init)
        self.init_symbolic(dae)


class GridEst(Grid):

    def __init__(self) -> None:
        Grid.__init__(self)
        self.y_simulation = []  # Store voltage results from the simulation in their full time resolution

    def _init_from_simulation(self, other: GridSim, dae: Dae) -> None:

        for node in self.buses:
            self.yinit[str(node)] = other.yf[str(node)][:, round(dae.T_start / dae.t)]
        dae.yinit = np.array(list(self.yinit.values())).reshape(self.nn * 2)
        dae.iinit = self.y_adm_matrix @ dae.yinit

    def _get_results(self, other: GridSim) -> None:
        y_simulation_list = []
        for bus in self.buses:
            y_simulation_list.append(other.yf[bus])
        self.y_simulation = np.vstack(y_simulation_list)

    def setup(self, dae: DaeEst, other: GridSim) -> None:

        self.build_y()
        self._init_from_simulation(other, dae)
        self._get_results(other)
        self.init_symbolic(dae)

    def init_symbolic(self, dae: DaeEst) -> None:

        super().init_symbolic(dae)
        # Prepare measurement matrices/vectors dimensions such that real measurements can be added below
        dae.y = SX.sym('y', dae.ny)
        dae.cy_meas_alg_matrix = np.empty((0, dae.ny))


class Dae:

    def __init__(self) -> None:

        # Counters
        self.nx: int = 0    # Number of differential states
        self.ny: int = 0    # Number of algebraic states
        self.ng: int = 0    # Number of algebraic equations
        self.np: int = 0    # Number of parameters/inputs (not used)
        self.nts: int = 0   # Number of time steps

        # Symbolic variables
        self.x: Optional[SX] = None  # Symbolic differential states
        self.y: Optional[SX] = None  # Symbolic algebraic states (voltages)
        self.f: Optional[SX] = None  # Symbolic first derivatives
        self.g: Optional[SX] = None  # Symbolic algebraic equations (current balance)
        self.p: Optional[SX] = None  # Will be used for parameters/inputs
        self.p0: Optional[SX] = None  # Will be used for parameters/inputs
        self.s: Optional[SX] = None  # Switches

        # Simulation/estimation outputs
        self.x_full: Optional[np.ndarray] = None  # Differential states output
        self.y_full: Optional[np.ndarray] = None  # Algebraic states output
        self.i_full: Optional[np.ndarray] = None  # Branch currents output

        # Simulation/estimation parameters
        self.T_start: float = 0.0
        self.T_end: float = 10.0
        self.time_steps: Optional[np.ndarray] = None  # Time steps of the est/sim
        self.Sb: float = 100
        self.fn: Literal[50, 60]
        self.t: float = 0.02

        # Initial values
        self.xinit: list = []
        self.yinit: list = []
        self.iinit: list = []
        self.xmin: list = [] # minimal state limiter values
        self.xmax: list = [] # maximal state limiter values
        # Store the grid as an attribute of the class
        self.grid: Optional[Grid] = None

        self.FG: Optional[Function] = None    # Casadi function for the DAE model

    def __reduce__(self):
        # Filter the attributes based on their types
        picklable_attrs = {}
        for key, value in self.__dict__.items():
            if isinstance(value, (float, int, list, np.ndarray)):
                # Only serialize float, int, list, or numpy arrays
                picklable_attrs[key] = value

        # Return the class constructor and the picklable attributes as a tuple
        return (self.__class__, (), picklable_attrs)

    def __setstate__(self, state):
        # Restore the state from the pickled attributes
        self.__dict__.update(state)

    def setup(self, **kwargs) -> None:
        # Overwrite default values
        self.__dict__.update(kwargs)
        # Number of time steps
        self.nts = round((self.T_end - self.T_start) / self.t)
        self.time_steps = np.arange(self.T_start, self.T_end, self.t)
        self.init_symbolic()
        self.xinit = np.array(self.xinit)
        self.xmin = np.array(self.xmin)
        self.xmax = np.array(self.xmax)

    def fgcall(self) -> None:
        pass

    def init_symbolic(self) -> None:
        pass

    def dist_short(self, clear: bool, bus_i: np.ndarray, bus_j: np.ndarray, y_adm: np.ndarray) -> None:

        self.grid.guncall(self)
        self.grid.build_y(clear=clear, dist='short', bus_i_short=bus_i, bus_j_short=bus_j, Y_short=y_adm)
        self.grid.gcall(self)
        self.fgcall()

    def dist_short_bus(self, clear: bool, bus: list, y_adm: np.ndarray) -> None:

        self.grid.guncall(self)
        self.grid.build_y(clear=clear, dist='fault', bus_short=bus, Y_short=y_adm)
        self.grid.gcall(self)
        self.fgcall()

    def dist_load(self, p: float, q: float, bus: list) -> None:
        idx_re = self.grid.get_node_index(bus)[1][0]
        idx_im = self.grid.get_node_index(bus)[2][0]
        self.g[idx_re] += (p / self.Sb * self.y[idx_re] + q / self.Sb * self.y[idx_im]) / (self.y[idx_re] ** 2 + self.y[idx_im] ** 2)
        self.g[idx_im] += (p / self.Sb * self.y[idx_im] - q / self.Sb * self.y[idx_re]) / (self.y[idx_re] ** 2 + self.y[idx_im] ** 2)
        self.fgcall()

    def check_disturbance(self, dist: Disturbance, iter_forward) -> None:
        active = dist.time < iter_forward * self.t
        if active.any():
            for idx, state in enumerate(active):
                if state:
                    match dist.type[idx]:
                        case "FAULT":
                            self.dist_short(clear=False, bus_i=dist.bus_i[idx], bus_j=dist.bus_j[idx], y_adm=dist.y[idx])
                        case "CLEAR":
                            self.dist_short(clear=True, bus_i=dist.bus_i[idx], bus_j=dist.bus_j[idx], y_adm=dist.y[idx])
                        case "LOAD":
                            self.dist_load(p=dist.p_delta[idx], q=dist.q_delta[idx], bus=[dist.bus[idx]])
                        case "FAULT_BUS":
                            self.dist_short_bus(clear=False, bus=[dist.bus[idx]], y_adm=dist.y[idx])
                        case "FAULT_BUS_CLEAR":
                            self.dist_short_bus(clear=True, bus=[dist.bus[idx]], y_adm=dist.y[idx])
                        case _:
                            raise 'Disturbance type not found'
                    for key, value in dist._params.items():
                        dist.__dict__[key] = np.array(dist.__dict__[key][1:])


class DaeSim(Dae):

    def __init__(self) -> None:
        Dae.__init__(self)

    def init_symbolic(self) -> None:

        self.x = SX.sym('x', self.nx)
        self.f = SX.sym('f', self.nx)
        self.s = SX.sym('s', self.nx)
        self.p = SX.sym('p', self.np)
        self.p0 = np.ones(self.np)

    def fgcall(self) -> None:
        dae_dict = {'x': self.x, 'z': self.y, 'p': self.s, 'ode': self.f, 'alg': self.g}
        # options = {'tf': self.t, 'print_stats': 1, 'collocation_scheme': 'radau', 'interpolation_order': 2}
        self.FG = integrator('FG', 'idas', dae_dict, 0, self.t)

    def simulate(self, dist: Disturbance) -> None:
        self.fgcall()

        iter_forward = 0
        self.x_full = np.zeros([self.nx, self.nts])
        self.y_full = np.zeros([self.ny, self.nts])
        self.i_full = np.zeros([4*self.grid.nb, self.nts])
        # set initial values
        x0 = self.xinit
        y0 = self.yinit
        s0 = [1] * self.nx
        self.x_full[:, iter_forward] = x0
        self.y_full[:, iter_forward] = y0

        for time_step in range(self.nts - 1):
            iter_forward += 1
            try:
                res = self.FG(x0=x0, z0=y0, p=s0)
            except RuntimeError:
                print("Simulation failed numerically")
                print("Try changing the disturbance")
                raise

            x0 = res['xf'].T
            x0 = np.clip(x0, self.xmin, self.xmax)
            y0 = res['zf'].T

            self.x_full[:, iter_forward] = x0
            self.y_full[:, iter_forward] = y0

            print(f'Simulation time is {round(iter_forward * self.t, 2)} [s]')

            self.check_disturbance(dist, iter_forward)

            self.i_full[:, iter_forward] = (self.grid.C_branches @ y0.T).T


class DaeEst(Dae):
    err_msg_est = (
        "Estimation failed \n"
        "Possible reasons: \n"
        " - Not enough measurements specified \n"
        " - Initialization point very bad \n"
        " - Estimator diverged from true state \n"
        " - Check if the disturbance rendered system unestimable \n"
        "Possible solutions: \n"
        "More measurements, less noise, different disturbance, better initialization..."
    )

    def __init__(self) -> None:

        Dae.__init__(self)
        self.nm: int = 0     # Number of measurements
        # Integration scheme
        self._schemes = {'trapezoidal': {'kf': 0.5, 'kb': 0.5}, 'forward': {'kf': 1.0, 'kb': 0.0}, 'backward': {'kf': 0.0, 'kb': 1.0}}
        # Set backward Euler as default
        self.int_scheme: str = 'backward'
        self.kf: float = 0.0
        self.kb: float = 1.0

        self.unknown = None
        self.proc_noise_alg: float = 0.0001  # default value
        self.proc_noise_diff: float = 0.0001  # default value
        self.init_error_diff: float = 1.0  # default value
        self.init_error_alg: bool = False # default value
        self.unknown_indices: list = []
        self.known_indices: list = []
        self.err_init: float = 0.001  # initial covariance matrix - default value

        # Matrices needed for calculation
        self.r_meas_noise_cov_matrix: Optional[np.ndarray] = None    # Measurement noise covariance matrix
        self.r_meas_noise__inv_cov_matrix: Optional[np.ndarray] = None    # Measurement noise covariance matrix
        self.q_proc_noise_diff_cov_matrix: Optional[np.ndarray] = None         # Process noise covariance matrix
        self.q_proc_noise_alg_cov_matrix: Optional[np.ndarray] = None
        self.q_proc_noise_cov_matrix: Optional[np.ndarray] = None
        self.c_meas_matrix: Optional[np.ndarray] = None
        self.z_meas_points_matrix: Optional[np.ndarray] = None
        self.p_est_init_cov_matrix: Optional[np.ndarray] = None

        self.x0: Optional[np.ndarray] = None    # actual initial vector of differential states
        self.y0: Optional[np.ndarray] = None    # actual vector of initial algebraic states
        self.s0: Optional[np.ndarray] = None  # actual vector of initial switch states

        self.f_func: Optional[Function] = None  # Function of differential equations
        self.g_func: Optional[Function] = None  # Function of algebraic equations
        self.df_dxy_jac: Optional[Function] = None  # Jacobian of differential equations
        self.dg_dxy_jac: Optional[Function] = None  # Jacobian of algebraic equations

        self.inner_tol: float = 1e-6  # default value for the inner estimation loop tolerance
        self.cov_tol: float = 1e-10  # minimal covariance matrix

    @property
    def te(self):
        return self._te

    @te.setter
    def te(self, value):
        self._te = value
        self.t = value

    def find_unknown_indices(self, grid: Grid) -> None:
        # This is to remove the equations at unknown nodes
        self.unknown_indices = []
        self.unknown_indices.extend(grid.get_node_index(dae_est.unknown)[1])
        self.unknown_indices.extend(grid.get_node_index(dae_est.unknown)[2])

        self.known_indices = [i for i in range(self.ny)]
        for i in range(len(self.unknown)):
            self.known_indices.remove(grid.buses.index(dae_est.unknown[i]) * 2)
            self.known_indices.remove(grid.buses.index(dae_est.unknown[i]) * 2 + 1)

    def init_symbolic(self) -> None:

        self.x = SX.sym('x', self.nx)
        self.f = SX.sym('f', self.nx)
        self.s = SX.sym('s', self.nx)

        self.q_proc_noise_diff_cov_matrix = np.zeros([self.nx, self.nx])
        self.r_meas_noise_cov_matrix = np.zeros([self.nm, self.nm])
        self.z_meas_points_matrix = np.zeros([self.nm, self.nts])
        self.c_meas_matrix = np.zeros([self.nm, self.nx + self.ny])

    def fgcall(self) -> None:
        for dev in device_list_est:
            if dev.properties['call']: dev.call(dae_est, dae_sim)
        # branch_voltage_p_m_u_est.call(dae_est, dae_sim)
        # branch_current_p_m_u_est.call(dae_est, dae_sim)
        dae_est.r_meas_noise__inv_cov_matrix = np.linalg.inv(dae_est.r_meas_noise_cov_matrix)
        self.f_func = Function('f', [self.x, self.y, self.s], [self.f])
        self.df_dxy_jac = self.f_func.jacobian()
        self.g_func = Function('g', [self.x, self.y, self.s], [self.g[self.known_indices]])
        self.dg_dxy_jac = self.g_func.jacobian()

    def _init_estimate(self) -> None:

        self.p_est_init_cov_matrix = np.eye(self.nx + self.ny) * self.err_init**(-1)

        # set initial values
        #         err = lambda: (np.random.uniform() - 0.5) * 0.2 * config.init_error_diff
        self.x0 = self.xinit
        self.y0 = self.yinit
        self.s0 = np.ones(self.nx)

        self.x_full = np.zeros([self.nx, self.nts])
        self.y_full = np.zeros([self.ny, self.nts])
        self.i_full = np.zeros([4*self.grid.nb, self.nts])

        if self.init_error_alg:
            self.y0 = [1, 0] * round(self.ny / 2)

    def estimate(self, dist: Disturbance, **kwargs) -> None:

        self.find_unknown_indices(self.grid)
        self.q_proc_noise_alg_cov_matrix = np.eye(self.grid.nn * 2) * (max(self.proc_noise_alg ** 2, self.cov_tol))  # Noise for the algebraic equations
        self.q_proc_noise_diff_cov_matrix *= max(self.proc_noise_diff**2, self.cov_tol)

        self.q_proc_noise_alg_cov_matrix = np.delete(self.q_proc_noise_alg_cov_matrix, self.unknown_indices, 0)
        self.q_proc_noise_alg_cov_matrix = np.delete(self.q_proc_noise_alg_cov_matrix, self.unknown_indices, 1)
        self.q_proc_noise_cov_matrix = block_diag(self.q_proc_noise_diff_cov_matrix, self.q_proc_noise_alg_cov_matrix)
        self.ng = self.ny - 2 * (len(self.unknown))  # number of algebraic equations
        self.fgcall()
        self._init_estimate()


        self.kf = self._schemes[self.int_scheme]['kf']
        self.kb = self._schemes[self.int_scheme]['kb']
        x0 = self.x0
        y0 = self.y0
        s0 = self.s0
        self.x_full[:, 0] = x0
        self.y_full[:, 0] = y0
        #  Create shorter variable names
        P_cov_inv = self.p_est_init_cov_matrix
        C = self.c_meas_matrix
        Rinv = self.r_meas_noise__inv_cov_matrix
        Q = self.q_proc_noise_cov_matrix
        A34 = np.zeros([self.ng, self.nx + self.ny])
        ones = np.eye(self.nx, self.nx + self.ny)
        iter_forward = 0
        for time_step in range(self.nts - 1):
            iter_forward += 1

            x1 = x0
            y1 = y0
            s1 = s0
            A_jac = self.df_dxy_jac(x0, y0, self.s0, 0)
            A12x = np.array(A_jac[0] * self.t * self.kf)
            A12y = np.array(A_jac[1] * self.t * self.kf)
            A12 = np.hstack((A12x, A12y))
            A = np.vstack((A12 + ones, A34))

            f_d = np.zeros(self.nx)
            f_d_0 = np.zeros(self.nx)

            if self.kf != 0:  # for forward Euler and trapezoidal
                f_d_0 = np.array(self.f_func(x0, y0, s0) * self.t * self.kf)[:, 0]
            if self.kb == 0:  # for forward Euler
                E12 = np.zeros([self.nx, self.nx + self.ny])
                f_d = f_d_0

            y = self.z_meas_points_matrix[:, iter_forward]
            print('Estimation time is ', round(iter_forward * self.t, 2), '[s]')
            # if the value is zero, add no noise
            p_nd = (np.sqrt(self.q_proc_noise_diff_cov_matrix)@np.random.randn(self.nx)) * (self.proc_noise_diff != 0)
            p_na = (np.sqrt(self.q_proc_noise_alg_cov_matrix)@np.random.randn(self.ng)) * (self.proc_noise_alg != 0)
            p_n = np.hstack((p_nd, p_na))

            for iter_kf in range(5):

                if self.kb != 0:  # for trapezoidal and backward Euler
                    E12_jac = self.df_dxy_jac(x1, y1, s1, 0)
                    E12x = np.array(E12_jac[0] * self.t * self.kb)
                    E12y = np.array(E12_jac[1] * self.t * self.kb)
                    E12 = np.hstack((E12x, E12y))

                    f_d = f_d_0 + np.array(self.f_func(x1, y1, s1) * self.t * self.kb)[:, 0]

                E34_jac = self.dg_dxy_jac(x1, y1, s1, 0)
                E34x = np.array(E34_jac[0])
                E34y = np.array(E34_jac[1])
                E34 = np.hstack((E34x, E34y))

                g_d = np.array(self.g_func(x1, y1, s1))[:, 0]
                E = np.vstack((E12 - ones, E34))
                xy1 = np.hstack((x1, y1))

                Cov_L = cholesky(Q + A.dot(cho_solve((P_cov_inv, True), A.T, check_finite=False)), check_finite=False, lower=True)

                Big_ = E.T.dot(cho_solve((Cov_L, True), E, check_finite=False)) + C.T.dot(Rinv).dot(C)

                delta_k = np.hstack((E12.dot(xy1) - x0 - f_d, E34.dot(xy1) - g_d)) + p_n

                small_ = E.T.dot(cho_solve((Cov_L, True), delta_k, check_finite=False)) + C.T.dot(Rinv).dot(y)

                try:
                    Big_chol = cholesky(Big_, lower=True)
                except numpy.linalg.LinAlgError:
                    raise Exception(DaeEst.err_msg_est)

                xy1_new = cho_solve((Big_chol, True), small_, check_finite=False)

                x1_raw = xy1_new[:self.nx]
                y1 = xy1_new[self.nx:self.nx + self.ny]
                x1 = np.clip(x1_raw, self.xmin, self.xmax)
                s1 = (x1 == x1_raw).astype(int)

                if np.max(np.abs(xy1_new - xy1)) < self.inner_tol:
                    break

            self.x_full[:, iter_forward], self.y_full[:, iter_forward] = x0, y0 = x1, y1

            P_cov_inv = Big_chol

            self.check_disturbance(dist, iter_forward)


# create the estimation grid
grid_est = GridEst()
# create the simulation grid
grid_sim = GridSim()
# initialize the DAE classes
dae_est = DaeEst()
dae_sim = DaeSim()

bus_init_sim = BusInit()
bus_unknown_est = BusUnknown()

line_sim = Line()
line_est = Line()

disturbance_sim = Disturbance()
disturbance_est = Disturbance()

device_list_sim = []
device_list_est = []

def stack_volt_power(vre, vim) -> np.ndarray:
    u_power = np.hstack((np.vstack((vre, vim)), np.vstack((vim, -vre))))
    return u_power
