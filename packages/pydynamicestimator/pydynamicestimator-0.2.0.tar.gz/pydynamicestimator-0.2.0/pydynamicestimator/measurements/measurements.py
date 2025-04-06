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
from typing import TYPE_CHECKING
import numpy as np
from typing import Optional

from pydynamicestimator.devices.device import Element

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from pydynamicestimator.system import DaeEst, DaeSim

np.random.seed(30)


class Measurement(Element):

    def __init__(self) -> None:
        super().__init__()
        self._params.update({'acc': 0.001, 'seed': 30, 'distr': 'normal'})  # Default entries for np.arrays
        self._descr.update({'prec': 'measurement weight', 'acc': 'standard deviation of measurement error', 'seed': 'random number ceed', 'u': 'device status'})
        self._meas: list[str] = []
        self._mand: list[str] = []  # mandatory attributes

        self._noise_mapping = {name: getattr(np.random, name) for name in dir(np.random) if callable(getattr(np.random, name)) and not name.startswith("_")}

        self.acc = np.array([], dtype=float)  # Measurement accuracy
        self.distr = np.array([], dtype=str)
        self.seed = np.array([], dtype=int)
        self.properties.update({'call': True, 'xy_index': True})

    def add(self, idx=None, name=None, **kwargs) -> None:
        """Add a measurement device"""

        super().add(idx=idx, name=name, **kwargs)
        distr = kwargs.get('distr')
        if distr not in self._noise_mapping.keys():
            raise Exception('The given noise distribution %s is not defined' % distr)

    def xy_index(self, dae: DaeEst, dae_sim: DaeSim) -> None:
        """Assign indices for measured quantities"""
        for var in range(self.n):
            for item in self._meas:
                self.__dict__[item][var] = dae.nm
                dae.nm += 1


class BusVoltagePMU(Measurement):

    def __init__(self) -> None:
        super().__init__()
        self._type = "pmuu"
        self._name = "PMU_voltage_measurement"
        self._data.update({'bus': '0'})
        self._params.update({'vre': 0, 'vim': 0})
        self._meas.extend(['vre', 'vim'])
        self._mand.extend(['bus'])
        self.bus: list[Optional[str]] = []  #  which buses are measured
        self.vre = np.array([], dtype=int)  # index of the measured quantity
        self.vim = np.array([], dtype=int)

    def call(self, dae: DaeEst, dae_sim: DaeSim) -> None:
        est_idx_re, est_idx_im = dae.grid.get_node_index(self.bus)[1:3]
        sim_idx_re, sim_idx_im = dae_sim.grid.get_node_index(self.bus)[1:3]
        noise = np.zeros([self.n * 2, dae.nts])
        # TODO: Implement the function to calculate the noise term properly for different noise distributions
        for var in range(self.n):
            selected_function = self._noise_mapping[self.distr[var]]
            noise[2 * var:2 * var + 2] = selected_function(size=[2, dae.nts]) * self.acc[var]

        dae.c_meas_matrix[self.vre, dae.nx + est_idx_re] = 1
        dae.c_meas_matrix[self.vim, dae.nx + est_idx_im] = 1

        dae.z_meas_points_matrix[self.vre] = dae_sim.y_full[sim_idx_re, round(dae.T_start / dae_sim.t):round(dae.T_end / dae_sim.t):round(dae.t / dae_sim.t)] + noise[
            np.arange(0, 2, 2 * self.n)]
        dae.z_meas_points_matrix[self.vim] = dae_sim.y_full[sim_idx_im, round(dae.T_start / dae_sim.t):round(dae.T_end / dae_sim.t):round(dae.t / dae_sim.t)] + noise[
            np.arange(1, 2, 2 * self.n)]

        dae.r_meas_noise_cov_matrix[self.vre, self.vre] = np.clip(self.acc**2, a_min=dae.cov_tol, a_max=1/(dae.cov_tol))
        dae.r_meas_noise_cov_matrix[self.vim, self.vim] = np.clip(self.acc**2, a_min=dae.cov_tol, a_max=1/(dae.cov_tol))


