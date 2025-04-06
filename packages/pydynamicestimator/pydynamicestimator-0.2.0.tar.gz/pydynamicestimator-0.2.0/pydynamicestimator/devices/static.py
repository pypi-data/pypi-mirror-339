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
if TYPE_CHECKING:
    from system import *
from pydynamicestimator.devices.device import *


class StaticLoadPower(DeviceRect):  # Not finished

    def __init__(self) -> None:
        super().__init__()
        self._type = "Static_load_power"
        self._name = "Static_load_power"
        self._setpoints.update({'p': 0.0, 'q': 0.0})
        self.p = np.array([], dtype=float)
        self.q = np.array([], dtype=float)
        self.properties.update({'fgcall': True, 'finit': True, 'init_data': True, 'xy_index': True, 'save_data': False})

    def gcall(self, dae: Dae) -> None:
        dae.g[self.vre] += (self.p / dae.Sb * dae.y[self.vre] + self.q / dae.Sb * dae.y[self.vim]) / (dae.y[self.vre] ** 2 + dae.y[self.vim] ** 2)
        dae.g[self.vim] += (self.p / dae.Sb * dae.y[self.vim] - self.q / dae.Sb * dae.y[self.vre]) / (dae.y[self.vre] ** 2 + dae.y[self.vim] ** 2)

    def fgcall(self, dae: Dae) -> None:

        self.gcall(dae)


class StaticLoadImpedance(DeviceRect):

    def __init__(self) -> None:
        super().__init__()
        self._type = "Static_load_impedance"
        self._name = "Static_load_impedance"
        self._setpoints.update({'g': 1.0, 'b': 1.0})
        self.g = np.array([], dtype=float)
        self.b = np.array([], dtype=float)
        self.properties.update({'fgcall': True, 'finit': True, 'init_data': True, 'xy_index': True, 'save_data': False})

    def gcall(self, dae: Dae):
        dae.g[self.vre] += self.g * dae.y[self.vre] - self.b * dae.y[self.vim]
        dae.g[self.vim] += self.b * dae.y[self.vre] + self.g * dae.y[self.vim]

    def fgcall(self, dae: Dae) -> None:

        self.gcall(dae)


class StaticInfiniteBus(DeviceRect):

    def __init__(self) -> None:
        super().__init__()
        self._type = "Infinite_bus"
        self._name = "Infinite_bus"
        self._setpoints.update({'vre_int': 1.0, 'vim_int': 0.0})
        self.vre_int = np.array([], dtype=float)
        self.vim_int = np.array([], dtype=float)
        self._params.update({'r': 0.001, 'x': 0.001})
        self.r = np.array([], dtype=float) # internal resistance
        self.x = np.array([], dtype=float) # internal reactance
        self.properties.update({'fgcall': True, 'finit': True, 'init_data': True, 'xy_index': True, 'save_data': False})

    def gcall(self, dae: Dae):
        dae.g[self.vre] += 1 / (self.r**2 + self.x**2) * ((dae.y[self.vre] - self.vre_int) * self.r + (dae.y[self.vim] - self.vim_int) * self.x)
        dae.g[self.vim] += 1 / (self.r**2 + self.x**2) * ((dae.y[self.vre] - self.vre_int) * -self.x + (dae.y[self.vim] - self.vim_int) * self.r)

    def fgcall(self, dae: Dae) -> None:

        self.gcall(dae)