class BranchCurrentPMU(Measurement):

    def __init__(self) -> None:
        super().__init__()
        self._type = "pmui"
        self._name = "PMU_current_measurement"
        self._data.update({'bus_i': '0', 'bus_j': '0'})
        self._params.update({'ire': 0, 'iim': 0})
        self._mand.extend(['bus_i', 'bus_j'])
        self._meas.extend(['ire', 'iim'])
        self.bus_i: list[Optional[str]] = []
        self.bus_j: list[Optional[str]] = []
        self.ire = np.array([], dtype=int)
        self.iim = np.array([], dtype=int)

    def call(self, dae: DaeEst, dae_sim: DaeSim) -> None:
        for idx_meas in range(self.n):
            # now include the choice of the distribution of noise
            selected_function = self._noise_mapping[self.distr[idx_meas]]
            noise = selected_function(size=[2, dae.nts]) * self.acc[idx_meas]

        idx_i_re, idx_i_im = dae.grid.get_node_index(self.bus_i)[1:3]
        idx_j_re, idx_j_im = dae.grid.get_node_index(self.bus_j)[1:3]

        idx_branch = dae.grid.get_branch_index(self.bus_i, self.bus_j)[0]
        idx_branch_dir = dae_sim.grid.get_branch_index(self.bus_i, self.bus_j)[1]
        idx_branch_dir_re = 2 * idx_branch_dir
        idx_branch_dir_im = 2 * idx_branch_dir + 1

        tr = dae.grid.line.trafo[idx_branch]
        g = dae.grid.line.g[idx_branch]
        b = dae.grid.line.b[idx_branch]

        Yrr = dae.grid.y_adm_matrix[idx_i_re, idx_j_re]
        Yri = dae.grid.y_adm_matrix[idx_i_re, idx_j_im]
        Yir = dae.grid.y_adm_matrix[idx_i_im, idx_j_re]
        Yii = dae.grid.y_adm_matrix[idx_i_im, idx_j_im]

        dae.c_meas_matrix[self.ire, dae.nx + idx_i_re] = - Yrr / tr + g / 2
        dae.c_meas_matrix[self.ire, dae.nx + idx_i_im] = - Yri / tr - b / 2
        dae.c_meas_matrix[self.iim, dae.nx + idx_i_re] = - Yir / tr + b / 2
        dae.c_meas_matrix[self.iim, dae.nx + idx_i_im] = - Yii / tr + g / 2

        dae.c_meas_matrix[self.ire, dae.nx + idx_j_re] = Yrr
        dae.c_meas_matrix[self.ire, dae.nx + idx_j_im] = Yri
        dae.c_meas_matrix[self.iim, dae.nx + idx_j_re] = Yir
        dae.c_meas_matrix[self.iim, dae.nx + idx_j_im] = Yii

        dae.r_meas_noise_cov_matrix[self.ire, self.ire] = np.clip(self.acc**2, a_min=1e-10, a_max=1e10)
        dae.r_meas_noise_cov_matrix[self.iim, self.iim] = np.clip(self.acc**2, a_min=1e-10, a_max=1e10)

        dae.z_meas_points_matrix[self.ire] = dae_sim.i_full[idx_branch_dir_re, round(dae.T_start / dae_sim.t):round(dae.T_end / dae_sim.t):round(dae.t / dae_sim.t)] + noise[
            np.arange(0, 2, 2 * self.n)]
        dae.z_meas_points_matrix[self.iim] = dae_sim.i_full[idx_branch_dir_im, round(dae.T_start / dae_sim.t):round(dae.T_end / dae_sim.t):round(dae.t / dae_sim.t)] + noise[
            np.arange(1, 2, 2 * self.n)]
